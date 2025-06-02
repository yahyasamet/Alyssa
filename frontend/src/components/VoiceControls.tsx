import React, { useState, useRef, useEffect } from 'react';
import { Mic, MicOff, Square, Play, Pause } from 'lucide-react';
import { cn } from '../utils';
import { VoiceVisualizer } from './VoiceVisualizer';
import { useAudioRecorder } from '../hooks/useAudioRecorder';

interface VoiceControlsProps {
  onAudioRecorded: (audio: Blob) => void;
  isProcessing: boolean;
  className?: string;
}

export const VoiceControls: React.FC<VoiceControlsProps> = ({
  onAudioRecorded,
  isProcessing,
  className
}) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const audioRef = useRef<HTMLAudioElement>(null);
  
  const {
    isRecording,
    audioLevel,
    startRecording,
    stopRecording,
    recordedAudio,
    isSupported,
    error
  } = useAudioRecorder();

  // Debug logging
  useEffect(() => {
    console.log('VoiceControls - isSupported:', isSupported);
    console.log('VoiceControls - error:', error);
    console.log('VoiceControls - isRecording:', isRecording);
  }, [isSupported, error, isRecording]);

  const handleRecordToggle = async () => {
    console.log('handleRecordToggle called - isRecording:', isRecording);
    
    if (isRecording) {
      console.log('Stopping recording...');
      const audio = await stopRecording();
      console.log('Recording stopped, audio blob:', audio);
      if (audio) {
        onAudioRecorded(audio);
      }
    } else {
      console.log('Starting recording...');
      await startRecording();
    }
  };

  const handlePlayRecorded = () => {
    if (recordedAudio && audioRef.current) {
      if (isPlaying) {
        audioRef.current.pause();
        setIsPlaying(false);
      } else {
        const audioUrl = URL.createObjectURL(recordedAudio);
        audioRef.current.src = audioUrl;
        audioRef.current.play();
        setIsPlaying(true);
      }
    }
  };

  useEffect(() => {
    const audio = audioRef.current;
    if (audio) {
      const handleEnded = () => setIsPlaying(false);
      audio.addEventListener('ended', handleEnded);
      return () => audio.removeEventListener('ended', handleEnded);
    }
  }, []);

  if (!isSupported) {
    return (
      <div className={cn("text-center p-4", className)}>
        <p className="text-red-500">Audio recording is not supported in this browser</p>
      </div>
    );
  }
  if (error) {
    return (
      <div className={cn("text-center p-4", className)}>
        <p className="text-red-500 mb-2">{error}</p>
        {error.includes('permission') && (
          <p className="text-sm text-gray-600 mb-3">
            Please allow microphone access in your browser settings and refresh the page.
          </p>
        )}
        <button 
          onClick={() => window.location.reload()}
          className="mt-2 px-4 py-2 bg-primary-600 text-white rounded-lg text-sm hover:bg-primary-700"
        >
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className={cn("flex flex-col items-center space-y-4", className)}>
      {/* Main Record Button */}
      <div className="relative">
        <button
          onClick={handleRecordToggle}
          disabled={isProcessing}
          className={cn(
            "relative w-20 h-20 rounded-full flex items-center justify-center transition-all duration-300 shadow-lg",
            isRecording
              ? "bg-red-500 hover:bg-red-600 animate-pulse"
              : "bg-primary-600 hover:bg-primary-700",
            isProcessing && "opacity-50 cursor-not-allowed"
          )}
        >
          {isRecording ? (
            <Square className="w-8 h-8 text-white" />
          ) : (
            <Mic className="w-8 h-8 text-white" />
          )}
          
          {/* Recording indicator ring */}
          {isRecording && (
            <div className="absolute inset-0 rounded-full border-4 border-red-300 animate-ping" />
          )}
        </button>
        
        {/* Voice visualizer */}
        {isRecording && (
          <div className="absolute -bottom-12 left-1/2 transform -translate-x-1/2">
            <VoiceVisualizer isActive={isRecording} audioLevel={audioLevel} />
          </div>
        )}
      </div>

      {/* Status text */}
      <div className="text-center">
        {isProcessing ? (
          <p className="text-sm text-gray-600">Processing...</p>
        ) : isRecording ? (
          <p className="text-sm text-red-600 font-medium">Recording... Click to stop</p>
        ) : (
          <p className="text-sm text-gray-600">Click to start recording</p>
        )}
      </div>

      {/* Playback controls for recorded audio */}
      {recordedAudio && !isRecording && (
        <div className="flex items-center space-x-2">
          <button
            onClick={handlePlayRecorded}
            className="btn-secondary text-sm flex items-center space-x-1"
          >
            {isPlaying ? (
              <>
                <Pause className="w-4 h-4" />
                <span>Pause</span>
              </>
            ) : (
              <>
                <Play className="w-4 h-4" />
                <span>Play Recording</span>
              </>
            )}
          </button>
        </div>
      )}

      {/* Hidden audio element for playback */}
      <audio ref={audioRef} className="hidden" />
    </div>
  );
};
