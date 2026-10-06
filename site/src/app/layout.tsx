import type { Metadata } from "next";
import Link from "next/link";

import "./globals.css";

export const metadata: Metadata = {
  title: "Bits and Bytes",
  description: "Lesson guide for the Bits and Bytes curriculum",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="en">
      <body>
        <div className="site-shell">
          <a className="skip-link" href="#main-content">Skip to content</a>
          <header className="site-header">
            <Link href="/">Bits and Bytes</Link>
          </header>
          {children}
        </div>
      </body>
    </html>
  );
}
