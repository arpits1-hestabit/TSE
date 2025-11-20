"use client";

export default function Card({ className = "", title, value, color1, color2 }) {
    return (
        <div className={`bg-white rounded-lg min-w-[100px] shadow-sm overflow-hidden flex flex-col flex-1 ${className}`}>
            <div className={`flex items-center justify-between p-4 text-white ${color1}`}>
                <div className="text-xl font-bold">
                    {title}
                </div>
            </div>
            <div className={`p-4 font-semibold text-lg ${color2}`}>
                {value}
            </div>
        </div>
    );
}
