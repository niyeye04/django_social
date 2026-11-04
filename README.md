# Social Media Backend API

A robust Django backend built for a social media platform, featuring custom user authentication, posts, comments, groups management, and media handling. Powered by modern Python tooling with `uv`, this was done as a more advance aproach of building backend APIs using Django

---

## 🚀 Tech Stack

* **Framework:** Django REST Framework
* **Package & Environment Management:** [`uv`]
* **Database:** SQLite (Development)
* **Image Processing:** Pillow

---

## 🛠️ Prerequisites

Make sure you have `uv` installed on your system. If you don't have it yet, you can install it by following instructions from thir official site 'https://docs.astral.sh/uv/getting-started/installation/'

## Setup and Running Instructions

### 1. Navigate to the Project Directory
Open your terminal and move to the project's backend root:
```bash
cd social/backend/main 
```

### 2. Synchronize Dependencies
Install and sync your environment dependencies using uv:
```bash
uv sync
```

### 3. Run Database Migrations
Apply your database migrations:
```bash
uv run python manage.py migrate
```

### 4. Start the Development Server
Launch the local Django server:
```bash
uv run python manage.py runserver
```
