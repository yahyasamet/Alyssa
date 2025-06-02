from typing import Dict, Any, List
import json
import os

class WeatherTool:
    """Sample weather tool - can be extended with real API"""
    
    async def get_weather(self, location: str) -> Dict[str, Any]:
        """Get weather for a location (mock implementation)"""
        # In a real implementation, you'd call a weather API
        return {
            "location": location,
            "temperature": "22°C",
            "condition": "Sunny",
            "humidity": "65%",
            "description": f"The weather in {location} is sunny with a temperature of 22°C"
        }

class FAQTool:
    """FAQ tool for common questions"""
    
    def __init__(self):
        self.faqs = {
            "how_to_use": "To use this voice assistant, simply speak into your microphone. I'll listen and respond with voice.",
            "what_can_you_do": "I can have conversations, answer questions, help with tasks, and provide information on various topics.",
            "voice_commands": "You can speak naturally - I understand both English and Arabic/Tunisian dialect.",
            "technical_support": "For technical issues, please check your microphone permissions and internet connection."
        }
    
    async def search_faq(self, query: str) -> str:
        """Search FAQ for relevant answers"""
        query_lower = query.lower()
        
        for key, answer in self.faqs.items():
            if any(word in query_lower for word in key.split("_")):
                return answer
        
        return "I don't have a specific FAQ answer for that question, but I'm happy to help in other ways!"

class ToolRegistry:
    """Registry for managing available tools"""
    
    def __init__(self):
        self.tools = {
            "weather": WeatherTool(),
            "faq": FAQTool()
        }
    
    async def execute_tool(self, tool_name: str, method: str, **kwargs) -> Any:
        """Execute a tool method"""
        if tool_name not in self.tools:
            raise ValueError(f"Tool '{tool_name}' not found")
        
        tool = self.tools[tool_name]
        if not hasattr(tool, method):
            raise ValueError(f"Method '{method}' not found in tool '{tool_name}'")
        
        method_func = getattr(tool, method)
        return await method_func(**kwargs)
    
    def get_available_tools(self) -> List[str]:
        """Get list of available tools"""
        return list(self.tools.keys())
    
    def register_tool(self, name: str, tool_instance: Any):
        """Register a new tool"""
        self.tools[name] = tool_instance

# Global tool registry instance
tool_registry = ToolRegistry()
