from os import path, rename, remove
from threading import Thread
import pyaudio
import wave


class Audio:
    run = True

    def __init__(self, interval=1):
        self.interval = interval
        thread = Thread(target=self.record)
        thread.daemon = True
        thread.start()

    def record(self):
        chunk = 1024  # Record in chunks of 1024 samples
        sample_format = pyaudio.paInt16  # 16 bits per sample
        channels = 1
        fs = 44100  # Record at 44100 samples per second
        seconds = 2
        filename = "audio_upload.wav"
        p = pyaudio.PyAudio()  # Create an interface to PortAudio
        stream = p.open(format=sample_format,
                        channels=channels,
                        rate=fs,
                        frames_per_buffer=chunk,
                        input=True)

        frames = []  # Initialize array to store frames
        # Store data in chunks for 3 seconds
        for i in range(0, int(fs / chunk * seconds)):
            data = stream.read(chunk, exception_on_overflow=False)
            frames.append(data)
        # Stop and close the stream
        stream.stop_stream()
        stream.close()
        # Terminate the PortAudio interface
        p.terminate()
        # Save the recorded data as a WAV file
        output = wave.open(filename, 'wb')
        output.setnchannels(channels)
        output.setsampwidth(p.get_sample_size(sample_format))
        output.setframerate(fs)
        output.writeframes(b''.join(frames))
        output.close()

        while self.run:
            chunk = 1024  # Record in chunks of 1024 samples
            sample_format = pyaudio.paInt16  # 16 bits per sample
            channels = 1
            fs = 44100  # Record at 44100 samples per second
            seconds = 2
            filename = "new.wav"
            p = pyaudio.PyAudio()  # Create an interface to PortAudio
            stream = p.open(format=sample_format,
                            channels=channels,
                            rate=fs,
                            frames_per_buffer=chunk,
                            input=True)
            frames = []  # Initialize array to store frames
            # Store data in chunks for 3 seconds
            for i in range(0, int(fs / chunk * seconds)):
                data = stream.read(chunk, exception_on_overflow=False)
                frames.append(data)
            # Stop and close the stream
            stream.stop_stream()
            stream.close()
            # Terminate the PortAudio interface
            p.terminate()
            # Save the recorded data as a WAV file
            new = wave.open(filename, 'wb')
            new.setnchannels(channels)
            new.setsampwidth(p.get_sample_size(sample_format))
            new.setframerate(fs)
            new.writeframes(b''.join(frames))
            new.close()

            files = ["audio_upload.wav", "new.wav"]
            data = []
            for file in files:
                w = wave.open(file, 'rb')
                data.append([w.getparams(), w.readframes(w.getnframes())])
                w.close()
            merge = wave.open("tmp.wav", 'wb')
            merge.setparams(data[0][0])
            merge.writeframes(data[0][1])
            merge.writeframes(data[1][1])
            merge.close()
            remove("audio_upload.wav")
            rename("tmp.wav", "audio_upload.wav")
        if path.exists("new.wav"):
            remove("new.wav")
