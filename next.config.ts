import type { NextConfig } from "next";

// Frozen: a platform change. Static export for GitHub Pages only.
// NEXT_BASE_PATH is the Pages project path ("/<repository>"), empty at the
// site root; trusted delivery code sets it, never the page code.
const basePath = process.env.NEXT_BASE_PATH ?? "";

const nextConfig: NextConfig = {
  output: "export",
  basePath,
  assetPrefix: basePath || undefined,
  // Pages serves `menu.html` for `/menu`, so pages export as flat files, the
  // same layout as the static template (no trailing-slash folders).
  trailingSlash: false,
  images: { unoptimized: true },
  // The same commit builds the same paths: the build id is the release.
  generateBuildId: async () => process.env.SITE_RELEASE ?? "local",
  productionBrowserSourceMaps: false,
  poweredByHeader: false,
  // The styles (tokens, layout and the @font-face rules) ship inside each
  // page instead of as a render-blocking stylesheet request: on a phone over
  // slow 4G the first paint no longer waits a round trip for them (#233 C16,
  // Lighthouse's mobile floor). About 2.5 KB gzipped a page.
  experimental: { inlineCss: true },
};

export default nextConfig;
