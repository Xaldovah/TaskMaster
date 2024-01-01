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

// Function to update a task
function updateTask(id) {
    // Implement the logic to update the task
    var updatedTitle = prompt("Enter updated title:");
    if (updatedTitle !== null) {
        // Get the task from localStorage
        var tasks = JSON.parse(localStorage.getItem("tasks")) || [];

        // Find the task with the given id
        var taskToUpdate = tasks.find(task => task.id === id);

        if (taskToUpdate) {
            // Update the task details
            taskToUpdate.title = updatedTitle;
            // Update other properties as needed

            // Save the updated tasks back to localStorage
            localStorage.setItem("tasks", JSON.stringify(tasks));

            // Reload the tasks on the page
            loadTasks();
        }
    }
}

// Function to delete a task
function deleteTask(id) {
    // Implement the logic to delete the task
    var confirmation = confirm("Are you sure you want to delete this task?");
    if (confirmation) {
        // Get the tasks from localStorage
        var tasks = JSON.parse(localStorage.getItem("tasks")) || [];

        // Filter out the task with the given id
        var filteredTasks = tasks.filter(task => task.id !== id);

        // Save the updated tasks back to localStorage
        localStorage.setItem("tasks", JSON.stringify(filteredTasks));

        // Reload the tasks on the page
        loadTasks();
    }
}

// Function to load tasks from localStorage and display them on the page
function loadTasks() {
    var tasksList = document.getElementById("tasksList");
    tasksList.innerHTML = ""; // Clear existing tasks

    // Get tasks from localStorage
    var tasks = JSON.parse(localStorage.getItem("tasks")) || [];

    // Display each task on the page
    tasks.forEach(function (task) {
        var li = document.createElement("li");
        li.textContent = task.title;

        // Add buttons for updating and deleting tasks
        var updateButton = document.createElement("button");
        updateButton.textContent = "Update";
        updateButton.onclick = function () {
            updateTask(task.id);
        };

        var deleteButton = document.createElement("button");
        deleteButton.textContent = "Delete";
        deleteButton.onclick = function () {
            deleteTask(task.id);
        };

        li.appendChild(updateButton);
        li.appendChild(deleteButton);

        tasksList.appendChild(li);
    });
}

// Call loadTasks when the page is loaded
window.onload = loadTasks;
