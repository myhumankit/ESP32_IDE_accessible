"""
Module which has functions and classes to manage the connection
and communication with the card
"""

import os
import time
import wx
from Serial_manager.send_infos import put_cmd
from constantes import NEWLINE_CRLF, NEWLINE_LF
from Panels.Device_tree import treeModel


class TerminalSetup:
    """
    Placeholder for various terminal settings. Used to pass the
    options to the TerminalSettingsDialog.
    """
    def __init__(self):
        """ Constructor method
        """
        self.echo = False
        self.unprintable = False
        self.newline = NEWLINE_CRLF


class ManageConnection():
    """
    Class with useful methods to manage Connection related with the frame
    """

    def __init__(self, frame):
        """Constructor for ManageConnection class

        :param frame: The MainWindow to get some properties
        :type frame: MainWindow class
        """

        self.frame = frame
        self.last_cmd = ""
        self.card = None
        self.nodename = None
        self.release = None
        self.version = None
        self.machine = None

    def get_card_infos(self, msg_cmd):
        """Get the name, the version of the firmware and the type of the
         connected device

        :param msg_cmd: Result of a command
        :type msg_cmd: string
        """
        try:
            count = 0
            msg_cmd = msg_cmd.split('(')[1]
            msg_cmd = msg_cmd.split(')')[0]
            res = tuple(map(str, msg_cmd.split(', ')))
            list_res = []

            for i in res:
                i = i.split('=')
                i = i[1][1:-1]
                list_res.append(i)
                count += 1

            self.card = list_res[0]
            self.nodename = list_res[1]
            self.release = list_res[2]
            self.version = list_res[3]
            self.machine = list_res[4]
        except Exception as e:
            print("Error get infos device:", e)

    def download_and_run(self, filename):
        """Execute the file gived in params on the MicroPython card

        :param filename: the path of the file to execute
        :type filename: str
        """

        time.sleep(1)
        put_cmd(self.frame, '\x03')
        put_cmd(self.frame, "exec(open(\'%s\').read(),globals())\r\n"
                % str(filename))
        self.frame.shell.SetFocus()

# TODO: rename to upload
    def download(self, filepath, filename):
        """ Download a file on the card

        :param filepath: path of the file to upload
        :type filepath: str
        :param filename: name of the file to upload
        :type filename: str
        :return: success flag
        :rtype: boolean
        """
        filepath = filepath.replace("\\", "/")
        file_to_open = _check_extension_file(filename, ".py")

        if not file_to_open:
            self.frame.shell.WriteText("Error extension file isn't .py\n")
            return False
        try:
            fileHandle = open(filepath, 'rbU')
            print("SIZE_open=", os.path.getsize(filepath))
        except Exception as e:
            print("Error file : %s" % (e))
            self.frame.shell.WriteText("Error on during file upload\n...")

        put_cmd(self.frame, '\x03')
        self.frame.show_cmd = False
        self.frame.shell.Clear()
        self.frame.shell.WriteText("Ready to download this file...!\n")
        self.write_in_file(fileHandle, file_to_open)

    def write_in_file(self, fileHandle, file_to_open):
        """Write bytes of a computer file on a file on the device

        :param fileHandle: fileHandle to read
        :type fileHandle: file handled see :function: open()
        :param file_to_open: device file
        :type file_to_open: str
        """
        cmd = "myfile=open(\'%s\',\'w\')\r\n" % str(file_to_open)

        self.frame.exec_cmd(cmd)
        aline = fileHandle.read()
        try:
            aline = aline.decode()
            aline = "myfile.write(%s)\r\n" % repr(aline)
            self.frame.exec_cmd(aline)

        except Exception as e:
            print(e)
        finally:
            fileHandle.close()
            self.frame.exec_cmd("myfile.close()\r\n")
            self.frame.exec_cmd("\r\n")
            self.frame.shell_text = ""
            treeModel(self.frame)


def ConnectSerial(self):
    """Try to connect the device and the software

    :return: success flag
    :rtype: boolean
    """
    self.shell.Clear()
    self.serial.write('\x03'.encode())

    startdata = ""
    startTime = time.time()
    while True:
        n = self.serial.inWaiting()
        if n > 0:
            startdata += (self.serial.read(n)).decode(encoding='utf-8', errors='ignore')
            print("[%s]" % startdata)
            if startdata.find('>>> '):
                print("OK")
                break
        time.sleep(0.1)
        endTime=time.time()
        if endTime-startTime > 10:
            self.serial.close()
            if not self.serial.isOpen():
                print("UPDATE FIRMWARE")
                return False
            return False
    senddata="import sys\r\n"
    put_cmd(self, "import sys\r\n")
    for i in senddata:
        self.serial.write(i.encode())
    startdata=""
    startTime=time.time()
    while True:
        n = self.serial.inWaiting()
        if n>0:
            startdata+=(self.serial.read(n)).decode('utf-8', 'ignore')
            if startdata.find('>>> ')>=0:
                self.shell.AppendText(">>> ")
                break
        time.sleep(0.1)
        endTime=time.time()
        if endTime-startTime>2:
            print(startdata)
            self.serial.close()
            self.shell.AppendText("connect serial timeout")
            return False

    senddata="sys.platform\r\n"
    for i in senddata:
        self.serial.write(i.encode())
    startdata=""
    startTime=time.time()
    while True:
        n = self.serial.inWaiting()
        if n>0:
            startdata+=(self.serial.read(n)).decode('utf-8')
            if startdata.find('>>> ')>=0:
                break
        time.sleep(0.1)
        endTime=time.time()
        if endTime-startTime>2:
            self.serial.close()
            self.shell.AppendText("connect serial timeout")
            return False

    # self.start_thread_serial()
    return True


# def try_send_data(frame):
#     startdata = ""
#     startTime = time.time()
#     while True:
#         n = frame.serial.inWaiting()
#         if n > 0:
#             startdata += (frame.serial.read(n)).decode(encoding='utf-8',
#                                                        errors='ignore')
#             print("[%s]" % startdata)
#             if startdata.find('>>> '):
#                 print("OK")
#                 return True
#         time.sleep(0.1)
#         endTime = time.time()
#         if endTime-startTime > 10:
#             frame.serial.close()
#             if not frame.serial.isOpen():
#                 print("UPDATE FIRMWARE")
#                 return False
#             return False

# TODO : vérifier ce qu'on envoie à cette fonction

def _check_extension_file(filename, extension):
    """Check the extension file correspond to the extension asked

    :param filename: file to chek
    :type filename: str
    :param extension: extensions to find
    :type extension: [type]
    :return:
    :rtype: [type]
    """
    finalname = ""
    if str(filename).find(extension) >= 0:
        if str(filename).find(":") < 0:
            finalname = str(filename)
            return finalname
        else:
            print("error path",)
            return None
    else:
        print("error extension")
        return None
