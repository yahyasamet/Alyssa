import os
import logging
import asyncio
import mimetypes
import struct
from typing import Optional
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv(override=True)

class TTSService:
    """Text-to-Speech service using Google Gemini TTS"""
    
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        self.client = genai.Client(api_key=self.api_key)
        self.model = "gemini-2.5-flash-preview-tts"
        self.is_playing = False
        
    async def generate_speech(
        self, 
        text: str, 
        voice: str = "Fenrir", 
        model: str = "gemini-2.5-flash-preview-tts",
        language: str = "auto"
    ) -> Optional[bytes]:
        """
        Generate spoken audio and return the audio data
        
        Args:
            text: The text to convert to speech
            voice: The voice to use (Fenrir, etc.)
            model: The TTS model to use
            language: Language/dialect preference
            
        Returns:
            bytes: The audio data in bytes format, or None if error
        """
        try:
            logger.info(f"Generating speech for text: {text[:50]}...")
            
            # Prepare content for Gemini
            contents = [
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_text(text=text),
                    ],
                ),
            ]
            
            # Configure speech generation
            generate_content_config = types.GenerateContentConfig(
                temperature=1,
                response_modalities=["audio"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name=voice
                        )
                    )
                ),
            )
            
            # Generate audio stream
            audio_chunks = []
            for chunk in self.client.models.generate_content_stream(
                model=self.model,
                contents=contents,
                config=generate_content_config,
            ):
                if (
                    chunk.candidates is None
                    or chunk.candidates[0].content is None
                    or chunk.candidates[0].content.parts is None
                ):
                    continue
                    
                if (chunk.candidates[0].content.parts[0].inline_data and 
                    chunk.candidates[0].content.parts[0].inline_data.data):
                    inline_data = chunk.candidates[0].content.parts[0].inline_data
                    data_buffer = inline_data.data
                    
                    # Convert to WAV if needed
                    file_extension = mimetypes.guess_extension(inline_data.mime_type)
                    if file_extension is None:
                        data_buffer = self._convert_to_wav(inline_data.data, inline_data.mime_type)
                    
                    audio_chunks.append(data_buffer)
            
            if audio_chunks:
                # Combine all audio chunks
                audio_data = b''.join(audio_chunks)
                logger.info(f"Generated {len(audio_data)} bytes of audio")
                return audio_data
            else:
                logger.error("No audio data generated")
                return None
                
        except Exception as e:
            logger.error(f"Error generating speech: {str(e)}")
            return None
    
    def _convert_to_wav(self, audio_data: bytes, mime_type: str) -> bytes:
        """Convert audio data to WAV format if needed"""
        try:
            parameters = self._parse_audio_mime_type(mime_type)
            bits_per_sample = parameters["bits_per_sample"]
            sample_rate = parameters["rate"]
            num_channels = 1
            data_size = len(audio_data)
            bytes_per_sample = bits_per_sample // 8
            block_align = num_channels * bytes_per_sample
            byte_rate = sample_rate * block_align
            chunk_size = 36 + data_size  # 36 bytes for header fields before data chunk size

            # Create WAV header
            header = struct.pack(
                "<4sI4s4sIHHIIHH4sI",
                b"RIFF",          # ChunkID
                chunk_size,       # ChunkSize (total file size - 8 bytes)
                b"WAVE",          # Format
                b"fmt ",          # Subchunk1ID
                16,               # Subchunk1Size (16 for PCM)
                1,                # AudioFormat (1 for PCM)
                num_channels,     # NumChannels
                sample_rate,      # SampleRate
                byte_rate,        # ByteRate
                block_align,      # BlockAlign
                bits_per_sample,  # BitsPerSample
                b"data",          # Subchunk2ID
                data_size         # Subchunk2Size (size of audio data)
            )
            return header + audio_data
        except Exception as e:
            logger.error(f"Error converting to WAV: {str(e)}")
            return audio_data

    def _parse_audio_mime_type(self, mime_type: str) -> dict:
        """Parse bits per sample and rate from an audio MIME type string"""
        bits_per_sample = 16
        rate = 24000

        # Extract rate from parameters
        parts = mime_type.split(";")
        for param in parts:
            param = param.strip()
            if param.lower().startswith("rate="):
                try:
                    rate_str = param.split("=", 1)[1]
                    rate = int(rate_str)
                except (ValueError, IndexError):
                    pass
            elif param.startswith("audio/L"):
                try:
                    bits_per_sample = int(param.split("L", 1)[1])
                except (ValueError, IndexError):
                    pass

        return {"bits_per_sample": bits_per_sample, "rate": rate}
    
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
            
            # Change extension to .wav since we're dealing with WAV data
            if filename.endswith('.mp3'):
                filename = filename.replace('.mp3', '.wav')
            
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
