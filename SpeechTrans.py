from threading import Thread
from mdutils.mdutils import MdUtils
import speech_recognition as sr

r = sr.Recognizer()
m = sr.Microphone()


class Recording:
    run = True
    mdFile = MdUtils(file_name='transcript_upload')
    tempStr = ""

    def __init__(self, interval=1):
        self.interval = interval
        thread = Thread(target=self.record)
        thread.daemon = True
        thread.start()

    def record(self):
        # while self.run:
        # GUI Blocking Audio Capture
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
        try:
            # recognize speech using Google Speech Recognition
            value = r.recognize_google(audio)
            self.mdFile.write("\"{}\" ".format(value))
            self.tempStr = value
        except sr.UnknownValueError:
            self.mdFile.write("**Program Didn't Understand** ")
            self.tempStr = "**Program Didn't Understand**"
        except sr.RequestError as e:
            self.mdFile.write(
                "**Error: Couldn't request results from Google Speech Recognition service; {0}** ".format(e))
            self.tempStr = "**Error: Couldn't request results from Google Speech Recognition service; {0}**".format(e)
        self.mdFile.create_md_file()
