import speech_recognition as sr
import time


r = sr.Recognizer()
m = sr.Microphone()
t = time.time()


recording = bool


class speech:
    def speak(self):
        try:
            print("A moment of silence, please...")
            with m as source: r.adjust_for_ambient_noise(source)
            print("Set minimum energy threshold to {}".format(r.energy_threshold))
            recording = True
            while recording:

                f = open("TextFile.txt", "a")
                print("Say something")
                with m as source: audio = r.listen(source)


                elasped_time = time.time()-t
                # recognize speech using Google Speech Recognition
                value = r.recognize_google(audio)
                print("{}".format(value))
                f.write("{} ".format(value) + "{" + "{}".format(elasped_time) + "}\n")

        except KeyboardInterrupt:
            pass
