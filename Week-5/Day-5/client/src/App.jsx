import { useState, useEffect } from "react";
import axios from "axios";

export default function App() {
  const [text, setText] = useState("");
  const [tasks, setTasks] = useState([]);

  const API_URL = import.meta.env.VITE_API_URL;

  const fetchTasks = async () => {
    const res = await axios.get(`${API_URL}/tasks`);
    setTasks(res.data);
  };

  const addTask = async () => {
    if (!text.trim()) return;
    const res = await axios.post(`${API_URL}/tasks`, { text });
    setTasks([...tasks, res.data]);
    setText("");
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  return (
    <div className="container">
      <h2>Task Adder</h2>

      <div className="input-row">
        <input
          className="input-field"
          type="text"
          placeholder="Enter task..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
        <button className="btn" onClick={addTask}>Add</button>
      </div>

      <ul className="task-list">
        {tasks.map((task) => (
          <li key={task._id} className="task-item">
            {task.text}
          </li>
        ))}
      </ul>
    </div>
  );
}