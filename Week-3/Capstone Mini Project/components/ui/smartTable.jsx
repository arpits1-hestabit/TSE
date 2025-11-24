"use client";
import Input from "./Input";
import React, { useState } from "react";
const sampleUsers = [
  { name: "Shivang Jha", email: "Shivang@gamail.com", role: "Admin", created: "18/10/2024 05:27", updated: "18/10/2024 05:27" },
  { name: "Arpit Saxena", email: "Arpit27@gamil.com", role: "User", created: "18/10/2024 05:27", updated: "18/10/2024 05:27" },
  { name: "Harshath Venkatesh", email: "HarshathHV18@gmail.com", role: "User", created: "18/10/2024 05:27", updated: "18/10/2024 05:27" },
  { name: "Aakash Sheoran", email: "Aakash.sheoran@gamil.com", role: "User", created: "18/10/2024 05:27", updated: "18/10/2024 05:27" },
  { name: "Shobhit Raj", email: "Shobbit.raj@gmail.com", role: "User", created: "18/10/2024 05:27", updated: "18/10/2024 05:27" },
  { name: "Chandramohan", email: "Chandramohan297@gmail.com", role: "User", created: "18/10/2024 05:27", updated: "18/10/2024 05:27" },
  { name: "Manya Sharma", email: "Manya.Sharma@gmail.com", role: "User", created: "18/10/2024 05:27", updated: "18/10/2024 05:27" },
  { name: "Vidhi", email: "Vidhi23802@gmail.com", role: "User", created: "18/10/2024 05:27", updated: "18/10/2024 05:27" },
  { name: "Farhan Nawaz", email: "Farhan2427@gamil.com", role: "User", created: "18/10/2024 05:27", updated: "18/10/2024 05:27" },
  { name: "Aryan Shukla", email: "Aryan0024@gmail.com", role: "User", created: "18/10/2024 05:27", updated: "18/10/2024 05:27" },
];

function SmartTable() {
  const [search, setSearch] = useState("");
  const filtered = sampleUsers.filter(
    user =>
      user.name.toLowerCase().includes(search.toLowerCase()) ||
      user.email.toLowerCase().includes(search.toLowerCase())
  );
  return (
    <div className="w-full bg-white border rounded-lg shadow-sm">
      <div className="flex justify-between items-center p-4 bg-gray-200">
        <h2 className="text-xl font-semibold">Users</h2>
        <div >
            <Input />
        </div>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-sm text-left">
          <thead className="border-b bg-gray-50">
            <tr>
              <th className="py-3 px-4">Name</th>
              <th className="py-3 px-4">Email</th>
              <th className="py-3 px-4">Role</th>
              <th className="py-3 px-4">Created at</th>
              <th className="py-3 px-4">Updated at</th>
            </tr>
          </thead>

          <tbody>
            {filtered.map((user, index) => (
              <tr key={index} className="border-b hover:bg-gray-50">
                <td className="py-3 px-4">{user.name}</td>
                <td className="py-3 px-4">{user.email}</td>
                <td className="py-3 px-4">{user.role}</td>
                <td className="py-3 px-4">{user.created}</td>
                <td className="py-3 px-4">{user.updated}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="flex justify-between items-center text-sm text-gray-600  p-4">
        <p>Showing {filtered.length} of 10 results</p>
        <div className="flex gap-2">
          <button className="border rounded-md px-2 py-1">1</button>
          <button className="border rounded-md px-2 py-1">2</button>
        </div>
      </div>
    </div>
  );
}

export default SmartTable;