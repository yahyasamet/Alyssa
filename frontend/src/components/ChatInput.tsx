import React, { useState, useRef, useEffect } from 'react';
import { Send, Loader } from 'lucide-react';
import { cn } from '../utils';

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  isLoading: boolean;
  placeholder?: string;
  className?: string;
  dark?: boolean;
}

export const ChatInput: React.FC<ChatInputProps> = ({
  onSendMessage,
  isLoading,
  placeholder = "Type your message...",
  className,
  dark = false
}) => {
  const [message, setMessage] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (message.trim() && !isLoading) {
      onSendMessage(message.trim());
      setMessage('');
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
      }
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  }, [message]);
  return (
    <form onSubmit={handleSubmit} className={cn("", className)}>
      <div className={cn("flex items-end space-x-2 p-4", dark ? "bg-gray-900/50 border border-gray-700/30 rounded-lg" : "card")}>
        <div className="flex-1 relative">
          <textarea
            ref={textareaRef}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder={placeholder}
            disabled={isLoading}
            rows={1}
            className={cn(
              "w-full resize-none border-0 bg-transparent",
              "focus:outline-none focus:ring-0",
              "min-h-[40px] max-h-[120px] py-2 px-0",
              dark 
                ? "placeholder-gray-400 text-gray-100" 
                : "placeholder-gray-500 text-gray-900",
              isLoading && "opacity-50 cursor-not-allowed"
            )}
            style={{ lineHeight: '1.5' }}
          />
        </div>
        
        <button
          type="submit"
          disabled={!message.trim() || isLoading}
          className={cn(
            "flex items-center justify-center w-10 h-10 rounded-lg transition-all duration-200",
            "focus:outline-none focus:ring-2 focus:ring-offset-2",
            dark ? "focus:ring-blue-500" : "focus:ring-primary-500",
            message.trim() && !isLoading
              ? dark
                ? "bg-blue-600 hover:bg-blue-700 text-white"
                : "bg-primary-600 hover:bg-primary-700 text-white"
              : dark
                ? "bg-gray-700 text-gray-500 cursor-not-allowed"
                : "bg-gray-200 text-gray-400 cursor-not-allowed"
          )}
        >
          {isLoading ? (
            <Loader className="w-5 h-5 animate-spin" />
          ) : (
            <Send className="w-5 h-5" />
          )}
        </button>
      </div>
    </form>
  );
};
