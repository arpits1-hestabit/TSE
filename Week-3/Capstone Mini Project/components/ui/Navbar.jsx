"use client";

import { FaBars, FaUserCircle, FaSearch, FaCaretDown } from "react-icons/fa";
import Input from "./Input";
import Link from "next/link";
import { useSidebar } from "@/context/SidebarContext";
import { useState } from "react";

export default function Navbar() {
  const { toggle } = useSidebar();
  const [showSearch, setShowSearch] = useState(false);

  return (
    <nav className="bg-[#343A40] px-4 sm:px-6 py-3 shadow-md sticky top-0 z-30">
      <div className="flex items-center justify-between gap-3">
        {/* Left: Menu Toggle */}
        <button
          onClick={toggle}
          className="text-[#bebebe] hover:text-white text-xl transition-colors p-2"
          aria-label="Toggle sidebar"
        >
          <FaBars />
        </button>

        {/* Center: Search Bar (Desktop) */}
        <div className="hidden md:flex items-center bg-white rounded-lg overflow-hidden shadow-sm flex-1 max-w-md">
          <Input
            placeholder="Search for..."
            className="flex-1 border-0 focus:ring-0 focus:outline-none px-4 py-2.5"
          />
          <button
            className="bg-[#efdd3e] hover:bg-[#f0b100] text-white px-5 py-3.5 transition-colors flex items-center justify-center"
            aria-label="Search"
          >
            <FaSearch className="text-base" />
          </button>
        </div>

        {/* Right: Search Icon (Mobile) & Profile */}
        <div className="flex items-center gap-2 sm:gap-4">
          {/* Mobile Search Toggle */}
          <button
            onClick={() => setShowSearch(!showSearch)}
            className="md:hidden text-[#e5e5e5] hover:text-white text-xl transition-colors p-2"
            aria-label="Toggle search"
          >
            <FaSearch />
          </button>

          {/* User Profile Dropdown */}
          <Link href="/dashboard/profile">
            <button className="flex items-center gap-2 text-[#ffffff] hover:text-white transition-colors p-2 rounded-lg hover:bg-[#2C3034]">
              <FaUserCircle className="text-2xl" />
              <span className="text-sm font-medium hidden sm:inline">
                Profile
              </span>
              <FaCaretDown className="text-xs hidden sm:inline" />
            </button>
          </Link>
        </div>
      </div>

      {/* Mobile Search Bar */}
      {showSearch && (
        <div className="md:hidden mt-3 flex items-center bg-white rounded-lg overflow-hidden shadow-sm">
          <Input
            placeholder="Search for..."
            className="flex-1 border-0 focus:ring-0 focus:outline-none px-4 py-2.5"
          />
          <button
            className="bg-[#efdd3e] hover:bg-[#f0b100] text-white px-5 py-2.5 transition-colors flex items-center justify-center"
            aria-label="Search"
          >
            <FaSearch className="text-base" />
          </button>
        </div>
      )}
    </nav>
  );
}
