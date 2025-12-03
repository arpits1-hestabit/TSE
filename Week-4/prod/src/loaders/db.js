import mongoose from "mongoose";
import config from "../config/env.js"
import logger from "../utils/logger.js"


export default async function loadDatabase() {
    try {
        await mongoose.connect(config.dbUri);
        logger.info("db connected");
    } catch (err) {
        logger.error("db connection error" + err.message);
        process.exit(1);
    }
}