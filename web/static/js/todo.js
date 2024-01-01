document.addEventListener("DOMContentLoaded", function() {
    // Sample data
    let tasks = [
        { id: 1, text: "Dashboard Design", status: "approved" },
        { id: 2, text: "Create a userflow", status: "progress" },
        // Add more tasks as needed
    ];

    const tasksWrapper = document.getElementById("tasks-wrapper");
    const upcomingTasksWrapper = document.getElementById("upcoming-tasks-wrapper");

    function renderTasks(container, tasks) {
        container.innerHTML = "";
        tasks.forEach(task => {
            const taskElement = createTaskElement(task);
            container.appendChild(taskElement);
        });
    }

    function createTaskElement(task) {
        const taskElement = document.createElement("div");
        taskElement.className = "task";
        taskElement.innerHTML = `
            <input type="checkbox" name="task" id="item-${task.id}" class="task-item" checked />
            <label for="item-${task.id}">
                <span class="label-text">${task.text}</span>
            </label>
            <span class="tag ${task.status}">${capitalizeFirstLetter(task.status)}</span>
        `;
        return taskElement;
    }

    function capitalizeFirstLetter(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }

    function addTask(text, status) {
        const newTask = {
            id: tasks.length + 1,
            text: text,
            status: status
        };
        tasks.push(newTask);
        renderTasks(tasksWrapper, tasks.filter(task => task.status !== "waiting"));
        renderTasks(upcomingTasksWrapper, tasks.filter(task => task.status === "waiting"));
    }

    function updateTask(id, text, status) {
        const index = tasks.findIndex(task => task.id === id);
        if (index !== -1) {
            tasks[index].text = text;
            tasks[index].status = status;
            renderTasks(tasksWrapper, tasks.filter(task => task.status !== "waiting"));
            renderTasks(upcomingTasksWrapper, tasks.filter(task => task.status === "waiting"));
        }
    }

    function deleteTask(id) {
        tasks = tasks.filter(task => task.id !== id);
        renderTasks(tasksWrapper, tasks.filter(task => task.status !== "waiting"));
        renderTasks(upcomingTasksWrapper, tasks.filter(task => task.status === "waiting"));
    }

    // Initial rendering
    renderTasks(tasksWrapper, tasks.filter(task => task.status !== "waiting"));
    renderTasks(upcomingTasksWrapper, tasks.filter(task => task.status === "waiting"));
});
