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
            'Authorization': `Bearer ${getAuthToken()}`, // Add this line for authentication
        },
        body: JSON.stringify(taskData),
    })
        .then(response => response.json())
        .then(data => {
            // Update the UI with the new task
            console.log(data);
            // Check if notifications are enabled before emitting a new task event
            if (getUserNotificationPreference()) {
                socket.emit('new_task', { message: `New task created: ${data.title}` });
            }
        })
        .catch(error => console.error('Error:', error));
}

// Function to update an existing task
function updateTask(taskId, updatedData) {
    fetch(`${tasksEndpoint}/${taskId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${getAuthToken()}`,
        },
        body: JSON.stringify(updatedData),
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
        })
        .catch(error => console.error('Error:', error));
}

async function getUserPreferences() {
    try {
        const response = await fetch(`${apiUrl}/user/preferences`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${getAuthToken()}`,
            },
        });

        if (!response.ok) {
            throw new Error('Failed to retrieve user preferences');
        }

        const data = await response.json();
        const preferences = {
            defaultTaskView: data.default_task_view,
            enableNotifications: data.enable_notifications,
            themePreference: data.theme_preference,
        };

        return preferences;
    } catch (error) {
        console.error('Error retrieving user preferences:', error);
        return null;
    }
}

// Function to get user authentication token
function getAuthToken() {
    return localStorage.getItem('authToken');
}

// Function to check if notifications are enabled for the user
function getUserNotificationPreference() {
    const userPreferences = getUserPreferences();
    // Check if the 'enableNotifications' field is true in user preferences
    return userPreferences && userPreferences.enableNotifications === true;
}

document.addEventListener('DOMContentLoaded', getTasks);
