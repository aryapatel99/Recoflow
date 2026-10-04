import type { Metadata } from "next";
import "./globals.css";
import { Providers } from "../components";

export const metadata: Metadata = {
  title: "RecoFlow",
  description:
    "Event-driven personalized recommendation and ranking platform",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
