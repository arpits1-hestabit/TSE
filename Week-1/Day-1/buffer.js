// Import Node.js built-in File System module
// This module provides APIs to interact with the file system (read/write files, etc.)
const fs = require("fs");

// Record the start time of execution using high-resolution timer
// process.hrtime.bigint() gives time in nanoseconds as a BigInt value
const startTime = process.hrtime.bigint();

// Record the initial heap memory usage before reading the file
// heapUsed represents the amount of memory currently used by the JavaScript heap
const startMemory = process.memoryUsage().heapUsed;

// Asynchronously read the file "bigfile.txt"
// This will load the entire file content into memory as a Buffer
fs.readFile("bigfile.txt", (err, data) => {
  // Handle error if the file is not found or cannot be read
  if (err) throw err;

  // Record the end time after the file has been successfully read
  const endTime = process.hrtime.bigint();

  // Record the memory usage after reading the file
  const endMemory = process.memoryUsage().heapUsed;

  // Print the file size in MB
  // data.length gives size in bytes, so we convert it into megabytes
  console.log(`File size: ${(data.length / (1024 * 1024)).toFixed(2)} MB`);

  // Print execution time in milliseconds
  // Difference is in nanoseconds, so divide by 1e6 to convert into ms
  console.log(`Execution time: ${Number(endTime - startTime) / 1e6} ms`);

  // Print the memory used during file reading in MB
  // Difference between endMemory and startMemory gives extra heap usage
  console.log(
    `Memory used: ${((endMemory - startMemory) / (1024 * 1024)).toFixed(2)} MB`,
  );
});
