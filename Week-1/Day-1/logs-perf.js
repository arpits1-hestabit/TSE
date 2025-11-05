const fs = require('fs');
const { execSync } = require('child_process');
const path = require('path');

const LOG_DIR = 'logs';
const LOG_FILE = path.join(LOG_DIR, 'day1-perf.json');

fs.mkdirSync(LOG_DIR, { recursive: true });

function runScript(script) {
  const startTime = process.hrtime.bigint();
  const startMem = process.memoryUsage().heapUsed;

  // run the existing Node script (blocking)
  execSync(`node ${script}`, { stdio: 'inherit' });

  const endTime = process.hrtime.bigint();
  const endMem = process.memoryUsage().heapUsed;

  const timeMs = Number(endTime - startTime) / 1e6;
  const memoryMB = (endMem - startMem) / (1024 * 1024);

  return {
    timestamp: new Date().toISOString(),
    script,
    timeMs: timeMs.toFixed(2),
    memoryMB: memoryMB.toFixed(2),
  };
}

// run both existing scripts
const results = [runScript('buffer.js'), runScript('stream.js')];

// read old logs (if any)
let existing = [];
if (fs.existsSync(LOG_FILE)) {
  existing = JSON.parse(fs.readFileSync(LOG_FILE, 'utf8'));
}

// append and save
existing.push(...results);
fs.writeFileSync(LOG_FILE, JSON.stringify(existing, null, 2));


