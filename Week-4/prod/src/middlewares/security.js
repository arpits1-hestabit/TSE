import cors from "cors";
import helmet from "helmet";
import rateLimit from "express-rate-limit";
import express from "express";


export const securityMiddleware = (app) => {
    //enabling CORS
    app.use(
        cors({
            origin: "http://localhost:3000",
            methods: "GET,POST,PUT,DELETE",
        })
    );

    app.use(helmet());

    app.use(
        rateLimit({
            windowMs: 1 * 60 * 1000, // 1 min.
            max: 10, // 10 requests per window
            message: {
                success: false,
                message: "Too many requests, slow down.",
                code: 429,
                timestamp: new Date().toISOString(),
            },
        })
    );

    // requesting payload limit
    app.use(express.json({ limit: "1mb" }));
};
