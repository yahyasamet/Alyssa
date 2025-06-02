import React, { useState, useEffect, useCallback, useRef } from 'react';
import { Settings, Trash2, Wifi, WifiOff, RefreshCw } from 'lucide-react';
import { ChatHistory, type ChatMessage } from './components/ChatHistory';
import { ChatInput } from './components/ChatInput';
import { VoiceControls } from './components/VoiceControls';
import { useWebSocket } from './hooks/useWebSocket';
import { apiService } from './services/api';
import { generateId } from './utils';
import './App.css';

function App() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [currentMode, setCurrentMode] = useState<'voice' | 'text'>('voice');
  const [error, setError] = useState<string | null>(null);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { isConnected, sendMessage, lastMessage, error: wsError, reconnect } = useWebSocket();

  // Auto-scroll to bottom when new messages arrive
  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, scrollToBottom]);

  // Handle WebSocket messages
  useEffect(() => {
    if (lastMessage?.type === 'chat_response' && lastMessage.response) {
      handleAssistantResponse(lastMessage.response);
    }
  }, [lastMessage]);

  const handleAssistantResponse = async (responseText: string) => {
    try {
      // Generate TTS audio
      const ttsResponse = await apiService.generateTTS(responseText);
      
      let audioUrl;
      if (ttsResponse.success && ttsResponse.audio_url) {
        audioUrl = `http://localhost:8000${ttsResponse.audio_url}`;
      }

      // Add assistant message to chat
      const assistantMessage: ChatMessage = {
        id: generateId(),
        type: 'assistant',
        content: responseText,
        timestamp: new Date(),
        audioUrl,
      };

      setMessages(prev => [...prev, assistantMessage]);
      setIsLoading(false);
      
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
      setIsLoading(false);
    }
  };

  const handleTextMessage = async (text: string) => {
    if (!text.trim()) return;

    setError(null);
    setIsLoading(true);

    // Add user message
    const userMessage: ChatMessage = {
      id: generateId(),
      type: 'user',
      content: text,
      timestamp: new Date(),
    };
    setMessages(prev => [...prev, userMessage]);

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
      setError('Failed to send message. Please try again.');
      setIsLoading(false);
    }
  };

  const handleAudioMessage = async (audioBlob: Blob) => {
    setError(null);
    setIsLoading(true);

    // Add user message with audio indicator
    const userMessage: ChatMessage = {
      id: generateId(),
      type: 'user',
      content: '🎤 Voice message',
      timestamp: new Date(),
      isAudio: true,
    };
    setMessages(prev => [...prev, userMessage]);

    try {
      // Convert blob to file
      const audioFile = new File([audioBlob], 'audio.webm', { type: audioBlob.type });
      
      // Send audio to backend
      const response = await apiService.sendAudioMessage(audioFile);
      await handleAssistantResponse(response.response);
      
    } catch (error) {
      console.error('Error sending audio:', error);
      setError('Failed to process audio. Please try again.');
      setIsLoading(false);
    }
  };

  const handleClearHistory = async () => {
    try {
      await apiService.clearConversation();
      setMessages([]);
      setError(null);
    } catch (error) {
      console.error('Error clearing conversation:', error);
      setError('Failed to clear conversation history.');
    }
  };

  const handleAudioPlayStart = () => {
    // Audio started playing - could be used for interruption logic
  };

  const handleAudioPlayEnd = () => {
    // Audio finished playing
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-sm border-b border-white/20 sticky top-0 z-10">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-gradient-to-br from-primary-600 to-accent-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-sm">AI</span>
              </div>
              <div>
                <h1 className="text-xl font-semibold text-gray-800">
                  Voice Assistant
                </h1>
                <div className="flex items-center space-x-2 text-sm">
                  {isConnected ? (
                    <>
                      <Wifi className="w-3 h-3 text-green-500" />
                      <span className="text-green-600">Connected</span>
                    </>
                  ) : (
                    <>
                      <WifiOff className="w-3 h-3 text-red-500" />
                      <span className="text-red-600">Disconnected</span>
                    </>
                  )}
                </div>
              </div>
            </div>

            <div className="flex items-center space-x-2">
              {/* Mode Toggle */}
              <div className="bg-gray-100 rounded-lg p-1 flex">
                <button
                  onClick={() => setCurrentMode('voice')}
                  className={`px-3 py-1 text-sm rounded transition-colors ${
                    currentMode === 'voice'
                      ? 'bg-white text-primary-600 shadow-sm'
                      : 'text-gray-600 hover:text-gray-800'
                  }`}
                >
                  Voice
                </button>
                <button
                  onClick={() => setCurrentMode('text')}
                  className={`px-3 py-1 text-sm rounded transition-colors ${
                    currentMode === 'text'
                      ? 'bg-white text-primary-600 shadow-sm'
                      : 'text-gray-600 hover:text-gray-800'
                  }`}
                >
                  Text
                </button>
              </div>

              {/* Action buttons */}
              {!isConnected && (
                <button
                  onClick={reconnect}
                  className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                  title="Reconnect"
                >
                  <RefreshCw className="w-4 h-4 text-gray-600" />
                </button>
              )}
              
              <button
                onClick={handleClearHistory}
                className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                title="Clear history"
              >
                <Trash2 className="w-4 h-4 text-gray-600" />
              </button>
              
              <button className="p-2 hover:bg-gray-100 rounded-lg transition-colors">
                <Settings className="w-4 h-4 text-gray-600" />
              </button>
            </div>
          </div>

          {/* Error display */}
          {(error || wsError) && (
            <div className="mt-3 p-3 bg-red-50 border border-red-200 rounded-lg">
              <p className="text-sm text-red-600">{error || wsError}</p>
            </div>
          )}
        </div>
      </header>

      {/* Main content */}
      <main className="max-w-4xl mx-auto flex flex-col h-[calc(100vh-120px)]">
        {/* Chat history */}
        <ChatHistory
          messages={messages}
          isLoading={isLoading}
          onAudioPlayStart={handleAudioPlayStart}
          onAudioPlayEnd={handleAudioPlayEnd}
          className="flex-1"
        />

        {/* Input area */}
        <div className="bg-white/50 backdrop-blur-sm border-t border-white/20 p-4">
          {currentMode === 'voice' ? (
            <VoiceControls
              onAudioRecorded={handleAudioMessage}
              isProcessing={isLoading}
              className="flex justify-center"
            />
          ) : (
            <ChatInput
              onSendMessage={handleTextMessage}
              isLoading={isLoading}
              placeholder="Type your message..."
            />
          )}
        </div>

        {/* Scroll anchor */}
        <div ref={messagesEndRef} />
      </main>
    </div>
  );
}

export default App;
