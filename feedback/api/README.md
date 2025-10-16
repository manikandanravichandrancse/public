# 📝 Feedback API

A **FastAPI** backend service for collecting and managing user feedback, powered by **SQLite** and **Alembic** for database migrations.

---

## 🚀 Overview

This API allows users to submit, view, and delete feedback entries.  
It’s lightweight, database-backed, and ideal for integration with any frontend or mobile app.

---

## 🧩 Features

- Built with **FastAPI** (high-performance Python web framework)
- Uses **SQLite** (default local database)
- **Alembic** for schema migrations
- Supports **environment variables** via `.env`
- Auto-generated **interactive API docs** (Swagger & ReDoc)

---

## ⚙️ Prerequisites

Make sure you have:

- **Python 3.12+**
- **Poetry 2.1.3** *(recommended)* or **pip**
- **SQLite** (bundled with Python, no setup needed)

---

## 🏗️ Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone <repo-url>
cd feedback/api
```

### 2️⃣ Create & Activate Virtual Environment

**Using `venv`:**

```bash
python -m venv venv
# Activate (choose your OS)
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
```

---

### 3️⃣ Install Dependencies

**Option 1: Using Poetry (recommended)**

```bash
poetry install
poetry shell
```

**Option 2: Using pip**

```bash
pip install -r requirements.txt
```

---

## 🗃️ Database Setup & Migrations

### Initialize or upgrade database:
```bash
alembic upgrade head
```

### Generate a new migration after model changes:
```bash
alembic revision --autogenerate -m "your message"
alembic upgrade head
```

> 💡 Tip: If migrations fail, you can delete the local `feedback.db` and re-run `alembic upgrade head`.

---

## 🧠 Environment Configuration

Environment variables are loaded from a `.env` file.  
Example `.env` file:

```
DATABASE_URL=sqlite:///./feedback.db
```

Default settings:
- `DATABASE_URL`: `sqlite:///./feedback.db`

---

## 🏃 Running the Server

Start the FastAPI development server:

```bash
poetry run uvicorn feedback_app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Access API documentation:
- Swagger UI → [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc → [http://localhost:8000/redoc](http://localhost:8000/redoc)

## 🧰 Troubleshooting

| Problem | Possible Fix |
|----------|---------------|
| **Port conflict (8000)** | Use a different port: `--port 8080` |
| **Migration errors** | Delete DB and run `alembic upgrade head` |
| **Env not loading** | Ensure `.env` file is in the project root |

---

## 🪪 License

This project is licensed under the **MIT License**.  
See the [LICENSE](LICENSE) file for more details.

---

## 📅 Created

**October 15, 2025**

---

## 👨‍💻 Author

**Manikandan Selva**  
Full-Stack Developer — Python | FastAPI | React | Next.js
