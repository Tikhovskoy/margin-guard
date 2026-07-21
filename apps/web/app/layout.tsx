import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "margin-guard — контроль маржи",
  description: "Рабочий dashboard для контроля маржи маркетплейсов.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ru">
      <body>{children}</body>
    </html>
  );
}
