const fs = require('fs');

const startTime = process.hrtime.bigint();
const startMemory = process.memoryUsage().heapUsed;

fs.readFile('bigfile.txt', (err, data) => {
  if (err) throw err;

  const endTime = process.hrtime.bigint();
  const endMemory = process.memoryUsage().heapUsed;

  console.log(`File size: ${(data.length / (1024 * 1024)).toFixed(2)} MB`);
  console.log(`Execution time: ${Number(endTime - startTime) / 1e6} ms`);
  console.log(`Memory used: ${((endMemory - startMemory) / (1024 * 1024)).toFixed(2)} MB`);
});
