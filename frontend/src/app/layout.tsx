import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "HaqDar (حقدار) — AI Women's Inheritance Rights Recovery Platform",
  description: "Autonomous multi-agent legal intelligence platform for women's inheritance recovery in Pakistan",
  icons: {
    icon: [
      { url: "/icon.svg", type: "image/svg+xml" },
      { url: "/favicon.ico", sizes: "any" },
    ],
    apple: "/apple-touch-icon.png",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased min-h-screen bg-[#F8FAFC] text-slate-900">
        {children}
      </body>
    </html>
  );
}
