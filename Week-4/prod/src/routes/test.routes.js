import express from "express";
import { sendNotificationEmail } from "../services/email.services.js";

const router = express.Router();

/**
 * @swagger
 * tags:
 *   name: Email
 *   description: Email job queue APIs
 */

/**
 * @swagger
 * /send-email:
 *   post:
 *     summary: Queue an email to be sent asynchronously (BullMQ worker)
 *     tags: [Email]
 *     parameters:
 *       - in: header
 *         name: X-Request-ID
 *         required: false
 *         schema:
 *           type: string
 *         description: Auto-generated request tracking ID
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             $ref: '#/components/schemas/SendEmail'
 *     responses:
 *       201:
 *         description: Email job queued successfully
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 success:
 *                   type: boolean
 *                   example: true
 *                 message:
 *                   type: string
 *                   example: "Email job queued"
 *                 requestId:
 *                   type: string
 *                   example: "c7c4c0e8-3de0-4e71-b0c1-92f65b6c0901"
 *       500:
 *         description: Internal server error
 */
router.post("/send-email", async (req, res) => {
  try {
    const requestId = req.requestId;

    await sendNotificationEmail({
      ...req.body,
      requestId,
    });

    res.status(201).json({
      success: true,
      message: "Email job queued",
      requestId,
    });

  } catch (err) {
    res.status(500).json({ success: false, message: err.message });
  }
});

export default router;
