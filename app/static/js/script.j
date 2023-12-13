const fetchTasks = async () => {
  try {
    const response = await fetch('/');
    const data = await response.json();
    if (data.tasks) {
      const taskListElement = document.getElementById('task-list');
      taskListElement.innerHTML = '';

      data.tasks.forEach((task) => {
        const taskItem = document.createElement('tr');
        taskItem.innerHTML = `
          <td>${task.title}</td>
          <td>${task.description || ''}</td>
          <td>${task.due_date || ''}</td>
          <td>${task.priority || ''}</td>
          <td>${task.status}</td>
          <td>${task.created_at}</td>
          <td>${task.updated_at}</td>
          <td>
            <a href="/tasks/${task.id}/edit" class="btn btn-primary">Edit</a>
            <a href="/tasks/${task.id}" class="btn btn-danger" data-confirm="Are you sure you want to delete this task?">Delete</a>
          </td>
        `;
        taskListElement.appendChild(taskItem);
      });
    }
  } catch (error) {
	  console.error(error);
	  alert('Internal server error. Please try again later.');
  }
};

fetchTasks();
