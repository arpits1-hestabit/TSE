import winston from "winston";

const logger = winston.createLogger({
    level: "info",
    format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.printf(({ timestamp, level, message }) => {
            return `${timestamp} ${level}: ${message}`;
        })
    ),
    transports: [
        new winston.transports.Console(),
        new winston.transports.File({ filename: 'src/logs/app.log' }),// if I don't want to hardcode the paths, then I will have to make use of fileURLToPath and path modules.
        new winston.transports.File({ filename: 'src/logs/error.log', level: 'error' })
    ]
});

export default logger;
