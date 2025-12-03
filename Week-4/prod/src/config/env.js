import fs from "fs";
import path from "path";
import dotenv from "dotenv";

const env = process.NODE_ENV || "local";  // for local|dev |prod
const envFile = `.env.${env}`;
const envPath = path.resolve(process.cwd(), envFile);

//will only execute if the file exists
if (fs.existsSync(envPath)) {
    dotenv.config({ path: envPath });
    console.log(`[CONFIG] Loaded environment file:${envFile}`);
} else {
    console.warn(`[CONFIG] Environment file not found: ${envFile}`);
}

export default {
    port: process.env.PORT || 5000,
    dbUri: process.env.DB_URI,
    nodeEnv: env,
}
