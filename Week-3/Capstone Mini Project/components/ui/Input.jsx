"use client";

export default function Input({ className = "", ...props }) {
    return (
        <input
            className={`flex-1 px-4 py-2.5 border rounded-l-lg focus:outline-none placeholder:text-gray-600 placeholder:font-bold text-black ${className}`}
            {...props}
        />
    );
}
