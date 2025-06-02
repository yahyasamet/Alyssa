import React from 'react';
import { User, Bot, Mic } from 'lucide-react';
import { cn, formatTime } from '../utils';
import { AudioPlayer } from './AudioPlayer';

export interface ChatMessage {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  audioUrl?: string;
  isAudio?: boolean;
}

interface ChatMessageProps {
  message: ChatMessage;
  onAudioPlayStart?: () => void;
  onAudioPlayEnd?: () => void;
  className?: string;
}

export const ChatMessageComponent: React.FC<ChatMessageProps> = ({
  message,
  onAudioPlayStart,
  onAudioPlayEnd,
  className
}) => {
  const isUser = message.type === 'user';

  return (
    <div className={cn("flex gap-3 mb-6", isUser && "flex-row-reverse", className)}>
      {/* Avatar */}
      <div className={cn(
        "flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center",
        isUser ? "bg-primary-600" : "bg-accent-600"
      )}>
        {isUser ? (
          message.isAudio ? (
            <Mic className="w-4 h-4 text-white" />
          ) : (
            <User className="w-4 h-4 text-white" />
          )
        ) : (
          <Bot className="w-4 h-4 text-white" />
        )}
      </div>

      {/* Message content */}
      <div className={cn("flex-1 max-w-xs sm:max-w-md md:max-w-lg lg:max-w-xl")}>
        <div className={cn(
          "p-3 rounded-lg",
          isUser 
            ? "bg-primary-600 text-white ml-auto" 
            : "bg-white shadow-sm border border-gray-200"
        )}>
          <p className={cn(
            "text-sm leading-relaxed whitespace-pre-wrap",
            isUser ? "text-white" : "text-gray-800"
          )}>
            {message.content}
          </p>
        </div>

        {/* Audio player for assistant messages */}
        {!isUser && message.audioUrl && (
          <div className="mt-2">
            <AudioPlayer
              audioUrl={message.audioUrl}
              text={message.content}
              autoPlay={true}
              onPlayStart={onAudioPlayStart}
              onPlayEnd={onAudioPlayEnd}
            />
          </div>
        )}

        {/* Timestamp */}
        <div className={cn(
          "text-xs text-gray-500 mt-1",
          isUser ? "text-right" : "text-left"
        )}>
          {formatTime(Math.floor((Date.now() - message.timestamp.getTime()) / 1000))} ago
        </div>
      </div>
    </div>
  );
};

interface ChatHistoryProps {
  messages: ChatMessage[];
  isLoading?: boolean;
  onAudioPlayStart?: () => void;
  onAudioPlayEnd?: () => void;
  className?: string;
}

export const ChatHistory: React.FC<ChatHistoryProps> = ({
  messages,
  isLoading = false,
  onAudioPlayStart,
  onAudioPlayEnd,
  className
}) => {
  return (
    <div className={cn("flex-1 overflow-y-auto p-4 space-y-4", className)}>
      {messages.length === 0 ? (
        <div className="text-center py-12">
          <Bot className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-600 mb-2">
            Welcome to AI Voice Assistant
          </h3>
          <p className="text-gray-500 max-w-md mx-auto">
            Start a conversation by speaking or typing a message. I can understand both audio and text inputs.
          </p>
        </div>
      ) : (
        <>
          {messages.map((message) => (
            <ChatMessageComponent
              key={message.id}
              message={message}
              onAudioPlayStart={onAudioPlayStart}
              onAudioPlayEnd={onAudioPlayEnd}
            />
          ))}
          
          {isLoading && (
            <div className="flex gap-3 mb-6">
              <div className="flex-shrink-0 w-8 h-8 rounded-full bg-accent-600 flex items-center justify-center">
                <Bot className="w-4 h-4 text-white" />
              </div>
              <div className="flex-1 max-w-xs sm:max-w-md">
                <div className="p-3 rounded-lg bg-white shadow-sm border border-gray-200">
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                  </div>
                </div>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
};
