import queue
import time
from threading import Thread
from utilitaries import SendCmdAsync
import asyncio

class readWriteUart(Thread):
    def __init__(self, q, parent):
        Thread.__init__(self)
        self.main_window=parent
        self.queue= q
        
    def run(self):
        while True:
            if self.main_window.serial.isOpen():
                if not self.queue.empty():
                    cmd=self.queue.get(timeout=1)
                    self.main_window.result = "err"
                    while self.main_window.result == "err":
                        asyncio.run(SendCmdAsync(self.main_window, cmd))
                        self.main_window.result = self.main_window.read_cmd(cmd[:-2])
                        #print(self.main_window.result)
                    self.queue.task_done()
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

