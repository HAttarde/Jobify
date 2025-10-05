# AI Job Application Agent

An automated job application assistant that generates tailored resumes, cover letters, and personalized outreach messages using AI and real contact data.

## Features

- **Resume Tailoring**: Automatically customizes your resume for specific job descriptions
- **Cover Letter Generation**: Creates compelling, personalized cover letters
- **Contact Discovery**: Finds real employee contacts at target companies via Hunter.io
- **Personalized Outreach**: Generates custom LinkedIn connection notes and cold emails
- **Dual AI Agents**: Specialized agents for resume optimization and networking outreach

## Tech Stack

**Frontend**: React, TailwindCSS  
**Backend**: Python, Flask, CrewAI  
**AI Models**: Google Gemini 2.5 Flash  
**APIs**: Hunter.io (contact discovery)  
**Deployment**: Docker, Docker Compose

## Prerequisites

- Docker and Docker Compose
- Hunter.io API key ([Get one free](https://hunter.io/api-keys))
- Google Gemini API key ([Get from Google AI Studio](https://aistudio.google.com/app/apikey))

## Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd ai-job-agent
```
2. **Create .env file in the root directory**
```bash
HUNTER_API_KEY=your_hunter_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

3. **Start the application**
```bash
docker-compose up --build
```

4. **Access the application**
```bash
Frontend: http://localhost:3000
Backend API: http://localhost:5001
```

## Project Structure
```
.
├── frontend/                # React application
│   ├── src/
│   │   ├── App.jsx         # Main UI component
│   │   └── index.js
│   └── package.json
├── backend/                 # Flask API
│   ├── agents/
│   │   ├── resume_agent.py     # Resume & cover letter specialist
│   │   └── outreach_agent.py   # Networking strategist
│   ├── tasks/
│   │   ├── resume_tasks.py
│   │   └── outreach_tasks.py   # Hunter.io integration
│   ├── main.py             # Flask server
│   └── requirements.txt
├── docker-compose.yml
└── .env
```
