// Import Node.js built-in OS module
// This module provides operating system-related utility methods and properties
const os = require("os");

// Import File System module (not used in this code currently, but can be used for saving output to a file)
const fs = require("fs");

// Get the operating system type (e.g., Linux, Windows_NT, Darwin)
const osType = os.type();

// Get the platform of the operating system (e.g., win32, linux, darwin)
const osPlatform = os.platform();

// Get the OS release version (e.g., kernel version)
const osRelease = os.release();

// Get system architecture (e.g., x64, arm)
const architecture = os.arch();

// Get the number of CPU cores available in the system
// os.cpus() returns an array of CPU core details
const cpuCores = os.cpus().length;

// Get total system memory in bytes and convert it into GB
const totalMemory = os.totalmem() / (1024 * 1024 * 1024);

// Get system uptime in seconds (time since last reboot)
const uptime = os.uptime();

// Convert uptime into HH:MM:SS format for better readability
const uptimeFormatted = new Date(uptime * 1000).toISOString().substr(11, 8);

// Get the currently logged-in user's username
const currentUser = os.userInfo().username;

// Get the path of the Node.js executable being used
const nodePath = process.execPath;

// Display collected system information in the console
console.log("OS:", `${osType} ${osPlatform} ${osRelease}`);
console.log("Architecture:", architecture);
console.log("CPU Cores:", cpuCores);
console.log("Total Memory:", `${totalMemory.toFixed(2)} GB`);
console.log("System Uptime:", uptimeFormatted);
console.log("Current Logged User:", currentUser);
console.log("Node Path:", nodePath);
