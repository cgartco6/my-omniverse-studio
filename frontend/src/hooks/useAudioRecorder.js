import { useState, useRef } from 'react';

export function useAudioRecorder() {
  const [isRecording, setIsRecording] = useState(false);
  const [audioBlob, setAudioBlob] = useState(null);
  const mediaRecorderInstanceRef = useRef(null);
  const trackedAudioChunksRef = useRef([]);

  const startRecording = async () => {
    trackedAudioChunksRef.current = [];
    try {
      const liveHardwareStream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderInstanceRef.current = new MediaRecorder(liveHardwareStream);
      
      mediaRecorderInstanceRef.current.ondataavailable = (event) => {
        if (event.data && event.data.size > 0) {
          trackedAudioChunksRef.current.push(event.data);
        }
      };

      mediaRecorderInstanceRef.current.onstop = () => {
        const structuralWavBlob = new Blob(trackedAudioChunksRef.current, { type: 'audio/wav' });
        setAudioBlob(structuralWavBlob);
      };

      mediaRecorderInstanceRef.current.start(200);
      setIsRecording(true);
    } catch (hardwareConfigurationError) {
      alert("Hardware Device Capture Failed: Physical Microphones not reachable.");
    }
  };

  const stopRecording = () => {
    if (mediaRecorderInstanceRef.current && isRecording) {
      mediaRecorderInstanceRef.current.stop();
      mediaRecorderInstanceRef.current.stream.getTracks().forEach(track => track.stop());
      setIsRecording(false);
    }
  };

  return { isRecording, audioBlob, startRecording, stopRecording };
}
