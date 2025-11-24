import Card from "@/components/ui/Card";
import AreaChart from "@/components/ui/AreaChart";
import BarChart from "@/components/ui/BarChart";
import DataTable from "@/components/ui/Table";


export default function Home() {
    return (
        <div className="flex min-h-screen flex-wrap flex-col flex-1 space-evenly bg-white font-sans text-black font-bold">

            <h1 className="text-4xl font-bold mt-4 ml-8 mb-3">Dashboard</h1>
            <div className="bg-gray-200 flex flex-wrap rounded-md p-3 mt-4 ml-8 mr-8 text-gray-700 font-semibold">
                Dashboard
            </div>


            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 ml-8 mr-8 mt-4">
                <Card title="Primary Button" value="View Details" color1="bg-blue-600" color2="bg-blue-400" />
                <Card title="Success Button" value="View Details" color1="bg-green-600" color2="bg-green-100" />
                <Card title="Warning Button" value="View Details" color1="bg-yellow-500" color2="bg-yellow-100" />
                <Card title="Danger Button" value="View Details" color1="bg-red-600" color2="bg-red-100" />
            </div>
            <div className="grid grid-cols-1 min-h-[350px] md:grid-cols-2 gap-6 mt-8 ml-8 mr-8">
                <div className="p-4 bg-white rounded shadow">
                    <AreaChart />
                </div>
                <div className="p-4 bg-white rounded shadow">
                    <BarChart />
                </div>
            </div>
            <div className="mt-4">
                <DataTable />
            </div>
        </div >
    );
}


export const metadata = {
    title: "About Page",
    description: "Capstone mini project — admin dashboard with reusable UI components.",
    keywords: "dashboard,nextjs,tailwind,charts,ui",
    authors: [{ name: "Arpit Saxena" }],
};