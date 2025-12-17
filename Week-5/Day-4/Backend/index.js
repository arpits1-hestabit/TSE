const express = require('express');
const bodyParser = require('body-parser');
const mongoose = require('mongoose');
const cors = require('cors');

// Connect to MongoDB
mongoose.connect('mongodb://mongo:27017/taskdb', { useNewUrlParser: true, useUnifiedTopology: true })
    .then(() => {
        console.log('Connected to MongoDB successfully');
    })
    .catch((error) => {
        console.error('Error connecting to MongoDB:', error);
    });

const app = express();
app.use(bodyParser.json());
app.use(cors(
    {
        origin: 'https://week5.day4',
        credentials: true
    }
));

// Define Task Schema and Model
const taskSchema = new mongoose.Schema({
    taskName: String,
    completed: Boolean
});

const Task = mongoose.model('Task', taskSchema);

// Routes

// GET /tasks - Retrieve all tasks
app.get('/api/tasks', async (req, res) => {
    try {
        const tasks = await Task.find();
        console.log(`Fetched ${tasks.length} tasks from the database.`);
        res.json(tasks);
    } catch (error) {
        console.error('Error fetching tasks:', error);
        res.status(500).json({ error: 'Error fetching tasks' });
    }
});

// POST /tasks - Create a new task
app.post('/api/tasks', async (req, res) => {
    const { taskName } = req.body;
    console.log(`Attempting to insert task: ${taskName}`);

    const newTask = new Task({
        taskName,
        completed: false
    });

    try {
        const savedTask = await newTask.save();
        console.log(`Task inserted successfully: ${savedTask}`);
        res.status(201).json(savedTask);
    } catch (error) {
        console.error('Error inserting task:', error);
        res.status(500).json({ error: 'Error inserting task' });
    }
});

app.get('/health', (req, res) => {
    res.status(200).send('OK');
});
const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});