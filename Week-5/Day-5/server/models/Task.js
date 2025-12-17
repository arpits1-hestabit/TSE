import mongoose from "mongoose";
const TaskSchema = new mongoose.Schema({
  text: {
    type: String,
    required: true,
  },
});
export default mongoose.model("Task", TaskSchema);