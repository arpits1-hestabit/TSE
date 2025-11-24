import "@/app/globals.css";
import Navbar from "@/components/ui/Navbar";
import Sidebar from "@/components/ui/Sidebar";

export const metadata = {
    title: "Dashboard",
    description: "Next.js Admin Dashboard Layout",
};


export default function RootLayout({ children }) {
    return (
        <html lang="en" className="h-full">
            <body className="h-full">
                <div className="flex h-full">

                    <Sidebar />

                    <div className="flex flex-col flex-1">
                        <Navbar />
                        <main className="flex-1 overflow-auto">
                            {children}
                        </main>
                    </div>
                </div>
            </body>
        </html>
    );
}
