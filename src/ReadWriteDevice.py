import queue
import time
from threading import Thread, active_count
from utilitaries import SendCmdAsync, put_cmd
import asyncio
import wx

class Exec_cmd(Thread):
    def __init__(self, cmd, parent):
        Thread.__init__(self)
        self.main_window=parent
        self.cmd = cmd
        
    def run(self):
        if self.main_window.serial.isOpen():
                cmd= self.cmd
                self.main_window.result = ""
                asyncio.run(SendCmdAsync(self.main_window, cmd))
                print(active_count())
        else:
            time.sleep(0.01)

def convert_cmd(cmd, writemsg):
    if type(cmd) is bytes:
        #print("BYTES")
        writemsg=cmd
    elif type(cmd) is str:
        #print("STR")
        writemsg=cmd.encode('utf-8')
    return writemsg

