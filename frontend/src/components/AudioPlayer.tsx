import React, { useState, useRef, useEffect } from 'react';
import { Volume2, VolumeX, Download, Loader } from 'lucide-react';
import { cn } from '../utils';

interface AudioPlayerProps {
  audioUrl?: string;
  text: string;
  isLoading?: boolean;
  autoPlay?: boolean;
  onPlayStart?: (audioElement: HTMLAudioElement) => void; // Modified
  onPlayEnd?: () => void;
  className?: string;
}

export const AudioPlayer: React.FC<AudioPlayerProps> = ({
  audioUrl,
  text,
  isLoading = false,
  autoPlay = false,
  onPlayStart,
  onPlayEnd,
  className
}) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [volume, setVolume] = useState(1);
  const [isMuted, setIsMuted] = useState(false);
  const audioRef = useRef<HTMLAudioElement>(null);

  useEffect(() => {
    const audio = audioRef.current;
    if (!audio) return;

    const handlePlay = () => {
      setIsPlaying(true);
      if (audioRef.current) {
        onPlayStart?.(audioRef.current);
      }
    };

    const handlePause = () => {
      setIsPlaying(false);
    };

    const handleEnded = () => {
      setIsPlaying(false);
      onPlayEnd?.();
    };

    const handleError = (e: any) => {
      console.error('Audio playback error:', e);
      setIsPlaying(false);
      onPlayEnd?.();
    };

    audio.addEventListener('play', handlePlay);
    audio.addEventListener('pause', handlePause);
    audio.addEventListener('ended', handleEnded);
    audio.addEventListener('error', handleError);

    return () => {
      audio.removeEventListener('play', handlePlay);
      audio.removeEventListener('pause', handlePause);
      audio.removeEventListener('ended', handleEnded);
      audio.removeEventListener('error', handleError);
    };
  }, [onPlayStart, onPlayEnd]);

  useEffect(() => {
    if (audioUrl && autoPlay && audioRef.current) {
      audioRef.current.play().catch(console.error);
    }
  }, [audioUrl, autoPlay]);

  useEffect(() => {
    if (audioRef.current) {
      audioRef.current.volume = isMuted ? 0 : volume;
    }
  }, [volume, isMuted]);

  const handlePlayPause = () => {
    if (!audioRef.current || !audioUrl) return;

    if (isPlaying) {
      audioRef.current.pause();
    } else {
      audioRef.current.play().catch(console.error);
    }
  };

  const handleVolumeToggle = () => {
    setIsMuted(!isMuted);
  };

  const handleDownload = () => {
    if (!audioUrl) return;
    
    const link = document.createElement('a');
    link.href = audioUrl;
    link.download = `ai-voice-${Date.now()}.mp3`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  if (isLoading) {
    return (
      <div className={cn("flex items-center space-x-2 p-3 card", className)}>
        <Loader className="w-5 h-5 animate-spin text-primary-600" />
        <span className="text-sm text-gray-600">Generating speech...</span>
      </div>
    );
  }

  if (!audioUrl) {
    return null;
  }

  return (
    <div className={cn("p-4 card", className)}>
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-3">
          {/* Play/Pause Button */}
          <button
            onClick={handlePlayPause}
            className={cn(
              "w-10 h-10 rounded-full flex items-center justify-center transition-colors",
              isPlaying
                ? "bg-red-500 hover:bg-red-600 text-white"
                : "bg-primary-600 hover:bg-primary-700 text-white"
            )}
          >
            {isPlaying ? (
              <div className="w-3 h-3 bg-white rounded-sm" />
            ) : (
              <div 
                className="w-0 h-0 ml-1"
                style={{
                  borderLeft: '6px solid white',
                  borderTop: '4px solid transparent',
                  borderBottom: '4px solid transparent'
                }}
              />
            )}
          </button>

          {/* Text preview */}
          <div className="flex-1 min-w-0">
            <p className="text-sm text-gray-700 truncate max-w-xs">
              {text}
            </p>
          </div>
        </div>

        <div className="flex items-center space-x-2">
          {/* Volume Control */}
          <button
            onClick={handleVolumeToggle}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            {isMuted ? (
              <VolumeX className="w-4 h-4 text-gray-500" />
            ) : (
              <Volume2 className="w-4 h-4 text-gray-500" />
            )}
          </button>

          {/* Download Button */}
          <button
            onClick={handleDownload}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
            title="Download audio"
          >
            <Download className="w-4 h-4 text-gray-500" />
          </button>
        </div>
      </div>

      {/* Volume Slider */}
      {!isMuted && (
        <div className="mt-3">
          <input
            type="range"
            min="0"
            max="1"
            step="0.1"
            value={volume}
            onChange={(e) => setVolume(parseFloat(e.target.value))}
            className="w-full h-1 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
          />
        </div>
      )}

      {/* Hidden audio element */}
      <audio ref={audioRef} src={audioUrl} className="hidden" />
    </div>
  );
};
