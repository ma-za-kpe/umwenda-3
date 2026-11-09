// Frozen static server for the browser check (owner-owned). It serves a built
// site as GitHub Pages does: `/` and `/dir/` serve their index.html, a path
// without an extension serves its .html page, anything else is 404 (with the
// site's own 404.html, if it has one). With a base path (`/<repository>/` on
// Pages, T-0504) only paths under it are the site, and the bare
// `/<repository>` redirects to it. Yard Crew's local CI serves the site with
// this same file, so local CI and Actions agree.
// The response headers are Pages' own too (observed on a published crew site,
// 2026-10-31), so a page's measured weight is what a visitor downloads (#233
// C16): text (HTML, CSS, JavaScript, SVG, JSON, plain text) is gzip-encoded
// when the request accepts gzip, and never Brotli, which Pages does not
// offer; fonts and images go as they are, already compressed. Every response
// says `Cache-Control: max-age=600` and `Vary: Accept-Encoding`, and text
// types name `charset=utf-8`.
// Usage: node tests/browser/serve.mjs [folder] [port] [base path]
import { createServer } from 'node:http';
import { readFile } from 'node:fs/promises';
import { extname, join, normalize } from 'node:path';
import { gzipSync } from 'node:zlib';

const [root = '/site', port = '8000', base = '/'] = process.argv.slice(2);
const text = '; charset=utf-8';
const types = {
  '.html': 'text/html' + text, '.css': 'text/css' + text, '.svg': 'image/svg+xml',
  '.js': 'text/javascript' + text, '.json': 'application/json' + text, '.txt': 'text/plain' + text,
  '.png': 'image/png', '.jpg': 'image/jpeg', '.webp': 'image/webp', '.ico': 'image/x-icon',
  '.woff2': 'font/woff2',
};
const compressed = new Set(['.html', '.css', '.svg', '.js', '.json', '.txt']);
const headers = { 'cache-control': 'max-age=600', vary: 'Accept-Encoding' };

function send(req, res, status, file, body) {
  const type = Object.hasOwn(types, extname(file)) ? extname(file) : '.html';
  const gzip = compressed.has(type) && /\bgzip\b/.test(req.headers['accept-encoding'] || '');
  res.writeHead(status, { ...headers, 'content-type': types[type],
    ...(gzip ? { 'content-encoding': 'gzip' } : {}) });
  res.end(req.method === 'HEAD' ? undefined : gzip ? gzipSync(body) : body);
}

createServer(async (req, res) => {
  let path;
  try {
    path = normalize(decodeURIComponent(new URL(req.url, 'http://x').pathname));
  } catch {
    res.writeHead(400); res.end();
    return;
  }
  if (path + '/' === base) {
    res.writeHead(301, { location: base }); res.end();
    return;
  }
  if (!path.startsWith(base)) {
    res.writeHead(404); res.end();
    return;
  }
  const inside = '/' + path.slice(base.length);
  const file = inside.endsWith('/') ? inside + 'index.html' : inside;
  // As Pages does: a path without an extension serves its .html page.
  for (const tried of extname(file) ? [file] : [file, file + '.html']) {
    try {
      send(req, res, 200, tried, await readFile(join(root, tried)));
      return;
    } catch { /* the next candidate, then 404 */ }
  }
  const missing = await readFile(join(root, '404.html')).catch(() => null);
  if (missing === null) {
    res.writeHead(404); res.end();
    return;
  }
  send(req, res, 404, '404.html', missing);
}).listen(Number(port), '127.0.0.1');
