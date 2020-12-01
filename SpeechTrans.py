import speech_recognition as sr
from threading import Thread

r = sr.Recognizer()
m = sr.Microphone()

class Recording:
    run = True
    output = []

    def __init__(self, interval=1):
        self.interval = interval
        thread = Thread(target=self.record)
        thread.daemon = True
        thread.start()

    def record(self):
        while self.run:
            # GUI Blocking Audio Capture
            with m as source:
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
            try:
                # recognize speech using Google Speech Recognition
                value = r.recognize_google(audio)
                Recording.output.append("\"{}\"".format(value))
                print(value)
            except sr.UnknownValueError:
                Recording.output.append("Oops! Didn't catch that")
            except sr.RequestError as e:
                Recording.output.append(
                    "Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
