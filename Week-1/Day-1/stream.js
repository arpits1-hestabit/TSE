// Import Node.js built-in File System module
// This module provides APIs to interact with the file system
const fs = require("fs");

// Record the start time using a high-resolution timer (nanoseconds as BigInt)
const startTime = process.hrtime.bigint();

// Record initial memory usage of the heap before starting the file read
const startMemory = process.memoryUsage().heapUsed;

// Create a readable stream for 'bigfile.txt'
// Streams allow reading large files piece by piece without loading the entire file into memory
const stream = fs.createReadStream("bigfile.txt");

// Variable to keep track of total bytes read
let bytesRead = 0;

// Event listener for 'data' event
// Triggered whenever a chunk of data is read from the file
stream.on("data", (chunk) => {
  bytesRead += chunk.length; // Increment total bytes read
});

// Event listener for 'end' event
// Triggered when the file has been fully read
stream.on("end", () => {
  // Record end time and memory usage after reading the file
  const endTime = process.hrtime.bigint();
  const endMemory = process.memoryUsage().heapUsed;

  // Display total file size in megabytes
  console.log(`File size: ${(bytesRead / (1024 * 1024)).toFixed(2)} MB`);

  // Display execution time in milliseconds
  console.log(`Execution time: ${Number(endTime - startTime) / 1e6} ms`);

  // Display memory used during the file reading process in megabytes
  console.log(
    `Memory used: ${((endMemory - startMemory) / (1024 * 1024)).toFixed(2)} MB`,
  );
});

// Event listener for 'error' event
// Triggered if an error occurs while reading the file
stream.on("error", (err) => {
  console.error("Error reading file:", err);
});
