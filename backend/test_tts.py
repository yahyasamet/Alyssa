#!/usr/bin/env python3
"""
Test script for the new Google Gemini TTS service
"""
import os
import asyncio
from dotenv import load_dotenv
from app.audio.tts import TTSService

# Load environment variables
load_dotenv()

async def test_tts():
    """Test the TTS service"""
    try:
        print("Initializing TTS service...")
        tts = TTSService()
        
        test_text = "Hello, this is a test of the new Google Gemini TTS service!"
        
        print(f"Generating speech for: '{test_text}'")
        audio_data = await tts.generate_speech(test_text)
        
        if audio_data:
            print(f"✅ Successfully generated {len(audio_data)} bytes of audio")
            
            # Save test file
            filename = "test_speech.wav"
            file_path = await tts.save_audio_file(audio_data, filename)
            
            if file_path:
                print(f"✅ Audio saved to: {file_path}")
            else:
                print("❌ Failed to save audio file")
        else:
            print("❌ Failed to generate audio")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_tts())
