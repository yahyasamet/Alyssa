import { useState, useEffect, useRef, useCallback } from 'react';
import { MicVAD } from '@ricky0123/vad-web';

export interface AudioRecorderHook {
  isRecording: boolean; // True when MediaRecorder is actively saving chunks
  audioLevel: number;
  // startRecording: () => Promise<void>; // Kept for compatibility, maps to activateVoiceDetection
  // stopRecording: () => Promise<Blob | null>;  // Kept for compatibility, maps to deactivateVoiceDetection
  recordedAudio: Blob | null; // Stores the last recorded blob
  isSupported: boolean;
  error: string | null;
  isSpeaking: boolean;     // True when VAD detects speech
  isVadActive: boolean;    // True when VAD is initialized and listening/paused
  activateVoiceDetection: () => Promise<void>;
  deactivateVoiceDetection: () => Promise<Blob | null>; // Stops VAD and any recording, returns final blob
}

export interface UseAudioRecorderOptions {
  onSpeechSegmentRecorded?: (blob: Blob) => void;
  onVadSpeechStart?: () => void; // New callback for when VAD detects speech start
  // Future VAD tuning options can go here
  // e.g., vadPositiveSpeechThreshold?: number;
}

export const useAudioRecorder = (options?: UseAudioRecorderOptions): AudioRecorderHook => {
  const [isRecording, setIsRecording] = useState(false); 
  const [isVadActiveInternal, setIsVadActiveInternal] = useState(false); // Internal state for VAD's activity
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [audioLevel, setAudioLevel] = useState(0);
  const [recordedAudio, setRecordedAudio] = useState<Blob | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isSupported, setIsSupported] = useState(false);

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioContextRef = useRef<AudioContext | null>(null);
  const analyserRef = useRef<AnalyserNode | null>(null);
  const dataArrayRef = useRef<Uint8Array | null>(null);
  const animationFrameRef = useRef<number | null>(null);
  const vadRef = useRef<MicVAD | null>(null);
  const recordingChunksRef = useRef<Blob[]>([]);
  const recordingResolverRef = useRef<((blob: Blob | null) => void) | null>(null);
  const currentStreamRef = useRef<MediaStream | null>(null); // To hold the stream for VAD and MediaRecorder


  useEffect(() => {
    setIsSupported(
      typeof navigator !== 'undefined' &&
      navigator.mediaDevices &&
      typeof navigator.mediaDevices.getUserMedia === 'function' &&
      typeof MediaRecorder !== 'undefined' &&
      typeof MicVAD !== 'undefined'
    );

    if (navigator.permissions) {
      navigator.permissions.query({ name: 'microphone' as any }).then((result) => {
        console.log('Microphone permission status:', result.state);
      }).catch((err) => {
        console.log('Could not check microphone permissions:', err);
      });
    }
    
    return () => {
      vadRef.current?.destroy();
      if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
        mediaRecorderRef.current.stop();
      }
      currentStreamRef.current?.getTracks().forEach(track => track.stop());
      audioContextRef.current?.close();
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
    };
  }, []);

  const updateAudioLevel = useCallback(() => {
    if (!analyserRef.current || !dataArrayRef.current || !isRecording) return;

    analyserRef.current.getByteFrequencyData(dataArrayRef.current);
    const average = dataArrayRef.current.reduce((a, b) => a + b) / dataArrayRef.current.length;
    const level = average / 255;
    setAudioLevel(level);

    animationFrameRef.current = requestAnimationFrame(updateAudioLevel);
  }, [isRecording]);

  const internalStartMediaRecorder = useCallback(async (streamToUse: MediaStream) => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
      console.log('MediaRecorder already recording');
      return;
    }
    console.log('internalStartMediaRecorder called');
    try {
      if (!audioContextRef.current || audioContextRef.current.state === 'closed') {
        audioContextRef.current = new (window.AudioContext || (window as any).webkitAudioContext)();
      }
      // Re-create analyser if it doesn't exist or if the stream source needs to be reconnected.
      // For simplicity, creating a new analyser node each time internalStartMediaRecorder is called with a new stream context.
      if (analyserRef.current && audioContextRef.current.destination !== analyserRef.current.context.destination) {
        analyserRef.current.disconnect();
        analyserRef.current = null; // Force re-creation if context changed (should not happen often)
      }
      if (!analyserRef.current) { 
        analyserRef.current = audioContextRef.current.createAnalyser();
      }
      
      const source = audioContextRef.current.createMediaStreamSource(streamToUse);
      // Ensure source is connected to analyser. If source is new, it needs connection.
      // If source is old but analyser is new, it also needs connection.
      // A simple approach is to always try to connect, but this might lead to multiple connections if not managed.
      // A safer way: disconnect previous source if it exists and is different.
      // For now, assuming streamToUse is a fresh stream or source needs re-establishing.
      source.connect(analyserRef.current); 
      analyserRef.current.fftSize = 256;
      const bufferLength = analyserRef.current.frequencyBinCount;
      dataArrayRef.current = new Uint8Array(bufferLength);

      const mimeType = getSupportedMimeType();
      mediaRecorderRef.current = new MediaRecorder(streamToUse, { mimeType });
      recordingChunksRef.current = [];

      mediaRecorderRef.current.ondataavailable = (event) => {
        console.log('MediaRecorder data available:', event.data.size, 'bytes');
        if (event.data.size > 0) {
          recordingChunksRef.current.push(event.data);
        }
      };

      mediaRecorderRef.current.onstop = () => {
        console.log('MediaRecorder stopped, creating blob from chunks:', recordingChunksRef.current.length);
        const blob = new Blob(recordingChunksRef.current, { type: mimeType });
        console.log('Created blob:', blob.size, 'bytes');
        setRecordedAudio(blob); // This state holds the latest complete blob
        setIsRecording(false);
        setAudioLevel(0);
        if (animationFrameRef.current) {
          cancelAnimationFrame(animationFrameRef.current);
        }
        
        if (recordingResolverRef.current) {
          console.log('Resolving stopRecording promise with blob from onstop');
          recordingResolverRef.current(blob);
          recordingResolverRef.current = null;
        }
        // The onSpeechSegmentRecorded callback is now handled in onSpeechEnd
      };

      mediaRecorderRef.current.start();
      console.log('MediaRecorder started');
      setIsRecording(true);
      updateAudioLevel();
    } catch (err) {
      console.error('Error starting MediaRecorder:', err);
      setError('Failed to start recording. Please check microphone.');
      setIsRecording(false); 
    }
  }, [updateAudioLevel]);

  const internalStopMediaRecorder = useCallback(async (): Promise<Blob | null> => {
    console.log('internalStopMediaRecorder called - MediaRecorder state:', mediaRecorderRef.current?.state);
    if (!mediaRecorderRef.current || mediaRecorderRef.current.state === 'inactive') {
      console.log('Cannot stop MediaRecorder - no recorder or already inactive');
      if (recordingResolverRef.current) {
        console.log('No active MediaRecorder, resolving with null');
        recordingResolverRef.current(null); 
        recordingResolverRef.current = null;
      }
      // If there's a previously recorded audio blob (e.g. from a segment), return that.
      // However, the primary mechanism for segment delivery is onSpeechSegmentRecorded.
      // This direct return is more for when stop is called explicitly.
      return recordedAudio; 
    }

    return new Promise((resolve) => {
      recordingResolverRef.current = resolve;
      mediaRecorderRef.current?.stop(); // onstop will handle setRecordedAudio and resolving
    });
  }, [isRecording, recordedAudio]);


  const activateVoiceDetection = useCallback(async () => {
    console.log('activateVoiceDetection called - isSupported:', isSupported, 'isVadActiveInternal:', isVadActiveInternal);
    if (!isSupported) {
      const errorMsg = 'Audio recording or VAD is not supported in this browser';
      console.error(errorMsg);
      setError(errorMsg);
      return;
    }
   
    if (vadRef.current && isVadActiveInternal) {
      console.log('VAD already active and listening.');
      // If VAD is paused, vadRef.current.start() would resume.
      // For simplicity, if it's active, we assume it's working.
      // To handle paused state explicitly, we'd need to track it.
      try {
        vadRef.current.start(); // Ensure it's listening
        console.log('VAD confirmed listening');
      } catch (e) {
        console.warn('Error trying to ensure VAD is listening, might need re-init:', e)
      }
      return;
    }
    
    // Clean up any existing VAD or stream before creating a new one
    if (vadRef.current) {
        vadRef.current.destroy();
        vadRef.current = null;
    }
    if (currentStreamRef.current) {
        currentStreamRef.current.getTracks().forEach(track => track.stop());
        currentStreamRef.current = null;
    }


    try {
      setError(null);
      setRecordedAudio(null); 
      console.log('Initializing VAD...');
      
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true,
        }
      });
      currentStreamRef.current = stream; // Store the stream

      vadRef.current = await MicVAD.new({
        stream: currentStreamRef.current,
        redemptionFrames: 20, // Use redemptionFrames to allow more silence (adjust value as needed)
        onSpeechStart: () => {
          console.log('VAD: Speech started');
          setIsSpeaking(true);
          options?.onVadSpeechStart?.(); // Call the new callback
          if (!isRecording) { 
            internalStartMediaRecorder(currentStreamRef.current!); 
          }
        },
        onSpeechEnd: (_unusedAudioParameter) => { 
          console.log('VAD: Speech ended');
          setIsSpeaking(false);
          // Important: internalStopMediaRecorder returns a promise.
          // We need to await it or handle its .then() to get the blob.
          internalStopMediaRecorder().then(blob => {
            console.log('Speech ended, MediaRecorder stopped. Blob size:', blob?.size);
            if (blob && options?.onSpeechSegmentRecorded) {
              console.log('Calling onSpeechSegmentRecorded');
              options.onSpeechSegmentRecorded(blob);
            }
            // setRecordedAudio(blob) is already called within onstop of MediaRecorder
          }).catch(error => {
            console.error("Error stopping media recorder after speech end:", error);
          });
        },
        onVADMisfire: () => {
          console.log("VAD: misfire");
        },
      });
      
      vadRef.current.start();
      setIsVadActiveInternal(true);
      console.log('VAD activated and listening');

    } catch (err) {
      console.error('Error activating VAD:', err);
      let message = 'Failed to access microphone or initialize VAD. Please check permissions.';
      if (err instanceof Error) {
        message += ` Details: ${err.message}`;
      }
      setError(message);
      setIsVadActiveInternal(false);
      setIsSpeaking(false);
      if (currentStreamRef.current) {
        currentStreamRef.current.getTracks().forEach(track => track.stop());
        currentStreamRef.current = null;
      }
    }
  }, [isSupported, isVadActiveInternal, internalStartMediaRecorder, internalStopMediaRecorder, isRecording, options]);

  const deactivateVoiceDetection = useCallback(async (): Promise<Blob | null> => {
    console.log('deactivateVoiceDetection called');
    if (vadRef.current) {
      vadRef.current.pause(); 
      console.log('VAD paused');
    }
    setIsVadActiveInternal(false); // Reflect that VAD is no longer actively listening for new speech starts
    setIsSpeaking(false); // Assume speech stops if VAD is deactivated

    let resultBlob: Blob | null = null;

    if (isRecording) {
      console.log('VAD deactivated while recording, stopping MediaRecorder.');
      resultBlob = await internalStopMediaRecorder();
    } else if (recordedAudio) {
      // If not recording, but there's a previously recorded blob (e.g., from a completed segment)
      console.log('VAD deactivated, returning existing recorded audio.');
      resultBlob = recordedAudio;
      setRecordedAudio(null); // Clear it after returning
    }
    
    // Clean up stream if VAD is fully deactivated and not just paused
    // if (!vadRef.current && currentStreamRef.current) { // Example: if destroyed
    //   currentStreamRef.current.getTracks().forEach(track => track.stop());
    //   currentStreamRef.current = null;
    // }
    console.log('VAD deactivated. Returning blob:', resultBlob?.size);
    return resultBlob;
  }, [isRecording, recordedAudio, internalStopMediaRecorder]);

  // ... remove legacy startRecording and stopRecording or map them if strict compatibility is needed
  // For now, let's assume direct usage of activate/deactivate

  useEffect(() => {
    return () => {
      console.log('Cleaning up useAudioRecorder on unmount');
      vadRef.current?.destroy(); // Ensure VAD is destroyed
      vadRef.current = null;

      if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
        mediaRecorderRef.current.stop(); 
      }
      mediaRecorderRef.current = null;

      currentStreamRef.current?.getTracks().forEach(track => track.stop());
      currentStreamRef.current = null;

      if (audioContextRef.current?.state !== 'closed') {
        audioContextRef.current?.close();
      }
      audioContextRef.current = null;

      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
      animationFrameRef.current = null;

      if (recordingResolverRef.current) {
        recordingResolverRef.current(null); // Resolve any pending promise
        recordingResolverRef.current = null;
      }
    };
  }, []);

  return {
    isRecording, 
    audioLevel,
    recordedAudio,
    isSupported,
    error,
    isSpeaking,     
    isVadActive: isVadActiveInternal, // Expose VAD active state
    activateVoiceDetection,
    deactivateVoiceDetection,
  };
};

function getSupportedMimeType(): string {
  const types = [
    'audio/webm;codecs=opus',
    'audio/webm',
    'audio/mp4', 
    'audio/ogg;codecs=opus', 
    'audio/aac', 
    'audio/mpeg', 
  ];

  for (const type of types) {
    if (MediaRecorder.isTypeSupported(type)) {
      console.log(`Supported MIME type found: ${type}`);
      return type;
    }
  }
  console.log('No specifically preferred MIME type supported, defaulting to audio/webm');
  return 'audio/webm'; 
}
