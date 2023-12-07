import axios from 'axios';

const api = axios.create({
  baseURL: '/',
  withCredentials: true // Ensure credentials (cookies) are sent with requests
});

// Include the Authorization header
const accessToken = localStorage.getItem('access_token');
if (accessToken) {
  api.defaults.headers.common.Authorization = `Bearer ${accessToken}`;
}

// login function
function login (username, password) {
  api.post('/login', { username, password })
    .then(response => {
      if (response.status === 200) {
        localStorage.setItem('access_token', response.data.access_token);
        window.location.href = '/tasks';
      } else {
        console.error('Login failed:', response.data.error);
      }
    })
    .catch(error => {
      console.error('Login failed:', error);
    });
}

function logout () {
  api.post('/logout')
    .then(response => {
      if (response.status === 200) {
        window.location.href = '/';
      } else {
        console.error('Logout failed:', response.data.error);
      }
    })
    .catch(error => {
      console.error('Logout failed:', error);
    });
}

function getTasks () {
  api.get('/tasks')
    .then(response => {
      const taskList = response.data.tasks;
      const taskListElement = document.getElementById('task-list');

      taskList.forEach(task => {
        const taskElement = document.createElement('div');
        taskElement.classList.add('task');

        const taskTitle = document.createElement('h3');
        taskTitle.textContent = task.title;

        const taskDescription = document.createElement('p');
        taskDescription.textContent = task.description;

        const taskDueDate = document.createElement('span');
        taskDueDate.textContent = task.dueDate ? 'Due Date: ' + task.dueDate : 'No Due Date';

        const taskPriority = document.createElement('span');
        taskPriority.textContent = 'Priority: ' + task.priority;

        const taskStatus = document.createElement('span');
        taskStatus.textContent = 'Status: ' + task.status;

        taskElement.appendChild(taskTitle);
        taskElement.appendChild(taskDescription);
        taskElement.appendChild(taskDueDate);
        taskElement.appendChild(taskPriority);
        taskElement.appendChild(taskStatus);
        taskListElement.appendChild(taskElement);
      });
      console.log('Retrieved tasks:', taskList);
    })
    .catch(error => {
      console.error('Error fetching tasks:', error);
    });
}

function createTask (title, description, dueDate, priority, updateUICallback) {
  api.post('/tasks', { title, description, dueDate, priority })
    .then(response => {
      if (response.status === 201) {
        console.log('Task created successfully:', response.data);

        if (typeof updateUICallback === 'function') {
          updateUICallback();
        }
      } else {
        console.error('Error creating task. Status code:', response.status);
      }
    })
    .catch(error => {
      console.error('Error creating task:', error);
    });
}

function updateTask (taskId, title, description, dueDate, priority, status, updateUICallback) {
  api.put(`/tasks/${taskId}`, { title, description, dueDate, priority, status })
    .then(response => {
      if (response.status === 200) {
        console.log('Task updated successfully:', response.data);

        if (typeof updateUICallback === 'function') {
          updateUICallback();
        }
      }
    })
    .catch(error => {
      console.error('Error updating task:', error);
    });
}

function deleteTask (taskId, updateUICallback) {
  api.delete(`/tasks/${taskId}`)
    .then(response => {
      if (response.status === 200) {
        console.log('Task deleted successfully');

        if (typeof updateUICallback === 'function') {
          updateUICallback();
        }
      } else {
        console.error('Error deleting task:', response.data.error);
      }
    })
    .catch(error => {
      console.error('Error deleting task:', error);
    });
}

function getUsers (updateUICallback) {
  api.get('/users')
    .then(response => {
      const users = response.data.users;
      const userListElement = document.getElementById('user-list');

      users.forEach(user => {
        const userElement = document.createElement('li');
        userElement.classList.add('user');

        const userName = document.createElement('span');
        userName.textContent = 'Username: ' + user.username;

        const userEmail = document.createElement('span');
        userEmail.textContent = 'Email: ' + user.email;

        userElement.appendChild(userName);
        userElement.appendChild(userEmail);

        userListElement.appendChild(userElement);
      });
      console.log('Retrieved users:', users);

      if (typeof updateUICallback === 'function') {
        updateUICallback();
      }
    })
    .catch(error => {
      console.error('Error fetching users:', error);
    });
}

function createUser (username, email, password, updateUICallback) {
  api.post('/register', { username, email, password })
    .then(response => {
      if (response.status === 201) {
        console.log('User created successfully');

        if (typeof updateUICallback === 'function') {
          updateUICallback();
        }
      } else {
        console.error('Error creating user:', response.data.error);
      }
    })
    .catch(error => {
      console.error('Error creating user:', error);
    });
}

function updateUser (userId, username, email, defaultTaskView, enableNotifications, themePreference, updateUICallback) {
  api.put(`/users/${userId}`, {
    username,
    email,
    defaultTaskView,
    enableNotifications,
    themePreference
  })
    .then(response => {
      if (response.status === 200) {
        console.log('User updated successfully:', response.data);

        if (typeof updateUICallback === 'function') {
          updateUICallback();
        }
      } else {
        console.error('Error updating user:', response.data.error);
      }
    })
    .catch(error => {
      console.error('Error updating user:', error);
    });
}

function deleteUser (userId, updateUICallback) {
  api.delete(`/users/${userId}`)
    .then(response => {
      if (response.status === 200) {
        console.log('User deleted successfully');

        if (typeof updateUICallback === 'function') {
          updateUICallback();
        }
      } else {
        console.error('Error deleting user:', response.data.error);
      }
    })
    .catch(error => {
      console.error('Error deleting user:', error);
    });
}

function createNotificationElement (notification) {
  const notificationElement = document.createElement('div');
  notificationElement.classList.add('notification');

  const notificationMessage = document.createElement('p');
  notificationMessage.textContent = notification.message;

  const notificationTimestamp = document.createElement('span');
  notificationTimestamp.textContent = 'Timestamp: ' + notification.created_at;

  notificationElement.appendChild(notificationMessage);
  notificationElement.appendChild(notificationTimestamp);

  return notificationElement;
}

function createNotification (message) {
  api.post('/notifications', { message })
    .then(response => {
      const notification = response.data.notification;

      const notificationElement = createNotificationElement(notification);
      document.getElementById('notification-list').appendChild(notificationElement);

      console.log('Notification created successfully:', response.data);
    })
    .catch(error => {
      console.error('Error creating notification:', error);
    });
}

function getNotifications () {
  api.get('/notifications')
    .then(response => {
      const notifications = response.data.notifications;
      const notificationListElement = document.getElementById('notification-list');

      notifications.forEach(notification => {
        const notificationElement = document.createElement('div');
        notificationElement.classList.add('notification');

        const notificationMessage = document.createElement('p');
        notificationMessage.textContent = notification.message;

        const notificationTimestamp = document.createElement('span');
        notificationTimestamp.textContent = 'Timestamp: ' + notification.created_at;

        notificationElement.appendChild(notificationMessage);
        notificationElement.appendChild(notificationTimestamp);

        notificationListElement.appendChild(notificationElement);
      });
      console.log('Retrieved notifications:', notifications);
    })
    .catch(error => {
      console.error('Error fetching notifications:', error);
    });
}

export {
  login,
  logout,
  getTasks,
  createTask,
  updateTask,
  deleteTask,
  getUsers,
  createUser,
  updateUser,
  deleteUser,
  createNotification,
  getNotifications
};
