import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "BWW | Multiplikatorenstelle & Rettungsdienstbildungsstelle",
  description: "BWW UG - Multiplikatorenstelle und Rettungsdienstbildungsstelle mit Schwerpunkt Erste Hilfe und Notfallmedizin.",
  icons: { icon: "/favicon.svg" },
  metadataBase: new URL("https://bww-erste-hilfe.sites.openai.com"),
  openGraph: {
    title: "BWW - Leben retten leicht gemacht",
    description: "Multiplikatorenstelle und Rettungsdienstbildungsstelle mit Schwerpunkt Erste Hilfe und Notfallmedizin.",
    type: "website",
    locale: "de_DE",
    images: [{ url: "/og.png", width: 1200, height: 630, alt: "BWW - Multiplikatorenstelle und Rettungsdienstbildungsstelle" }],
  },
  twitter: { card: "summary_large_image", images: ["/og.png"] },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="de"><body>{children}</body></html>;
}
