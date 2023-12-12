(function () {
  const accessToken = localStorage.getItem('access_token');

  if (accessToken) {
    $.ajaxSetup({
      headers: {
        Authorization: `Bearer ${accessToken}`
      }
    });
  }

  function login(username, password) {
    $.post(`/login`, { username, password })
      .done(response => {
        if (response.status === 200) {
          localStorage.setItem('access_token', response.data.access_token);
          window.location.href = '/dashboard';
        } else {
          console.error('Login failed:', response.data.error);
        }
      })
      .fail(error => {
        console.error('Login failed:', error);
      });
  }

  function logout() {
    $.post(`/logout`)
      .done(response => {
        if (response.status === 200) {
          window.location.href = '/';
        } else {
          console.error('Logout failed:', response.data.error);
        }
      })
      .fail(error => {
        console.error('Logout failed:', error);
      });
  }

  $(document).ready(function () {
    getTasks();
  });

  function getTasks() {
    const authToken = accessToken;

    $.ajax({
      url: `/tasks`,
      type: 'GET',
      headers: {
        'Authorization': `Bearer ${authToken}`
      },
      success: response => {
        const taskList = response.data.tasks;
        const taskListElement = $('#task-list');

        taskList.forEach(task => {
          const taskElement = $('<div class="task"></div>');

          const taskTitle = $('<h3></h3>').text(task.title);
          const taskDescription = $('<p></p>').text(task.description);
          const taskDueDate = $('<span></span>').text(task.dueDate ? 'Due Date: ' + task.dueDate : 'No Due Date');
          const taskPriority = $('<span></span>').text('Priority: ' + task.priority);
          const taskStatus = $('<span></span>').text('Status: ' + task.status);

          taskElement.append(taskTitle, taskDescription, taskDueDate, taskPriority, taskStatus);
          taskListElement.append(taskElement);
        });

        console.log('Retrieved tasks:', taskList);
      },
      error: (xhr, textStatus, errorThrown) => {
        console.error('Error fetching tasks:', errorThrown);
        console.log('XHR status:', xhr.status);
        console.log('Text status:', textStatus);
      }
    });
  }

  function createTask(title, description, dueDate, priority, updateUICallback) {
    $.post(`/tasks`, { title, description, dueDate, priority })
      .done(response => {
        if (response.status === 201) {
          console.log('Task created successfully:', response.data);

          if (typeof updateUICallback === 'function') {
            updateUICallback();
          }
        } else {
          console.error('Error creating task. Status code:', response.status);
        }
      })
      .fail(error => {
        console.error('Error creating task:', error);
      });
  }

  function updateTask(taskId, title, description, dueDate, priority, status, updateUICallback) {
    $.ajax({
      url: `/tasks/${taskId}`,
      method: 'PUT',
      data: { title, description, dueDate, priority, status }
    })
      .done(response => {
        if (response.status === 200) {
          console.log('Task updated successfully:', response.data);

          if (typeof updateUICallback === 'function') {
            updateUICallback();
          }
        }
      })
      .fail(error => {
        console.error('Error updating task:', error);
      });
  }

  function deleteTask(taskId, updateUICallback) {
    $.ajax({
      url: `/tasks/${taskId}`,
      method: 'DELETE'
    })
      .done(response => {
        if (response.status === 200) {
          console.log('Task deleted successfully');

          if (typeof updateUICallback === 'function') {
            updateUICallback();
          }
        } else {
          console.error('Error deleting task:', response.data.error);
        }
      })
      .fail(error => {
        console.error('Error deleting task:', error);
      });
  }

  function getUsers(updateUICallback) {
    $.get(`/users`)
      .done(response => {
        const users = response.data.users;
        const userListElement = $('#user-list');

        users.forEach(user => {
          const userElement = $('<li class="user"></li>');
          const userName = $('<span></span>').text('Username: ' + user.username);
          const userEmail = $('<span></span>').text('Email: ' + user.email);

          userElement.append(userName, userEmail);
          userListElement.append(userElement);
        });
        console.log('Retrieved users:', users);

        if (typeof updateUICallback === 'function') {
          updateUICallback();
        }
      })
      .fail(error => {
        console.error('Error fetching users:', error);
      });
  }

  function createUser(username, email, password, updateUICallback) {
    $.post(`/register`, { username, email, password })
      .done(response => {
        if (response.status === 201) {
          console.log('User created successfully');

          if (typeof updateUICallback === 'function') {
            updateUICallback();
          }
        } else {
          console.error('Error creating user:', response.data.error);
        }
      })
      .fail(error => {
        console.error('Error creating user:', error);
      });
  }

  function updateUser(userId, username, email, updateUICallback) {
    $.ajax({
      url: `/users/${userId}`,
      method: 'PUT',
      data: {
        username,
        email,
      }
    })
      .done(response => {
        if (response.status === 200) {
          console.log('User updated successfully:', response.data);

          if (typeof updateUICallback === 'function') {
            updateUICallback();
          }
        } else {
          console.error('Error updating user:', response.data.error);
        }
      })
      .fail(error => {
        console.error('Error updating user:', error);
      });
  }

  function deleteUser(userId, updateUICallback) {
    $.ajax({
      url: `/users/${userId}`,
      method: 'DELETE'
    })
      .done(response => {
        if (response.status === 200) {
          console.log('User deleted successfully');

          if (typeof updateUICallback === 'function') {
            updateUICallback();
          }
        } else {
          console.error('Error deleting user:', response.data.error);
        }
      })
      .fail(error => {
        console.error('Error deleting user:', error);
      });
  }

  function createNotificationElement(notification) {
    const notificationElement = $('<div class="notification"></div>');
    const notificationMessage = $('<p></p>').text(notification.message);
    const notificationTimestamp = $('<span></span>').text('Timestamp: ' + notification.created_at);

    notificationElement.append(notificationMessage, notificationTimestamp);

    return notificationElement;
  }

  function createNotification(message) {
    $.post(`/notifications`, { message })
      .done(response => {
        const notification = response.data.notification;
        const notificationElement = createNotificationElement(notification);

        $('#notification-list').append(notificationElement);
        console.log('Notification created successfully:', response.data);
      })
      .fail(error => {
        console.error('Error creating notification:', error);
      });
  }

  function getNotifications() {
    $.get(`/notifications`)
      .done(response => {
        const notifications = response.data.notifications;
        const notificationListElement = $('#notification-list');

        notifications.forEach(notification => {
          const notificationElement = createNotificationElement(notification);
          notificationListElement.append(notificationElement);
        });
        console.log('Retrieved notifications:', notifications);
      })
      .fail(error => {
        console.error('Error fetching notifications:', error);
      });
  }

})();
