import React, { useState, useEffect, useCallback } from 'react';
import { Mic, Send, Volume2 } from 'lucide-react';
import { cn } from '../utils';
import { useAudioRecorder, type UseAudioRecorderOptions } from '../hooks/useAudioRecorder';

interface OnboardingScreenProps {
  isAssistantSpeaking?: boolean;
  onMicClick?: () => void;
  onSendText?: (text: string) => void;
  onAudioRecorded?: (audio: Blob) => void; // New prop for handling recorded audio
  className?: string;
}

export const OnboardingScreen: React.FC<OnboardingScreenProps> = ({
  isAssistantSpeaking = false,
  onMicClick,
  onSendText,
  onAudioRecorded,
  className
}) => {
  const [inputText, setInputText] = useState('');
  const [orbitAnimation, setOrbitAnimation] = useState(false);

  useEffect(() => {
    // Start orbit animation on mount
    setOrbitAnimation(true);
  }, []);

  // Audio recorder for voice functionality
  const handleSpeechSegmentRecorded = useCallback((blob: Blob) => {
    console.log('OnboardingScreen: Speech segment recorded', blob);
    if (onAudioRecorded) {
      onAudioRecorded(blob);
    }
  }, [onAudioRecorded]);

  const audioRecorderOptions: UseAudioRecorderOptions = {
    onSpeechSegmentRecorded: handleSpeechSegmentRecorded,
  };  const {
    error: recorderError,
    isVadActive,     
    activateVoiceDetection,
    deactivateVoiceDetection,
  } = useAudioRecorder(audioRecorderOptions);

  // Use actual VAD state for listening indicator
  const isListening = isVadActive && !isAssistantSpeaking;

  const handleMicClick = async () => {
    if (recorderError) {
      console.error('Cannot operate, recorder error present:', recorderError);
      return;
    }

    if (isVadActive) {
      console.log('VAD is active, deactivating...');
      const finalBlob = await deactivateVoiceDetection();
      if (finalBlob) {
        console.log('VAD deactivated, final blob recorded:', finalBlob);
        if (onAudioRecorded) {
          onAudioRecorded(finalBlob);
        }
      }
    } else {
      console.log('VAD is not active, activating...');
      await activateVoiceDetection();
    }

    // Also call the original onMicClick if provided
    if (onMicClick) {
      onMicClick();
    }
  };

  const handleSendClick = () => {
    if (inputText.trim() && onSendText) {
      onSendText(inputText.trim());
      setInputText('');
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendClick();
    }
  };

  return (
    <div className={cn(
      "min-h-screen bg-black text-white flex flex-col items-center justify-center relative overflow-hidden",
      className
    )}>      {/* Background gradient effects */}
      <div className="absolute inset-0 bg-gradient-to-br from-blue-900/20 via-purple-900/10 to-black" />
      
      {/* Top hint */}
      <div className="absolute top-6 left-1/2 transform -translate-x-1/2 z-20">
        <div className="bg-white/10 backdrop-blur-sm rounded-full px-4 py-2 border border-white/20">
          <p className="text-white/70 text-sm text-center">
            🎤 <span className="text-blue-300">Speak</span> for voice mode • ✍️ <span className="text-purple-300">Type</span> for conversation
          </p>
        </div>
      </div>
      
      {/* Main content container */}
      <div className="relative z-10 flex flex-col items-center justify-center flex-1 px-8 max-w-2xl mx-auto">        {/* Title Section */}
        <div className="text-center mb-16">
          <h1 className="text-5xl md:text-6xl font-medium text-white mb-3 tracking-wide">
            Alyssa
          </h1>
          <p className="text-gray-400 text-base md:text-lg font-light">
            Meet your AI assistant
          </p>
        </div>        {/* Dynamic Orb */}
        <div className="relative mb-20">
          {/* Main orb */}
          <div className={cn(
            "w-64 h-64 md:w-80 md:h-80 rounded-full relative transition-all duration-1000",
            "bg-gradient-to-br from-blue-400/60 via-blue-500/80 to-blue-600/60",
            "shadow-2xl shadow-blue-500/30",
            isListening && "scale-110 shadow-blue-400/50",
            isAssistantSpeaking && "scale-105 shadow-purple-500/50 bg-gradient-to-br from-purple-400/60 via-purple-500/80 to-purple-600/60"
          )}>
            {/* Inner glow layers */}
            <div className={cn(
              "absolute inset-6 rounded-full bg-gradient-to-br from-blue-300/40 to-blue-500/30 transition-all duration-500",
              isListening && "from-blue-200/50 to-blue-400/40",
              isAssistantSpeaking && "from-purple-300/40 to-purple-500/30"
            )} />
            
            <div className={cn(
              "absolute inset-12 rounded-full bg-gradient-to-br from-blue-200/60 to-blue-400/40 transition-all duration-300",
              isListening && "animate-pulse from-blue-100/70 to-blue-300/50",
              isAssistantSpeaking && "animate-pulse from-purple-200/60 to-purple-400/40"
            )} />

            {/* Core center */}
            <div className={cn(
              "absolute inset-20 rounded-full bg-gradient-to-br from-blue-100/50 to-blue-300/30 transition-all duration-300",
              isListening && "animate-pulse from-blue-50/60 to-blue-200/40",
              isAssistantSpeaking && "animate-pulse from-purple-100/50 to-purple-300/30"
            )} />

            {/* Subtle orbiting elements */}
            {orbitAnimation && (
              <>
                <div className="absolute inset-0 animate-spin" style={{ animationDuration: '30s' }}>
                  <div className="absolute w-1.5 h-1.5 bg-blue-300/70 rounded-full -top-2 left-1/2 transform -translate-x-1/2" />
                </div>
                <div className="absolute inset-0 animate-spin" style={{ animationDuration: '40s', animationDirection: 'reverse' }}>
                  <div className="absolute w-1 h-1 bg-blue-200/60 rounded-full top-1/2 -right-2 transform -translate-y-1/2" />
                </div>
              </>
            )}
          </div>

          {/* Outer ring - more subtle */}
          <div className={cn(
            "absolute inset-0 rounded-full border border-blue-400/20 transition-all duration-500",
            "w-72 h-72 md:w-88 md:h-88 -m-4",
            isListening && "border-blue-300/30 scale-105",
            isAssistantSpeaking && "border-purple-400/30 scale-102"
          )} />
        </div>        {/* Welcome text - removed */}
      </div>

      {/* Bottom Input Bar */}
      <div className="fixed bottom-0 left-0 right-0 z-20 bg-gray-900/90 backdrop-blur-md border-t border-gray-700/30">
        <div className="max-w-4xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between bg-gray-800/70 rounded-2xl px-6 py-4 backdrop-blur-sm border border-gray-600/30">
            {/* Left side - Status indicators */}
            <div className="flex items-center space-x-6">
              {/* Listening indicator */}
              <div className="flex items-center space-x-2">
                <div className={cn(
                  "w-3 h-3 rounded-full transition-all duration-300",
                  isListening ? "bg-green-500 animate-pulse shadow-lg shadow-green-500/50" : "bg-gray-600"
                )} />
                <span className={cn(
                  "text-sm font-medium transition-colors duration-300",
                  isListening ? "text-green-400" : "text-gray-400"
                )}>
                  Listening...
                </span>
              </div>

              {/* Speaking indicator */}
              <div className="flex items-center space-x-2">
                <span className={cn(
                  "text-sm font-medium transition-colors duration-300",
                  isAssistantSpeaking ? "text-blue-400" : "text-gray-500"
                )}>
                  Speaking...
                </span>
              </div>
            </div>

            {/* Center - Text input area */}
            <div className="flex-1 max-w-md mx-8">
              <input
                type="text"
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Type a message..."
                className="w-full bg-transparent text-white placeholder-gray-500 border-none outline-none text-sm text-center"
              />
            </div>

            {/* Right side - Controls */}
            <div className="flex items-center space-x-4">
              {/* Volume control */}
              <button className="p-2 text-gray-400 hover:text-white transition-colors rounded-lg hover:bg-gray-700/50">
                <Volume2 className="w-5 h-5" />
              </button>              {/* Microphone */}
              <button
                onClick={handleMicClick}
                className={cn(
                  "p-3 rounded-full transition-all duration-300",
                  isListening 
                    ? "bg-pink-500 hover:bg-pink-600 text-white shadow-lg shadow-pink-500/30" 
                    : "bg-gray-700 hover:bg-gray-600 text-gray-300"
                )}
              >
                <Mic className="w-5 h-5" />
              </button>{/* Send button */}
              <button
                onClick={handleSendClick}
                disabled={!inputText.trim()}
                className={cn(
                  "p-3 rounded-full transition-all duration-300",
                  inputText.trim()
                    ? "bg-blue-500 hover:bg-blue-600 text-white shadow-lg shadow-blue-500/25"
                    : "bg-gray-700 text-gray-500 cursor-not-allowed"
                )}
              >
                <Send className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
