const os =  require('os')
const fs = require('fs')

const osType = os.type();
const osPlatform = os.platform();
const osRelease = os.release();

const architecture = os.arch();

const cpuCores = os.cpus().length;

const totalMemory = os.totalmem() / (1024*1024*1024);

const uptime = os.uptime();
const uptimeFormatted = new Date(uptime * 1000).toISOString().substr(11,8);

const currentUser = os.userInfo().username;
const nodePath = process.execPath;

console.log('OS:', `${osType} ${osPlatform} ${osRelease}`);
console.log('Architecture:', architecture);
console.log('CPU Cores:', cpuCores);
console.log('Total Memory:', `${totalMemory.toFixed(2)} GB`);
console.log('System Uptime:', uptimeFormatted);
console.log('Current Logged User:', currentUser);
console.log('Node Path:', nodePath);
