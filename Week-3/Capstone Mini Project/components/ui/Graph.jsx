"use client";

import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    BarElement,
    ArcElement,
    Title as ChartTitle,
    Tooltip,
    Legend,
    Filler,
} from "chart.js";
import { Chart } from "react-chartjs-2";
import { FaChartBar, FaChartLine, FaChartArea } from "react-icons/fa";

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    BarElement,
    ArcElement,
    ChartTitle,
    Tooltip,
    Legend,
    Filler
);

export default function Graph({ type = "line", data, options, title, icon }) {
    const IconComponent =
        icon ||
        (type === "line" ? FaChartLine : type === "bar" ? FaChartBar : FaChartArea);

    return (
        <div className="border border-gray-300 rounded shadow-sm bg-white h-full w-full flex flex-col">
            {title && (
                <div className="flex items-center p-3 border-b border-gray-300 text-gray-700 font-semibold">
                    <IconComponent className="h-5 w-5 mr-2" />
                    {title}
                </div>
            )}
            <div className="p-4 flex-1">
                <Chart
                    type={type}
                    data={data}
                    options={{ responsive: true, maintainAspectRatio: false, ...options }}
                    style={{ width: "100%", height: "100%" }}
                />
            </div>
        </div>
    );
}
