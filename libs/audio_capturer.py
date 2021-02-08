import pyaudio # Soundcard audio I/O access library
import wave # Python 3 module for reading / writing simple .wav files

class AudioCapturer():
    def __init__(self, record_time):
        # Setup channel info
        self.FORMAT = pyaudio.paInt16 # data type formate
        self.CHANNELS = 1 # Adjust to your number of channels
        self.RATE = 16000 # Sample Rate
        self.CHUNK = int(self.RATE / 10) # Block Size
        self.RECORD_SECONDS = record_time # Record time
        self.WAVE_OUTPUT_FILENAME = "file.wav"
    
    def record_instance(self):
        # Startup pyaudio instance
        self.audio = pyaudio.PyAudio()

        # start Recording
        stream = self.audio.open(format=self.FORMAT, channels=self.CHANNELS,
                        rate=self.RATE, input=True,
                        frames_per_buffer=self.CHUNK)
        print("Starting recording...")
        frames = []
        
        # Record for RECORD_SECONDS
        for _ in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
            data = stream.read(self.CHUNK)
            frames.append(data)
        print("Finished recording...")

        # Stop Recording
        stream.stop_stream()
        stream.close()
        self.audio.terminate()
        return b''.join(frames)

    def save_to_file(self, byte_stream):
        # Write your new .wav file with built in Python 3 Wave module
        waveFile = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')
        waveFile.setnchannels(self.CHANNELS)
        waveFile.setsampwidth(self.audio.get_sample_size(self.FORMAT))
        waveFile.setframerate(self.RATE)
        waveFile.writeframes(byte_stream)
        waveFile.close()