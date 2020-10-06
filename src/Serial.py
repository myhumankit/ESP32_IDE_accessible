"""
Module which has functions and classes to manage the connection and communication with the card
"""

from Packages import wx, os, time
from Constantes import *

class SerialRxEvent(wx.PyCommandEvent):
    eventType = SERIALRX

    def __init__(self, windowID, data):
        wx.PyCommandEvent.__init__(self, self.eventType, windowID)
        self.data = data
        print("DATA = ", end='')
        print(data)

    def Clone(self):
        return self.__class__(self.GetId(), self.data)

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
    Class with useful methods to manage Connection related with the frame
    """
    
    def __init__(self, frame):
        """Constructor for ManageConnection class

        :param frame: The MainWindow to get some properties
        :type frame: MainWindow class
        """
        
        self.frame = frame
        self.last_cmd = ""

    def SendEventRx(self, data):
        event = SerialRxEvent(self.frame.GetId(), data)
        self.frame.GetEventHandler().AddPendingEvent(event)

    def put_cmd(self, msg): 
        """Send a Python command to the connected card

        :param msg: command to send
        :type msg: str
        """
                  
        self.frame.serial.write(msg.encode('utf-8'))
        self.frame.serial.flush()
    
    def downloadRun(self, filename):
        """Execute the file gived in params on the MicroPython card

        :param filename: the path of the file to execute(root is the device connected)
        :type filename: str
        """
        time.sleep(1)
        self.put_cmd('\x03')
        self.put_cmd("exec(open(\'%s\').read(),globals())\r\n"%str(filename))
        
    def downloadFile(self, filepath ,filename):
        
        filepath = filepath.replace("\\","/")
        print("downloadFile===============================%s\n"%filename)
        if str(filename).find(".py")>=0:
            if str(filename).find(":")<0:
                afile=str(filename)
            else:
                print("error path")
                return False    
        else:
            print("error extension")
            return False    
        try:
            fileHandle=open(filepath,'rbU')
        except Exception as e:
            print("Error file : %s"%(e))
        self.put_cmd('\x03')
        self.frame.show_cmd = False
        startTime=time.time()
        self.frame.Shell.AppendText("Ready to download this file,please wait!")
        time.sleep(1)
        cmd = "myfile=open(\'%s\',\'w\')\r\n"%str(afile)
        self.put_cmd(cmd)
        time.sleep(1)
        #self.frame.Shell.SetValue("Ready to download this file,please wait!\n...")
        ##################
        #write(msg)
        ##################
        done=0
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
                    self.put_cmd(i)
                    time.sleep(0.001)
            else:
                done=1
        fileHandle.close()
        self.put_cmd("myfile.close()\r\n")
        return