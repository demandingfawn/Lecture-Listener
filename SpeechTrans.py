
import speech_recognition as sr
from threading import Thread
from mdutils.mdutils import MdUtils

r = sr.Recognizer()
m = sr.Microphone()


class Recording:
    run = True

    def __init__(self, interval=1):
        self.interval = interval
        thread = Thread(target=self.record)
        thread.daemon = True
        thread.start()

    def record(self):
        mdFile = MdUtils(file_name='transcript')
        txt = open("transcript.txt", "w")
        txt.close()
        txt = open("transcript.txt", "a")

        while self.run:
            # GUI Blocking Audio Capture
            with m as source:
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)

            try:
                # recognize speech using Google Speech Recognition
                value = r.recognize_google(audio)
                mdFile.write("\"{}\" ".format(value))
                txt.write("\"{}\" ".format(value))

            except sr.UnknownValueError:
                mdFile.write("**Program Didn't Understand** ")
                txt.write("**Program Didn't Understand** ")
            except sr.RequestError as e:
                mdFile.write(
                    "**Error: Couldn't request results from Google Speech Recognition service; {0}** ".format(e))
                txt.write(
                    "**Error: Couldn't request results from Google Speech Recognition service; {0}** ".format(e))

        mdFile.create_md_file()
        txt.close()