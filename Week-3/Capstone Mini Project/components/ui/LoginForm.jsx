"use client";

import { useState } from "react";
import { FaUser, FaLock } from "react-icons/fa";

export default function LoginForm() {


    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-100">
            <div className="w-[380px] p-6">

                <div className="flex items-center gap-3 bg-white border rounded-lg px-4 py-3 mb-4 shadow-sm">
                    <FaUser className="text-gray-400 text-lg" />
                    <input
                        type="text"
                        placeholder="Username"
                        className="w-full outline-none text-gray-700 placeholder-gray-400"
                    />
                </div>

                <div className="flex items-center gap-3 bg-white border rounded-lg px-4 py-3 mb-4 shadow-sm">
                    <FaLock className="text-gray-400 text-lg" />
                    <input
                        type="password"
                        placeholder="Password"
                        className="w-full outline-none text-gray-700 placeholder-gray-400"
                    />
                </div>

                <div className="flex justify-between items-center mb-5">
                    <label className="flex items-center gap-2 text-gray-600 text-sm">
                        <input
                            type="checkbox"
                            className="h-4 w-4"
                        />
                        Remember me
                    </label>

                    <button className="text-gray-500 text-sm hover:underline">
                        Forgot Password?
                    </button>
                </div>

                <button className="w-full bg-green-500 hover:bg-green-600 text-white font-semibold py-3 rounded-lg">
                    LOGIN
                </button>
            </div>
        </div>
    );
}
