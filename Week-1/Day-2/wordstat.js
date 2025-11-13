#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const yargs = require('yargs');
const { Worker, isMainThread, parentPort, workerData } = require('worker_threads');

// Parse CLI arguments only in the main thread
const argv = isMainThread
  ? yargs
    .usage('Usage: $0 --file <file> --top <number> --minLen <number> --unique --concurrency <number>')
    .option('file', {
      alias: 'f',
      description: 'Path to the corpus text file',
      type: 'string',
      demandOption: true,
    })
    .option('top', {
      alias: 't',
      description: 'Number of top most repeated words to display',
      type: 'number',
      default: 10,
    })
    .option('minLen', {
      alias: 'm',
      description: 'Minimum word length to include in analysis',
      type: 'number',
      default: 1,
    })
    .option('unique', {
      alias: 'u',
      description: 'Show only unique words in the analysis',
      type: 'boolean',
      default: false,
    })
    .option('concurrency', {
      alias: 'c',
      description: 'Number of worker threads to use for concurrency',
      type: 'number',
      default: 1, // Default concurrency level is 1
    })
    .argv
  : null; // Don't parse arguments in worker threads

// Function to process a chunk of file in worker thread
if (!isMainThread) {
  const { start, end, filePath } = workerData;

  const buffer = Buffer.alloc(end - start);
  const fd = fs.openSync(filePath, 'r');
  fs.read(fd, buffer, 0, buffer.length, start, (err, bytesRead, buffer) => {
    if (err) {
      parentPort.postMessage({ error: err.message });
      return;
    }

    const data = buffer.toString('utf-8');
    const words = data
      .toLowerCase()
      .replace(/[^a-z\s]/g, '') // Remove non-alphabetic characters
      .split(/\s+/);

    parentPort.postMessage({ words });
  });
}

// Main thread: logic to split the file into chunks and process concurrently using workers
if (isMainThread) {
  const processFileConcurrently = (filePath, chunkSize, concurrencyLevel) => {
    const fileStats = fs.statSync(filePath);
    const fileSize = fileStats.size;
    const numChunks = Math.ceil(fileSize / chunkSize);
    const workers = [];
    const chunkPromises = [];

    console.log(`Processing file ${filePath} with ${concurrencyLevel} workers...`);

    const chunksPerWorker = Math.ceil(numChunks / concurrencyLevel);

    // Distribute the chunks evenly among workers
    for (let i = 0; i < concurrencyLevel; i++) {
      const start = i * chunksPerWorker * chunkSize;
      const end = Math.min((i + 1) * chunksPerWorker * chunkSize, fileSize);

      const worker = new Worker(__filename, {
        workerData: { start, end, filePath },
      });

      const promise = new Promise((resolve, reject) => {
        worker.on('message', (result) => {
          if (result.error) {
            reject(result.error);
          } else {
            resolve(result.words);
          }
        });

        worker.on('error', reject);
        worker.on('exit', (code) => {
          if (code !== 0) reject(new Error(`Worker stopped with exit code ${code}`));
        });
      });

      chunkPromises.push(promise);
    }

    return Promise.all(chunkPromises);
  };

  // Function to benchmark the processing time and memory usage
  const benchmarkPerformance = async (filePath, concurrencyLevel) => {
    const startTime = Date.now();
    const startMemory = process.memoryUsage().heapUsed;

    const chunkSize = 1 * 1024 * 1024; // 1 MB chunk size for each worker
    try {
      const allWords = await processFileConcurrently(filePath, chunkSize, concurrencyLevel);

      // Aggregate and process words from all chunks
      const allWordsFlat = allWords.flat();
      const wordCounts = allWordsFlat.reduce((acc, word) => {
        acc[word] = (acc[word] || 0) + 1;
        return acc;
      }, {});

      const sortedWords = Object.entries(wordCounts)
        .sort(([, a], [, b]) => b - a)
        .slice(0, argv.top);

      console.log(`Top ${argv.top} most repeated words:`);
      sortedWords.forEach(([word, count]) => {
        console.log(`${word}: ${count}`);
      });
    } catch (err) {
      console.error('Error processing file:', err);
    }

    const endTime = Date.now();
    const endMemory = process.memoryUsage().heapUsed;

    // Log performance metrics
    const executionTimeInSeconds = (endTime - startTime) / 1000;
    const memoryUsageInMB = (endMemory - startMemory) / 1024 / 1024;

    console.log(`\nConcurrency Level: ${concurrencyLevel}`);
    console.log(`Execution time: ${executionTimeInSeconds} seconds`);
    console.log(`Memory used: ${memoryUsageInMB} MB`);

    // Save the performance metrics to a JSON file
    const perfLog = {
      concurrencyLevel,
      executionTimeInSeconds,
      memoryUsageInMB,
    };

    // Ensure 'logs' directory exists
    const logDirectory = path.resolve(__dirname, 'logs');
    if (!fs.existsSync(logDirectory)) {
      fs.mkdirSync(logDirectory, { recursive: true });
    }

    const logFilePath = path.resolve(logDirectory, 'perf-summary.json');
    try {
      let existingLogData = [];
      if (fs.existsSync(logFilePath)) {
        const rawData = fs.readFileSync(logFilePath, 'utf-8');
        existingLogData = JSON.parse(rawData);
      }

      existingLogData.push(perfLog);

      fs.writeFileSync(logFilePath, JSON.stringify(existingLogData, null, 2));
      console.log(`Performance logged in ${logFilePath}`);
    } catch (error) {
      console.error('Error writing to perf-summary.json:', error);
    }
  };

  // Run benchmark for the provided concurrency level
  benchmarkPerformance(path.resolve(argv.file), argv.concurrency);
}
