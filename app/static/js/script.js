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

const editTaskForm = document.getElementById('edit-task-form');

editTaskForm.addEventListener('submit', async (event) => {
  event.preventDefault();

  const taskId = document.getElementById('task-id').value;
  const formData = new FormData(event.target);
  const data = {
    title: formData.get('title'),
    description: formData.get('description'),
    due_date: formData.get('due_date'),
    priority: formData.get('priority'),
    status: formData.get('status'),
  };

  try {
    const response = await fetch(`/tasks/${taskId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    const result = await response.json();

    if (result.task_id) {
      alert('Task updated successfully!');
      editTaskForm.reset();
      fetchTasks();
    } else {
      alert(result.error);
    }
  } catch (error) {
    console.error(error);
    alert('Internal server error. Please try again later.');
  }
});

const confirmDeleteButtons = document.querySelectorAll('[data-confirm]');

confirmDeleteButtons.forEach((button) => {
  button.addEventListener('click', (event) => {
    event.preventDefault();

    if (confirm(button.dataset.confirm)) {
      const taskId = button.dataset.taskId;

      fetch(`/tasks/${taskId}`, {
        method: 'DELETE',
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.message === 'Task deleted successfully') {
            alert('Task deleted successfully!');
            fetchTasks();
          } else {
            alert(data.error);
          }
        })
        .catch((error) => {
          console.error(error);
          alert('Internal server error. Please try again later.');
        });
    }
  });
});
