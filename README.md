# 🧠 Gemini-Based AI Voice Assistant

A modern, modular AI voice assistant powered by Google's Gemini 2.0 Flash and OpenAI's TTS.

## ✨ Features

- 🎙️ **Voice Activation**: Automatic voice detection and recording
- 🧠 **Gemini Integration**: Direct audio processing without STT
- 💬 **Smart Conversations**: Contextual AI responses
- 🔊 **High-Quality TTS**: OpenAI's GPT-4o-mini-TTS with Tunisian dialect
- 🔁 **Voice Interruption**: Stop TTS when user starts speaking
- 🎨 **Modern UI**: Beautiful React interface with Tailwind CSS
- 🔌 **Modular Architecture**: Easily extensible with tools and agents

## 🚀 Quick Start

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Environment Variables
Create a `.env` file with:
```
GOOGLE_API_KEY=your_gemini_api_key
OPENAI_API_KEY=your_openai_api_key
```

## 🛠️ Tech Stack

- **Frontend**: React + Vite + TypeScript + Tailwind CSS
- **Backend**: FastAPI + Python
- **AI**: Google Gemini 2.0 Flash
- **TTS**: OpenAI GPT-4o-mini-TTS
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
