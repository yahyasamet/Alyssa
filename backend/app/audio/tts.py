import os
import logging
import asyncio
from typing import Optional
from openai import AsyncOpenAI
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv(override=True)

class TTSService:
    """Text-to-Speech service using OpenAI's TTS"""
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.client = AsyncOpenAI(api_key=self.api_key)
        self.is_playing = False
        
    async def generate_speech(
        self, 
        text: str, 
        voice: str = "nova", 
        model: str = "gpt-4o-mini-tts",
        language: str = "auto"
    ) -> Optional[bytes]:
        """
        Generate spoken audio and return the audio data
        
        Args:
            text: The text to convert to speech
            voice: The voice to use (nova, alloy, echo, fable, onyx, shimmer)
            model: The TTS model to use
            language: Language/dialect preference
            
        Returns:
            bytes: The audio data in bytes format, or None if error
        """
        try:
            # Determine instructions based on language
            instructions = self._get_voice_instructions(language, text)
            
            logger.info(f"Generating speech for text: {text[:50]}...")
            
            audio_data = None
            async with self.client.audio.speech.with_streaming_response.create(
                model=model,
                voice=voice,
                input=text,
                instructions=instructions,
                response_format="mp3",
            ) as response:
                # Collect the audio data
                audio_data = await response.read()
                logger.info(f"Generated {len(audio_data)} bytes of audio")
                return audio_data
                
        except Exception as e:
            logger.error(f"Error generating speech: {str(e)}")
            return None
    
    def _get_voice_instructions(self, language: str, text: str) -> str:
        """Get voice instructions based on language preference"""
        
        # Check if text contains Arabic/Tunisian content
        if self._is_arabic_or_tunisian(text):
            return """تحدّث بلهجة تونسية طبيعية ودافئة، كما يتحدث التونسيون في حياتهم اليومية. استخدم الدارجة التونسية بطلاقة وبدون تكلّف، مع الحفاظ على نبرة صوت ودودة ومتعاونة."""
        
        # Default English instructions
        return "Speak in a natural, warm, and friendly tone. Use clear pronunciation and maintain a conversational pace."
    
    def _is_arabic_or_tunisian(self, text: str) -> bool:
        """Check if text contains Arabic or Tunisian dialect"""
        # Simple heuristic - check for Arabic characters
        arabic_chars = set('\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF')
        return any(char in arabic_chars for char in text)
    
    async def save_audio_file(self, audio_data: bytes, filename: str) -> str:
        """
        Save audio data to file
        
        Args:
            audio_data: Audio bytes
            filename: Filename to save as
            
        Returns:
            str: Full path to saved file
        """
        try:
            # Ensure static/audio directory exists
            os.makedirs("static/audio", exist_ok=True)
            
            file_path = f"static/audio/{filename}"
            
            with open(file_path, "wb") as f:
                f.write(audio_data)
            
            logger.info(f"Saved audio to {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"Error saving audio file: {str(e)}")
            return ""
    
    def set_playing_state(self, playing: bool):
        """Set the current playing state"""
        self.is_playing = playing
        
    def stop_playback(self):
        """Stop current playback (to be called when interrupted)"""
        self.is_playing = False
        logger.info("TTS playback stopped")

# Global TTS service instance
tts_service = TTSService()
