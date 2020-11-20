from threading import Thread


def speak(frame, txt):
    frame.voice_on.say(txt)


class Speak(Thread):
    """Thread chargé simplement d'afficher une lettre dans la console."""

    def __init__(self, frame, info):
        Thread.__init__(self)
        self.frame = frame
        self.info = info

    def run(self):
        speak(self.frame, self.info)
        self.frame.voice_on.runAndWait()


def my_speak(frame, txt):
    if frame.speak_on:
        if frame.speak_thread is not None:
            frame.voice_on.stop()
            frame.speak_thread.join()
        frame.speak_thread = Speak(frame, txt)
        frame.speak_thread.daemon = True
        frame.speak_thread.start()
        frame.voice_on.stop()
        frame.speak_thread = None
