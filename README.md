# Project Title: Task Master
## Project Overview:
Task Master is a task management application with a Flask backend that provides API endpoints for user authentication, task management, notifications, and user preferences.

### Getting Started:
#### Prerequisites:
1. Python 3.7 or later
2. MySQL database
3. RabbitMQ server for Celery (optional, for background task processing)
#### Installation:
##### Clone the repository:
```git clone https://github.com/your-username/task-master.git```

####Install dependencies:

```
pip install -r requirements.txt
```
Set up your MySQL database and update the SQLALCHEMY_DATABASE_URI in app/__init__.py with your database connection details.

(Optional) Set up RabbitMQ for Celery and update the CELERY_BROKER_URL in app/__init__.py if using Celery.

##### Run migrations to create the database tables:

```
flask db init
flask db migrate
flask db upgrade
Start the Flask application:
```
```
flask run
```

#### Modules:
##### 1. Authentication Module:
###### API Endpoints:
1. POST /api/login: Log in with a username and password, returns an access token.
2. POST /api/logout: Log out the current user.
##### 2. Celery Module:
###### Function:
make_celery(app): Create a Celery instance for background task processing.
##### 3. Extensions Module:
###### Configurations:
Flask-RESTful, Flask-JWT-Extended, Flask-Login configurations.
##### 4. Initialization Module:
###### Configurations:
Flask, Flask-SocketIO, Flask-SQLAlchemy, Flask-Migrate, Flask-Bcrypt, Flask-JWT-Extended, Flask-Login.

##### 5. Models Module:
###### SQLAlchemy Models:
1. User: Represents application users.
2. Task: Represents tasks created by users.
3. Category: Represents task categories.
4. Notification: Represents notifications for users.
##### 6. Notifications Module:
###### Functions:
1. create_notification(user, message): Create a notification for a user with the specified message.
2. mark_notification_as_read(notification_id): Mark a notification as read.
##### 7. Notifications API Module:
###### API Endpoints:
1. GET /api/notifications: Retrieve notifications for the current user.
2. POST /api/notifications: Create a new notification for the current user.
##### 8. Preferences API Module:
###### API Endpoint:
1. GET /api/user/preferences: Retrieve user preferences for the current user.
##### 9. Tasks API Module:
###### API Endpoints:
1. GET /api/tasks: Retrieve tasks for the current user.
2. POST /api/tasks: Create a new task for the current user.
3. PUT /api/tasks/{task_id}: Update an existing task.
4. DELETE /api/tasks/{task_id}: Delete a task.
5. POST /api/tasks/{task_id}/disable-notifications: Disable notifications for a specific task.
##### 10. Users API Module:
###### API Endpoints:
1. GET /api/users: Retrieve a list of all users.
2. POST /api/register: Create a new user.
3. PUT /api/users/{user_id}: Update user preferences.
4. DELETE /api/users/{user_id}: Delete a user.

#### Usage:
##### Authentication:
1. Use the /api/login endpoint to obtain an access token by providing a JSON payload with a valid username and password.
2. Use the access token for authentication in other secured endpoints.

##### User Management:
1. Create a new user with the /api/register endpoint.
2. Retrieve, update, or delete user information using /api/users endpoints.
##### Task Management:
1. Retrieve, create, update, or delete tasks using the /api/tasks endpoints.
2. Disable notifications for a specific task with the /api/tasks/{task_id}/disable-notifications endpoint.
##### Notifications:
1. Retrieve or create notifications using the /api/notifications endpoints.
##### User Preferences:
1. Retrieve user preferences with the /api/user/preferences endpoint.
2. Update user preferences with the /api/users/{user_id} endpoint.
##### Background Task Processing:
The application uses Celery for background task processing.
Background tasks are triggered in the create_task endpoint to send notifications asynchronously.

### Frontend
The frontend for Task Master is currently under development. It will provide a user-friendly interface to interact with the task management application.

#### Technologies Used:
1. HTML
2. CSS
3. JavaScript

##### Development Setup
Navigate to the frontend directory.
###### Install frontend dependencies:
```
npm install
```
###### Start the frontend development server:
```
npm start
```

#### Future Enhancements:
1. Add more features for task management, such as task categorization and sorting.
2. Improve security measures and error handling.
3. Extend API documentation for easier integration.

### Contribution:
Feel free to contribute to this project by forking and submitting a pull request. Issues and feature requests are welcome on the GitHub repository.

### License:
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT) - see the LICENSE file for details.
