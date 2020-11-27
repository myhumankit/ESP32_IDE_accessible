"""
    Module wich contains classes and function srelated to the voice synthese(with pyttx3)
"""

from threading import Thread


class Speak(Thread):
    """Thread to say some voacl indications"""

    def __init__(self, frame, info):
        """Constructor method

        :param frame: main window
        :type frame: :class: MainWindow
        :param info: text to speech
        :type info: str
        """
        Thread.__init__(self)
        self.frame = frame
        self.info = info

    def run(self):
        """Thread run
        """
        self.frame.voice_on.say(self.info)
        self.frame.voice_on.runAndWait()


def my_speak(frame, txt):
    """Speak the texte given in params by creating a thread dedicated

    :param frame: main_window
    :type frame: :class: MainWindow
    :param txt: text to speech
    :type txt: str
    """
    if frame.speak_on:
        if frame.speak_thread is not None:
            frame.voice_on.stop()
            frame.speak_thread.join()
        frame.speak_thread = Speak(frame, txt)
        frame.speak_thread.daemon = True
        frame.speak_thread.start()
        frame.voice_on.stop()
        frame.speak_thread = None
