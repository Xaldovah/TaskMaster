$(document).ready(function () {
    // Fetch and display tasks on page load
    fetchTasks();

    // Submit task form
    $('#taskForm').submit(function (event) {
        event.preventDefault();
        addTask();
    });

    function fetchTasks() {
        // Fetch tasks from the backend using AJAX
        $.ajax({
            url: '/api/tasks',
            method: 'GET',
            success: function (data) {
                displayTasks(data.tasks);
            },
            error: function (error) {
                console.error('Error fetching tasks:', error);
            }
        });
    }

    function displayTasks(tasks) {
        // Clear existing task list
        $('#taskList').empty();

        // Display each task
        tasks.forEach(function (task) {
            $('#taskList').append(`
                <div class="card mb-3">
                    <div class="card-body">
                        <h5 class="card-title">${task.title}</h5>
                        <p class="card-text">${task.description}</p>
                        <p class="card-text">Due Date: ${task.due_date}</p>
                        <p class="card-text">Priority: ${task.priority}</p>
                    </div>
                </div>
            `);
        });
    }

    function addTask() {
        // Get form data
        const title = $('#taskTitle').val();
        const description = $('#taskDescription').val();
        const dueDate = $('#dueDate').val();
        const priority = $('#priority').val();

        // Create task object
        const taskData = {
            title: title,
            description: description,
            due_date: dueDate,
            priority: priority
        };

        // Add task to the backend using AJAX
        $.ajax({
            url: '/api/tasks',
            method: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(taskData),
            success: function () {
                // Clear form fields
                $('#taskTitle').val('');
                $('#taskDescription').val('');
                $('#dueDate').val('');
                $('#priority').val('low');

                // Fetch and display updated tasks
                fetchTasks();
            },
            error: function (error) {
                console.error('Error adding task:', error);
            }
        });
    }
});
