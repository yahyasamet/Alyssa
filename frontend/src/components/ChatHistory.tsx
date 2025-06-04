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
  onAudioPlayStart?: (audioElement: HTMLAudioElement) => void; // Modified
  onAudioPlayEnd?: () => void;
  className?: string;
  dark?: boolean; // Add dark mode prop
}

export const ChatMessageComponent: React.FC<ChatMessageProps> = ({
  message,
  onAudioPlayStart,
  onAudioPlayEnd,
  className,
  dark = false // Default to light mode
}) => {
  const isUser = message.type === 'user';

  return (
    <div className={cn("flex gap-3 mb-6", isUser && "flex-row-reverse", className)}>      {/* Avatar */}
      <div className={cn(
        "flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center",
        isUser 
          ? dark ? "bg-blue-600" : "bg-primary-600"
          : dark ? "bg-purple-600" : "bg-accent-600"
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
      <div className={cn("flex-1 max-w-xs sm:max-w-md md:max-w-lg lg:max-w-xl")}>        <div className={cn(
          "p-3 rounded-lg",
          isUser 
            ? dark 
              ? "bg-blue-600 text-white ml-auto" 
              : "bg-primary-600 text-white ml-auto"
            : dark
              ? "bg-gray-800/50 border border-gray-700/30 text-white" 
              : "bg-white shadow-sm border border-gray-200"
        )}>          <p className={cn(
            "text-sm leading-relaxed whitespace-pre-wrap",
            isUser 
              ? "text-white" 
              : dark 
                ? "text-gray-100" 
                : "text-gray-800"
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
              onPlayStart={(audioEl) => onAudioPlayStart && onAudioPlayStart(audioEl as HTMLAudioElement)} // Modified to pass audio element
              onPlayEnd={onAudioPlayEnd}
            />
          </div>
        )}        {/* Timestamp */}
        <div className={cn(
          "text-xs mt-1",
          isUser ? "text-right" : "text-left",
          dark ? "text-gray-400" : "text-gray-500"
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
  onAudioPlayStart?: (audioElement: HTMLAudioElement) => void; // Modified
  onAudioPlayEnd?: () => void;
  className?: string;
  dark?: boolean; // Add dark mode prop
}

export const ChatHistory: React.FC<ChatHistoryProps> = ({
  messages,
  isLoading = false,
  onAudioPlayStart,
  onAudioPlayEnd,
  className,
  dark = false
}) => {  return (
    <div className={cn("flex-1 overflow-y-auto p-4 space-y-4", className)}>
      {messages.length === 0 ? (
        <div className="text-center py-12">
          <Bot className={cn("w-16 h-16 mx-auto mb-4", dark ? "text-gray-500" : "text-gray-400")} />
          <h3 className={cn("text-lg font-medium mb-2", dark ? "text-gray-200" : "text-gray-600")}>
            Welcome to AI Voice Assistant
          </h3>
          <p className={cn("max-w-md mx-auto", dark ? "text-gray-400" : "text-gray-500")}>
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
              dark={dark}
            />
          ))}
          
          {isLoading && (
            <div className="flex gap-3 mb-6">
              <div className={cn(
                "flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center",
                dark ? "bg-purple-600" : "bg-accent-600"
              )}>
                <Bot className="w-4 h-4 text-white" />
              </div>
              <div className="flex-1 max-w-xs sm:max-w-md">
                <div className={cn(
                  "p-3 rounded-lg",
                  dark 
                    ? "bg-gray-800/50 border border-gray-700/30" 
                    : "bg-white shadow-sm border border-gray-200"
                )}>
                  <div className="flex space-x-1">
                    <div className={cn("w-2 h-2 rounded-full animate-bounce", dark ? "bg-gray-500" : "bg-gray-400")} style={{ animationDelay: '0ms' }} />
                    <div className={cn("w-2 h-2 rounded-full animate-bounce", dark ? "bg-gray-500" : "bg-gray-400")} style={{ animationDelay: '150ms' }} />
                    <div className={cn("w-2 h-2 rounded-full animate-bounce", dark ? "bg-gray-500" : "bg-gray-400")} style={{ animationDelay: '300ms' }} />
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
