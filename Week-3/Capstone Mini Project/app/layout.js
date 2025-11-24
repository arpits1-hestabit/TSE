import "./globals.css";
import { SmoothCursor } from "@/components/ui/smooth-cursor";


export const metadata = {
  title: "Dashboard",
  description: "Next.js Admin Dashboard Layout",
};


export default function RootLayout({ children }) {
  return (
    <html lang="en">

      <body>
        <SmoothCursor />
        {children}
      </body>
    </html>
  );
}
