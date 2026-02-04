"use client";
import Sidebar from "@/components/ui/Sidebar";
import Navbar from "@/components/ui/Navbar";
import { SidebarProvider } from "@/context/SidebarContext";

export default function DashboardLayout({ children }) {
  return (
    <SidebarProvider>
      <div className="flex h-screen overflow-hidden">
        <Sidebar />

        <div className="flex flex-col flex-1 overflow-hidden">
          <Navbar />

          <main className="flex-1 overflow-y-auto bg-gray-100 p-4 sm:p-6 lg:p-8">
            {children}
          </main>
        </div>
      </div>
    </SidebarProvider>
  );
}
