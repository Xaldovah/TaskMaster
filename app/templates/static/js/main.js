$(document).ready(function () {
  getTasksFromBackend();

  $('#taskForm').submit(function (event) {
    event.preventDefault();
    addTask();
  });

  function addTask () {
    const title = $('#taskTitle').val();
    const description = $('#taskDescription').val();
    const dueDate = $('#dueDate').val();
    const priority = $('#priority').val();

    const taskData = {
      title,
      description,
      due_date: dueDate,
      priority
    };
    addTaskToBackend(taskData);
  }

  function getTasksFromBackend () {
    $.ajax({
      url: '/tasks',
      method: 'GET',
      headers: {
        Authorization: 'Bearer ' + localStorage.getItem('access_token')
      },
      success: function (data) {
        displayTasks(data.tasks);
      },
      error: function (error) {
        console.error('Error fetching tasks:', error);
      }
    });
  }

  function displayTasks (tasks) {
	  $('#taskList').empty();

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

  function addTaskToBackend (taskData) {
    $.ajax({
      url: '/tasks',
      method: 'POST',
      contentType: 'application/json',
      data: JSON.stringify(taskData),
      headers: {
        Authorization: 'Bearer ' + localStorage.getItem('access_token')
      },
      success: function () {
        $('#taskTitle').val('');
        $('#taskDescription').val('');
        $('#dueDate').val('');
        $('#priority').val('low');

        getTasksFromBackend();
      },
      error: function (error) {
        console.error('Error adding task:', error);
      }
    });
  }
});
