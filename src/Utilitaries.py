import wx, time, json, asyncio, sys
from my_serial import SendCmdAsync, put_cmd
from threading import Thread

def load_img(path):
    return wx.Image(path,wx.BITMAP_TYPE_ANY).ConvertToBitmap()

async def speak(main_window, txt):
    print(txt)
    main_window.voice_on.say(txt)
    main_window.voice_on.runAndWait()

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
        return_cmd = shell_text.split(cmd, 1)[1]
        return_cmd = return_cmd[:-4]
    except Exception:
        print ("ERROR: |" + shell_text +  "|")
        return "err"
    print ("SUCCESS:" + return_cmd)
    return return_cmd

async def SetView(main_window, info):
    main_window.show_cmd = info


class Speak(Thread):
    """Thread chargé simplement d'afficher une lettre dans la console."""

    def __init__(self, main_window):
        Thread.__init__(self)
        self.main_window = main_window

    def run(self):
        """Code à exécuter pendant l'exécution du thread."""
        while True:
            if self.main_window.speak_on:
                print(self.main_window.speak_on)
                speak(self.main_window, self.main_window.speak_on)
                self.main_window.speak_on = None
                

