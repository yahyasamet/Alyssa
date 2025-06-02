import numpy as np
import logging
from typing import Tuple, Optional
import asyncio

logger = logging.getLogger(__name__)

class AudioProcessor:
    """Audio processing utilities for voice activity detection and processing"""
    
    def __init__(self, sample_rate: int = 16000):
        self.sample_rate = sample_rate
        self.vad_threshold = 0.01  # Voice activity detection threshold
        self.silence_duration = 2.0  # Seconds of silence to stop recording
        
    def detect_voice_activity(self, audio_data: np.ndarray) -> bool:
        """
        Simple voice activity detection based on energy
        
        Args:
            audio_data: Audio samples as numpy array
            
        Returns:
            bool: True if voice activity detected
        """
        try:
            # Calculate RMS energy
            rms_energy = np.sqrt(np.mean(audio_data ** 2))
            return rms_energy > self.vad_threshold
        except Exception as e:
            logger.error(f"Error in voice activity detection: {e}")
            return False
    
    def process_audio_chunk(self, audio_chunk: bytes) -> Tuple[bool, Optional[np.ndarray]]:
        """
        Process an audio chunk and detect voice activity
        
        Args:
            audio_chunk: Raw audio bytes
            
        Returns:
            Tuple of (voice_detected, processed_audio)
        """
        try:
            # Convert bytes to numpy array (assuming 16-bit PCM)
            audio_array = np.frombuffer(audio_chunk, dtype=np.int16)
            
            # Normalize to [-1, 1]
            audio_normalized = audio_array.astype(np.float32) / 32768.0
            
            # Detect voice activity
            voice_detected = self.detect_voice_activity(audio_normalized)
            
            return voice_detected, audio_normalized
            
        except Exception as e:
            logger.error(f"Error processing audio chunk: {e}")
            return False, None
    
    def calculate_silence_duration(self, is_voice_active: bool, last_voice_time: float) -> float:
        """
        Calculate how long silence has been detected
        
        Args:
            is_voice_active: Current voice activity status
            last_voice_time: Timestamp of last voice activity
            
        Returns:
            float: Duration of silence in seconds
        """
        import time
        current_time = time.time()
        
        if is_voice_active:
            return 0.0
        else:
            return current_time - last_voice_time
    
    def should_stop_recording(self, silence_duration: float) -> bool:
        """
        Determine if recording should stop based on silence duration
        
        Args:
            silence_duration: Current silence duration in seconds
            
        Returns:
            bool: True if recording should stop
        """
        return silence_duration >= self.silence_duration
    
    def preprocess_for_gemini(self, audio_data: np.ndarray) -> bytes:
        """
        Preprocess audio data for Gemini API
        
        Args:
            audio_data: Audio samples as numpy array
            
        Returns:
            bytes: Processed audio as bytes
        """
        try:
            # Ensure audio is in the right format for Gemini
            # Convert back to 16-bit PCM
            audio_int16 = (audio_data * 32767).astype(np.int16)
            return audio_int16.tobytes()
            
        except Exception as e:
            logger.error(f"Error preprocessing audio for Gemini: {e}")
            return b""

class VoiceInterrupter:
    """Handles voice interruption logic for TTS"""
    
    def __init__(self):
        self.is_speaking = False
        self.interrupt_callback = None
        
    def set_speaking_state(self, speaking: bool):
        """Set current TTS speaking state"""
        self.is_speaking = speaking
        
    def set_interrupt_callback(self, callback):
        """Set callback function to call when interruption is needed"""
        self.interrupt_callback = callback
        
    async def handle_voice_interruption(self, voice_detected: bool):
        """
        Handle voice interruption during TTS playback
        
        Args:
            voice_detected: Whether user voice is detected
        """
        if voice_detected and self.is_speaking and self.interrupt_callback:
            logger.info("Voice interruption detected, stopping TTS")
            await self.interrupt_callback()
            self.is_speaking = False

# Global instances
audio_processor = AudioProcessor()
voice_interrupter = VoiceInterrupter()
