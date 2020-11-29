import pyaudio
import wave

filename = "recorded.wav"
chunk = 1024
FORMAT = pyaudio.paInt16
channels = 1
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT,
                channels=channels,
                input=True,
                output=True,
                frames_per_buffer=chunk)
frames = []
recording = True
print("Recording...")
while recording:
    data = stream.read(chunk)
    frames.append(data)
stream.stop_stream()
stream.close()
p.terminate()
wf = wave.open(filename, "wb")
wf.setnchannels(channels)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.writeframes(b"".join(frames))
wf.close()