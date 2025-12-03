import { Worker } from "bullmq";
import { emailQueue } from "../queues/email.queue.js";
import fs from "fs";
import path from "path";

const logFile = path.resolve("src/logs/email.app.log");

const logger = {
    info: (message, requestId = null) => {
        const timestamp = new Date().toISOString();
        const logMessage = requestId
            ? `[${timestamp}] [INFO] [${requestId}] ${message}`
            : `[${timestamp}] [INFO] ${message}`;
        fs.appendFileSync(logFile, logMessage + "\n");
        console.log(logMessage);
    },
    error: (message, requestId = null) => {
        const timestamp = new Date().toISOString();
        const logMessage = requestId
            ? `[${timestamp}] [ERROR] [${requestId}] ${message}`
            : `[${timestamp}] [ERROR] ${message}`;
        fs.appendFileSync(logFile, logMessage + "\n");
        console.error(logMessage);
    },
};

export const emailWorker = () => {
    const worker = new Worker(
        "emailQueue",
        async (job) => {
            const requestId = job.data.requestId || null;
            logger.info(`[Worker] Processing job ${job.id}: ${JSON.stringify(job.data)}`, requestId);
            // dummy mail sending logic
            await new Promise((resolve) => setTimeout(resolve, 1000))

            logger.info(`[Worker] Job ${job.id} processed successfully`, requestId);
            return { status: "done" };
        },
        { connection: emailQueue.opts.connection }
    );

    worker.on("completed", (job) => {
        const requestId = job.data.requestId || null;
        logger.info(`[Worker] Job ${job.id} completed`, requestId);
    });

    worker.on("failed", (job, err) => {
        const requestId = job.data.requestId || null;
        logger.error(`[Worker] Job ${job.id} failed: ${err?.message || "unknown error"}`, requestId);
    });

    logger.info("[Worker] Email worker initialized");
};
