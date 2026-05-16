# 🚀 GitHub Dev Card Generator

An AI-powered GitHub Dev Card Generator built using FastAPI, Gemini AI, MCP Tools, and a modern frontend UI.

Generate beautiful developer profile cards from any public GitHub username with AI-powered profile analysis, skills extraction, and dynamic developer card generation.

---

# ✨ Features

* 🔍 Fetch public GitHub profile data
* 🤖 AI-powered developer analysis using Gemini
* 🎨 Dynamic developer card themes
* 📊 Top repositories and language insights
* ⚡ FastAPI backend
* 🌐 Responsive frontend UI
* 🧠 MCP Tool integration
* 🔗 Shareable developer cards

---

# 🛠️ Tech Stack

## Backend

* Python
* FastAPI
* MCP (FastMCP)
* Google Gemini AI
* HTTPX

## Frontend

* HTML
* CSS
* JavaScript

## APIs

* GitHub REST API
* Google Gemini API

---

# 📂 Project Structure

```bash
github-card-generator/
│
├── backend/
│   ├── main.py
│   ├── mcp_server.py
│   ├── agent.py
│   ├── requirements.txt
│   ├── .env
│   └── static/
│       └── cards/
│
├── frontend/
│   └── index.html
│
├── .gitignore
└── README.md
```

---

# ⚙️ Setup Instructions

## Clone Repository

```bash
git clone https://github.com/ompatil0/github-dev-card-generator.git
```

```bash
cd github-dev-card-generator
```

---

# 🔑 API Configuration

## Gemini API Key

Get your API key from:

https://aistudio.google.com/app/apikey

---

## Optional GitHub Token

Generate from:

https://github.com/settings/tokens

This improves GitHub API rate limits and reliability.

---

# 📝 Environment Variables

Create a `.env` file inside `backend/`

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
GITHUB_TOKEN=YOUR_GITHUB_TOKEN
```

---

# 📦 Backend Setup

## Navigate to backend

```bash
cd backend
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv .venv
```

---

## Activate Virtual Environment

### PowerShell

```bash
.\.venv\Scripts\activate
```

After activation terminal should look like:

```bash
(.venv)
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Install dotenv

```bash
pip install python-dotenv
```

---

# ▶️ Run Backend

```bash
uvicorn main:app --reload --port 8080
```

Backend runs at:

```text
http://127.0.0.1:8080
```

---

# 🌐 Frontend Setup

Open a new terminal.

## Navigate to frontend

```bash
cd frontend
```

---

## Start frontend server

```bash
python -m http.server 5500
```

Frontend runs at:

```text
http://127.0.0.1:5500
```

---

# 👨‍💻 Author

Om Patil

Built with ❤️ using FastAPI + Gemini AI

---

# ⭐ Support

If you like this project, consider giving it a ⭐ on GitHub and following for more AI & developer projects 🚀

Repository:
https://github.com/ompatil0/github-dev-card-generator
