// Function to fetch tasks from the server
function fetchTasks() {
    // Retrieve the access token from the server
    $.ajax({
        url: '/login',
        type: 'GET',
        dataType: 'json',
        success: function(data) {
            // Use the retrieved access token for subsequent requests
	    let accessToken = localStorage.getItem('access_token');
            displayTasks(accessToken);
        },
        error: function(error) {
            console.error('Error retrieving access token:', error);
        }
    });
}

// Function to display tasks in the UI
function displayTasks(accessToken) {
    $.ajax({
        url: '/tasks',
        type: 'GET',
        dataType: 'json',
        headers: {
            'Authorization': 'Bearer ' + accessToken,
        },
        success: function(data) {
            var taskList = $('#task-list');
            taskList.empty(); // Clear existing tasks

            data.tasks.forEach(function(task) {
                var listItem = $('<li></li>');
                listItem.html(`
                    <span>Title:</span> ${task.title}<br>
                    <span>Description:</span> ${task.description}<br>
                    <span>Due Date:</span> ${task.due_date}<br>
                    <span>Priority:</span> ${task.priority}<br>
                    <span>Status:</span> ${task.status}<br>
                `);
                taskList.append(listItem);
            });
        },
        error: function(error) {
            console.error('Error fetching tasks:', error);
        }
    });
}

// Submit the form to create a new task
$('#create-task-form').submit(function(event) {
    event.preventDefault();

    var formData = {
        title: $('#title').val(),
        description: $('#description').val(),
        due_date: $('#due_date').val(),
        priority: $('#priority').val(),
        status: $('#status').val()
    };

    // Retrieve the access token from the server
    $.ajax({
        url: '/tasks',
        type: 'GET',
        dataType: 'json',
        success: function(data) {
            // Use the retrieved access token for the create task request
            let accessToken = localStorage.getItem('access_token');

            $.ajax({
                url: '/tasks',
                type: 'POST',
                dataType: 'json',
                headers: {
                    'Authorization': 'Bearer ' + accessToken,
                    'Content-Type': 'application/json'
                },
                data: JSON.stringify(formData),
                success: function(response) {
                    alert(response.message);
                    // Refresh the task list
                    fetchTasks();
                },
                error: function(error) {
                    console.error('Error creating task:', error);
                }
            });
        },
        error: function(error) {
            console.error('Error retrieving access token:', error);
        }
    });
});
