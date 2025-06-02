import { useState, useEffect, useRef, useCallback } from 'react';

export interface AudioRecorderHook {
  isRecording: boolean;
  audioLevel: number;
  startRecording: () => Promise<void>;
  stopRecording: () => Promise<Blob | null>;
  recordedAudio: Blob | null;
  isSupported: boolean;
  error: string | null;
}

export const useAudioRecorder = (): AudioRecorderHook => {
  const [isRecording, setIsRecording] = useState(false);
  const [audioLevel, setAudioLevel] = useState(0);
  const [recordedAudio, setRecordedAudio] = useState<Blob | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isSupported, setIsSupported] = useState(false);

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const audioContextRef = useRef<AudioContext | null>(null);
  const analyserRef = useRef<AnalyserNode | null>(null);
  const dataArrayRef = useRef<Uint8Array | null>(null);
  const animationFrameRef = useRef<number | null>(null);

  useEffect(() => {
    // Check if browser supports audio recording
    setIsSupported(
      typeof navigator !== 'undefined' &&
      navigator.mediaDevices &&
      typeof navigator.mediaDevices.getUserMedia === 'function' &&
      typeof MediaRecorder !== 'undefined'
    );

    // Check microphone permissions
    if (navigator.permissions) {
      navigator.permissions.query({ name: 'microphone' as any }).then((result) => {
        console.log('Microphone permission status:', result.state);
      }).catch((err) => {
        console.log('Could not check microphone permissions:', err);
      });
    }
  }, []);

  const updateAudioLevel = useCallback(() => {
    if (!analyserRef.current || !dataArrayRef.current) return;

    analyserRef.current.getByteFrequencyData(dataArrayRef.current);
    
    const average = dataArrayRef.current.reduce((a, b) => a + b) / dataArrayRef.current.length;
    const level = average / 255;
    
    setAudioLevel(level);

    if (isRecording) {
      animationFrameRef.current = requestAnimationFrame(updateAudioLevel);
    }
  }, [isRecording]);  const recordingResolverRef = useRef<((blob: Blob | null) => void) | null>(null);
  const recordingChunksRef = useRef<Blob[]>([]);

  const startRecording = useCallback(async () => {
    console.log('startRecording called - isSupported:', isSupported);
    
    if (!isSupported) {
      const errorMsg = 'Audio recording is not supported in this browser';
      console.error(errorMsg);
      setError(errorMsg);
      return;
    }

    try {
      setError(null);
      console.log('Requesting microphone access...');
      
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true,
        }
      });

      console.log('Microphone access granted, stream:', stream);
      streamRef.current = stream;

      // Set up audio analysis for volume visualization
      audioContextRef.current = new (window.AudioContext || (window as any).webkitAudioContext)();
      analyserRef.current = audioContextRef.current.createAnalyser();
      const source = audioContextRef.current.createMediaStreamSource(stream);
      source.connect(analyserRef.current);

      analyserRef.current.fftSize = 256;
      const bufferLength = analyserRef.current.frequencyBinCount;
      dataArrayRef.current = new Uint8Array(bufferLength);

      // Set up MediaRecorder
      const mimeType = getSupportedMimeType();
      console.log('Using MIME type:', mimeType);
      mediaRecorderRef.current = new MediaRecorder(stream, { mimeType });

      // Reset chunks array
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
        setRecordedAudio(blob);
        setIsRecording(false);
        setAudioLevel(0);
        
        // Resolve the promise if there's a resolver waiting
        if (recordingResolverRef.current) {
          console.log('Resolving stopRecording promise with blob');
          recordingResolverRef.current(blob);
          recordingResolverRef.current = null;
        }
      };

      mediaRecorderRef.current.start();
      console.log('MediaRecorder started');
      setIsRecording(true);
      
      // Start audio level monitoring
      updateAudioLevel();

    } catch (err) {
      console.error('Error starting recording:', err);
      setError('Failed to access microphone. Please check permissions.');
    }
  }, [isSupported, updateAudioLevel]);  const stopRecording = useCallback(async (): Promise<Blob | null> => {
    console.log('stopRecording called - isRecording:', isRecording, 'mediaRecorder:', !!mediaRecorderRef.current);
    
    if (!mediaRecorderRef.current || !isRecording) {
      console.log('Cannot stop recording - no recorder or not recording');
      return null;
    }

    return new Promise((resolve) => {
      // Store the resolver for when the onstop event fires
      recordingResolverRef.current = resolve;
      
      console.log('Calling mediaRecorder.stop()');
      if (mediaRecorderRef.current) {
        mediaRecorderRef.current.stop();
      }

      // Clean up
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop());
        streamRef.current = null;
      }

      if (audioContextRef.current) {
        audioContextRef.current.close();
        audioContextRef.current = null;
      }

      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
        animationFrameRef.current = null;
      }

      setIsRecording(false);
      setAudioLevel(0);
    });
  }, [isRecording]);

  // Clean up on unmount
  useEffect(() => {
    return () => {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop());
      }
      if (audioContextRef.current) {
        audioContextRef.current.close();
      }
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
    };
  }, []);

  return {
    isRecording,
    audioLevel,
    startRecording,
    stopRecording,
    recordedAudio,
    isSupported,
    error,
  };
};

function getSupportedMimeType(): string {
  const types = [
    'audio/webm;codecs=opus',
    'audio/webm',
    'audio/mp4',
    'audio/mpeg',
  ];

  for (const type of types) {
    if (MediaRecorder.isTypeSupported(type)) {
      return type;
    }
  }

  return 'audio/webm';
}
