"""The stack allowlist for crew-written code. Standard library only.

The crew writes real React (pages, components, client islands, a local data
layer) in TypeScript, styles, SVG artwork and static files. The product is
offline first: nothing it ships may reach the network or run code from
elsewhere. This module is the one statement of that rule. The frozen
`tests/test_stack.py` runs it in this repository's CI, and Yard Crew's
trusted build runs the same file before `next build` executes any page code.

TypeScript and JSX are read by a structural tokenizer, not a regex over
text: comments, strings, template literals, regular expressions and JSX
(tags, attributes, text and `{}` expressions) are told apart, so the words
of the page's copy ("we fetch the route") are never mistaken for code. It is
not a type checker; `next build` type-checks. Each violation is one line:

    stack: <path>:<line>: <what is wrong> (<what to do instead>)

What is allowed:
- imports of react, next/link, next/navigation, motion (the pinned motion
  library: `motion/react`, or its small `motion/mini` animate), idb (the
  pinned IndexedDB wrapper), the pinned self-hosted
  @fontsource faces, and the repository's own files (`@/...`, `./...`);
- client islands (`"use client"`), IndexedDB through `lib/db.ts`, outbound
  links (`href`), SVG artwork and self-hosted fonts.
What is refused: any network call (fetch, XMLHttpRequest, WebSocket,
EventSource, sendBeacon, workers), eval and `new Function`, raw HTML
injection, dynamic imports and require, server code (`"use server"`, route
handlers, middleware), runtime environment reads beyond the build's base
path and release, external URLs anywhere but a link's href, and embedded
documents, scripts and forms.
"""

import json
import re
import sys
import xml.etree.ElementTree as ElementTree
from pathlib import Path

# --- what the stack admits -------------------------------------------------------

PACKAGES = (
    "react",
    "react-dom",
    "next/link",
    "next/navigation",
    "motion",
    "motion/react",
    # The same pinned library's small animate on the browser's own engine
    # (about 2 KB), for an island that needs no React motion runtime.
    "motion/mini",
    "idb",
)
# Self-hosted fonts: side-effect CSS imports of the pinned faces only.
FONT_PACKAGE = re.compile(r"@fontsource(?:-variable)?/[a-z0-9-]+(?:/[a-z0-9-]+\.css)?")
# Where crew code lives; everything else in a TypeScript file's place is refused.
CODE_ROOTS = ("app/", "components/", "lib/")
CODE = (".ts", ".tsx")
SCRIPT = (".js", ".mjs", ".cjs", ".jsx")
STYLE_ROOTS = ("app/", "components/", "styles/")
PUBLIC_TYPES = (
    ".svg",
    ".png",
    ".jpg",
    ".jpeg",
    ".webp",
    ".avif",
    ".woff2",
    ".json",
    ".txt",
    ".ico",
    ".webmanifest",
)
# Files Next.js treats as server code or request handling: a static export has none.
SERVER_FILE = re.compile(
    r"(?:^|/)(?:route|middleware|proxy|instrumentation)\.(?:ts|tsx|js|mjs)$|^pages/api/"
)
# The only build-time environment page code reads; trusted code sets both.
ENVIRONMENT = ("NEXT_BASE_PATH", "SITE_RELEASE")

NETWORK = {
    "fetch": "a network call",
    "XMLHttpRequest": "a network call",
    "WebSocket": "a network connection",
    "WebSocketStream": "a network connection",
    "EventSource": "a network connection",
    "RTCPeerConnection": "a network connection",
    "sendBeacon": "a tracking beacon",
    "importScripts": "loading a script",
    "Worker": "a worker that can load scripts",
    "SharedWorker": "a worker that can load scripts",
    "serviceWorker": "a service worker",
    "eval": "running text as code",
    "execScript": "running text as code",
    "dangerouslySetInnerHTML": "raw HTML injection",
    "innerHTML": "raw HTML injection",
    "outerHTML": "raw HTML injection",
    "insertAdjacentHTML": "raw HTML injection",
    "createContextualFragment": "raw HTML injection",
    "srcdoc": "an embedded document",
    "srcDoc": "an embedded document",
    "postMessage": "messaging another window",
    "require": "an unchecked module load",
}
# Members refused on these objects only (`document.cookie`, `window.open`).
MEMBERS = {
    ("document", "cookie"): "a cookie",
    ("document", "write"): "writing raw HTML",
    ("document", "writeln"): "writing raw HTML",
    ("document", "domain"): "changing the origin",
    ("window", "open"): "opening another window",
    ("navigator", "sendBeacon"): "a tracking beacon",
    ("location", "assign"): "a redirect",
    ("location", "replace"): "a redirect",
}
TAGS = {
    "script": "a script element (bundle the code as a component)",
    "iframe": "an embedded document",
    "frame": "an embedded document",
    "frameset": "an embedded document",
    "object": "an embedded object",
    "embed": "an embedded object",
    "applet": "an embedded object",
    "portal": "an embedded document",
    "base": "a base element (links keep the base path through next/link)",
    "form": "a form (forms post somewhere; use inputs and a button handler)",
}
ATTRIBUTES = {
    "dangerouslySetInnerHTML": "raw HTML injection",
    "srcDoc": "an embedded document",
    "formAction": "a form action",
    "httpEquiv": "an http-equiv meta (a refresh or policy from markup)",
}
URL_ATTRIBUTES = ("src", "srcSet", "poster", "data", "action", "href", "xlinkHref", "background")
SCRIPT_URL = re.compile(r"\s*(?:javascript|vbscript|data:text/html)", re.I)
EXTERNAL = re.compile(r"(?:[a-z][a-z0-9+.-]*:)?//", re.I)
OUTBOUND = re.compile(r"(?:https://|mailto:|tel:)", re.I)

FIX_NETWORK = "the product is offline first: keep data in lib/db.ts (IndexedDB) and app/*.json"
FIX_MARKUP = "render plain elements; behaviour belongs in a client component's handlers"
FIX_IMPORT = (
    "import only react, next/link, next/navigation, motion/react, motion/mini, idb, the pinned "
    "@fontsource faces and the repository's own files"
)


class _Error(ValueError):
    pass


# --- a structural tokenizer for TypeScript and JSX ------------------------------------

_ID_START = re.compile(r"[A-Za-z_$]")
_ID = re.compile(r"[A-Za-z_$][A-Za-z0-9_$]*")
_NUMBER = re.compile(
    r"(?:0[xXbBoO][0-9a-fA-F_]+|(?:\d[\d_]*\.?[\d_]*|\.\d[\d_]*)(?:[eE][+-]?\d+)?)n?"
)
_PUNCT = re.compile(
    r">>>=|\.\.\.|===|!==|\*\*=|<<=|>>=|>>>|\?\?=|&&=|\|\|=|=>|==|!=|<=|>=|&&|\|\||\?\?|\?\."
    r"|\+\+|--|\+=|-=|\*=|/=|%=|&=|\|=|\^=|\*\*|<<|>>|[{}()\[\];,<>+\-*/%&|^!~?:=.@#]"
)
_JSX_NAME = re.compile(r"[A-Za-z_$][A-Za-z0-9_$.:-]*")
# After these, `<` opens JSX and `/` opens a regular expression.
_EXPRESSION_KEYWORDS = frozenset(
    {"return", "yield", "await", "default", "case", "else", "do", "in", "of", "typeof",
     "void", "delete", "new", "throw", "extends"}
)  # fmt: skip
_AFTER_VALUE = frozenset({")", "]", "}"})


class Token:
    __slots__ = ("kind", "value", "line", "context")

    def __init__(self, kind, value, line, context=None):
        self.kind, self.value, self.line, self.context = kind, value, line, context

    def __repr__(self):
        return f"Token({self.kind!r}, {self.value!r}, {self.line})"


class _Lexer:
    """Tokens: id, str, num, punct, regex, tag (JSX element name), attr (JSX name).

    A string token's `context` is the JSX attribute it is the value of, if any.
    """

    def __init__(self, source):
        self.s, self.i, self.out = source, 0, []

    def line(self, at=None):
        return self.s.count("\n", 0, self.i if at is None else at) + 1

    def emit(self, kind, value, at, context=None):
        self.out.append(Token(kind, value, self.line(at), context))

    def previous(self):
        return self.out[-1] if self.out else None

    def expression_expected(self):
        """True where a value may start: so `<` is JSX and `/` a regex."""
        last = self.previous()
        if last is None:
            return True
        if last.kind in ("str", "num", "regex", "tag-end"):
            return False
        if last.kind == "id":
            return last.value in _EXPRESSION_KEYWORDS
        return last.kind == "punct" and last.value not in _AFTER_VALUE

    def skip_space(self):
        s, n = self.s, len(self.s)
        while self.i < n:
            c = s[self.i]
            if c in " \t\r\n﻿":
                self.i += 1
            elif s.startswith("//", self.i):
                end = s.find("\n", self.i)
                self.i = n if end < 0 else end
            elif s.startswith("/*", self.i):
                end = s.find("*/", self.i + 2)
                if end < 0:
                    raise _Error("an unclosed comment")
                self.i = end + 2
            else:
                return

    def code(self, until_brace=False):
        """Code up to the end, or to the `}` that closes an expression."""
        depth, s = 0, self.s
        while True:
            self.skip_space()
            if self.i >= len(s):
                if until_brace:
                    raise _Error("an unclosed {")
                return
            c, at = s[self.i], self.i
            if c in "\"'":
                self.emit("str", self.string(c), at)
            elif c == "`":
                self.template(at)
            elif _ID_START.match(c):
                word = _ID.match(s, self.i).group(0)
                self.i += len(word)
                self.emit("id", word, at)
            elif c.isdigit() or (c == "." and self.i + 1 < len(s) and s[self.i + 1].isdigit()):
                number = _NUMBER.match(s, self.i).group(0)
                self.i += len(number)
                self.emit("num", number, at)
            elif c == "<" and self.expression_expected() and self.jsx_ahead():
                saved = (self.i, len(self.out))
                try:
                    self.element()
                except _Error:
                    # Not JSX after all (a generic such as `<T,>`): one punctuator.
                    self.i, self.out[saved[1] :] = saved[0], []
                    self.i += 1
                    self.emit("punct", "<", at)
            elif c == "/" and self.expression_expected():
                self.emit("regex", self.regex(), at)
            else:
                match = _PUNCT.match(s, self.i)
                if not match:
                    raise _Error(f"an unexpected character {c!r}")
                value = match.group(0)
                if value == "}" and depth == 0 and until_brace:
                    return  # the caller consumes the closing brace
                self.i += len(value)
                depth += {"{": 1, "}": -1}.get(value, 0)
                self.emit("punct", value, at)

    def string(self, quote):
        s, i, parts = self.s, self.i + 1, []
        while i < len(s):
            c = s[i]
            if c == "\\":
                parts.append(s[i + 1 : i + 2])
                i += 2
            elif c == quote:
                self.i = i + 1
                return "".join(parts)
            elif c == "\n":
                break
            else:
                parts.append(c)
                i += 1
        raise _Error("an unclosed string")

    def template(self, at):
        """A template literal: its text as one str token, each `${}` as code."""
        s, self.i, text = self.s, self.i + 1, []
        while self.i < len(s):
            c = s[self.i]
            if c == "\\":
                text.append(s[self.i + 1 : self.i + 2])
                self.i += 2
            elif c == "`":
                self.i += 1
                self.emit("str", "".join(text), at)
                return
            elif s.startswith("${", self.i):
                self.i += 2
                text.append("${}")
                self.code(until_brace=True)
                self.i += 1
            else:
                text.append(c)
                self.i += 1
        raise _Error("an unclosed template literal")

    def regex(self):
        s, i, in_class = self.s, self.i + 1, False
        while i < len(s) and s[i] != "\n":
            c = s[i]
            if c == "\\":
                i += 2
                continue
            if c == "[":
                in_class = True
            elif c == "]":
                in_class = False
            elif c == "/" and not in_class:
                i += 1
                while i < len(s) and (s[i].isalnum() or s[i] == "_"):
                    i += 1
                value, self.i = s[self.i : i], i
                return value
            i += 1
        raise _Error("an unclosed regular expression")

    def braced(self):
        """A `{...}` expression inside JSX, with both braces as tokens."""
        self.emit("punct", "{", self.i)
        self.i += 1
        self.code(until_brace=True)
        self.emit("punct", "}", self.i)
        self.i += 1

    def jsx_ahead(self):
        rest = self.s[self.i + 1 : self.i + 2]
        return rest == ">" or bool(_ID_START.match(rest))

    def element(self):
        """One JSX element or fragment, from its `<` to the end of its closing tag."""
        s, at = self.s, self.i
        self.i += 1
        if s.startswith(">", self.i):
            self.i += 1
            self.emit("tag", "", at)
            self.children("")
            return
        name = _JSX_NAME.match(s, self.i)
        if not name:
            raise _Error("not JSX")
        tag = name.group(0)
        self.i = name.end()
        self.emit("tag", tag, at)
        while True:
            self.skip_space()
            if self.i >= len(s):
                raise _Error("an unclosed JSX tag")
            if s.startswith("/>", self.i):
                self.i += 2
                self.emit("tag-end", tag, self.i)
                return
            if s[self.i] == ">":
                self.i += 1
                self.children(tag)
                return
            if s[self.i] == "{":
                self.braced()
                continue
            attr = _JSX_NAME.match(s, self.i)
            if not attr:
                raise _Error("not JSX")
            self.emit("attr", attr.group(0), self.i)
            self.i = attr.end()
            self.skip_space()
            if not s.startswith("=", self.i):
                continue
            self.i += 1
            self.skip_space()
            c, where = s[self.i : self.i + 1], self.i
            if c in ('"', "'"):
                end = s.find(c, self.i + 1)
                if end < 0:
                    raise _Error("an unclosed attribute")
                self.emit("str", s[self.i + 1 : end], where, attr.group(0))
                self.i = end + 1
            elif c == "{":
                start = len(self.out)
                self.braced()
                for token in self.out[start:]:
                    if token.kind == "str" and token.context is None:
                        token.context = attr.group(0)
            elif c == "<":
                self.element()
            else:
                raise _Error("not JSX")

    def children(self, tag):
        s = self.s
        while True:
            if self.i >= len(s):
                raise _Error(f"<{tag}> is never closed")
            c = s[self.i]
            if s.startswith("</", self.i):
                end = s.find(">", self.i)
                if end < 0 or s[self.i + 2 : end].strip() != tag:
                    raise _Error(f"<{tag}> is closed by the wrong tag")
                self.i = end + 1
                self.emit("tag-end", tag, self.i)
                return
            if c == "<":
                self.element()
            elif c == "{":
                self.braced()
            else:
                # JSX text is copy, never code: it is skipped.
                nxt = min(
                    (p for p in (s.find("<", self.i), s.find("{", self.i)) if p >= 0),
                    default=len(s),
                )
                self.i = nxt


def tokens(source):
    """The tokens of one TypeScript or TSX file; ValueError if it cannot be read."""
    lexer = _Lexer(source)
    try:
        lexer.code()
    except _Error as error:
        raise ValueError(f"line {lexer.line()}: {error}") from None
    return lexer.out


# --- the rules ------------------------------------------------------------------------


def _module_allowed(name, path):
    if name in PACKAGES or name.startswith(("@/", "./", "../")):
        return True
    # Fonts are imported for their CSS, once, by the design system's app/fonts.ts.
    return FONT_PACKAGE.fullmatch(name) is not None and path == "app/fonts.ts"


def _imports(found, path, toks):
    for n, token in enumerate(toks):
        if token.kind != "id" or token.value not in ("import", "export"):
            continue
        before = toks[n - 1] if n else None
        if before is not None and before.kind == "punct" and before.value == ".":
            continue  # `import.meta` is read below; a member named import is not a load
        after = toks[n + 1] if n + 1 < len(toks) else None
        if token.value == "import" and after is not None and after.kind == "punct":
            if after.value == "(":
                found.append((token.line, "a dynamic import()", FIX_IMPORT))
                continue
            if after.value == ".":
                found.append((token.line, "import.meta", "read nothing from the runtime"))
                continue
        if after is not None and after.kind == "id" and after.value == "type":
            continue  # `import type` / `export type` is erased: types load nothing
        # The module is the first string before the statement ends.
        for m in range(n + 1, min(n + 64, len(toks))):
            later = toks[m]
            if later.kind == "punct" and later.value == ";":
                break
            if later.kind == "id" and later.value in ("function", "const", "class", "let"):
                break
            if later.kind == "str":
                source = toks[m - 1].kind == "id" and toks[m - 1].value == "from"
                if token.value == "export" and not source:
                    break
                if not _module_allowed(later.value, path):
                    found.append((later.line, f'an import of "{later.value}"', FIX_IMPORT))
                break


def _network(found, toks):
    for n, token in enumerate(toks):
        if token.kind not in ("id", "attr"):
            continue
        before = toks[n - 1] if n else None
        owner = toks[n - 2] if n > 1 else None
        member = before is not None and before.kind == "punct" and before.value in (".", "?.")
        if token.kind == "attr" and token.value in ATTRIBUTES:
            found.append((token.line, f"{token.value} ({ATTRIBUTES[token.value]})", FIX_MARKUP))
            continue
        if token.kind == "attr":
            continue
        after = toks[n + 1] if n + 1 < len(toks) else None
        if member and owner is not None and owner.kind == "id":
            why = MEMBERS.get((owner.value, token.value))
            if why:
                found.append((token.line, f"{owner.value}.{token.value} ({why})", FIX_NETWORK))
                continue
        # An object key (`{ fetch: 1 }`) or a type member is not a use.
        if after is not None and after.kind == "punct" and after.value == ":" and not member:
            if before is not None and before.kind == "punct" and before.value in ("{", ",", ";"):
                continue
        if token.value in NETWORK:
            found.append((token.line, f"{token.value} ({NETWORK[token.value]})", FIX_NETWORK))
        elif token.value == "Function" and (
            (after is not None and after.kind == "punct" and after.value == "(")
            or (before is not None and before.kind == "id" and before.value == "new")
        ):
            found.append((token.line, "new Function (running text as code)", FIX_NETWORK))
        elif token.value == "env" and member and owner is not None and owner.value == "process":
            name = toks[n + 2] if n + 2 < len(toks) else None
            if not (
                after is not None
                and after.kind == "punct"
                and after.value == "."
                and name is not None
                and name.value in ENVIRONMENT
            ):
                found.append(
                    (
                        token.line,
                        "process.env beyond NEXT_BASE_PATH and SITE_RELEASE",
                        "a static export has no runtime environment and holds no secrets",
                    )
                )
        elif token.value == "src" and member and after is not None and after.value == "=":
            found.append(
                (token.line, "setting .src from code", "write the URL in JSX from your own files")
            )


def _jsx(found, toks):
    tags = [t for t in toks if t.kind == "tag"]
    for token in tags:
        if token.value in TAGS:
            found.append((token.line, f"<{token.value}>: {TAGS[token.value]}", FIX_MARKUP))
    current = None
    for token in toks:
        if token.kind == "tag":
            current = token.value
        if token.kind != "str":
            continue
        value = token.value
        if SCRIPT_URL.match(value):
            found.append((token.line, "a javascript:, vbscript: or data:text/html URL", FIX_MARKUP))
            continue
        external = EXTERNAL.match(value.strip()) or "://" in value
        if not external:
            continue
        if token.context in ("xmlns", "xmlnsXlink", "xmlns:xlink"):
            continue  # an SVG namespace names, never loads
        link = token.context == "href" and current not in ("link", "script", "base")
        if link and OUTBOUND.match(value.strip()):
            continue  # an outbound https link a person follows
        if token.context is None and _key_before(toks, token) == "href":
            continue  # `{ href: "https://..." }`, rendered as a link
        found.append(
            (
                token.line,
                f'an external URL "{value[:60]}"',
                "only a link's href may leave the site; self-host fonts, images and data",
            )
        )


def _key_before(toks, token):
    """The object key a string is the value of (`href: "..."`), if any."""
    n = toks.index(token)
    if n >= 2 and toks[n - 1].kind == "punct" and toks[n - 1].value == ":":
        return toks[n - 2].value if toks[n - 2].kind in ("id", "str") else None
    return None


def _directives(found, toks):
    for n, token in enumerate(toks):
        if token.kind == "str" and token.value == "use server" and token.context is None:
            found.append(
                (
                    token.line,
                    '"use server" (a server action)',
                    "a static export has no server: keep logic in client islands",
                )
            )


def code(path, source):
    """[(line, what, fix)] for one TypeScript or TSX file."""
    try:
        toks = tokens(source)
    except ValueError as error:
        return [(1, f"cannot be read ({error})", "write plain TypeScript and JSX")]
    found = []
    _imports(found, path, toks)
    _network(found, toks)
    _jsx(found, toks)
    _directives(found, toks)
    return sorted(set(found))


# --- styles, artwork and static files ---------------------------------------------------

_CSS_COMMENT = re.compile(r"/\*.*?\*/", re.S)
_CSS_URL = re.compile(r"url\(\s*(['\"]?)([^'\")]*)\1\s*\)", re.I)
_CSS_IMPORT = re.compile(r"@import\s+(?:url\()?\s*['\"]?([^'\";)\s]+)", re.I)


def style(source):
    """[(line, what, fix)] for one stylesheet."""
    found = []
    text = _CSS_COMMENT.sub(lambda m: "\n" * m.group(0).count("\n"), source)

    def line(at):
        return text.count("\n", 0, at) + 1

    for match in _CSS_IMPORT.finditer(text):
        target = match.group(1)
        if EXTERNAL.match(target):
            found.append(
                (line(match.start()), f"@import of {target[:60]}", "self-host every stylesheet")
            )
    for match in _CSS_URL.finditer(text):
        target = match.group(2).strip()
        if EXTERNAL.match(target) or SCRIPT_URL.match(target):
            found.append(
                (
                    line(match.start()),
                    f"url({target[:60]}) leaves the site",
                    "use files under public/ or inline SVG",
                )
            )
    for bad, why in (
        (r"expression\s*\(", "a CSS expression"),
        (r"-moz-binding", "a CSS binding"),
        (r"(?<![\w-])behavior\s*:", "a CSS behavior"),
    ):
        for match in re.finditer(bad, text, re.I):
            found.append((line(match.start()), why, "remove it: styles never run code"))
    return sorted(set(found))


_SVG = "{http://www.w3.org/2000/svg}"
_XLINK = "{http://www.w3.org/1999/xlink}href"
SVG_ELEMENTS = frozenset(
    {"svg", "g", "path", "circle", "rect", "ellipse", "line", "polygon", "polyline", "defs",
     "linearGradient", "radialGradient", "stop", "clipPath", "mask", "pattern", "use", "symbol",
     "title", "desc", "text", "tspan", "filter", "feGaussianBlur", "feOffset", "feBlend",
     "feColorMatrix", "feMerge", "feMergeNode", "feFlood", "feComposite", "feTurbulence",
     "feDisplacementMap", "metadata"}
)  # fmt: skip


def artwork(source):
    """[(line, what, fix)] for one SVG file: safe, self-contained artwork only."""
    fix = "draw with shapes, gradients and patterns only; reference only #ids in this file"
    if "<!ENTITY" in source or "<!DOCTYPE" in source:
        return [(1, "an SVG with a DOCTYPE or entities", fix)]
    try:
        root = ElementTree.fromstring(source)
    except ElementTree.ParseError as error:
        return [(error.position[0], "an SVG that is not well-formed XML", fix)]
    found = []
    for element in root.iter():
        tag = element.tag.removeprefix(_SVG)
        if tag not in SVG_ELEMENTS:
            found.append((1, f"an SVG <{tag}> element", fix))
        for name, value in element.attrib.items():
            local = name.rsplit("}", 1)[-1]
            if local.lower().startswith("on"):
                found.append((1, f"an SVG event handler {local}", fix))
            if name in ("href", _XLINK) and not value.startswith("#"):
                found.append((1, f"an SVG reference to {value[:60]}", fix))
            if "url(" in value and not re.fullmatch(r"url\(#[\w.-]+\)", value.strip()):
                found.append((1, f"an SVG url() to {value[:60]}", fix))
        if tag == "style":
            found.append((1, "an SVG <style>", fix))
    return sorted(set(found))


def placement(path):
    """What is wrong with a file's place in the repository, or None."""
    if SERVER_FILE.search(path):
        return ("server code (a route handler or middleware)", "a static export has no server")
    if path.endswith(CODE) and not path.startswith(CODE_ROOTS) and "/" in path:
        return ("TypeScript outside app/, components/ and lib/", "move it under one of them")
    if path.endswith(SCRIPT) and path.startswith(("app/", "components/", "lib/", "public/")):
        return ("a JavaScript file", "write TypeScript under app/, components/ or lib/")
    if path.startswith("public/") and not path.lower().endswith(PUBLIC_TYPES):
        kinds = ", ".join(PUBLIC_TYPES)
        return ("a static file type the site does not serve", f"public/ holds {kinds}")
    return None


def packages(manifest, pinned):
    """[(line, what, fix)]: package.json's dependencies must be the pinned ones, exactly."""
    try:
        data = json.loads(manifest)
        mine = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
    except (ValueError, AttributeError):
        return [(1, "package.json is not a JSON object", "restore the platform's package.json")]
    found = []
    for name, version in sorted(mine.items()):
        if pinned.get(name) != version:
            found.append(
                (
                    1,
                    f"the dependency {name}@{version} is not the platform's pin",
                    "dependencies are platform files: use what the template pins",
                )
            )
    return found


SKIPPED = ("node_modules/", ".next/", "out/", "site/", "tests/", ".github/", "qa/")


def violations(files, pinned=None):
    """Every violation as one line, in path order; [] when the repository is clean.

    `files` is {path: text}; `pinned` the platform's {package: version}, which
    package.json must match exactly when given.
    """
    lines = []
    for path in sorted(files):
        if path.startswith(SKIPPED):
            continue
        text = files[path]
        found = []
        where = placement(path)
        if where:
            found.append((1, *where))
        elif path.endswith(CODE) and path.startswith(CODE_ROOTS):
            found += code(path, text)
        elif path.endswith(".css") and path.startswith(STYLE_ROOTS):
            found += style(text)
        elif path.endswith(".svg") and path.startswith(("public/", "app/")):
            found += artwork(text)
        elif path == "package.json" and pinned is not None:
            found += packages(text, pinned)
        for line, what, fix in found:
            lines.append(f"stack: {path}:{line}: {what} ({fix})")
    return lines


def repository(root):
    """{path: text} of a checked-out repository, as `violations` reads it."""
    root = Path(root)
    files = {}
    for path in sorted(root.rglob("*")):
        name = path.relative_to(root).as_posix()
        if not path.is_file() or name.startswith(SKIPPED) or "/." in "/" + name:
            continue
        if name.endswith((*CODE, *SCRIPT, ".css", ".svg")) or name == "package.json":
            files[name] = path.read_text(encoding="utf-8", errors="replace")
        elif name.startswith("public/"):
            files[name] = ""
    return files


if __name__ == "__main__":
    found = violations(repository(sys.argv[1] if len(sys.argv) > 1 else "."))
    print("\n".join(found) or "stack: clean")
    sys.exit(1 if found else 0)
