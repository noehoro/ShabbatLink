import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'ShabbatLink - Find Your Shabbat Dinner',
  description: 'Connect with hosts and guests for Friday night Shabbat dinners through the Jewish Latin Center',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
