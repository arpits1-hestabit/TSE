import createApp from "./prod/src/loaders/app.js";
import config from "./prod/src/config/env.js";
import logger from "./prod/src/utils/logger.js";
import errorMiddleware from "./prod/src/middlewares/error.middleware.js";
import { emailWorker } from "./prod/src/workers/email.worker.js";

(async () => {
    try {
        console.log("Starting server...");
        const app = await createApp();

        app.use(errorMiddleware);


        app.listen(config.port, () => {
            logger.info(`✔ Server started on port ${config.port} [${config.nodeEnv}]`);
        });

        emailWorker();
        logger.info("Email worker started")

        process.on("unhandledRejection", (err) => {
            logger.error("Unhandled Promise Rejection: " + err);
            process.exit(1);
        });

        process.on("uncaughtException", (err) => {
            logger.error("Uncaught Exception: " + err);
            process.exit(1);
        });

    } catch (err) {
        logger.error("Fatal startup error: " + err.message);
        process.exit(1);
    }
})();
