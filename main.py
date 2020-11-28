import speech_recognition as sr
import time




r = sr.Recognizer()
m = sr.Microphone()
t = time.time()

try:
    print("A moment of silence, please...")
    with m as source: r.adjust_for_ambient_noise(source)
    print("Set minimum energy threshold to {}".format(r.energy_threshold))
    while True:
        f = open("TextFile.txt", "a")
        print("Say something")
        with m as source: audio = r.listen(source)
        try:
            elasped_time = time.time()-t
            # recognize speech using Google Speech Recognition
            value = r.recognize_google(audio)
            f.write("{} ".format(value) + "{}\n".format(elasped_time))

        except sr.UnknownValueError:
            print("Didn't catch that")
            break
        except sr.RequestError as e:
            print("Couldn't request results from Google Speech Recognition service; {0}".format(e))
except KeyboardInterrupt:
    pass
