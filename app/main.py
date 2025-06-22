import asyncio
import base64
import json
import os
from pathlib import Path
from typing import AsyncIterable
from datetime import datetime

from dotenv import load_dotenv
from fastapi import FastAPI, Query, WebSocket
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from google.adk.agents import LiveRequestQueue
from google.adk.agents.run_config import RunConfig
from google.adk.events.event import Event
from google.adk.runners import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from google.genai import types
from manager.agent import root_agent
import glob

#
# ADK Streaming
#

# Load Gemini API Key
load_dotenv(override=True)

APP_NAME = "ADK Streaming example"
session_service = InMemorySessionService()

# Create logs directory if it doesn't exist
LOGS_DIR = Path(r"manager\sub_agents\case_summary_agent\tools")
LOGS_DIR.mkdir(exist_ok=True)
def clear_conversation_logs():
    """Delete all .txt files in the LOGS_DIR"""
    for txt_file in LOGS_DIR.glob("*.txt"):
        try:
            txt_file.unlink()
            print(f"Deleted: {txt_file}")
        except Exception as e:
            print(f"Error deleting {txt_file}: {e}")
    print("Conversation logs cleared")
clear_conversation_logs()

def log_conversation(session_id: str, role: str, content: str, mime_type: str = "text/plain"):
    """Log conversation to a text file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file = LOGS_DIR / f"conversation_{session_id}.txt"
    
    # Format the log entry
    if mime_type == "text/plain":
        log_entry = f"[{timestamp}] {role.upper()}: {content}\n"
    else:
        log_entry = f"[{timestamp}] {role.upper()}: [{mime_type}] {content}\n"
    
    # Append to file
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(log_entry)

def start_agent_session(session_id, is_audio=False):
    """Starts an agent session"""

    # Create a Session
    session = session_service.create_session(
        app_name=APP_NAME,
        user_id=session_id,
        session_id=session_id,
    )

    # Create a Runner
    runner = Runner(
        app_name=APP_NAME,
        agent=root_agent,
        session_service=session_service,
    )

    # Set response modality
    modality = "AUDIO" if is_audio else "TEXT"

    # Create speech config with voice settings
    speech_config = types.SpeechConfig(
        voice_config=types.VoiceConfig(
            # Puck, Charon, Kore, Fenrir, Aoede, Leda, Orus, and Zephyr
            prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Fenrir")
        )
    )

    # Create run config with basic settings
    config = {"response_modalities": [modality], "speech_config": speech_config}

    # Add output_audio_transcription when audio is enabled to get both audio and text
    if is_audio:
        config["output_audio_transcription"] = {}

    run_config = RunConfig(**config)

    # Create a LiveRequestQueue for this session
    live_request_queue = LiveRequestQueue()

    # Start agent session
    live_events = runner.run_live(
        session=session,
        live_request_queue=live_request_queue,
        run_config=run_config,
    )
    return live_events, live_request_queue


async def agent_to_client_messaging(
    websocket: WebSocket, live_events: AsyncIterable[Event | None], session_id: str
):
    """Agent to client communication"""
    Assistant_response = ""  # Initialize the response accumulator
    while True:
        async for event in live_events:
            if event is None:
                continue

            # If the turn complete or interrupted, send it
            if event.turn_complete or event.interrupted:
                message = {
                    "turn_complete": event.turn_complete,
                    "interrupted": event.interrupted,
                }
                await websocket.send_text(json.dumps(message))
                print(f"[AGENT TO CLIENT]: {message}")
                continue

            # Read the Content and its first Part
            part = event.content and event.content.parts and event.content.parts[0]
            if not part:
                continue

            # Make sure we have a valid Part
            if not isinstance(part, types.Part):
                continue

            # Only send text if it's a partial response (streaming)
            # Skip the final complete message to avoid duplication
            if part.text:
                Assistant_response += part.text
                # Only log when the response is complete (not partial)
                if not event.partial:
                    log_conversation(session_id, "assistant", Assistant_response, "text/plain")
                    Assistant_response = ""  # Reset for next response
            if part.text and event.partial:
                message = {
                    "mime_type": "text/plain",
                    "data": part.text,
                    "role": "model",
                }
                await websocket.send_text(json.dumps(message))
                print(f"[AGENT TO CLIENT]: text/plain: {part.text}")
                
                # Log the agent's text response
                # log_conversation(session_id, "assistant", part.text, "text/plain")

            # If it's audio, send Base64 encoded audio data
            is_audio = (
                part.inline_data
                and part.inline_data.mime_type
                and part.inline_data.mime_type.startswith("audio/pcm")
            )
            if is_audio:
                audio_data = part.inline_data and part.inline_data.data
                if audio_data:
                    message = {
                        "mime_type": "audio/pcm",
                        "data": base64.b64encode(audio_data).decode("ascii"),
                        "role": "model",
                    }
                    await websocket.send_text(json.dumps(message))
                    print(f"[AGENT TO CLIENT]: audio/pcm: {len(audio_data)} bytes.")
                    
                    # Log the agent's audio response
                    # log_conversation(session_id, "assistant", f"{len(audio_data)} bytes", "audio/pcm")


async def client_to_agent_messaging(
    websocket: WebSocket, live_request_queue: LiveRequestQueue, session_id: str
):
    """Client to agent communication"""
    while True:
        # Decode JSON message
        message_json = await websocket.receive_text()
        message = json.loads(message_json)
        mime_type = message["mime_type"]
        data = message["data"]
        role = message.get("role", "user")  # Default to 'user' if role is not provided

        # Send the message to the agent
        if mime_type == "text/plain":
            # Send a text message
            content = types.Content(role=role, parts=[types.Part.from_text(text=data)])
            live_request_queue.send_content(content=content)
            print(f"[CLIENT TO AGENT PRINT]: {data}")
            
            # Log the user's text message
            log_conversation(session_id, "user", data, "text/plain")
            
        elif mime_type == "audio/pcm":
            # Send audio data
            decoded_data = base64.b64decode(data)

            # Send the audio data - note that ActivityStart/End and transcription
            # handling is done automatically by the ADK when input_audio_transcription
            # is enabled in the config
            live_request_queue.send_realtime(
                types.Blob(data=decoded_data, mime_type=mime_type)
            )
            print(f"[CLIENT TO AGENT]: audio/pcm: {len(decoded_data)} bytes")
            
            # Log the user's audio message
            # log_conversation(session_id, "user", f"{len(decoded_data)} bytes", "audio/pcm")

        else:
            raise ValueError(f"Mime type not supported: {mime_type}")


#
# FastAPI web app
#

app = FastAPI()

STATIC_DIR = Path("static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/")
async def root():
    """Serves the index.html"""
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))


@app.websocket("/ws/{session_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    session_id: str,
    is_audio: str = Query(...),
):
    """Client websocket endpoint"""

    # Wait for client connection
    await websocket.accept()
    print(f"Client #{session_id} connected, audio mode: {is_audio}")
    
    # Log session start
    log_conversation(session_id, "system", f"Session started - Audio mode: {is_audio}")

    # Start agent session
    live_events, live_request_queue = start_agent_session(
        session_id, is_audio == "true"
    )

    # Start tasks
    agent_to_client_task = asyncio.create_task(
        agent_to_client_messaging(websocket, live_events, session_id)
    )
    client_to_agent_task = asyncio.create_task(
        client_to_agent_messaging(websocket, live_request_queue, session_id)
    )
    try:
        await asyncio.gather(agent_to_client_task, client_to_agent_task)
    except Exception as e:
        print(f"An error occurred in the websocket tasks: {e}")
        # Log the error
        log_conversation(session_id, "system", f"Error: {e}")
    finally:
        # Disconnected
        print(f"Client #{session_id} disconnected")
        # Log session end
        log_conversation(session_id, "system", "Session ended")
