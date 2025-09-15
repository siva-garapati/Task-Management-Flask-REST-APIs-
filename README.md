# Task-Management-Flask-REST-APIs-
A simple Task Management CRUD application built with Flask REST APIs and React frontend. Features JWT authentication, UUID-based task and user IDs, and basic task management (create, read, update, delete). Designed for learning and full-stack practice.

# Task Management App (Flask + React)

A simple Task Management CRUD application using **Flask REST APIs** for the backend and **React** for the frontend.

---

## Features

- User registration and login with **JWT authentication**
- UUID-based **user and task IDs**
- Task CRUD operations:
  - Create a new task
  - Read all tasks or a single task
  - Update task details
  - Delete a task
- Minimal validation and error handling
- Task fields: `title`, `content`, `status`, `created_at`, `deadline`
- JWT tokens that do not expire until the user logs out (handled on frontend)

---

## Tech Stack

- **Backend:** Python, Flask, SQLAlchemy, SQLite
- **Frontend:** React.js
- **Authentication:** JWT
- **Styling:** Minimal CSS / frontend styles
- **Database:** SQLite (can be switched to PostgreSQL/MySQL)

---

task-m-rest/
│
├── app/
│ ├── init.py
│ ├── models.py
│ ├── routes/
│ │ ├── auth.py
│ │ └── tasks.py
│ ├── extensions.py
│ ├── config.py
│ └── templates/
│ └── home.html <-- API Documentation
│
├── run.py
├── requirements.txt
└── README.md


---

## API Endpoints

### **Authentication**

- **Register:** `POST /api/auth/register`
- **Login:** `POST /api/auth/login`

### **Tasks (JWT protected)**

- **Create Task:** `POST /api/tasks/addtask`
- **Get All Tasks:** `GET /api/tasks/tasks`
- **Get Single Task:** `GET /api/tasks/tasks/<task_id>`
- **Update Task:** `PUT /api/tasks/tasks/<task_id>`
- **Delete Task:** `DELETE /api/tasks/tasks/<task_id>`

**Notes:**
- Include JWT in headers: `Authorization: Bearer <token>`
- Deadline format: `YYYY-MM-DD`
- Status values: `"Pending"` or `"Completed"`

---

## Project Structure

