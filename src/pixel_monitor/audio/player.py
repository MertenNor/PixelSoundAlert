"""Audio playback using pydub and winsound"""

import os
import time
import tempfile
import threading
import winsound
from pydub import AudioSegment


class AudioPlayer:
    """Handles audio playback with volume control"""
    
    @staticmethod
    def play_sound(area):
        """Play the sound for an area"""
        if not area.get('sound_file'):
            return
        
        def play_sound_thread():
            try:
                # Load and adjust volume
                audio = AudioSegment.from_file(area['sound_file'])
                volume = AudioPlayer._get_volume(area)
                
                # Adjust volume (pydub uses dB, so we convert 0.0-1.0 to dB)
                # 0.0 = -inf dB (mute), 1.0 = 0 dB (original), 0.5 = -6 dB
                if volume > 0:
                    change_in_dB = 20 * (volume - 1.0)  # Convert to dB change
                    audio = audio + change_in_dB
                else:
                    return  # Don't play if volume is 0
                
                # Convert to WAV format and play with winsound
                # Create a temporary file for winsound (it requires a file path)
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
                try:
                    audio.export(temp_file.name, format="wav")
                    temp_file.close()
                    # Play asynchronously (non-blocking)
                    winsound.PlaySound(temp_file.name, winsound.SND_FILENAME | winsound.SND_ASYNC)
                finally:
                    # Clean up temp file after a delay (give time for playback to start)
                    def cleanup():
                        time.sleep(1)  # Wait a bit for playback to start
                        try:
                            os.unlink(temp_file.name)
                        except:
                            pass
                    threading.Thread(target=cleanup, daemon=True).start()
            except Exception as e:
                print(f"Error playing sound: {e}")
        
        threading.Thread(target=play_sound_thread, daemon=True).start()
    
    @staticmethod
    def _get_volume(area):
        """Get volume value from entry (0.0 to 1.0)"""
        try:
            val = int(area['ui']['volume_entry'].get())
            return max(0, min(100, val)) / 100.0
        except:
            return 0.5

