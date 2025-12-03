module.exports = {
  apps: [
    {
      name: "tse-email-service",  
      script: "../index.js",
      watch: false,
      exec_mode: "cluster", // this is optional, used for clustering
      instances: 20,
      env: {
        NODE_ENV: "development",
        PORT: 5000,
        DB_URI: "mongodb://localhost:27017/mydatabase"
      },
      env_production: {
        NODE_ENV: "production",
        PORT: 5000,
      },
      error_file: "./logs/pm2-err.log",   // PM2 logs
      out_file: "./logs/pm2-out.log",
      merge_logs: true,
      log_date_format: "YYYY-MM-DD HH:mm:ss",
    },
  ],
};
