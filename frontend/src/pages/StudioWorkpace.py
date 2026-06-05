import React, { useState, useRef } from 'react';
import './StudioWorkspace.css'; // Add responsive CSS layouts here

export default function StudioWorkspace() {
  const [textPrompt, setTextPrompt] = useState('');
  const [recording, setRecording] = useState(false);
  const [audioBlob, setAudioBlob] = useState(null);
  const mediaRecorderRef = useRef(null);

  // Native recording integration for capturing your own voice instantly
  const startRecording = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorderRef.current = new MediaRecorder(stream);
    const chunks = [];
    
    mediaRecorderRef.current.ondataavailable = (e) => chunks.push(e.data);
    mediaRecorderRef.current.onstop = () => {
      const blob = new Blob(chunks, { type: 'audio/ogg; codecs=opus' });
      setAudioBlob(blob);
    };
    
    mediaRecorderRef.current.start();
    setRecording(true);
  };

  const stopRecording = () => {
    mediaRecorderRef.current.stop();
    setRecording(false);
  };

  const handleGenerationExecute = async () => {
    const formData = new FormData();
    formData.append('text_prompt', textPrompt);
    if (audioBlob) {
      formData.append('vocal_file', audioBlob, 'owner_voice.ogg');
    }
    
    // Grabbing custom file references from input nodes
    const imageInput = document.getElementById('imageUpload').files[0];
    if (imageInput) formData.append('image_file', imageInput);

    const response = await fetch('http://localhost:8000/api/v1/synthesize', {
      method: 'POST',
      body: formData,
    });
    const data = await response.json();
    console.log("Synthesized Output Metadata:", data);
  };

  return (
    <div className="studio-container">
      <header className="studio-header">
        <h1>Omniverse Studio Workspace</h1>
        <span className="badge-owner">Owner Authorization: Root</span>
      </header>

      <main className="studio-grid">
        {/* Left Side Panel: Generation Modalities */}
        <section className="control-panel">
          <h2>1. Input Configurations</h2>
          <textarea 
            placeholder="Describe the sonic atmosphere, genre fusions (e.g., Synthwave Jazz)..."
            value={textPrompt}
            onChange={(e) => setTextPrompt(e.target.value)}
          />

          <div className="media-inputs">
            <label>Image Reference (Seedance style):</label>
            <input type="file" id="imageUpload" accept="image/*" />

            <div className="voice-recorder">
              <p>Voice / Instrument Source File:</p>
              {!recording ? (
                <button className="btn-rec" onClick={startRecording}>● Record Own Voice</button>
              ) : (
                <button className="btn-stop" onClick={stopRecording}>■ Stop Recording</button>
              )}
              {audioBlob && <span className="status-ready">✓ Voice Asset Loaded</span>}
            </div>
          </div>

          <button className="btn-execute" onClick={handleGenerationExecute}>
            Generate Track & Visuals
          </button>
        </section>

        {/* Right Side Panel: Output Node & Memory Monitoring */}
        <section className="output-panel">
          <h2>2. Production Engine Monitor</h2>
          <div className="waveform-display">
            <p>[ Audio Visualizer Window ]</p>
          </div>
          <div className="memory-vault-status">
            <h3>Active Long-Term Memory</h3>
            <p className="txt-muted">System is matching current output parameters against past tracking profiles to ensure consistent style preservation.</p>
          </div>
        </section>
      </main>
    </div>
  );
}
