# Larvi AI Agent 🤖

**Larvi** is an AI-powered personal assistant that allows users to manage **Gmail and Google Calendar** using natural-language commands.

Instead of manually navigating through Gmail or Google Calendar, users can communicate with Larvi through simple commands such as:

> "Find emails from LinkedIn"

> "Create a meeting tomorrow at 11 AM called Larvi Test Meeting"

Larvi understands the request, routes it to the appropriate agent, and performs the required action through Google's APIs.

---

## ✨ Features

### 🔐 Google Authentication

* Google OAuth 2.0 authentication
* Secure Google account connection
* Gmail API access
* Google Calendar API access
* OAuth token management

### 📧 Gmail Agent

Larvi supports:

* View recent emails
* Search emails
* Read individual emails
* Summarize emails
* Create email drafts
* Send emails
* Reply to emails

### 📅 Calendar Agent

Larvi supports:

* View upcoming calendar events
* Create meetings/events
* Reschedule events
* Delete/cancel events

### 🧠 Master Agent

The Master Agent acts as the main controller.

It analyzes the user's natural-language request and routes it to the appropriate agent/tool.

```text
User Request
     │
     ▼
Master Agent
     │
     ├───────────────┐
     ▼               ▼
Gmail Agent     Calendar Agent
     │               │
     ▼               ▼
 Gmail API      Calendar API
```

---

## 🛠️ Tech Stack

| Technology          | Purpose              |
| ------------------- | -------------------- |
| Python              | Backend development  |
| FastAPI             | REST API             |
| LangChain           | LLM/agent framework  |
| LangGraph           | Agent workflow       |
| Google OAuth 2.0    | Authentication       |
| Gmail API           | Email operations     |
| Google Calendar API | Calendar operations  |
| HTML                | Frontend             |
| CSS                 | Frontend styling     |
| JavaScript          | Frontend interaction |

---

## 📁 Project Structure

```text
Larvi/
│
├── app/
│   ├── agents/
│   │   ├── calendar_agent.py
│   │   ├── email_agent.py
│   │   └── master_agent.py
│   │
│   ├── auth/
│   │   └── google_auth.py
│   │
│   ├── state/
│   │   └── conversation_state.py
│   │
│   ├── tools/
│   │   ├── calendar_tool.py
│   │   ├── calendar_tools.py
│   │   ├── email_tools.py
│   │   └── gmail_tool.py
│   │
│   ├── config.py
│   └── main.py
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/tehreem1214/Larvi-AI-Agent.git
cd Larvi-AI-Agent
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

---

## 🔑 Google OAuth Setup

Larvi requires Google OAuth credentials to access Gmail and Google Calendar.

### 1. Create a Google Cloud Project

Create a project in Google Cloud Console.

### 2. Enable APIs

Enable:

* Gmail API
* Google Calendar API

### 3. Configure OAuth

Create an OAuth 2.0 Client ID and configure the required consent screen.

Download the Google OAuth client credentials required by the application.

### 4. Environment Variables

Create a `.env` file using `.env.example` as a reference.

```text
.env
```

Add the required Google OAuth and application configuration.

> ⚠️ **Never commit `.env`, Google OAuth client secrets, or OAuth tokens to GitHub.**

---

## ▶️ Run the Application

Start the FastAPI backend:

```powershell
uvicorn app.main:app --reload
```

The application will normally be available at:

```text
http://127.0.0.1:8000
```

FastAPI Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 💬 Example Commands

### Gmail

```text
Show my recent emails
```

```text
Find emails from LinkedIn
```

```text
Read email 1a0298705bdc827f
```

```text
Summarize email 1a0298705bdc827f
```

```text
Create a draft email to example@gmail.com subject Test Subject body Hello
```

```text
Send an email to example@gmail.com subject Test Email body Hello from Larvi
```

```text
Reply to email MESSAGE_ID with body Thank you for your email.
```

### Google Calendar

```text
Show my calendar
```

```text
Create a meeting tomorrow at 11 AM called Larvi Test Meeting
```

```text
Reschedule Larvi Test Meeting to August 23 at 2 PM
```

```text
Delete the meeting Larvi Test Meeting
```

---

## 🧪 Tested Functionality

Larvi's core integrations have been tested successfully using real Gmail and Google Calendar operations.

### Gmail

* ✅ Google authentication
* ✅ Account connection
* ✅ Recent emails
* ✅ Email search
* ✅ Read email
* ✅ Email summarization
* ✅ Create email draft
* ✅ Send email
* ✅ Reply to email

### Google Calendar

* ✅ Show calendar
* ✅ Create event
* ✅ Reschedule event
* ✅ Delete event

---

## 🔄 Example Agent Flow

For example, when the user enters:

```text
Find emails from LinkedIn
```

The request follows this flow:

```text
User
 │
 ▼
FastAPI
 │
 ▼
Master Agent
 │
 ▼
Email Agent
 │
 ▼
Gmail Tool
 │
 ▼
Gmail API
 │
 ▼
Email Results
 │
 ▼
User
```

For a calendar request:

```text
User
 │
 ▼
FastAPI
 │
 ▼
Master Agent
 │
 ▼
Calendar Agent
 │
 ▼
Calendar Tool
 │
 ▼
Google Calendar API
 │
 ▼
Calendar Result
 │
 ▼
User
```

---

## 🔒 Security

Sensitive credentials are intentionally excluded from this repository.

The following files/data should **never** be committed:

```text
.env
google_token.json
Google OAuth client secrets
venv/
__pycache__/
```

The `.gitignore` file is configured to help prevent accidental commits of sensitive/local files.

---

## 📌 Project Status

### Core functionality: COMPLETE ✅

Larvi currently provides working Gmail and Google Calendar integrations through a natural-language AI agent architecture.

The project is currently suitable for:

* Local demonstration
* Academic project presentation
* AI agent demonstrations
* Further development
* Future deployment/customization

---

## 🔮 Future Improvements

Possible future improvements include:

* Voice-based interaction
* Better conversational memory
* More Google Workspace integrations
* Google Drive integration
* Google Docs integration
* Smarter multi-step agent workflows
* Production deployment
* Improved frontend UI
* User-specific permissions and session management

---

## 👩‍💻 Author

**Syeda Tehreem Fatima**

GitHub:
https://github.com/tehreem1214

Project Repository:
https://github.com/tehreem1214/Larvi-AI-Agent

---

## 📄 License

This project is intended for educational and demonstration purposes.
