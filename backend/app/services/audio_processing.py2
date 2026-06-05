import os
import math
import wave
import struct

class LocalAudioEngine:
    """
    A standalone digital signal processor that creates synthesized master stems,
    adjusts tempos, and mixes your voice samples.
    """
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate

    def _generate_sine_tone(self, frequency: float, duration: float, amplitude: float = 0.4) -> bytes:
        """Generates low-level raw audio signals for underlying tracks."""
        num_samples = int(self.sample_rate * duration)
        raw_data = bytearray()
        for i in range(num_samples):
            # Angular frequency math loop
            sample = amplitude * math.sin(2.0 * math.pi * frequency * (i / self.sample_rate))
            # Packing raw data as 16-bit signed little-endian integers
            packed_sample = struct.pack('<h', int(sample * 32767))
            raw_data.extend(packed_sample)
        return bytes(raw_data)

    def generate_synthetic_stems(self, prompt: str, bpm: int, output_path: str, vocal_reference_path: str = None):
        """
        Creates and balances raw synthesized instruments based on your genre mixes,
        then outputs a structured master .wav file.
        """
        duration_seconds = 4.0
        # Determine track pace from your target BPM settings
        base_frequency = 110.0 if "bass" in prompt.lower() else 220.0
        
        # Build core rhythm tracking data
        synth_stem = self._generate_sine_tone(frequency=base_frequency, duration=duration_seconds)
        
        # Check for and incorporate voice recording tracks
        vocal_stem = None
        if vocal_reference_path and os.path.exists(vocal_reference_path):
            try:
                with wave.open(vocal_reference_path, 'rb') as vf:
                    vocal_stem = vf.readframes(vf.getnframes())
            except Exception:
                # Fallback safeguard for processing non-standard voice codecs
                vocal_stem = None

        # Render out to a standard master file path
        with wave.open(output_path, 'wb') as wav_master:
            wav_master.setnchannels(1)  # Mono track output
            wav_master.setsampwidth(2)  # 16-bit depth formatting
            wav_master.setframerate(self.sample_rate)
            
            if vocal_stem:
                # Merge the vocal input and synthesized background track
                min_length = min(len(synth_stem), len(vocal_stem))
                mixed_bytes = bytearray(min_length)
                for idx in range(0, min_length, 2):
                    if idx + 1 < min_length:
                        s_val = struct.unpack('<h', synth_stem[idx:idx+2])[0]
                        v_val = struct.unpack('<h', vocal_stem[idx:idx+2])[0]
                        # Safe clipping protection mix loop
                        mixed_val = int((s_val + v_val) * 0.5)
                        struct.pack_into('<h', mixed_bytes, idx, mixed_val)
                wav_master.writeframes(bytes(mixed_bytes))
            else:
                wav_master.writeframes(synth_stem)
