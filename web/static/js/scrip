// Logout function
function logout() {
    // Clear user data from memory
    localStorage.removeItem('access_token');
    localStorage.removeItem('email');
    // Redirect to the logout endpoint
    window.location.href = '/logout';
}

// Function to create a new task
function createTask() {
    // Get task details from the form
    const title = document.getElementById('title').value;
    const description = document.getElementById('description').value;
    const dueDate = document.getElementById('due_date').value;
    const priority = document.getElementById('priority').value;
    const status = document.getElementById('status').value;

    // Prepare data to send to the backend
    const taskData = {
        title: title,
        description: description,
        due_date: dueDate,
        priority: priority,
        status: status,
    };

    // Send a POST request to create a new task
    fetch('/tasks', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + getAccessToken(),
        },
        body: JSON.stringify(taskData),
    })
    .then(response => response.json())
    .then(data => {
        // Handle the response from the backend
        console.log('New task created:', data);
        // Update the UI
    })
    .catch(error => {
        console.error('Error creating task:', error);
    });
}

// Function to get tasks for the current user
function getTasks() {
    // Send a GET request to retrieve tasks
    fetch('/tasks', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + getAccessToken(),
        },
    })
    .then(response => response.json())
    .then(data => {
        // Handle the response from the backend
        console.log('Tasks retrieved:', data);
        displayTasks(data); // Display tasks on the page
    })
    .catch(error => {
        console.error('Error retrieving tasks:', error);
    });
}

// Function to get the access token from the response data
function getAccessToken() {
    // Retrieve the access token from the response data
    const responseJson = JSON.parse(localStorage.getItem('response_data'));
    return responseJson.access_token;
}

// Storing the response data in localStorage during login
function handleLoginResponse(responseData) {
    // Store the response data in localStorage
    localStorage.setItem('response_data', JSON.stringify(responseData));
}

// function to display tasks on the page
function displayTasks(tasks) {
    const tasksList = document.getElementById('tasksList');
    tasksList.innerHTML = ''; // Clear existing tasks

    tasks.forEach(task => {
        const listItem = document.createElement('li');
        listItem.textContent = task.title;
        tasksList.appendChild(listItem);
    });
}

// Load tasks when the page is loaded
window.onload = function() {
    getTasks();
};
