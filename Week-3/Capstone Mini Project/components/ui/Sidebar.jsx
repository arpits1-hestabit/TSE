// components/ui/Sidebar.jsx
import Link from "next/link";
import {
    FaTachometerAlt,
    FaLayerGroup,
    FaFileAlt,
    FaChartBar,
    FaTable,
} from "react-icons/fa";

export default function Sidebar() {
    return (
        <aside className="bg-[#202529] text-white  min-w-[180px] max-w-[16rem] w-full">


            <div className="px-2 py-6 text-xl max-h-[180px] font-bold bg-[#343A40]">
                <Link href="/">Start Bootstrap</Link>
            </div>



            <nav className="p-4 space-y-5 text-xl">
                <Link
                    href="/dashboard"
                    className="flex items-center gap-3 px-3 py-2 hover:bg-yellow-800 rounded"
                >
                    <FaTachometerAlt />
                    Dashboard
                </Link>

                <div className="text-gray-400 uppercase text-sm px-3 mt-4">Interface</div>

                <Link
                    href="#"
                    className="flex items-center gap-3 px-3 py-2 hover:bg-yellow-800 rounded"
                >
                    <FaLayerGroup />
                    Layouts
                </Link>

                <Link
                    href="#"
                    className="flex items-center gap-3 px-3 py-2 hover:bg-yellow-800 rounded"
                >
                    <FaFileAlt />
                    Pages
                </Link>

                <div className="text-gray-400 uppercase text-sm px-3 mt-4">Addons</div>

                <Link
                    href="#"
                    className="flex items-center gap-3 px-3 py-2 hover:bg-yellow-800 rounded"
                >
                    <FaChartBar />
                    Charts
                </Link>

                <Link
                    href="dashboard/users"
                    className="flex items-center gap-3 px-3 py-2 hover:bg-yellow-800 rounded"
                >
                    <FaTable />
                    Tables
                </Link>
            </nav>
        </aside>
    );
}
