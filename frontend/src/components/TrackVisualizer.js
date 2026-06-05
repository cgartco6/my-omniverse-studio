import React from 'react';

export function TrackVisualizer({ audioUrl, videoUrl }) {
  if (!audioUrl && !videoUrl) {
    return (
      <div style={{ padding: '40px', border: '1px dashed #334155', textAlign: 'center', color: '#64748b', borderRadius: '4px' }}>
        No compiled media tracking monitors are active. Trigger production.
      </div>
    );
  }

  return (
    <div style={{ backgroundColor: '#0f1115', padding: '15px', borderRadius: '6px', border: '1px solid #1e293b' }}>
      <h4 style={{ color: '#3b82f6', marginTop: 0, marginBottom: '15px' }}>LIVE MASTER MONITOR PLATFORM</h4>
      
      {videoUrl && (
        <div style={{ marginBottom: '20px', textAlign: 'center', backgroundColor: '#000', borderRadius: '4px', overflow: 'hidden' }}>
          <video src={videoUrl} controls autoPlay loop style={{ width: '100%', maxHeight: '320px', objectFit: 'contain' }} />
        </div>
      )}

      {audioUrl && (
        <div style={{ padding: '10px', backgroundColor: '#1e222b', borderRadius: '4px' }}>
          <label style={{ display: 'block', fontSize: '11px', color: '#94a3b8', marginBottom: '5px' }}>MASTER STEREO BUS OUT</label>
          <audio src={audioUrl} controls style={{ width: '100%' }} />
        </div>
      )}
    </div>
  );
}
