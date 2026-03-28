import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Soundtrack - AI Music Recommendations",
  description: "Describe your moment, get the right soundtrack for it.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
        <main className="max-w-2xl mx-auto px-4 py-12">
          {children}
        </main>
      </body>
    </html>
  );
}
