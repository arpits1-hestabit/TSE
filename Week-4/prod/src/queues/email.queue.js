import { Queue } from "bullmq";
import IORedis from "ioredis";

//Redis connection options for BullMQ
const connection = new IORedis({
  host: "127.0.0.1",
  port: 6379,
  maxRetriesPerRequest: null, // IMPORTANT for BullMQ
});

export const emailQueue = new Queue("emailQueue", {
  connection,
});

export const addEmailJob = async (data) => {
  await emailQueue.add("sendEmail", data, {
    attempts: 5,
    backoff: { type: "exponential", delay: 5000 },
    removeOnComplete: true,
    removeOnFail: false,
  });
};
