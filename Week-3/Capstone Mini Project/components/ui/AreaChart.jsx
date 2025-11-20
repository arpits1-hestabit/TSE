"use client";
import Graph from "./Graph";
const areaData = {
    labels: ["Mar 1", "Mar 3", "Mar 5", "Mar 7", "Mar 9", "Mar 11", "Mar 13"],
    datasets: [
        {
            data: [10000, 30000, 22000, 29000, 26000, 33000, 38000],
            fill: true,
            backgroundColor: "rgba(59, 130, 246, 0.3)",
            tension: 0.4,
            pointRadius: 4,
            pointBackgroundColor: "rgba(59, 130, 246, 1)",
        },
    ],
};
const areaOptions = {
    plugins: {
        legend: {
            display: false,
        },
    },
};

export default function AreaChart() {
    return (
        <div className="w-full h-96">
            <Graph type="line" data={areaData} options={areaOptions} title="Area Chart Example" />
        </div>
    );
}
