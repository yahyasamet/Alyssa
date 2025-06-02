import React from 'react';
import { cn } from '../utils';

interface VoiceVisualizerProps {
  isActive: boolean;
  audioLevel: number;
  className?: string;
}

export const VoiceVisualizer: React.FC<VoiceVisualizerProps> = ({
  isActive,
  audioLevel,
  className
}) => {
  const barCount = 5;
  const bars = Array.from({ length: barCount }, (_, i) => i);

  return (
    <div className={cn("flex items-center justify-center space-x-1", className)}>
      {bars.map((bar) => (
        <div
          key={bar}
          className={cn(
            "w-1 bg-primary-500 rounded-full transition-all duration-100",
            isActive ? "voice-wave" : "h-1"
          )}
          style={{
            height: isActive 
              ? `${Math.max(4, audioLevel * 40 + Math.random() * 10)}px`
              : '4px',
            animationDelay: `${bar * 0.1}s`
          }}
        />
      ))}
    </div>
  );
};
