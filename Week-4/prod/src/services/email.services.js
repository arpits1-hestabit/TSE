import { addEmailJob } from "../queues/email.queue.js";

export const sendNotificationEmail = async ({ to, subject, text, requestId }) => {
    await addEmailJob({ to, subject, text, requestId });
    console.log(`[Service] Job added for ${to} (requestId: ${requestId})`);
};
