import React, { useState, useRef, useEffect, useCallback } from 'react';
import { Mic, Square, Play, Pause, Loader2, AlertTriangle, Settings2 } from 'lucide-react';
import { cn } from '../utils';
import { VoiceVisualizer } from './VoiceVisualizer';
import { useAudioRecorder, type UseAudioRecorderOptions } from '../hooks/useAudioRecorder'; // Use type-only import for UseAudioRecorderOptions

interface VoiceControlsProps {
  onAudioRecorded: (audio: Blob) => void; 
  isProcessing: boolean; 
  className?: string;
  isAssistantSpeaking?: boolean;
  onInterrupt?: () => void; 
  onVadSpeechStart?: () => void; // Added new prop
  onListeningStateChange?: (isListening: boolean) => void; // New prop for listening state
}

export const VoiceControls: React.FC<VoiceControlsProps> = ({
  onAudioRecorded,
  isProcessing: appIsProcessing, // Rename to avoid conflict with internal isLoading
  className,
  isAssistantSpeaking,
  onInterrupt,
  onVadSpeechStart, // Added this line
  onListeningStateChange, // Added this line
}) => {
  const [lastRecordedBlob, setLastRecordedBlob] = useState<Blob | null>(null);
  const [isPlayingLastSegment, setIsPlayingLastSegment] = useState(false);
  const playbackAudioRef = useRef<HTMLAudioElement>(null);

  const handleSpeechSegmentRecorded = useCallback((blob: Blob) => {
    console.log('VoiceControls: Speech segment recorded', blob);
    setLastRecordedBlob(blob); 
    onAudioRecorded(blob); 
  }, [onAudioRecorded]);

  const audioRecorderOptions: UseAudioRecorderOptions = {
    onSpeechSegmentRecorded: handleSpeechSegmentRecorded,
    onVadSpeechStart, // Added this line
  };

  const {
    audioLevel,
    isSupported,
    error: recorderError,
    isSpeaking,      
    isVadActive,     
    activateVoiceDetection,
    deactivateVoiceDetection,
  } = useAudioRecorder(audioRecorderOptions);

  // isLoading now primarily reflects VAD activity or recorder errors.
  // App-level processing (appIsProcessing) is handled separately for button disabling.
  const vadIsLoading = isVadActive && !isSpeaking && !recorderError;

  // Notify parent component when listening state changes
  useEffect(() => {
    if (onListeningStateChange) {
      onListeningStateChange(isVadActive && !isAssistantSpeaking);
    }
  }, [isVadActive, isAssistantSpeaking, onListeningStateChange]);

  const handleMicButtonClick = async () => {
    if (recorderError) {
      console.error('Cannot operate, recorder error present:', recorderError);
      return;
    }

    if (isAssistantSpeaking && onInterrupt) {
      console.log('Interrupting assistant and activating VAD');
      onInterrupt();
      await activateVoiceDetection();
      return;
    }

    if (isVadActive) {
      console.log('VAD is active, deactivating...');
      const finalBlob = await deactivateVoiceDetection();
      if (finalBlob) {
        console.log('VAD deactivated, final blob recorded:', finalBlob);
        setLastRecordedBlob(finalBlob);
      }
    } else {
      console.log('VAD is not active, activating...');
      setLastRecordedBlob(null); 
      await activateVoiceDetection();
    }
  };

  // Effect to handle playback of the last recorded segment
  useEffect(() => {
    if (lastRecordedBlob && playbackAudioRef.current) {
      const audioUrl = URL.createObjectURL(lastRecordedBlob);
      playbackAudioRef.current.src = audioUrl;
      return () => URL.revokeObjectURL(audioUrl);
    }
  }, [lastRecordedBlob]);

  const handlePlayLastSegment = () => {
    if (playbackAudioRef.current) {
      if (isPlayingLastSegment) {
        playbackAudioRef.current.pause();
      } else {
        playbackAudioRef.current.play().catch(console.error);
      }
    }
  };

  useEffect(() => {
    const audioEl = playbackAudioRef.current;
    if (!audioEl) return;

    const handlePlay = () => setIsPlayingLastSegment(true);
    const handlePauseOrEnd = () => setIsPlayingLastSegment(false);

    audioEl.addEventListener('play', handlePlay);
    audioEl.addEventListener('playing', handlePlay); // Some browsers might need this
    audioEl.addEventListener('pause', handlePauseOrEnd);
    audioEl.addEventListener('ended', handlePauseOrEnd);

    return () => {
      audioEl.removeEventListener('play', handlePlay);
      audioEl.removeEventListener('playing', handlePlay);
      audioEl.removeEventListener('pause', handlePauseOrEnd);
      audioEl.removeEventListener('ended', handlePauseOrEnd);
    };
  }, []);


  if (!isSupported) {
    return (
      <div className={cn("text-center p-4 text-red-500 flex flex-col items-center space-y-2", className)}>
        <AlertTriangle className="w-10 h-10" />
        <p>Audio recording/VAD is not supported in this browser.</p>
      </div>
    );
  }

  let buttonIcon;
  let buttonClass;
  let statusText;

  if (recorderError) {
    buttonIcon = <AlertTriangle className="w-8 h-8 text-white" />;
    buttonClass = "bg-red-500 hover:bg-red-600";
    statusText = <p className="text-xs text-red-500 truncate w-full px-2">Error: {recorderError}</p>;
  } else if (isAssistantSpeaking) {
    buttonIcon = <Settings2 className="w-8 h-8 text-white animate-spin" /> 
    buttonClass = "bg-yellow-500 hover:bg-yellow-600";
    statusText = <p className="text-sm text-yellow-700 font-medium">Assistant speaking. Speak to interrupt.</p>; // Changed text
  } else if (isVadActive && isSpeaking) {
    buttonIcon = <Square className="w-8 h-8 text-white" />;
    buttonClass = "bg-red-500 hover:bg-red-600 animate-pulse";
    statusText = <p className="text-sm text-red-600 font-medium">Listening... Speaking detected</p>;
  } else if (vadIsLoading) { // Use vadIsLoading here
    buttonIcon = <Loader2 className="w-8 h-8 text-white animate-spin" />;
    buttonClass = "bg-blue-500 hover:bg-blue-600";
    statusText = <p className="text-sm text-blue-700 font-medium">Listening for voice...</p>;
  } else { // VAD is not active
    buttonIcon = <Mic className="w-8 h-8 text-white" />;
    buttonClass = "bg-primary-600 hover:bg-primary-700";
    statusText = <p className="text-sm text-gray-600">Click to start speaking</p>;
  }
  
  const mainButtonDisabled = appIsProcessing; // Button disabled if app is processing (e.g. API call)

  return (
    <div className={cn("flex flex-col items-center space-y-3", className)}>
      {/* Main VAD Control Button */}
      <div className="relative">
        <button
          onClick={handleMicButtonClick}
          disabled={mainButtonDisabled && !isAssistantSpeaking} // Allow interrupt even if processing
          className={cn(
            "relative w-20 h-20 rounded-full flex items-center justify-center transition-all duration-300 shadow-lg",
            buttonClass,
            mainButtonDisabled && !isAssistantSpeaking && "opacity-60 cursor-not-allowed"
          )}
        >
          {buttonIcon}
          {(isVadActive && isSpeaking) && (
            <div className="absolute inset-0 rounded-full border-4 border-red-300 animate-ping" />
          )}
        </button>
        
        {(isVadActive || isSpeaking) && (
          <div className="absolute -bottom-10 left-1/2 transform -translate-x-1/2">
            <VoiceVisualizer isActive={isSpeaking || isVadActive} audioLevel={audioLevel} />
          </div>
        )}
      </div>

      {/* Status text */}
      <div className="text-center h-5 mt-1">
        {statusText}
      </div>

      {/* Playback for last recorded segment (optional) */}
      {lastRecordedBlob && !isVadActive && !isSpeaking && (
        <div className="flex items-center space-x-2 mt-3 p-2 border rounded-md bg-gray-50 shadow-sm">
          <button
            onClick={handlePlayLastSegment}
            disabled={appIsProcessing} // Disable if app is busy
            className="btn-secondary text-sm flex items-center space-x-1 p-2"
          >
            {isPlayingLastSegment ? (
              <><Pause className="w-4 h-4" /><span>Pause</span></>
            ) : (
              <><Play className="w-4 h-4" /><span>Play Last</span></>
            )}
          </button>
          <p className="text-xs text-gray-500">({(lastRecordedBlob.size / 1024).toFixed(1)} KB)</p>
        </div>
      )}
      <audio ref={playbackAudioRef} className="hidden" />
    </div>
  );
};
