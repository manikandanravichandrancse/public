# ⚛️ Feedback

A modern **React** frontend built with **Vite**, providing a user interface to submit and view feedback from the FastAPI backend.

---

## 🚀 Overview

This frontend application connects with the FastAPI backend to display and manage user feedback.  
It uses **Axios** for API requests, **React Router** for navigation, and **MUI** for the UI components.

---

## 🧩 Prerequisites

Make sure you have installed:

- **Node.js v22.14.0**
- **Yarn 1.22.22** (recommended package manager)

---

## 🏗️ Setup Instructions

### 1️⃣ Clone Repository

```bash
git clone <repo-url>
cd feedback/frontend
```

### 2️⃣ Install Dependencies

```bash
yarn install
```

---

## 🧠 Running Development Server

Start the Vite dev server on port **3000**:

```bash
yarn dev
```

Open your browser at:

👉 [http://localhost:3000](http://localhost:3000)

The frontend communicates with the backend API at:

```
http://localhost:8000/api/latest
```

> ⚠️ No Vite proxy is configured — the frontend uses full backend URLs via Axios.

## 🧹 Linting & Formatting

Run **ESLint** and **Prettier** to maintain code style and quality:

```bash
yarn lint
```

---

## 🏗️ Building for Production

Generate the optimized static build:

```bash
yarn build
```

The production-ready files are output to the `dist/` directory.

You can serve them via:

- Any static file server, or  
- FastAPI static files integration

---

## 🧰 Troubleshooting

| Issue | Possible Fix |
|--------|---------------|
| Backend not reachable | Ensure FastAPI runs on `http://localhost:8000` |
| Wrong Axios URL | Check `src/api.js` baseURL configuration |
| Port conflict | Use another port: `yarn dev -- --port 3001` |
| Styling errors | Reinstall MUI: `yarn add @mui/material @emotion/react @emotion/styled` |

---

## 🪪 License

This project is licensed under the **MIT License**.

---

## 📅 Created

**October 15, 2025**

---

## 👨‍💻 Author

**Manikandan Selva**  
Full-Stack Developer — React | Next.js | FastAPI | Python
