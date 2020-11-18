import speech_recognition as sr

r = sr.Recognizer()
m = sr.Microphone()

try:
    print("A moment of silence, please...")
    with m as source: r.adjust_for_ambient_noise(source)
    print("Set minimum energy threshold to {}".format(r.energy_threshold))
    while True:
        print("Say something")
        with m as source: audio = r.listen(source)
        try:
            # recognize speech using Google Speech Recognition
            value = r.recognize_google(audio)

            print("You said {}".format(value))
        except sr.UnknownValueError:
            print("Didn't catch that")
        except sr.RequestError as e:
            print("Couldn't request results from Google Speech Recognition service; {0}".format(e))
except KeyboardInterrupt:
    pass