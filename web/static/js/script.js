function logout() {
    localStorage.removeItem("email");
    window.location.href = "/login";
}

function createTask() {
    // Fetch values from the form
    const title = document.getElementById('title').value;
    const description = document.getElementById('description').value;
    const dueDate = document.getElementById('due_date').value;
    const priority = document.getElementById('priority').value;
    const status = document.getElementById('status').value;

    // Create a task object
    const newTask = {
	user: localStorage.getItem('email'),
        title: title,
        description: description,
        due_date: dueDate,
        priority: priority,
        status: status
    };

    // Retrieve existing tasks from localStorage
    const existingTasks = JSON.parse(localStorage.getItem('tasks')) || [];

    // Add the new task to the array
    existingTasks.push(newTask);

    // Save the updated tasks array to localStorage
    localStorage.setItem('tasks', JSON.stringify(existingTasks));

    // Refresh the task list
    fetchAndRenderTasks();
}

// Function to fetch tasks from localStorage and render them on the page
function fetchAndRenderTasks() {
    const tasksList = document.getElementById('tasksList');
    tasksList.innerHTML = ''; // Clear existing tasks

    // Retrieve tasks from localStorage
    const tasks = JSON.parse(localStorage.getItem('tasks')) || [];

    // Filter tasks based on the current user
    const currentUser = localStorage.getItem('email');
    const userTasks = tasks.filter(task => task.user === currentUser);

    // Render tasks on the page
    userTasks.forEach(task => {
        const taskItem = document.createElement('li');
        taskItem.innerHTML = `
            <span>Title:</span> ${task.title}<br>
            <span>Description:</span> ${task.description}<br>
            <span>Due Date:</span> ${task.due_date}<br>
            <span>Priority:</span> ${task.priority}<br>
            <span>Status:</span> ${task.status}<br>
            <hr>
        `;
        tasksList.appendChild(taskItem);
    });
}

// Call the function when the page loads
window.addEventListener('load', fetchAndRenderTasks);
