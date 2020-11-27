"""
    Module wich contains the functions used to send infos from the device connected
"""
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
    """Asynchrone fonction to send command (allow to read the command back easily)

    :param frame: main window
    :type frame: :class:MainWindow
    :param cmd: command to send
    :type cmd: str
    :return: None
    """
    frame.cmd_return = ""
    put_cmd(frame, cmd)
    await asyncio.sleep(frame.time_to_send)


class Exec_cmd(Thread):
    """ Thread which execute command when he's created

    :param Thread: Python thread
    :type Thread: :class: threading.Thread
    """
    def __init__(self, cmd, frame):
        """Constructor Method

        :param cmd: command to send
        :type cmd: str
        :param frame: main window
        :type frame: Main_window
        """
        Thread.__init__(self)
        self.frame = frame
        self.cmd = cmd

    def run(self):
        """
        Thread run
         """
        if self.frame.serial.isOpen():
            cmd = self.cmd
            self.frame.result = ""
            asyncio.run(SendCmdAsync(self.frame, cmd))
        else:
            time.sleep(0.01)
