import { FaBars, FaUserCircle, FaSearch, FaCaretDown } from "react-icons/fa";
import Input from "./Input";
import Link from "next/link";

export default function Navbar() {
    return (
        <nav className="flex justify-between items-center bg-[#343A40] px-6 py-3 min-h-[60px]">
            <div className="flex items-center gap-3 px-2">
                <FaBars className="text-[#9FA8A8] text-xl cursor-pointer" />
            </div>

            <div className="flex items-center gap-4 flex-1 justify-end min-w-0">

                <div className="flex items-center bg-white rounded-lg flex-1 max-w-lg min-w-[120px]">

                    <Input
                        placeholder="Search for..."
                        className="flex-1 rounded-l-lg border-white"
                    />

                    <button className="bg-yellow-400 text-white px-4 py-4 rounded-r-lg flex items-center justify-center">
                        <FaSearch className="text-xl" />
                    </button>
                </div>

                <Link href="/dashboard/profile">
                    <button className="flex items-center text-2xl text-[#9FA8A8] cursor-pointer gap-1">
                        <FaUserCircle />
                        <FaCaretDown />
                    </button>
                </Link>

            </div>

        </nav>
    );
}
