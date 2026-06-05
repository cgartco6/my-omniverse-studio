import React, { useState, useRef } from 'react';

export default function App() {
  const [prompt, setPrompt] = useState('Cyberpunk synth lines with deep rhythmic drive');
  const [genres, setGenres] = useState('Synthwave Industrial');
  const [bpm, setBpm] = useState(124);
  const [recording, setRecording] = useState(false);
  const [audioBlob, setAudioBlob] = useState(null);
  const [processing, setProcessing] = useState(false);
  const [outputData, setOutputData] = useState(null);
  
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  // Hardware capture layer using browser APIs
  const toggleRecording = async () => {
    if (recording) {
      mediaRecorderRef.current.stop();
      setRecording(false);
    } else {
      audioChunksRef.current = [];
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorderRef.current = new MediaRecorder(stream);
        mediaRecorderRef.current.ondataavailable = (event) => {
          if (event.data.size > 0) audioChunksRef.current.push(event.data);
        };
        mediaRecorderRef.current.onstop = () => {
          const finishedBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
          setAudioBlob(finishedBlob);
        };
        mediaRecorderRef.current.start();
        setRecording(true);
      } catch (err) {
        alert("Hardware Ingestion Refused: Check your physical microphone connectivity profiles.");
      }
    }
  };

  const executeStudioEngine = async () => {
    setProcessing(true);
    const payload = new FormData();
    payload.append('text_prompt', prompt);
    payload.append('genre_mix', genres);
    payload.append('target_bpm', bpm);
    
    if (audioBlob) {
      payload.append('vocal_file', audioBlob, 'studio_vocal_capture.wav');
    }

    try {
      const response = await fetch('http://localhost:8000/api/v1/ingest-workspace', {
        method: 'POST',
        body: payload
      });
      const data = await response.json();
      setOutputData(data);
    } catch (error) {
      console.error("Pipeline failure:", error);
    } finally {
      setProcessing(false);
    }
  };

  return (
    <div style={{ padding: '30px', backgroundColor: '#0f1115', color: '#e2e8f0', fontFamily: 'monospace', minHeight: '100vh' }}>
      <header style={{ borderBottom: '2px dashed #3b82f6', paddingBottom: '15px', marginBottom: '30px' }}>
        <h1 style={{ color: '#3b82f6', margin: 0 }}>OMNIVERSE MULTI-MODAL STUDIO</h1>
        <small style={{ color: '#10b981' }}>OWNER STATUS: ROOT PRIVILEGES (FREE OPERATION UNLOCKED)</small>
      </header>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '30px' }}>
        {/* Input parameters panel */}
        <div style={{ backgroundColor: '#1e222b', padding: '20px', borderRadius: '8px' }}>
          <h3>1. CONFIGURATION MANIFEST</h3>
          
          <label style={{ display: 'block', margin: '15px 0 5px' }}>Text Prompt Matrix</label>
          <textarea style={{ width: '100%', height: '80px', backgroundColor: '#0f1115', color: '#fff', border: '1px solid #475569', borderRadius: '4px', padding: '10px' }} 
            value={prompt} onChange={(e) => setPrompt(e.target.value)} />

          <label style={{ display: 'block', margin: '15px 0 5px' }}>Genre Blend Profile</label>
          <input type="text" style={{ width: '100%', backgroundColor: '#0f1115', color: '#fff', border: '1px solid #475569', borderRadius: '4px', padding: '10px' }} 
            value={genres} onChange={(e) => setGenres(e.target.value)} />

          <label style={{ display: 'block', margin: '15px 0 5px' }}>Target Tempo Clock (BPM): {bpm}</label>
          <input type="range" min="60" max="200" style={{ width: '100%' }} value={bpm} onChange={(e) => setBpm(Number(e.target.value))} />

          <div style={{ marginTop: '25px', padding: '15px', border: '1px solid #3b82f6', borderRadius: '4px', textAlign: 'center' }}>
            <button onClick={toggleRecording} style={{ padding: '10px 20px', backgroundColor: recording ? '#ef4444' : '#2563eb', color: '#fff', border: 'none', cursor: 'pointer', fontWeight: 'bold' }}>
              {recording ? "■ STOP VOICE RECORDING" : "● RECORD LIVE VOICE/STEM"}
            </button>
            {audioBlob && <div style={{ color: '#10b981', marginTop: '10px' }}>✓ Audio Asset Staged In RAM Buffer</div>}
          </div>

          <button onClick={executeStudioEngine} disabled={processing} style={{ marginTop: '20px', width: '100%', padding: '15px', backgroundColor: '#10b981', color: '#000', fontWeight: 'bold', border: 'none', cursor: 'pointer', opacity: processing ? 0.5 : 1 }}>
            {processing ? "PROCESSING PIPELINE & VECTORING..." : "COMPILE AND GENERATE TRACK"}
          </button>
        </div>

        {/* Studio engine monitor panel */}
        <div style={{ backgroundColor: '#1e222b', padding: '20px', borderRadius: '8px', display: 'flex', flexDirection: 'column' }}>
          <h3>2. STUDIO WORKSPACE MONITOR</h3>
          
          <div style={{ flexGrow: 1, backgroundColor: '#0f1115', border: '1px solid #475569', padding: '15px', borderRadius: '4px', overflowY: 'auto' }}>
            {outputData ? (
              <div>
                <h4 style={{ color: '#10b981' }}>Pipeline Status: {outputData.status}</h4>
                <p><strong>Tracking Registry ID:</strong> {outputData.session_id}</p>
                
                <h5 style={{ color: '#3b82f6', marginTop: '20px' }}>Vector Memory Connections Recalled:</h5>
                <pre style={{ backgroundColor: '#1e222b', padding: '10px', overflowX: 'auto' }}>
                  {JSON.stringify(outputData.memory_context_applied, null, 2)}
                </pre>

                <h5 style={{ color: '#3b82f6', marginTop: '20px' }}>Generated System Assets:</h5>
                <p>Master Out URL: <span style={{ color: '#f59e0b' }}>{outputData.assets.master_audio_route}</span></p>
              </div>
            ) : (
              <p style={{ color: '#64748b', textAlign: 'center', marginTop: '40px' }}>Ready for engine compilation input...</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
