# Larvi AI Agent

Larvi is an AI-powered personal assistant that connects with Google services to help users manage Gmail and Google Calendar through natural-language commands.

## Features

### Google Authentication

* Google OAuth 2.0 authentication
* Secure Google account connection
* OAuth token management

### Gmail Integration

Larvi can:

* Show recent emails
* Search emails
* Read individual emails
* Summarize emails
* Create email drafts
* Send emails
* Reply to emails

### Google Calendar Integration

Larvi can:

* Show upcoming calendar events
* Create meetings and events
* Reschedule events
* Delete or cancel events

### AI Agent Architecture

Larvi uses an agent-based architecture to understand user requests and route them to the appropriate tools.

The master agent determines whether a request is related to Gmail, Google Calendar, or another supported assistant task.

## Tech Stack

* Python
* FastAPI
* LangChain
* LangGraph
* Google OAuth 2.0
* Gmail API
* Google Calendar API
* HTML
* CSS
* JavaScript

## Project Structure

```text
Larvi/
|
|-- app/
|   |-- agents/
|   |   |-- calendar_agent.py
|   |   |-- email_agent.py
|   |   `-- master_agent.py
|   |
|   |-- auth/
|   |   `-- google_auth.py
|   |
|   |-- state/
|   |   `-- conversation_state.py
|   |
|   |-- tools/
|   |   |-- calendar_tool.py
|   |   |-- calendar_tools.py
|   |   |-- email_tools.py
|   |   `-- gmail_tool.py
|   |
|   |-- config.py
|   `-- main.py
|
|-- frontend/
|   |-- index.html
|   |-- script.js
|   `-- style.css
|
|-- .env.example
|-- .gitignore
|-- requirements.txt
`-- README.md
```

## Installation

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

Activate the virtual environment:

```powershell
venv\Scripts\activate
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

## Google OAuth Setup

Larvi requires Google OAuth credentials to access Gmail and Google Calendar.

Create a Google Cloud project and enable:

* Gmail API
* Google Calendar API

Configure an OAuth client and download the Google client credentials.

Create a `.env` file based on `.env.example` and add the required configuration.

Never upload `.env`, Google OAuth tokens, or Google client secrets to GitHub.

## Run the Application

Start the FastAPI server:

```powershell
uvicorn app.main:app --reload
```

The backend will normally be available at:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

## Example Commands

### Gmail

```text
Show my recent emails
```

```text
Find emails from LinkedIn
```

```text
Read email 1a02993a567be211
```

```text
Summarize email 1a02993a567be211
```

```text
Create a draft email to example@gmail.com
```

```text
Send an email to example@gmail.com
```

```text
Reply to email 1a02993a567be211
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

## Tested Functionality

### Gmail

* Google authentication
* Account connection
* Recent emails
* Email search
* Read email
* Email summarization
* Create email draft
* Send email
* Reply to email

### Google Calendar

* Show calendar
* Create event
* Reschedule event
* Delete event

## Security

Sensitive credentials are intentionally excluded from the repository.

The following files should never be committed:

```text
.env
google_token.json
Google OAuth client secrets
venv/
__pycache__/
```

## Project Status

Larvi's core Gmail and Google Calendar integrations have been implemented and tested successfully.

The project is currently suitable for local demonstration and further development.

## Author

**Syeda Tehreem Fatima**

GitHub:

https://github.com/tehreem1214

## License

This project is intended for educational and demonstration purposes.
