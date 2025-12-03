import fs from "fs";

const logFilePath = "../src/logs/email.app.log";

const writeLog = (level, message) => {
    const timestamp = new Date().toISOString();
    const logMessage = `[${timestamp}] [${level.toUpperCase()}] ${message}\n`;

    fs.appendFileSync(logFilePath, logMessage);
};

const logger = {
    info: (msg) => writeLog("info", msg),
    error: (msg) => writeLog("error", msg),
    warn: (msg) => writeLog("warn", msg),
};

export default logger;
