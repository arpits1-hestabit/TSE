import React from "react";

export default function Footer() {
    return (
        <footer className="bg-white-500 rounded-lg shadow">
            <div className="w-full max-w-screen-xl p-2 md:flex justify-between items-center">

                <a href="#" className="flex items-center space-x-3 mb-4 md:mb-0">
                    <img
                        src="https://img.freepik.com/premium-vector/web-analytics-vector-icon-design-illustration_1174953-12812.jpg?semt=ais_hybrid&w=740&q=80"
                        alt="Logo"
                        className="h-8"
                    />
                    <span className="text-2xl font-semibold whitespace-nowrap text-white">
                        Flowbite
                    </span>
                </a>

                <ul className="flex flex-wrap items-center text-sm font-medium text-gray-600">
                    <li>
                        <a href="#" className="mr-4 hover:underline md:mr-6">
                            About
                        </a>
                    </li>
                    <li>
                        <a href="#" className="mr-4 hover:underline md:mr-6">
                            Privacy Policy
                        </a>
                    </li>
                    <li>
                        <a href="#" className="mr-4 hover:underline md:mr-6">
                            Licensing
                        </a>
                    </li>
                    <li>
                        <a href="#" className="hover:underline">
                            Contact
                        </a>
                    </li>
                </ul>
            </div>

            <hr className="border-gray-300 mx-auto max-w-screen-xl mt-2" />

            <div className="w-full max-w-screen-xl p-4 text-center">
                <span className="text-sm text-gray-500">
                    © 2025 Start BootStrap
                </span>
            </div>
        </footer>
    );
}
