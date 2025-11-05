#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const yargs = require('yargs');

// Parse CLI arguments
const argv = yargs
  .usage('Usage: $0 --file <file> --top <number> --minLen <number> --unique')
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
  .argv;

// Function to process the corpus text file
const processFile = (filePath, minLen, top, unique) => {
  fs.readFile(filePath, 'utf8', (err, data) => {
    if (err) {
      console.error('Error reading the file:', err);
      return;
    }

    // Clean and split the data into words
    const words = data
      .toLowerCase()
      .replace(/[^a-z\s]/g, '') // Remove non-alphabetic characters
      .split(/\s+/)
      .filter(word => word.length >= minLen); // Filter based on minLen

    // Word count calculations
    const wordCounts = words.reduce((acc, word) => {
      acc[word] = (acc[word] || 0) + 1;
      return acc;
    }, {});

    const totalWords = words.length;
    const uniqueWords = Object.keys(wordCounts).length;

    const longestWord = words.reduce((longest, current) => current.length > longest.length ? current : longest, '');
    const shortestWord = words.reduce((shortest, current) => current.length < shortest.length ? current : shortest, words[0]);

    // Sort words by frequency
    const sortedWords = Object.entries(wordCounts)
      .sort(([, a], [, b]) => b - a) // Sort by frequency, descending
      .slice(0, top);

    // Output the results
    console.log(`Total words: ${totalWords}`);
    console.log(`Unique words: ${uniqueWords}`);
    console.log(`Longest word: ${longestWord}`);
    console.log(`Shortest word: ${shortestWord}`);
    console.log(`Top ${top} most repeated words:`);

    sortedWords.forEach(([word, count]) => {
      console.log(`${word}: ${count}`);
    });
  });
};

// Main execution
processFile(path.resolve(argv.file), argv.minLen, argv.top, argv.unique);
