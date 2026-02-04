// app/dashboard/page.jsx
"use client";

import { FaChartArea } from "react-icons/fa";

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      {/* Page Heading */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <h1 className="text-2xl sm:text-3xl font-bold text-gray-800">Dashboard</h1>
      </div>

      {/* Button Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Primary Button Card */}
        <div className="rounded-lg shadow-md overflow-hidden">
          <div className="bg-blue-600 text-white p-4 sm:p-6">
            <h3 className="text-lg sm:text-xl font-bold">Primary Button</h3>
          </div>
          <div className="bg-blue-100 p-4 sm:p-6">
            <button className="text-blue-800 hover:text-blue-900 font-semibold text-sm sm:text-base transition-colors">
              View Details →
            </button>
          </div>
        </div>

        {/* Success Button Card */}
        <div className="rounded-lg shadow-md overflow-hidden">
          <div className="bg-green-600 text-white p-4 sm:p-6">
            <h3 className="text-lg sm:text-xl font-bold">Success Button</h3>
          </div>
          <div className="bg-green-100 p-4 sm:p-6">
            <button className="text-green-800 hover:text-green-900 font-semibold text-sm sm:text-base transition-colors">
              View Details →
            </button>
          </div>
        </div>

        {/* Warning Button Card */}
        <div className="rounded-lg shadow-md overflow-hidden">
          <div className="bg-yellow-500 text-white p-4 sm:p-6">
            <h3 className="text-lg sm:text-xl font-bold">Warning Button</h3>
          </div>
          <div className="bg-yellow-100 p-4 sm:p-6">
            <button className="text-yellow-800 hover:text-yellow-900 font-semibold text-sm sm:text-base transition-colors">
              View Details →
            </button>
          </div>
        </div>

        {/* Danger Button Card */}
        <div className="rounded-lg shadow-md overflow-hidden">
          <div className="bg-red-600 text-white p-4 sm:p-6">
            <h3 className="text-lg sm:text-xl font-bold">Danger Button</h3>
          </div>
          <div className="bg-red-100 p-4 sm:p-6">
            <button className="text-red-800 hover:text-red-900 font-semibold text-sm sm:text-base transition-colors">
              View Details →
            </button>
          </div>
        </div>
      </div>

      {/* Chart Section */}
      <div className="bg-white rounded-lg shadow-md p-4 sm:p-6">
        <div className="flex items-center gap-2 mb-4 pb-4 border-b border-gray-200">
          <FaChartArea className="text-gray-600 text-xl" />
          <h2 className="text-lg sm:text-xl font-bold text-gray-800">Area Chart Example</h2>
        </div>
        
        <div className="h-64 sm:h-80 bg-gradient-to-br from-blue-50 to-blue-100 rounded flex items-center justify-center">
          <div className="text-center">
            <FaChartArea className="text-blue-300 text-6xl mx-auto mb-4" />
            <p className="text-gray-600 font-medium">Area Chart Placeholder</p>
            <p className="text-gray-400 text-sm mt-2">Install chart.js to display charts</p>
          </div>
        </div>
      </div>

      {/* Additional Info Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
        <div className="bg-white p-6 rounded-lg shadow-md border-l-4 border-blue-500">
          <div className="text-sm font-semibold text-blue-600 uppercase">Earnings (Monthly)</div>
          <div className="text-2xl font-bold text-gray-800 mt-2">$40,000</div>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow-md border-l-4 border-green-500">
          <div className="text-sm font-semibold text-green-600 uppercase">Earnings (Annual)</div>
          <div className="text-2xl font-bold text-gray-800 mt-2">$215,000</div>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow-md border-l-4 border-yellow-500">
          <div className="text-sm font-semibold text-yellow-600 uppercase">Tasks</div>
          <div className="text-2xl font-bold text-gray-800 mt-2">50%</div>
        </div>
        
        <div className="bg-white p-6 rounded-lg shadow-md border-l-4 border-red-500">
          <div className="text-sm font-semibold text-red-600 uppercase">Pending Requests</div>
          <div className="text-2xl font-bold text-gray-800 mt-2">18</div>
        </div>
      </div>
    </div>
  );
}