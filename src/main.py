from Packages import *
from menus import *
from panels import *
from Serial import *
from Constantes import *
from Utilitaries import *
from Shortcuts import InitShortcuts
from BurnFirmware import FirmwareManager
from Install_fonts import Install_fonts

#TODO: change focus when new editor tab

class MainWindow(wx.Frame):
    """MainWindow of the app which will contains all the children classes and custom functions

    :param wx.Frame: see https://wxpython.org/Phoenix/docs/html/wx.Frame.html
    """    
    def __init__(self, name, size):
        """MainWindow constructor

        :param name: name of the window
        :type name: str
        :param size: define dimensions of the window (width, height)
        :type size: tuple(int, int)
        """              
        wx.Frame.__init__(self, None, 1, title = name, size = size)
        self.SetIcon(wx.Icon("./img/Icone.png"))
        self.__set_properties__()
        e = wx.FontEnumerator()
        e.EnumerateFacenames()
        elist= e.GetFacenames()
        
    def __set_properties__(self):
        self.serial = serial.Serial()
        self.serial.timeout = 0.5
        self.time_to_send = 0.5   # make sure that the alive event can be checked from time to time
        self.settings = TerminalSetup()  # placeholder for the settings
        self.thread = None
        self.alive = threading.Event()
        #####
        self.messycode=b''
        self.keyPressMsg=''
        self.recvdata=""
        self.show_cmd = True
        self.connected = False
        self.Shell_text = ""
        self.get_cmd = False
        self.cmd_return = ""
        #####
        self.who_is_focus = 0
        self.top_menu = Init_Top_Menu(self)
        self.statusbar = MyStatusBar(self)
        self.serial_manager = ManageConnection(self)
        self.voice_on = True
        self.firmware_manager = FirmwareManager()
        
        Init_Panels(self)
        Init_ToolBar(self)
        InitShortcuts(self)
        
        self.__attach_events()
         
    def __attach_events(self):
        self.Bind(EVT_SERIALRX, self.OnSerialRead)
        self.Shell.Bind(wx.EVT_CHAR, self.OnKey)

    def StartThread(self):
        """Start the receiver thread"""
        self.thread = threading.Thread(target=self.ComPortThread)
        self.thread.setDaemon(1)
        self.alive.set()
        self.thread.start()
        self.serial.rts = True
        self.serial.dtr = True

    def StopThread(self):
        """Stop the receiver thread, wait until it's finished."""
        if self.thread is not None:
            self.alive.clear()          # clear alive event for thread
            self.thread.join()          # wait until thread has finished
            self.thread = None

    def OnKey(self, event):
        """\
        Key event handler. If the key is in the ASCII range, write it to the
        serial port. Newline handling is also done here.
        """
        code = event.GetUnicodeKey()
        if code < 256:
            code = event.GetKeyCode()
        if code == 13:                      # is it a newline? (check for CR which is the RETURN key)
            self.serial.write(b'\n')     # send LF
        char = chr(code)
        self.serial.write(char.encode('UTF-8', 'replace'))

    def ReadCmd(self, data):
        """Get the return of the cmd sent to the MicroPython card

        :param data: The commande sent
        :type data: str
        :return: the return of the command sent
        :rtype: str
        """
        b = self.serial.read(self.serial.in_waiting)
        self.is_data = False
        if b:
            self.is_data  = True
            # newline transformation
            if self.settings.newline == NEWLINE_CR:
                b = b.replace(b'\r', b'\n')
            elif self.settings.newline == NEWLINE_LF:
                pass
            elif self.settings.newline == NEWLINE_CRLF:
                b = b.replace(b'\r\n', b'\n')
        #self.serial_manager.SendEventRx(b)
        self.OnSerialRead(b)
    
        return GetCmdReturn(self.Shell_text, data)

    def OnSerialRead(self, data):
        """Handle input from the serial port."""
        print(self.show_cmd)
        #data = event.data
        if type(data) is bytes:
            print("Text red bytes = " + data.decode('UTF-8', 'replace'))
        else:
            print("Text red = " + data)
        
        if data == b'\x08': #backspace
            txt = self.Shell.GetValue()
            cursor = self.Shell.GetInsertionPoint()
            self.Shell.SetValue(txt[:-1])
            self.Shell_text = self.Shell_text[:-1]
            self.Shell.SetInsertionPoint(cursor)
        elif data == b'\x1b[K':
            pass
        else:
            self.Shell_text += data.decode('UTF-8', 'ignore')
            if self.show_cmd == True:
                asyncio.run(self.Shell.Asyncappend(data.decode('UTF-8', 'ignore')))

    def ComPortThread(self):
        """\
        Thread that handles the incoming traffic. Does the basic input
        transformation (newlines) and call an OnSerialRead
        """
        while self.alive.isSet():
            #print("J'y passe")
            b = self.serial.read(self.serial.in_waiting)
            self.is_data = False
            if b and b != b'\x00':
                self.is_data  = True
                # newline transformation
                if self.settings.newline == NEWLINE_CR:
                    b = b.replace(b'\r', b'\n')
                elif self.settings.newline == NEWLINE_LF:
                    pass
                elif self.settings.newline == NEWLINE_CRLF:
                    b = b.replace(b'\r\n', b'\n')
                #self.serial_manager.SendEventRx(b)
                self.OnSerialRead(b)

    def ChangeStatus(self):
        """Actualize the Status Bar

        :param evt: Event binded to trigger the function
        :type evt: wx.Event https://wxpython.org/Phoenix/docs/html/wx.Event.html
        """
        if self.connected:
            self.statusbar.SetStatusText("Status: %s %s %s"%("Connected",self.serial_manager.card, self.serial_manager.version), 1)
        else:
            self.statusbar.SetStatusText("Status: %s"%"Not Connected", 1)

    def OnChangeFocus(self, event):
        """Allow to navigate in the differents region of the Frame after an event

        :param evt: Event binded to trigger the function
        :type evt: wx.Event https://wxpython.org/Phoenix/docs/html/wx.Event.html
        """
        widgets = [self.FileTree, self.MyNotebook.GetCurrentPage(), self.Shell]
        if self.who_is_focus == 1 and widgets[self.who_is_focus] == None:
            self.who_is_focus += 1
            widgets[self.who_is_focus].SetFocus()
            return
        widgets[self.who_is_focus].SetFocus()
        if self.who_is_focus < 2:
            self.who_is_focus += 1
        else:
            self.who_is_focus = 0
    
    def OnZoomIn(self, evt):
        """Zoom On which affects the EditWindow panel

        :param evt: Event binded to trigger the function
        :type evt: wx.Event https://wxpython.org/Phoenix/docs/html/wx.Event.html
        """
        page = self.MyNotebook.GetCurrentPage()
        if page != None:
            page.ZoomIn()
        if self.Shell.HasFocus() == True:
            self.Shell.ZoomIn()

    def OnZoomOut(self, evt):
        """Zoom Out which affects the EditWindow panel

        :param evt: Event binded to trigger the function
        :type evt: wx.Event https://wxpython.org/Phoenix/docs/html/wx.Event.html
        """
        page = self.MyNotebook.GetCurrentPage()
        if page != None:
            page.ZoomOut()
        if self.Shell.HasFocus() == True:
            self.Shell.ZoomOut()

    def OnStatus(self, evt):
        """Set the Focus on the Status Bar

        :param evt: Event binded to trigger the function
        :type evt: wx.Event https://wxpython.org/Phoenix/docs/html/wx.Event.html
        """
        self.statusbar.SetFocus()
        speak(self, self.statusbar.GetStatusText(1))
            
class Myapp(wx.App):
    """Minimal class to launch the app

    :param wx.App: https://wxpython.org/Phoenix/docs/html/wx.App.html
    """    
    def OnInit(self):
        """Special constructor (do not modify) which affect the Mainwindow to the App

        :return: a boolean to stop or continue the 
        :rtype: Bool
            --if False exit or error
            --if True the app works
        """        
        wx.InitAllImageHandlers()
        window = MainWindow("Blind-IDE", (800, 600))
        self.SetTopWindow(window)
        window.Show()
        return True

if __name__ == "__main__":
    sys.stdout = sys.__stdout__
    if sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):
        FONTDIRS=os.path.join(os.environ['WINDIR'],'Fonts')
        fonts=os.listdir(FONTDIRS)
        flags=False
    for filename in fonts:
        if(filename.find('FiraCode')==0):
            flags=True
            break
    if flags is False:  
        try:
            fonts = ["./FiraCode-Medium.ttf", "./FiraCode-Regular.ttf", "./FiraCode-Retina.ttf", "./FiraCode-Light.ttf"]
            Install_fonts(fonts)
        except:
            print("install ttf false.")
    app = Myapp()
    app.MainLoop()