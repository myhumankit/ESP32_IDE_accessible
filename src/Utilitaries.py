import wx, time, json, asyncio, sys
from my_serial import SendCmdAsync, put_cmd
from threading import Thread, active_count
import pyttsx3

def load_img(path):
    return wx.Image(path,wx.BITMAP_TYPE_ANY).ConvertToBitmap()

def speak(main_window, txt):
    #print(txt)
    try:
        main_window.voice_on.say(txt)
        main_window.voice_on.runAndWait()
        main_window.voice_on.stop()
    except RuntimeError:
        main_window.voice_on.stop()
        main_window.voice_on.say(txt)
        main_window.voice_on.runAndWait()
        main_window.voice_on.stop()
        

def remove_char(shell, main_window):
    txt = shell.GetValue()
    cursor = shell.GetInsertionPoint()
    print(cursor)
    shell.Remove(cursor - 1, cursor)
    print(cursor)
    #shell.Clear()
    #main_window.shell_text = shell.GetValue()
    #shell.SetInsertionPoint(cursor)

def move_key_left(shell):
    cursor = shell.GetInsertionPoint()
    shell.SetInsertionPoint(cursor - 1)

def move_key_right(shell):
    cursor = shell.GetInsertionPoint()
    shell.SetInsertionPoint(cursor + 1)

def cursor_at_end(shell, text):
    cursor = shell.GetInsertionPoint()
    maxi = len(text)
    return cursor == maxi

def GetCmdReturn(shell_text, cmd):
    """Return the result of a command launched in MicroPython

    :param shell_text: The text catched on the shell panel
    :type shell_text: str
    :param cmd: The cmd return asked
    :type cmd: str
    :return: the return of the command searched
    :rtype: str
    """
    try:
        return_cmd = shell_text.split(cmd)
        return_cmd = return_cmd[len(return_cmd) - 1]
        return_cmd = return_cmd[:-4]
    except Exception:
        print ("ERROR: |" + shell_text +  "|")
        return "err"
    print ("SUCCESS: | " + return_cmd + "|")
    return return_cmd

class Speak(Thread):
    """Thread chargé simplement d'afficher une lettre dans la console."""

    def __init__(self, main_window, info):
        Thread.__init__(self)
        self.main_window = main_window
        self.info = info

    def run(self):
        speak(self.main_window, self.info)
        print("pass")

def my_speak(main_window, txt):
    if main_window.speak_on: 
        main_window.speak_thread = Speak(main_window, txt)
        main_window.speak_thread.daemon = True
        main_window.speak_thread.start()
        main_window.speak_thread = None

def get_cmd_result(main_window, cmd):
    main_window.exec_cmd(cmd)
    return main_window.result
