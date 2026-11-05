# MindBridge AI
### A Multilingual Mental Wellness Assistant Powered by AWS Strands SDK

MindBridge AI is an AI-powered mental wellness support application designed to provide empathetic conversations, practical coping guidance, and safety-aware responses across supported languages.

The application combines a React frontend, a FastAPI backend, AWS Strands SDK-based safety assessment, Amazon Bedrock, and OpenAI-powered conversational responses.

## The Problem

Many people experience stress, anxiety, emotional distress, or difficulty discussing their mental well-being. Access to timely, understandable, and multilingual emotional support can be limited.

MindBridge AI aims to make everyday mental wellness conversations more accessible while recognizing situations that may require professional assistance.

## Key Features

- **AI-Powered Conversations:** Context-aware responses for everyday emotional wellness discussions.
- **Multilingual Support:** Language detection and responses in supported languages.
- **AWS Strands SDK Integration:** Agent-based safety assessment using AWS-powered AI services.
- **Crisis Safety Assessment:** Identifies potential crisis signals and routes responses through additional safety checks.
- **Persistent Distress Detection:** Recognizes indications of prolonged emotional distress.
- **Medical Safety Guidance:** Encourages appropriate professional consultation when medical or mental health concerns arise.
- **Response Validation:** Additional checks before AI-generated responses are returned.
- **Responsive Interface:** React-based interface designed for desktop and mobile devices.
- **Light and Dark Modes:** Accessible visual presentation.
- **Session-Based Conversation History:** Supports restoration of an active conversation during its valid session.

## Technology Stack

| Layer | Technology |
|---|---|
| Frontend | React, Vite, JavaScript, CSS |
| Backend | Python, FastAPI, Uvicorn |
| Agent Framework | AWS Strands SDK |
| AWS AI Services | Amazon Bedrock |
| Conversational AI | OpenAI API |
| Testing | Pytest |
| Version Control | Git and GitHub |

## High-Level Architecture

```text
User
  |
  v
React Frontend
  |
  v
FastAPI Backend
  |
  +--> Language Detection
  |
  +--> Safety Assessment
  |       |
  |       +--> AWS Strands SDK
  |       +--> Amazon Bedrock
  |
  +--> AI Response Generation
  |       |
  |       +--> OpenAI API
  |
  +--> Response Safety Validation
  |
  v
Safety-Aware Response to User
```

## Safety-First Approach

MindBridge AI uses multiple safety-oriented components to assess potentially concerning messages and validate responses.

The application is intended for general mental wellness support, not diagnosis or treatment.

**Important:** MindBridge AI is not a licensed therapist, medical professional, or emergency response service. It does not replace qualified healthcare professionals. People experiencing an immediate emergency should contact local emergency services.

AI safety checks have limitations and may not identify every risk.

## Run Locally

### Backend

```bash
cd backend
python -m venv venv
```

Activate the virtual environment and install dependencies:

```bash
pip install -r requirements.txt
```

Configure the required API credentials through environment variables or an untracked `.env` file.

Start the backend:

```bash
python -m uvicorn main:app --reload
```

Backend URL: `http://127.0.0.1:8000`

### Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend URL: `http://localhost:5173`

## Testing

Backend automated tests can be executed with:

```bash
cd backend
python -m pytest tests -q
```

## Current Development Status

MindBridge AI currently includes a functioning local frontend and backend, real AI integrations, safety assessment components, and automated backend tests.

The following capabilities are planned or require additional production work:

- Public deployment and end-to-end verification
- Persistent database-backed conversation storage
- User registration and authentication
- Long-term conversation archive
- Stronger privacy, security, and retention controls
- Additional multilingual safety validation

## Project Repository

https://github.com/RuhamaMansoor/MindBridge-AI

## Responsible AI Statement

MindBridge AI is designed to provide supportive wellness conversations with safety checks and professional-referral guidance when appropriate.

It is a software project under development and should not be relied upon as a substitute for professional mental healthcare or emergency intervention.

---

**MindBridge AI — Connecting Technology with Compassion.**
