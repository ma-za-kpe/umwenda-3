import type { Metadata, Viewport } from "next";
import Link from "next/link";
import "./fonts";
import "./tokens.css";
import "./globals.css";

export const metadata: Metadata = {
  title: "Coming soon",
  description: "A product built by Yard Crew.",
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
};

// The release marker: trusted delivery code sets SITE_RELEASE to the exact
// commit it builds, and the live check requires it on the published page.
const release = process.env.SITE_RELEASE ?? "local";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body data-release={release}>
        <header className="site-header container">
          <Link className="brand" href="/">
            Coming soon
          </Link>
        </header>
        {children}
        <footer className="site-footer container">
          <p>Built by Yard Crew.</p>
        </footer>
      </body>
    </html>
  );
}
