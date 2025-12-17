import express from "express";
import mongoose from "mongoose";
import cors from "cors";
import dotenv from "dotenv";
import Task from "./models/Task.js";

dotenv.config();
const app = express();
app.use(express.json());
app.use(cors());
mongoose
  .connect(process.env.MONGO_URI)
  .then(() => console.log("MongoDB Connected"))
  .catch((err) => console.log(err));

app.get('/api',(_,res)=>{
  console.log("request hit");
  res.json("request hit");
})
app.get("/health", (req, res) =>{
 res.send("OK")
})
app.get("/api/tasks", async (req, res) => {
  const tasks = await Task.find();
  res.json(tasks);
});
app.post("/api/tasks", async (req, res) => {
  const task = new Task({ text: req.body.text });
  await task.save();
  res.json(task);
});
app.listen(process.env.PORT, () =>
  console.log(`Server running on port ${process.env.PORT}`)
);