export default function errorMiddleware(err, req, res, next) {
    console.error("Error:", err);
        
    res.status(400).json({
        success: false,
        message: err.message || "Something went wrong",
        code: 400,
        timestamp: new Date().toISOString(),
        path: req.originalUrl
    });
}
