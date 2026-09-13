# Productivity App - Flask Auth Backend

A secure Flask REST API backend for a productivity app. Implements JWT-based authentication and full CRUD for a user-owned Task resource, with pagination and per-user access control.

## Features

- User signup and login with JWT authentication
- Passwords hashed with bcrypt
- Full CRUD for Tasks (create, read, update, delete)
- Pagination on the tasks index route
- Users can only view or modify their own tasks

## Installation

1. Clone this repository
2. Install dependencies: pipenv install
3. Activate the virtual environment: pipenv shell
4. Set the Flask app environment variable: export FLASK_APP=app.py
5. Run database migrations: flask db upgrade
6. (Optional) Seed the database with example data: python seed.py

## Running the App

python app.py

The API will run on http://127.0.0.1:5555.

## Endpoints

### Auth

POST /signup - Create a new user account. Body: username, password. Returns user and access_token.

POST /login - Log in an existing user. Body: username, password. Returns user and access_token.

GET /me - Returns the currently authenticated user. Requires Authorization: Bearer token header.

### Tasks (all require Authorization: Bearer token header)

GET /tasks?page=1&per_page=10 - Returns a paginated list of the logged-in user's tasks.

GET /tasks/:id - Returns a single task, if it belongs to the logged-in user.

POST /tasks - Creates a new task for the logged-in user. Body: title, description, completed.

PATCH /tasks/:id - Updates a task, if it belongs to the logged-in user.

DELETE /tasks/:id - Deletes a task, if it belongs to the logged-in user.

## Tech Stack

Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-Bcrypt, Flask-JWT-Extended, Flask-CORS, SQLite
