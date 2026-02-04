"use client";

import Link from "next/link";
import {
  FaTachometerAlt,
  FaLayerGroup,
  FaFileAlt,
  FaChartBar,
  FaTable,
  FaTimes,
} from "react-icons/fa";
import { useSidebar } from "@/context/SidebarContext";

export default function Sidebar() {
  const { isOpen, close } = useSidebar();

  return (
    <>
      {/* Overlay for mobile */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-40 lg:hidden"
          onClick={close}
        />
      )}

      {/* Sidebar */}
      <aside
        className={`
                    fixed lg:static inset-y-0 left-0 z-50
                    bg-[#202529] text-white w-64 flex flex-col
                    transform transition-transform duration-300 ease-in-out
                    ${isOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0"}
                `}
      >
        {/* Header */}
        <div className="px-6 py-8 bg-[#343A40] flex items-center justify-between">
          <Link
            href="/"
            className="text-xl font-bold hover:text-gray-300 transition-colors"
          >
            Start Bootstrap
          </Link>

          {/* Close button for mobile */}
          <button
            onClick={close}
            className="lg:hidden text-gray-400 hover:text-white transition-colors"
            aria-label="Close sidebar"
          >
            <FaTimes className="text-xl" />
          </button>
        </div>

        {/* Navigation */}
        <nav className="flex-1 p-4 space-y-1 overflow-y-auto">
          <Link
            href="/dashboard"
            onClick={close}
            className="flex items-center gap-3 px-3 py-2.5 text-base hover:bg-[#343A40] rounded transition-colors"
          >
            <FaTachometerAlt className="text-lg flex-shrink-0" />
            <span>Dashboard</span>
          </Link>

          {/* Interface Section */}
          <div className="text-gray-400 uppercase text-xs font-semibold px-3 pt-6 pb-2">
            Interface
          </div>

          <Link
            href="#"
            onClick={close}
            className="flex items-center gap-3 px-3 py-2.5 text-base hover:bg-[#343A40] rounded transition-colors"
          >
            <FaLayerGroup className="text-lg flex-shrink-0" />
            <span>Layouts</span>
          </Link>

          <Link
            href="#"
            onClick={close}
            className="flex items-center gap-3 px-3 py-2.5 text-base hover:bg-[#343A40] rounded transition-colors"
          >
            <FaFileAlt className="text-lg flex-shrink-0" />
            <span>Pages</span>
          </Link>

          {/* Addons Section */}
          <div className="text-gray-400 uppercase text-xs font-semibold px-3 pt-6 pb-2">
            Addons
          </div>

          <Link
            href="#"
            onClick={close}
            className="flex items-center gap-3 px-3 py-2.5 text-base hover:bg-[#343A40] rounded transition-colors"
          >
            <FaChartBar className="text-lg flex-shrink-0" />
            <span>Charts</span>
          </Link>

          <Link
            href="/dashboard/users"
            onClick={close}
            className="flex items-center gap-3 px-3 py-2.5 text-base hover:bg-[#343A40] rounded transition-colors"
          >
            <FaTable className="text-lg flex-shrink-0" />
            <span>Tables</span>
          </Link>
        </nav>
      </aside>
    </>
  );
}
