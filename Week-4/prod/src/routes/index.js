import express from "express";
import productRouter from "./products.routes.js";
import testRoutes from "./test.routes.js";

const router = express.Router();

/**
 * @swagger
 * /hello:
 *   get:
 *     summary: Returns a Hello World message
 *     tags: [General]
 *     responses:
 *       200:
 *         description: Successful response
 *         content:
 *           text/plain:
 *             schema:
 *               type: string
 *               example: Hello World!
 */
router.get("/hello", (req, res) => {
    res.send("Hello World!");
});

/**
 * @swagger
 * /test:
 *   get:
 *     summary: Returns a test message
 *     tags: [General]
 *     responses:
 *       200:
 *         description: Successful response
 *         content:
 *           text/plain:
 *             schema:
 *               type: string
 *               example: Test endpoint
 */
router.get("/test", (req, res) => {
    res.send("Test endpoint");
});

/**
 * @swagger
 * /api:
 *   get:
 *     summary: Test API routes base path
 *     tags: [Test]
 *     description: This is the base path for all test API routes.
 *     responses:
 *       200:
 *         description: Returns test-related data (provided inside test.routes.js)
 */
router.use("/api", testRoutes);

/**
 * @swagger
 * /products:
 *   get:
 *     summary: Product routes base path
 *     tags: [Products]
 *     description: All product-related API endpoints start here.
 *     responses:
 *       200:
 *         description: Provides access to product APIs (from products.routes.js)
 */
router.use("/products", productRouter);

export default router;
