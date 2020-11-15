# Lecture-Listener
Basic code to convert speech to text. Does not use Deepspeech

To use it you will have to go to https://www.lfd.uci.edu/~gohlke/pythonlibs/
to find the wheel for pyaudio, im using PyAudio‑0.2.11‑cp39‑cp39‑win_amd64.whl since im on python 3.9

you will then need to install it using pip. you also need to pip install SpeechRecognition pydub. both of these will let the code work. it currently listens until the user stops speaking to which it will print the text and begin listening again
