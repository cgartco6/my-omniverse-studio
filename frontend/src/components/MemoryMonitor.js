import React from 'react';

export function MemoryMonitor({ contextArray }) {
  return (
    <div style={{ marginTop: '20px', padding: '15px', backgroundColor: '#111827', borderRadius: '6px', border: '1px solid #374151' }}>
      <h4 style={{ color: '#10b981', marginTop: 0, marginBottom: '10px' }}>LONG-TERM COGNITIVE VECTOR STORAGE FEED</h4>
      {(!contextArray || contextArray.length === 0) ? (
        <p style={{ color: '#4b5563', fontSize: '12px', margin: 0 }}>Memory engine clear. No historical alignment vectors referenced.</p>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
          {contextArray.map((item, index) => (
            <div key={index} style={{ backgroundColor: '#1f2937', padding: '10px', borderRadius: '4px', borderLeft: '3px solid #10b981' }}>
              <span style={{ fontSize: '11px', color: '#9ca3af', display: 'block' }}>RECALLED PROFILE #{index + 1}</span>
              <p style={{ margin: '5px 0 0', fontSize: '12px', color: '#f3f4f6' }}>{item.historical_profile}</p>
              <small style={{ color: '#6b7280', fontSize: '10px' }}>Session UUID Metadata Connection: {item.meta?.session_id}</small>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
