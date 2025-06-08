# 🧠 Gemini-Based AI Voice Assistant

A modern, modular AI voice assistant powered by Google's Gemini 2.0 Flash and OpenAI's TTS.

## ✨ Features

- 🎙️ **Voice Activation**: Automatic voice detection and recording
- 🧠 **Gemini Integration**: Direct audio processing without STT
- 💬 **Smart Conversations**: Contextual AI responses
- 🔊 **High-Quality TTS**: Google Gemini 2.5 Flash TTS with voice customization
- 🔁 **Voice Interruption**: Stop TTS when user starts speaking
- 🎨 **Modern UI**: Beautiful React interface with Tailwind CSS
- 🔌 **Modular Architecture**: Easily extensible with tools and agents

## 🚀 Quick Start

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
# Copy and configure environment variables
cp .env.example .env
# Edit .env file with your API keys
python main.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Environment Variables
Create a `.env` file in the backend directory with:
```
GOOGLE_API_KEY=your_GOOGLE_API_KEY
GOOGLE_API_KEY=your_GOOGLE_API_KEY
```

## 🛠️ Tech Stack

- **Frontend**: React + Vite + TypeScript + Tailwind CSS
- **Backend**: FastAPI + Python
- **AI**: Google Gemini 2.0 Flash
- **TTS**: Google Gemini 2.5 Flash TTS
- **Audio**: Web Audio API + MediaRecorder

## 📦 Project Structure

```
ai-voice-assistant/
├── backend/                 # Python FastAPI backend
├── frontend/                # React frontend
├── .env                     # Environment variables
└── README.md               # This file
```

## 🔧 Extensions

The modular architecture allows easy extension with:
- 🔌 Custom tools (weather, FAQ, etc.)
- 🧑‍🤝‍🧑 Role-based agents
- 🎚️ Admin dashboard
- 📊 Analytics and monitoring
