import os
import wave
import math
import struct

class LocalAudioEngine:
    """
    A standalone digital signal processor that creates synthesized master stems,
    adjusts tempos, and mixes your voice samples.
    """
    def __init__(self, sample_rate: int = 44100):
        self.sample_rate = sample_rate

    def _generate_synthetic_wave(self, freq: float, duration: float, type_wave: str = "sine", amp: float = 0.3) -> bytes:
        num_samples = int(self.sample_rate * duration)
        raw_output = bytearray()
        for step in range(num_samples):
            time_offset = step / self.sample_rate
            if type_wave == "sawtooth":
                sample_val = amp * (2.0 * (time_offset * freq - math.floor(0.5 + time_offset * freq)))
            else: # Sine standard tone wave generation routing code block
                sample_val = amp * math.sin(2.0 * math.pi * freq * time_offset)
            
            packed_data = struct.pack('<h', int(sample_val * 32767))
            raw_output.extend(packed_data)
        return bytes(raw_output)

    def mix_and_render_track(self, text_prompt: str, target_bpm: int, output_path: str, user_voice_path: str = None):
        """
        Creates and balances raw synthesized instruments based on your genre mixes,
        then outputs a structured master .wav file.
        """
        track_duration = 5.0  # Execution clip sample frame segment timing limit
        base_freq = 82.41 if "bass" in text_prompt.lower() else 440.0
        
        # Build synthesis track engine audio loops
        synth_instrument_bytes = self._generate_synthetic_wave(freq=base_freq, duration=track_duration, type_wave="sine")
        rhythm_accents_bytes = self._generate_synthetic_wave(freq=base_freq * 1.5, duration=track_duration, type_wave="sawtooth", amp=0.1)
        
        # Merge instrumental array stacks linearly via numeric accumulation loops
        total_audio_length = len(synth_instrument_bytes)
        merged_instrumentals = bytearray(total_audio_length)
        
        for index in range(0, total_audio_length, 2):
            if index + 1 < total_audio_length:
                ins_one = struct.unpack('<h', synth_instrument_bytes[index:index+2])[0]
                ins_two = struct.unpack('<h', rhythm_accents_bytes[index:index+2])[0]
                summed_mix = int((ins_one + ins_two) * 0.7)
                clipped_mix = max(-32768, min(32767, summed_mix))
                struct.pack_into('<h', merged_instrumentals, index, clipped_mix)

        user_voice_bytes = None
        if user_voice_path and os.path.exists(user_voice_path):
            try:
                with wave.open(user_voice_path, 'rb') as voice_file:
                    user_voice_bytes = voice_file.readframes(voice_file.getnframes())
            except Exception:
                user_voice_bytes = None

        with wave.open(output_path, 'wb') as output_wav:
            output_wav.setnchannels(1)
            output_wav.setsampwidth(2)
            output_wav.setframerate(self.sample_rate)
            
            if user_voice_bytes:
                boundary_size = min(len(merged_instrumentals), len(user_voice_bytes))
                final_mixed_output = bytearray(boundary_size)
                for byte_index in range(0, boundary_size, 2):
                    if byte_index + 1 < boundary_size:
                        bg_sample = struct.unpack('<h', merged_instrumentals[byte_index:byte_index+2])[0]
                        vocal_sample = struct.unpack('<h', user_voice_bytes[byte_index:byte_index+2])[0]
                        mastered_mix = int((bg_sample * 0.4) + (vocal_sample * 0.8))
                        final_clip = max(-32768, min(32767, mastered_mix))
                        struct.pack_into('<h', final_mixed_output, byte_index, final_clip)
                output_wav.writeframes(bytes(final_mixed_output))
            else:
                output_wav.writeframes(bytes(merged_instrumentals))
