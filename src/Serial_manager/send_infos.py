import asyncio
import time

from threading import Thread


def put_cmd(frame, msg_cmd):
    """Send a Python command to the connected card

    :param frame: MainWindow
    :type msg_cmd: :class:MainWindow
    :param msg_cmd: command to send
    :type msg_cmd: str
    """
    # frame.show_cmd = False
    frame.serial.write(msg_cmd.encode('utf-8'))
    frame.serial.flush()


async def SendCmdAsync(frame, cmd):
    frame.cmd_return = ""
    print("CMDsend = " + cmd)
    put_cmd(frame, cmd)
    await asyncio.sleep(frame.time_to_send)


class Exec_cmd(Thread):
    def __init__(self, cmd, parent):
        Thread.__init__(self)
        self.frame = parent
        self.cmd = cmd

    def run(self):
        if self.frame.serial.isOpen():
            cmd = self.cmd
            self.frame.result = ""
            asyncio.run(SendCmdAsync(self.frame, cmd))
        else:
            time.sleep(0.01)


def convert_cmd(cmd, writemsg):
    if type(cmd) is bytes:
        # print("BYTES")
        writemsg = cmd
    elif type(cmd) is str:
        # print("STR")
        writemsg = cmd.encode('utf-8')
    return writemsg
