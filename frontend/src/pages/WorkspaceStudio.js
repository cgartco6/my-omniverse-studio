import React, { useState } from 'react';
import { useAudioRecorder } from '../hooks/useAudioRecorder';
import { TrackVisualizer } from '../components/TrackVisualizer';
import { MemoryMonitor } from '../components/MemoryMonitor';

export function WorkspaceStudio() {
  const [textPrompt, setTextPrompt] = useState('Heavy industrial glitch beats with melodic synth lines');
  const [genreMix, setGenreMix] = useState('Glitchcore IDM Techno');
  const [targetBpm, setTargetBpm] = useState(132);
  const [isProcessing, setIsProcessing] = useState(false);
  const [engineResponse, setEngineResponse] = useState(null);
  
  const { isRecording, audioBlob, startRecording, stopRecording } = useAudioRecorder();

  const handlePipelineSubmission = async () => {
    setIsProcessing(true);
    const formPayload = new FormData();
    formPayload.append('text_prompt', textPrompt);
    formPayload.append('genre_mix', genreMix);
    formPayload.append('target_bpm', targetBpm);

    if (audioBlob) {
      formPayload.append('vocal_file', audioBlob, 'studio_vocal_capture.wav');
    }

    const imageElementField = document.getElementById('visualAnchorInput');
    if (imageElementField && imageElementField.files[0]) {
      formPayload.append('image_file', imageElementField.files[0]);
    }

    try {
      const response = await fetch('http://localhost:8000/api/v1/ingest-workspace', {
        method: 'POST',
        body: formPayload,
      });
      const data = await response.json();
      setEngineResponse(data);
    } catch (err) {
      console.error("Critical Execution Fault encountered in generation system network matrix:", err);
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div style={{ maxWidth: '1400px', margin: '0 auto', padding: '20px' }}>
      <header style={{ borderBottom: '2px solid #2563eb', paddingBottom: '15px', marginBottom: '25px', display: 'flex', justifyContent: 'between', alignItems: 'center' }}>
        <div>
          <h1 style={{ color: '#2563eb', margin: 0, fontSize: '24px' }}>OMNIVERSE MULTIMEDIA WORKSPACE V2.0</h1>
          <small style={{ color: '#4ade80' }}>STATUS: ROOT ACCESS AUTHENTICATED // FREE PROCESSING ENGINE RUNNING</small>
        </div>
      </header>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '35px' }}>
        <div style={{ backgroundColor: '#111827', padding: '20px', borderRadius: '8px', border: '1px solid #1f2937' }}>
          <h3 style={{ color: '#3b82f6', marginTop: 0 }}>1. CONFIGURATION LAYOUT</h3>
          
          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px', color: '#9ca3af' }}>Text Architecture Prompt</label>
            <textarea style={{ width: '96%', height: '70px', backgroundColor: '#030712', color: '#fff', border: '1px solid #374151', padding: '10px', borderRadius: '4px', fontFamily: 'monospace' }}
              value={textPrompt} onChange={(e) => setTextPrompt(e.target.value)} />
          </div>

          <div style={{ marginBottom: '15px' }}>
            <label style={{ display: 'block', marginBottom: '5px', color: '#9ca3af' }}>Genre Convergence Matrix</label>
            <input type="text" style={{ width: '96%', backgroundColor: '#030712', color: '#fff', border: '1px solid #374151', padding: '10px', borderRadius: '4px', fontFamily: 'monospace' }}
              value={genreMix} onChange={(e) => setGenreMix(e.target.value)} />
          </div>

          <div style={{ marginBottom: '20px' }}>
            <label style={{ display: 'block', marginBottom: '5px', color: '#9ca3af' }}>Master Clock Frequency Target: {targetBpm} BPM</label>
            <input type="range" min="60" max="220" style={{ width: '100%', cursor: 'pointer' }} value={targetBpm} onChange={(e) => setTargetBpm(Number(e.target.value))} />
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px', marginBottom: '20px' }}>
            <div style={{ border: '1px dashed #4b5563', padding: '10px', borderRadius: '4px', textAlign: 'center' }}>
              <span style={{ fontSize: '11px', display: 'block', marginBottom: '10px', color: '#9ca3af' }}>VISUAL ANCHOR (SEEDANCE ENGINE MODALITY)</span>
              <input type="file" id="visualAnchorInput" accept="image/*" style={{ fontSize: '11px', color: '#9ca3af' }} />
            </div>

            <div style={{ border: '1px dashed #4b5563', padding: '10px', borderRadius: '4px', textAlign: 'center' }}>
              <span style={{ fontSize: '11px', display: 'block', marginBottom: '10px', color: '#9ca3af' }}>VOCAL CAPTURE LOOP ENGINE</span>
              <button onClick={isRecording ? stopRecording : startRecording} style={{ padding: '6px 12px', backgroundColor: isRecording ? '#dc2626' : '#2563eb', color: '#fff', border: 'none', cursor: 'pointer', fontWeight: 'bold', fontSize: '11px', borderRadius: '2px' }}>
                {isRecording ? "■ DISENGAGE CAPTURE" : "● ENGAGE HARDWARE MIC"}
              </button>
              {audioBlob && <small style={{ color: '#4ade80', display: 'block', marginTop: '5px' }}>✓ RAM Stream Ready</small>}
            </div>
          </div>

          <button onClick={handlePipelineSubmission} disabled={isProcessing} style={{ width: '100%', padding: '12px', backgroundColor: '#2563eb', color: '#fff', fontWeight: 'bold', border: 'none', borderRadius: '4px', cursor: isProcessing ? 'not-allowed' : 'pointer', fontSize: '14px' }}>
            {isProcessing ? "PROCESSING STRUCTURAL SYNTHESIS PIPELINE..." : "TRIGGER ENGINE EXECUTION GENERATION LOOP"}
          </button>
        </div>

        <div>
          <TrackVisualizer 
            audioUrl={engineResponse?.assets?.master_audio_route} 
            videoUrl={engineResponse?.assets?.master_video_route} 
          />
          <MemoryMonitor contextArray={engineResponse?.memory_context_applied} />
        </div>
      </div>
    </div>
  );
}
