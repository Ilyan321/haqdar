import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "HaqDar (حقدار) — AI Women's Inheritance Rights Recovery Platform",
  description: "Autonomous multi-agent legal intelligence platform for women's inheritance recovery in Pakistan",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased min-h-screen bg-background text-slate-900 font-sans">
        {children}
      </body>
    </html>
  );
}
