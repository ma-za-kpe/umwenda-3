// The page's one orchestrated load moment (docs/design/MOTION.md): each
// Reveal rises into place in `order`, a beat after the one before. It is CSS,
// not script, on purpose: without JavaScript, under reduced motion and before
// hydration the content is simply there, and nothing is hidden first. With
// motion allowed it moves but never fades in from nothing, so the page's
// largest content paints at once (Lighthouse's mobile floor, #233 C16). The
// keyframes and timing tokens are in app/tokens.css and app/globals.css.
import type { CSSProperties, ReactNode } from "react";

type Props = { children: ReactNode; order?: number; className?: string };

export default function Reveal({ children, order = 0, className }: Props) {
  const style = { "--reveal-order": String(order) } as CSSProperties;
  return (
    <div data-reveal="" className={className} style={style}>
      {children}
    </div>
  );
}
