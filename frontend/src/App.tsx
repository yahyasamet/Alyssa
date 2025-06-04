import { useState, useEffect } from 'react';
import { OnboardingScreen } from './components/OnboardingScreen';
import { ChatHistory } from './components/ChatHistory';
import { ChatInput } from './components/ChatInput';
import { useWebSocket } from './hooks/useWebSocket';
import { apiService } from './services/api';
import { generateId, cn } from './utils';
import './App.css';

// Keep minimal ChatMessage type for backend compatibility
export interface ChatMessage {
  id: string;
  content: string;
  type: 'user' | 'assistant';
  timestamp: Date;
  audioUrl?: string;
  isAudio?: boolean;
}

function App() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [conversationMode, setConversationMode] = useState<'onboarding' | 'text'>('onboarding');
  const [isAssistantSpeaking, setIsAssistantSpeaking] = useState(false);
  const [activeAudioPlayerRef, setActiveAudioPlayerRef] = useState<HTMLAudioElement | null>(null);
  
  const { isConnected, sendMessage, lastMessage } = useWebSocket();

  // Handle WebSocket messages
  useEffect(() => {
    if (lastMessage?.type === 'chat_response' && lastMessage.response) {
      handleAssistantResponse(lastMessage.response);
    }
  }, [lastMessage]);
  const handleAssistantResponse = async (responseText: string) => {
    try {
      // If assistant is currently speaking, interrupt it before playing new audio
      if (isAssistantSpeaking && activeAudioPlayerRef) {
        console.log(`handleAssistantResponse: Assistant is speaking, interrupting before new response.`);
        handleInterrupt();
        // Add a small delay to ensure the interruption is processed before new audio starts
        await new Promise(resolve => setTimeout(resolve, 100)); 
      }

      // Generate TTS audio
      const ttsResponse = await apiService.generateTTS(responseText);
      
      let audioUrl;
      if (ttsResponse.success && ttsResponse.audio_url) {
        audioUrl = `http://localhost:8000${ttsResponse.audio_url}`;
        // Create audio element and play
        const audio = new Audio(audioUrl);
        audio.onplay = () => handleAudioPlayStart(audio);
        audio.onended = () => handleAudioPlayEnd();
        audio.onerror = () => handleAudioPlayEnd();
        audio.play();
      }      // Add assistant message to conversation
      const assistantMessage: ChatMessage = {
        id: generateId(),
        type: 'assistant',
        content: responseText,
        timestamp: new Date(),
        audioUrl,
      };
      setMessages(prev => [...prev, assistantMessage]);
      
    } catch (error) {
      console.error('Error generating TTS:', error);
      
      // Add message without audio
      const assistantMessage: ChatMessage = {
        id: generateId(),
        type: 'assistant',
        content: responseText,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, assistantMessage]);
    }
  };
  const handleTextMessage = async (text: string) => {
    if (!text.trim()) return;    // Add user message to conversation
    const userMessage: ChatMessage = {
      id: generateId(),
      type: 'user',
      content: text,
      timestamp: new Date(),
    };
    setMessages(prev => [...prev, userMessage]);

    // Switch to conversation mode when user sends text
    setConversationMode('text');

    try {
      if (isConnected) {
        // Send via WebSocket for real-time response
        sendMessage({
          type: 'chat',
          message: text,
        });
      } else {
        // Fallback to REST API
        const response = await apiService.sendTextMessage(text);
        await handleAssistantResponse(response.response);
      }
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };
  const handleAudioMessage = async (audioBlob: Blob) => {    // Add user message with audio indicator
    const userMessage: ChatMessage = {
      id: generateId(),
      type: 'user',
      content: '🎤 Voice message processing...',
      timestamp: new Date(),
      isAudio: true,
    };
    setMessages(prev => [...prev, userMessage]);

    try {
      // Convert blob to file
      const audioFile = new File([audioBlob], 'audio.webm', { type: audioBlob.type });
      
      // Send audio to backend
      const response = await apiService.sendAudioMessage(audioFile);
        // Update user message with transcription if available
      setMessages(prev => prev.map(msg => 
        msg.id === userMessage.id 
          ? { ...msg, content: '🎤 Voice message' }
          : msg
      ));
      
      await handleAssistantResponse(response.response);
      
    } catch (error) {
      console.error('Error sending audio:', error);
      setMessages(prev => prev.map(msg => 
        msg.id === userMessage.id 
          ? { ...msg, content: '⚠️ Error processing voice message' }
          : msg
      ));
    }
  };

  const handleAudioPlayStart = (newAudioElement: HTMLAudioElement) => {
    if (activeAudioPlayerRef && activeAudioPlayerRef !== newAudioElement) {
      console.log("New audio starting, stopping previous active audio");
      activeAudioPlayerRef.pause();
    }
    setIsAssistantSpeaking(true);
    setActiveAudioPlayerRef(newAudioElement);
  };

  const handleAudioPlayEnd = () => {
    console.log("Audio play ended");
    setIsAssistantSpeaking(false);
    setActiveAudioPlayerRef(null);
  };

  const handleInterrupt = () => {
    if (activeAudioPlayerRef) {
      console.log("Interrupting audio");
      activeAudioPlayerRef.pause();
    }
    setIsAssistantSpeaking(false); 
    setActiveAudioPlayerRef(null);
  };
  // Handlers for onboarding screen
  const handleOnboardingMicClick = () => {
    // Voice activation is handled within the onboarding screen
    // Keep in onboarding mode for voice interactions
  };

  const handleOnboardingTextSend = (text: string) => {
    handleTextMessage(text);
  };

  // Handler to switch back to onboarding mode
  const handleBackToOnboarding = () => {
    setConversationMode('onboarding');
  };
  // Conditional rendering based on conversation mode
  if (conversationMode === 'text' && messages.length > 0) {
    // Show conversation view for text chat with same design as onboarding
    return (
      <div className="min-h-screen bg-black text-white flex flex-col relative overflow-hidden">
        {/* Background gradient effects - same as onboarding */}
        <div className="absolute inset-0 bg-gradient-to-br from-blue-900/20 via-purple-900/10 to-black" />
        
        {/* Top hint */}
        <div className="absolute top-6 left-1/2 transform -translate-x-1/2 z-20">
          <div className="bg-white/10 backdrop-blur-sm rounded-full px-4 py-2 border border-white/20">
            <p className="text-white/70 text-sm text-center">
              💬 <span className="text-purple-300">Conversation Mode</span> • 
              <button 
                onClick={handleBackToOnboarding}
                className="text-blue-300 hover:text-blue-200 underline ml-2"
              >
                Switch to Voice
              </button>
            </p>
          </div>
        </div>

        {/* Header with Alyssa title - same style as onboarding */}
        <div className="relative z-10 text-center pt-20 pb-8">
          <h1 className="text-4xl md:text-5xl font-medium text-white mb-2 tracking-wide">
            Alyssa
          </h1>
          <p className="text-gray-400 text-sm md:text-base font-light">
            Conversation History
          </p>
        </div>        {/* Chat history area */}
        <div className="relative z-10 flex-1 max-w-4xl mx-auto w-full px-4 pb-32">
          <ChatHistory
            messages={messages}
            isLoading={false}
            onAudioPlayStart={handleAudioPlayStart}
            onAudioPlayEnd={handleAudioPlayEnd}
            className="h-full"
            dark={true}
          />
        </div>

        {/* Bottom Input Bar - same style as onboarding */}
        <div className="fixed bottom-0 left-0 right-0 z-20 bg-gray-900/90 backdrop-blur-md border-t border-gray-700/30">
          <div className="max-w-4xl mx-auto px-6 py-4">
            <div className="flex items-center justify-between bg-gray-800/70 rounded-2xl px-6 py-4 backdrop-blur-sm border border-gray-600/30">
              {/* Left side - Status indicators */}
              <div className="flex items-center space-x-6">
                {/* Connection status */}
                <div className="flex items-center space-x-2">
                  <div className="w-3 h-3 rounded-full bg-green-500 animate-pulse shadow-lg shadow-green-500/50" />
                  <span className="text-sm font-medium text-green-400">Connected</span>
                </div>

                {/* Speaking indicator */}
                <div className="flex items-center space-x-2">
                  <span className={cn(
                    "text-sm font-medium transition-colors duration-300",
                    isAssistantSpeaking ? "text-blue-400" : "text-gray-500"
                  )}>
                    {isAssistantSpeaking ? "Speaking..." : "Ready"}
                  </span>
                </div>
              </div>              {/* Center - Enhanced text input */}
              <div className="flex-1 max-w-md mx-8">
                <ChatInput
                  onSendMessage={handleTextMessage}
                  isLoading={false}
                  placeholder="Type your message..."
                  dark={true}
                />
              </div>

              {/* Right side - Voice mode button */}
              <div className="flex items-center space-x-4">
                <button
                  onClick={handleBackToOnboarding}
                  className="px-4 py-2 bg-blue-500/80 hover:bg-blue-500 text-white rounded-lg transition-all duration-300 text-sm font-medium"
                >
                  🎤 Voice Mode
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Always show the onboarding screen for voice mode or initial state
  return (
    <OnboardingScreen
      isAssistantSpeaking={isAssistantSpeaking}
      onMicClick={handleOnboardingMicClick}
      onSendText={handleOnboardingTextSend}
      onAudioRecorded={handleAudioMessage}
    />
  );
}

export default App;
