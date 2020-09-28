from Packages import *
from menus import *
from panels import *
from Serial import *
from InitConfig import Preferences
from Constantes import *

#TODO: change focus when new editor tab

def InitShortcuts(frame):
    """Initiate shortcuts of the Application with wx.Accelerator Table
    
        :param frame: parent class to bind events)
        :Type frame: MainWindow()
    """
    def InitF6(frame):
        """F6 to navigate between regions

        :param frame: see InitShorcuts->param
        :type frame: idem
        :return: entrie(here tuple) for AcceleratorTable
        :rtype: tuple(int, int, int)
        """        
        frame.Bind(wx.EVT_MENU, frame.OnChangeFocus, id=wx.ID_MOVE)
        return (wx.ACCEL_NORMAL,  wx.WXK_F6, wx.ID_MOVE)

    def InitCTRL_plus(frame):
        """Ctrl + = to zoom on the editor

        :param frame: see InitShorcuts->param
        :type frame: idem
        :return: entrie(here tuple) for AcceleratorTable
        :rtype: tuple(int, int, int)
        """
        frame.Bind(wx.EVT_MENU, frame.OnZoomIn, id=wx.ID_ZOOM_IN)
        return (wx.ACCEL_CTRL,  ord('='), wx.ID_ZOOM_IN)        

    def InitCTRL_moins(frame):
        """Ctrl + - to zoom on the editor

        :param frame: see InitShorcuts->param
        :type frame: idem
        :return: entrie(here tuple) for AcceleratorTable
        :rtype: tuple(int, int, int)
        """
        frame.Bind(wx.EVT_MENU, frame.OnZoomOut, id=wx.ID_ZOOM_OUT)
        return (wx.ACCEL_CTRL,  ord('-'), wx.ID_ZOOM_OUT)        

    accel_tbl = wx.AcceleratorTable([InitF6(frame), InitCTRL_plus(frame), InitCTRL_moins(frame)])
    frame.SetAcceleratorTable(accel_tbl)

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
        
    def __set_properties__(self):
        self.serial = serial.Serial()
        self.serial.timeout = 0.5   # make sure that the alive event can be checked from time to time
        self.settings = TerminalSetup()  # placeholder for the settings
        self.thread = None
        self.alive = threading.Event()
        #####
        self.messycode=b''
        self.keyPressMsg=''
        self.recvdata=""
        self.show_cmd = True
        self.connected = False
        #####
        self.who_is_focus = 0
        self.top_menu = Init_Top_Menu(self)
        self.preferences = Preferences(self)
        self.statusbar = MyStatusBar(self)
        self.serial_manager = ManageConnection(self)
        self.voice_on = True
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

    def OnSerialRead(self, event):
        """Handle input from the serial port."""
        data = event.data
        if event.data == "not_show_cmd":
            self.show_cmd = False
            return
        elif event.data == "show_cmd":
            self.show_cmd = True
            return
        print("Text red = " + data.decode('UTF-8', 'replace'))
        if data == b'\x08': #backspace
            txt = self.Shell.GetValue()
            cursor = self.Shell.GetInsertionPoint()
            self.Shell.SetValue(txt[:-1])
            self.Shell.SetInsertionPoint(cursor)
        elif data == b'\x1b[K':
            pass
        else:
            if self.show_cmd == True:
                self.Shell.AppendText(event.data.decode('UTF-8', 'ignore'))

    def ComPortThread(self):
        """\
        Thread that handles the incoming traffic. Does the basic input
        transformation (newlines) and generates an SerialRxEvent
        """
        while self.alive.isSet():
            b = self.serial.read(self.serial.in_waiting or 1)
            if b:
                # newline transformation
                if self.settings.newline == NEWLINE_CR:
                    b = b.replace(b'\r', b'\n')
                elif self.settings.newline == NEWLINE_LF:
                    pass
                elif self.settings.newline == NEWLINE_CRLF:
                    b = b.replace(b'\r\n', b'\n')
                event = SerialRxEvent(self.GetId(), b)
                self.GetEventHandler().AddPendingEvent(event)

    def ChangeStatus(self, evt):
        print("SALUT MON POTE")
        page = self.MyNotebook.GetCurrentPage()
        line = page.GetCurrentLine()
        margin = page.GetLineIndentation(line)
        end = page.GetLineIndentPosition(line)
        print(line)
        self.statusbar.SetStatusText("%s/%s"%(margin, end), 1)

    def OnChangeFocus(self, event):
        """Allow to navigate in the differents region of the Frame after an event

        :param event: Passive arg but important for binding events
        :type event: None
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
        page = self.MyNotebook.GetCurrentPage()
        if page != None:
            page.ZoomIn()
        if self.Shell.HasFocus() == True:
            self.Shell.ZoomIn()

    def OnZoomOut(self, evt):
        page = self.MyNotebook.GetCurrentPage()
        if page != None:
            page.ZoomOut()
        if self.Shell.HasFocus() == True:
            self.Shell.ZoomOut()
            
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
    app = Myapp()
    app.MainLoop()