import fs from "fs";
import path from "path";
import dotenv from "dotenv";

const env = process.env.NODE_ENV || "local";

// Map of environment file names
const envFileMap = {
  production: ".env.prod",
  development: ".env.dev",
  local: ".env.local",
};

const envFile = envFileMap[env] || `.env.${env}`;
const envPath = path.resolve(process.cwd(), envFile);

//will only execute if the file exists
if (fs.existsSync(envPath)) {
  dotenv.config({ path: envPath });
  console.log(`[CONFIG] Loaded environment file: ${envFile}`);
} else {
  console.warn(`[CONFIG] Environment file not found: ${envFile}`);
  process.exit(1);
}

export default {
  port: process.env.PORT || 5000,
  dbUri: process.env.MONGODB_URI || process.env.DB_URI,
  nodeEnv: env,
};
