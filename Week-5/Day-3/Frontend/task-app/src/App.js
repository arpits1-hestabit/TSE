// src/App.js
import React, { useState, useEffect } from "react";

function App() {
  const [tasks, setTasks] = useState([]);
  const [taskInput, setTaskInput] = useState("");

  const API_URL = "http://localhost:3000/tasks";

  // Fetch tasks from backend
  const fetchTasks = async () => {
    try {
      const response = await fetch(API_URL);
      const data = await response.json();
      setTasks(data);
    } catch (error) {
      console.error("Error fetching tasks:", error);
    }
  };

  // Add a new task
  const addTask = async () => {
    if (!taskInput) return;
    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ taskName: taskInput }),
      });

      if (response.ok) {
        setTaskInput(""); // Clear input
        fetchTasks();     // Reload tasks
      } else {
        console.error("Error adding task");
      }
    } catch (error) {
      console.error("Error adding task:", error);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>Task List</h1>

      <ul>
        {tasks.map((task) => (
          <li key={task._id}>{task.taskName}</li>
        ))}
      </ul>

      <input
        type="text"
        value={taskInput}
        placeholder="Add a new task"
        onChange={(e) => setTaskInput(e.target.value)}
      />
      <button onClick={addTask}>Add Task</button>
    </div>
  );
}

export default App;
