"use client";

import Graph from "./Graph";

const barData = {
    labels: ["January", "February", "March", "April", "May", "June"],
    datasets: [
        {
            data: [4000, 5200, 6300, 7800, 9900, 15000],
            backgroundColor: "rgba(37, 99, 235, 1)",
        },
    ],
};

const barOptions = {
    plugins: {
        legend: {
            display: false,
        },
    },
};

export default function BarChart() {
    return (
        <div className="w-full h-96">
            <Graph type="bar" data={barData} options={barOptions} title="Bar Chart Example" />
        </div>
    );
}
