"""
Module which has functions and classes to manage the connection and communication with the card
"""

from packages import wx, os, time, asyncio
from constantes import *

class TerminalSetup:
    """
    Placeholder for various terminal settings. Used to pass the
    options to the TerminalSettingsDialog.
    """
    def __init__(self):
        self.echo = False
        self.unprintable = False
        self.newline = NEWLINE_CRLF

class ManageConnection():
    """
    Class with useful methods to manage Connection related with the main_window
    """
    
    def __init__(self, main_window):
        """Constructor for ManageConnection class

        :param main_window: The MainWindow to get some properties
        :type main_window: MainWindow class
        """
        
        self.main_window = main_window
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
            print("[%s]"%msg_cmd)
            count = 0
            msg_cmd = msg_cmd.split('(')[1]
            msg_cmd = msg_cmd.split(')')[0]
            res = tuple(map(str, msg_cmd.split(', ')))
            list_infos = [self.card, self.nodename, self.release, self.version, \
                            self.machine]
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
            print(e)

    def download_and_run(self, filename):
        """Execute the file gived in params on the MicroPython card

        :param filename: the path of the file to execute(root is the device connected)
        :type filename: str
        """

        time.sleep(1)
        put_cmd(self.main_window,'\x03')
        put_cmd(self.main_window, "exec(open(\'%s\').read(),globals())\r\n"%str(filename))
      
    def download(self, filepath ,filename):
        filepath = filepath.replace("\\","/")
        print("download===============================%s\n"%filename)
        file_to_open = _check_extension_file(filename, ".py")

        if not file_to_open:
            self.main_window.shell.AppendText("Error extension file is not .py\n...")
            return False
        try:
            fileHandle=open(filepath,'rbU')
        except Exception as e:
            print("Error file : %s"%(e))
            self.main_window.shell.AppendText("Error on during file upload\n...")
    
        put_cmd(self.main_window, '\x03')
        self.main_window.show_cmd = False
        self.main_window.shell.Clear()
        self.main_window.shell.AppendText("Ready to download this file,please wait!")
        self.write_in_file(fileHandle, file_to_open)

    def write_in_file(self, fileHandle, file_to_open):
        cmd = "myfile=open(\'%s\',\'w\')\r\n"%str(file_to_open)
        done=0

        put_cmd(self.main_window, cmd)
        while not done:
            aline = fileHandle.read(128)
            if(str(aline)!="b''"):
                try:
                    aline=aline.decode()
                    aline=aline.replace("\r\n","\r")
                    aline=aline.replace("\n","\r")
                    aline="myfile.write(%s)\r"%repr(aline)
                except:
                    aline="myfile.write(%s)\r"%repr(aline)
                for i in aline:
                    put_cmd(self.main_window, i)
            else:
                done=1
        fileHandle.close()
        put_cmd(self.main_window, "myfile.close()\r\n")

def ConnectSerial(self):
        self.shell.Clear()
        self.serial.write('\x03'.encode())

        startdata=""
        startTime=time.time()
        while True:
            n = self.serial.inWaiting()
            if n>0:
                startdata += (self.serial.read(n)).decode(encoding='utf-8',errors='ignore')
                print("[%s]"%startdata)
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
        senddata="import sys\r\n"
        put_cmd(self, "import sys\r\n")
        for i in senddata:
            self.serial.write(i.encode())
        startdata=""
        startTime=time.time()
        while True:
            n = self.serial.inWaiting()
            if n>0:
                startdata+=(self.serial.read(n)).decode('utf-8')
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

        senddata="sys.platform\r"
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

        self.start_thread_serial()
        return True

def _check_extension_file(filename, extension):
    finalname = ""
    if str(filename).find(extension)>=0:
        if str(filename).find(":")<0:
            finalname = str(filename)
            return finalname
        else:
            print("error path",)
            return None    
    else:
        print("error extension")
        return None    

def put_cmd(main_window, msg_cmd): 
    """Send a Python command to the connected card

    :param main_window: MainWindow
    :type msg_cmd: :class:MainWindow
    :param msg_cmd: command to send
    :type msg_cmd: str
    """
                
    main_window.serial.write(msg_cmd.encode('utf-8'))
    main_window.serial.flush()

async def SendCmdAsync(main_window, cmd):
    main_window.cmd_return = ""
    print("CMDsend = " +cmd)
    put_cmd(main_window, cmd)
    await asyncio.sleep(main_window.time_to_send) 
