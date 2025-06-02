import base64
import os
import logging
from typing import Dict, Any, Optional
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class GeminiAgent:
    """
    Gemini AI agent for processing audio and text messages
    """
    
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
        
        os.environ["GOOGLE_API_KEY"] = self.api_key
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            temperature=0.7
        )
        
        self.conversation_history = []
        
    async def process_audio_message(
        self, 
        audio_data: bytes, 
        audio_mime_type: str = "audio/mpeg",
        user_context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Process audio input directly with Gemini (no STT needed)
        
        Args:
            audio_data: Raw audio bytes
            audio_mime_type: MIME type of the audio
            user_context: Additional context about the user
            
        Returns:
            str: AI response text
        """
        try:
            # Encode audio to base64
            encoded_audio = base64.b64encode(audio_data).decode("utf-8")
            
            # Create system prompt
            system_prompt = self._build_system_prompt(user_context)
            
            # Create message with audio
            message = HumanMessage(
                content=[
                    {"type": "text", "text": system_prompt},
                    {
                        "type": "media",
                        "data": encoded_audio,
                        "mime_type": audio_mime_type,
                    },
                ]
            )
            
            # Get response from Gemini
            response = await self._invoke_with_retry(message)
            
            # Store in conversation history
            self.conversation_history.append({
                "type": "audio_input",
                "response": response.content,
                "timestamp": self._get_timestamp()
            })
            
            return response.content
            
        except Exception as e:
            logger.error(f"Error processing audio message: {str(e)}")
            return "I'm sorry, I couldn't process your audio message. Could you please try again?"
    
    async def process_text_message(
        self, 
        text: str, 
        user_context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Process text input with Gemini
        
        Args:
            text: User's text message
            user_context: Additional context about the user
            
        Returns:
            str: AI response text
        """
        try:
            # Create system prompt
            system_prompt = self._build_system_prompt(user_context)
            
            # Create message
            full_message = f"{system_prompt}\n\nUser: {text}"
            message = HumanMessage(content=full_message)
            
            # Get response from Gemini
            response = await self._invoke_with_retry(message)
            
            # Store in conversation history
            self.conversation_history.append({
                "type": "text_input",
                "user_message": text,
                "response": response.content,
                "timestamp": self._get_timestamp()
            })
            
            return response.content
            
        except Exception as e:
            logger.error(f"Error processing text message: {str(e)}")
            return "I'm sorry, I encountered an error. Could you please try again?"
    
    def _build_system_prompt(self, user_context: Optional[Dict[str, Any]] = None) -> str:
        """Build system prompt with context"""
        base_prompt = """You are a helpful AI voice assistant. Please:

1. Transcribe and understand the user's audio input (if provided)
2. Provide helpful, concise, and friendly responses
3. Maintain context from previous conversations
4. If the user speaks in Arabic or Tunisian dialect, respond appropriately in the same language
5. Keep responses natural and conversational
6. If you're unsure about something, ask for clarification

Previous conversation context:"""
        
        # Add conversation history
        if self.conversation_history:
            context_messages = "\n".join([
                f"- {msg.get('response', '')[:100]}..." 
                for msg in self.conversation_history[-3:]  # Last 3 messages
            ])
            base_prompt += f"\n{context_messages}\n"
        
        # Add user context if provided
        if user_context:
            base_prompt += f"\nUser context: {user_context}\n"
        
        base_prompt += "\nPlease respond to the current message:"
        
        return base_prompt
    
    async def _invoke_with_retry(self, message: HumanMessage, max_retries: int = 3):
        """Invoke Gemini with retry logic"""
        for attempt in range(max_retries):
            try:
                return self.llm.invoke([message])
            except Exception as e:
                logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt == max_retries - 1:
                    raise e
                await self._sleep(1)  # Wait before retry
    
    async def _sleep(self, seconds: int):
        """Async sleep helper"""
        import asyncio
        await asyncio.sleep(seconds)
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def get_conversation_summary(self) -> Dict[str, Any]:
        """Get conversation summary"""
        return {
            "total_messages": len(self.conversation_history),
            "recent_messages": self.conversation_history[-5:] if self.conversation_history else []
        }
