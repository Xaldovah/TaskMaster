const apiUrl = 'http://127.0.0.1:5000/api';
const tasksEndpoint = `${apiUrl}/tasks`;

// Function to retrieve tasks from the backend
function getTasks() {
    fetch(tasksEndpoint)
        .then(response => response.json())
        .then(data => {
            // Update the UI with the retrieved tasks
            console.log(data);
        })
        .catch(error => console.error('Error:', error));
}

// Function to create a new task
function createTask(taskData) {
    fetch(tasksEndpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(taskData),
    })
        .then(response => response.json())
        .then(data => {
            // Update the UI with the new task
            console.log(data);
        })
        .catch(error => console.error('Error:', error));
}

// Function to update an existing task
function updateTask(taskId, updatedData) {
    fetch(`${tasksEndpoint}/${taskId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(updatedData),
    })
        .then(response => response.json())
        .then(data => {
            // Update the UI with the updated task
            console.log(data);
        })
        .catch(error => console.error('Error:', error));
}

document.addEventListener('DOMContentLoaded', getTasks);
