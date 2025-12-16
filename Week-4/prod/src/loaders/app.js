import express from "express";
import loadDatabase from "./db.js";
import loadExpress from "./express.js";
import loadMiddlewares from "../middlewares/index.js";
import routes from "../routes/index.js";
import { securityMiddleware } from "../middlewares/security.js";
import errorMiddleware from "../middlewares/error.middleware.js";
import logger from "../utils/logger.js";
import { requestIdMiddleware } from "../middlewares/requestId.middleware.js";
import { swaggerDocs } from "../config/swagger.js";

export default async function createApp() {
    const app = express();

    await loadDatabase();

    loadExpress(app);

    securityMiddleware(app);

    app.use(requestIdMiddleware);

    loadMiddlewares(app);

    logger.info("Middlewares loaded");

    swaggerDocs(app)

    app.use(routes);


    app.use(errorMiddleware);

    logger.info("App initialized");

    return app;
}
