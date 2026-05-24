# 🛕 TempleAI Voice Assistant

An AI-powered temple guide website with bilingual voice support (English + Kannada). Devotees can speak to the AI assistant and receive voice replies about temple information, pooja timings, festivals, and more.

![Tech Stack](https://img.shields.io/badge/Next.js-14-black?style=flat-square)
![Python](https://img.shields.io/badge/FastAPI-0.115-green?style=flat-square)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-brightgreen?style=flat-square)
![AI](https://img.shields.io/badge/OpenAI-GPT--4o-blue?style=flat-square)

---

## ✨ Features

- **🎤 Voice Assistant** — Speak in English or Kannada and get voice replies
- **🤖 AI-Powered** — GPT-4o with full temple knowledge
- **🌐 Bilingual** — Automatic language detection (English & Kannada)
- **🗣️ Text-to-Speech** — Natural voice replies via ElevenLabs
- **🛕 Temple Information** — Live status, pooja timings, festivals, darshan info
- **🌗 Dark/Light Mode** — Beautiful spiritual theme
- **📱 Fully Responsive** — Works on mobile, tablet, and desktop
- **⚡ Fast** — Next.js with server components

---

## 🏗️ Architecture

```
User speaks → Browser MediaRecorder → POST /api/speech-to-text (Whisper)
→ Detected Language + Text → POST /api/chat (GPT-4o + Temple Context)
→ AI Response → POST /api/text-to-speech (ElevenLabs)
→ Audio Stream → Browser Audio Playback
```

### Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 14 (App Router) + Tailwind CSS |
| Backend | FastAPI (Python) |
| Database | MongoDB Atlas |
| AI Chat | OpenAI GPT-4o-mini |
| Speech-to-Text | OpenAI Whisper |
| Text-to-Speech | ElevenLabs Multilingual v2 |
| Animations | Framer Motion |
| Icons | Lucide React |

---

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ and npm
- Python 3.10+
- API keys (see below)

### 1. Clone & Install

```bash
# Frontend
cd frontend
npm install

# Backend
cd ../backend
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy `.env.example` to `backend/.env` and fill in your API keys:

```env
OPENAI_API_KEY=sk-...          # Required for AI chat + speech-to-text
ELEVENLABS_API_KEY=...         # Required for text-to-speech
ELEVENLABS_VOICE_ID=...        # Your preferred voice ID
MONGODB_URI=mongodb+srv://...  # MongoDB Atlas connection string
```

Frontend env (`frontend/.env.local`):
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Run Locally

```bash
# Terminal 1 — Backend
cd backend
python main.py
# Backend starts on http://localhost:8000

# Terminal 2 — Frontend
cd frontend
npm run dev
# Frontend starts on http://localhost:3000
```

### 4. Open Browser

Navigate to `http://localhost:3000` and enjoy! 🛕

---

## 🔑 API Keys Setup

### OpenAI (Required)
1. Go to [platform.openai.com](https://platform.openai.com)
2. Create an API key
3. Add to `OPENAI_API_KEY`

### ElevenLabs (Required for voice output)
1. Go to [elevenlabs.io](https://elevenlabs.io)
2. Create account & get API key
3. Choose a multilingual voice from your dashboard
4. Add `ELEVENLABS_API_KEY` and `ELEVENLABS_VOICE_ID`

### MongoDB Atlas (Required for database)
1. Go to [cloud.mongodb.com](https://cloud.mongodb.com)
2. Create a free cluster
3. Create database user & whitelist IP
4. Get connection string and add to `MONGODB_URI`

> **Note**: The app works with sample data even without MongoDB connected!

---

## 📁 Project Structure

```
temple-ai-assistant/
├── frontend/                   # Next.js App
│   ├── src/
│   │   ├── app/               # Pages (App Router)
│   │   ├── components/        # React Components
│   │   ├── hooks/             # Custom Hooks
│   │   ├── utils/             # API Client
│   │   └── data/              # Static Data
│   └── package.json
├── backend/                    # FastAPI Server
│   ├── routes/                # API Endpoints
│   ├── services/              # Business Logic
│   ├── database/              # MongoDB
│   ├── models/                # Pydantic Schemas
│   ├── data/                  # Sample Data
│   └── main.py
├── .env.example
├── docker-compose.yml
└── README.md
```

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|---------|-------------|
| POST | `/api/chat` | AI chat with temple context |
| POST | `/api/speech-to-text` | Convert audio to text (Whisper) |
| POST | `/api/text-to-speech` | Convert text to audio (ElevenLabs) |
| GET | `/api/temple-status` | Live open/closed status |
| GET | `/api/pooja-timings` | Daily + special pooja schedules |
| GET | `/api/festivals` | Upcoming festivals |
| GET | `/api/announcements` | Active announcements |
| GET | `/api/health` | API health & config check |

---

## 🐳 Docker Deployment

```bash
docker-compose up --build
```

This starts:
- Frontend on port 3000
- Backend on port 8000
- MongoDB on port 27017

---

## 📄 License

MIT License. Built with 🙏 for devotees worldwide.
