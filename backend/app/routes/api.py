from fastapi import APIRouter, UploadFile, File, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from typing import Optional, Dict, Any
import json
import logging
import asyncio
import io
import uuid
from datetime import datetime

from app.core.agent import GeminiAgent
from app.core.tools import tool_registry
from app.audio.tts import tts_service
from app.audio.processor import audio_processor, voice_interrupter

logger = logging.getLogger(__name__)
router = APIRouter()

# Pydantic models
class ChatMessage(BaseModel):
    message: str
    user_context: Optional[Dict[str, Any]] = None

class TTSRequest(BaseModel):
    text: str
    voice: str = "Fenrir"
    language: str = "auto"

class ConnectionManager:
    """Manage WebSocket connections"""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        logger.info(f"Client {client_id} connected")
    
    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
            logger.info(f"Client {client_id} disconnected")
    
    async def send_message(self, client_id: str, message: dict):
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_text(json.dumps(message))

# Global connection manager and agent
manager = ConnectionManager()
gemini_agent = GeminiAgent()

@router.post("/chat/text")
async def chat_text(request: ChatMessage):
    """Handle text-based chat messages"""
    try:
        response = await gemini_agent.process_text_message(
            request.message, 
            request.user_context
        )
        
        return JSONResponse({
            "success": True,
            "response": response,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in text chat: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat/audio")
async def chat_audio(audio_file: UploadFile = File(...)):
    """Handle audio-based chat messages"""
    try:
        # Read audio file
        audio_data = await audio_file.read()
        
        # Determine MIME type
        mime_type = audio_file.content_type or "audio/mpeg"
        
        # Process with Gemini
        response = await gemini_agent.process_audio_message(audio_data, mime_type)
        
        return JSONResponse({
            "success": True,
            "response": response,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in audio chat: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tts/generate")
async def generate_tts(request: TTSRequest):
    """Generate TTS audio from text"""
    try:
        # Generate audio
        audio_data = await tts_service.generate_speech(
            request.text,
            voice=request.voice,
            language=request.language
        )
        
        if not audio_data:
            raise HTTPException(status_code=500, detail="Failed to generate audio")
        
        # Generate unique filename
        filename = f"tts_{uuid.uuid4().hex}.wav"
        
        # Save audio file
        file_path = await tts_service.save_audio_file(audio_data, filename)
        
        if not file_path:
            raise HTTPException(status_code=500, detail="Failed to save audio file")
        
        return JSONResponse({
            "success": True,
            "audio_url": f"/static/audio/{filename}",
            "filename": filename
        })
        
    except Exception as e:
        logger.error(f"Error generating TTS: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tts/stream")
async def stream_tts(request: TTSRequest):
    """Stream TTS audio directly"""
    try:
        # Generate audio
        audio_data = await tts_service.generate_speech(
            request.text,
            voice=request.voice,
            language=request.language
        )
        
        if not audio_data:
            raise HTTPException(status_code=500, detail="Failed to generate audio")
        
        # Create streaming response
        def generate():
            yield audio_data
        
        return StreamingResponse(
            generate(),
            media_type="audio/wav",
            headers={"Content-Disposition": "inline; filename=speech.wav"}
        )
        
    except Exception as e:
        logger.error(f"Error streaming TTS: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """WebSocket endpoint for real-time communication"""
    await manager.connect(websocket, client_id)
    
    try:
        while True:
            # Receive message
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            message_type = message_data.get("type")
            
            if message_type == "chat":
                # Handle chat message
                text = message_data.get("message", "")
                response = await gemini_agent.process_text_message(text)
                
                await manager.send_message(client_id, {
                    "type": "chat_response",
                    "response": response,
                    "timestamp": datetime.now().isoformat()
                })
                
            elif message_type == "voice_activity":
                # Handle voice activity detection
                is_active = message_data.get("is_active", False)
                await voice_interrupter.handle_voice_interruption(is_active)
                
            elif message_type == "ping":
                # Handle ping
                await manager.send_message(client_id, {
                    "type": "pong",
                    "timestamp": datetime.now().isoformat()
                })
    
    except WebSocketDisconnect:
        manager.disconnect(client_id)

@router.get("/conversation/history")
async def get_conversation_history():
    """Get conversation history"""
    try:
        summary = gemini_agent.get_conversation_summary()
        return JSONResponse({
            "success": True,
            "data": summary
        })
    except Exception as e:
        logger.error(f"Error getting conversation history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/conversation/clear")
async def clear_conversation():
    """Clear conversation history"""
    try:
        gemini_agent.clear_history()
        return JSONResponse({
            "success": True,
            "message": "Conversation history cleared"
        })
    except Exception as e:
        logger.error(f"Error clearing conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tools/available")
async def get_available_tools():
    """Get list of available tools"""
    try:
        tools = tool_registry.get_available_tools()
        return JSONResponse({
            "success": True,
            "tools": tools
        })
    except Exception as e:
        logger.error(f"Error getting tools: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status")
async def get_status():
    """Get API status"""
    return JSONResponse({
        "status": "healthy",
        "services": {
            "gemini": "connected",
            "tts": "available",
            "websocket": "running"
        },
        "timestamp": datetime.now().isoformat()
    })
