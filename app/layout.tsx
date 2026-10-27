import type { Metadata } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

const jetbrainsMono = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-jetbrains-mono",
  display: "swap",
});

export const metadata: Metadata = {
  title: "Pranav S — Mechatronics Engineering Portfolio | PLC, CAD & Robotics",
  description:
    "Portfolio of Pranav S, a Mechatronics Engineering Student specializing in PLC programming (Delta WPLSoft), 3D mechanical CAD design (AutoCAD, Fusion 360, SolidWorks), electrical panel building, and robotics (Robocon 2025 & AGV).",
  keywords: [
    "Pranav S",
    "Mechatronics Engineering",
    "PLC Programming",
    "Delta WPLSoft",
    "SolidWorks",
    "Fusion 360",
    "AutoCAD",
    "Robotics",
    "Automated Guided Vehicle",
    "AGV",
    "Robocon 2025",
    "Kumaraguru College of Technology",
    "Vellore",
    "Coimbatore",
  ],
  authors: [{ name: "Pranav S" }],
  openGraph: {
    title: "Pranav S — Mechatronics Engineering Portfolio",
    description:
      "PLC Programming, Mechanical CAD Design, Electrical Control Panel Building & Autonomous Robotics.",
    type: "website",
    locale: "en_US",
  },
  twitter: {
    card: "summary_large_image",
    title: "Pranav S — Mechatronics Engineering Portfolio",
    description:
      "PLC Programming, Mechanical CAD Design, Electrical Control Panel Building & Autonomous Robotics.",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`dark ${inter.variable} ${jetbrainsMono.variable}`}>
      <body className="min-h-screen bg-slate-950 text-slate-100 font-sans antialiased selection:bg-sky-500/30 selection:text-sky-300">
        {children}
      </body>
    </html>
  );
}
