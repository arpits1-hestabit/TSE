#!/usr/bin/env node
// This line allows the script to be run directly from the command line as a Node.js program

const fs = require("fs"); // File system module to read files
const path = require("path"); // Module to handle file paths
const yargs = require("yargs"); // Library to parse command-line arguments
const {
  Worker,
  isMainThread,
  parentPort,
  workerData,
} = require("worker_threads");
// Worker threads allow us to run CPU-intensive tasks in parallel

// Parse command-line arguments
// Only the main thread parses CLI arguments
const argv = isMainThread
  ? yargs
      .usage(
        "Usage: $0 --file <file> --top <number> --minLen <number> --unique --concurrency <number>",
      )
      .option("file", {
        alias: "f",
        description: "The text file to analyze",
        type: "string",
        demandOption: true,
      })
      .option("top", {
        alias: "t",
        description: "Number of most frequent words to show",
        type: "number",
        default: 10,
      })
      .option("minLen", {
        alias: "m",
        description: "Ignore words shorter than this length",
        type: "number",
        default: 1,
      })
      .option("unique", {
        alias: "u",
        description: "Show only words that appear once",
        type: "boolean",
        default: false,
      })
      .option("concurrency", {
        alias: "c",
        description: "Number of parallel workers to use",
        type: "number",
        default: 1,
      }).argv
  : null; // Worker threads do not need CLI arguments

// Worker thread code
// This code runs inside a worker thread and processes a portion of the file
if (!isMainThread) {
  const { start, end, filePath } = workerData; // Get data passed from main thread

  // Create a buffer to hold this chunk of the file
  const buffer = Buffer.alloc(end - start);
  const fd = fs.openSync(filePath, "r");

  // Read the chunk from the file
  fs.read(fd, buffer, 0, buffer.length, start, (err, bytesRead, buffer) => {
    if (err) {
      parentPort.postMessage({ error: err.message }); // Send error back to main thread
      return;
    }

    // Convert the chunk to a string, clean it, and split into words
    const data = buffer.toString("utf-8");
    const words = data
      .toLowerCase()
      .replace(/[^a-z\s]/g, "") // Remove everything except letters and spaces
      .split(/\s+/); // Split into words based on whitespace

    parentPort.postMessage({ words }); // Send the words back to the main thread
  });
}

// Main thread code
if (isMainThread) {
  
   //Split the file into chunks and process each chunk with a worker
   //@param filePath - the path of the file to analyze
   //@param chunkSize - size of each chunk in bytes
   //@param concurrencyLevel - how many workers to run at the same time
  
  const processFileConcurrently = (filePath, chunkSize, concurrencyLevel) => {
    const fileStats = fs.statSync(filePath); // Get file info (size)
    const fileSize = fileStats.size; // Total size of file in bytes
    const numChunks = Math.ceil(fileSize / chunkSize); // Total chunks needed
    const chunkPromises = []; // Will store promises from workers

    console.log(
      `Processing file ${filePath} with ${concurrencyLevel} workers...`,
    );

    const chunksPerWorker = Math.ceil(numChunks / concurrencyLevel); // Divide work evenly

    // Launch workers

    for (let i = 0; i < concurrencyLevel; i++) {
      const start = i * chunksPerWorker * chunkSize;
      const end = Math.min((i + 1) * chunksPerWorker * chunkSize, fileSize);

      const worker = new Worker(__filename, {
        workerData: { start, end, filePath },
      });

      // Wrap each worker in a promise to wait for its result
      const promise = new Promise((resolve, reject) => {
        worker.on("message", (result) => {
          if (result.error) {
            reject(result.error); // Worker reported an error
          } else {
            resolve(result.words); // Worker finished successfully
          }
        });

        worker.on("error", reject); // Handle thread errors
        worker.on("exit", (code) => {
          if (code !== 0)
            reject(new Error(`Worker stopped with exit code ${code}`));
        });
      });

      chunkPromises.push(promise);
    }

    return Promise.all(chunkPromises); // Wait for all workers to finish
  };

  
   //Measure performance of processing the file
   //Logs execution time, memory usage, and top repeated words
   
  const benchmarkPerformance = async (filePath, concurrencyLevel) => {
    const startTime = Date.now();
    const startMemory = process.memoryUsage().heapUsed;

    const chunkSize = 1 * 1024 * 1024; // 1 MB chunks

    try {
      // Process file with workers
      const allWords = await processFileConcurrently(
        filePath,
        chunkSize,
        concurrencyLevel,
      );

      // Flatten arrays from all workers into one array
      const allWordsFlat = allWords.flat();

      // Count occurrences of each word
      const wordCounts = allWordsFlat.reduce((acc, word) => {
        acc[word] = (acc[word] || 0) + 1;
        return acc;
      }, {});

      // Sort words by count and pick top N
      const sortedWords = Object.entries(wordCounts)
        .sort(([, a], [, b]) => b - a)
        .slice(0, argv.top);

      console.log(`Top ${argv.top} most repeated words:`);
      sortedWords.forEach(([word, count]) => console.log(`${word}: ${count}`));
    } catch (err) {
      console.error("Error processing file:", err);
    }

    const endTime = Date.now();
    const endMemory = process.memoryUsage().heapUsed;

    // Show execution metrics
    console.log(`\nConcurrency Level: ${concurrencyLevel}`);
    console.log(`Execution time: ${(endTime - startTime) / 1000} seconds`);
    console.log(`Memory used: ${(endMemory - startMemory) / 1024 / 1024} MB`);

    // Save metrics to a JSON log file
    const perfLog = {
      concurrencyLevel,
      executionTimeInSeconds: (endTime - startTime) / 1000,
      memoryUsageInMB: (endMemory - startMemory) / 1024 / 1024,
    };

    const logDirectory = path.resolve(__dirname, "logs");
    if (!fs.existsSync(logDirectory))
      fs.mkdirSync(logDirectory, { recursive: true });

    const logFilePath = path.resolve(logDirectory, "perf-summary.json");
    try {
      let existingLogData = [];
      if (fs.existsSync(logFilePath)) {
        existingLogData = JSON.parse(fs.readFileSync(logFilePath, "utf-8"));
      }
      existingLogData.push(perfLog);
      fs.writeFileSync(logFilePath, JSON.stringify(existingLogData, null, 2));
      console.log(`Performance logged in ${logFilePath}`);
    } catch (error) {
      console.error("Error writing log file:", error);
    }
  };

  // Run performance benchmark using the provided concurrency level
  benchmarkPerformance(path.resolve(argv.file), argv.concurrency);
}
