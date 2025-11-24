import React from 'react';
import Input from './Input';
import { FaTable } from 'react-icons/fa';

const DataTable = () => {
    return (
        <div className="border border-gray-300 rounded-md mx-8 mt-4">

            <div className="bg-gray-200 flex flex-row items-center gap-2 rounded-t-md p-3 text-gray-700 font-semibold">
                <FaTable className="text-lg" />
                <span>DataTable Example</span>
            </div>

            <div className="flex justify-between items-center p-2 mt-4">

                <div className="flex items-center">
                    <label className="mr-2">Show</label>
                    <select className="border rounded-md px-2 py-1">
                        <option value={10}>10</option>
                        <option value={25}>25</option>
                        <option value={50}>50</option>
                        <option value={100}>100</option>
                    </select>
                    <label className="ml-2">entries</label>
                </div>

                <div className="w-64">
                    <Input
                        placeholder="Search for..."
                        className="rounded-md border-gray-300 w-full"
                    />
                </div>

            </div>
        </div>
    );
};

export default DataTable;
