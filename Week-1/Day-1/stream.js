const fs = require('fs');

const startTime = process.hrtime.bigint();
const startMemory = process.memoryUsage().heapUsed;

const stream = fs.createReadStream('bigfile.txt');

let bytesRead = 0;

stream.on('data', chunk => {
  bytesRead += chunk.length;
});

stream.on('end', () => {
  const endTime = process.hrtime.bigint();
  const endMemory = process.memoryUsage().heapUsed;

  console.log(`File size: ${(bytesRead / (1024 * 1024)).toFixed(2)} MB`);
  console.log(`Execution time: ${Number(endTime - startTime) / 1e6} ms`);
  console.log(`Memory used: ${((endMemory - startMemory) / (1024 * 1024)).toFixed(2)} MB`);
});

stream.on('error', err => {
  console.error(err);
});
