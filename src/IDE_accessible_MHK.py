from packages import *
from menus import *
from panels import *
from my_serial import *
from constantes import *
from utilitaries import *
from shortcuts import InitShortcuts
from firmware import FirmwareManager
from install_fonts import Install_fonts

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
        self.serial.timeout = 0.01
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
        self.shell_text = ""
        self.get_cmd = False
        self.cmd_return = ""
        #####
        self.who_is_focus = 0
        self.theme = 'Dark Theme'
        self.top_menu = init_top_menu(self)
        self.statusbar = create_status_bar(self)
        self.serial_manager = ManageConnection(self)
        self.voice_on = True
        self.firmware_manager = FirmwareManager()
        
        create_panels(self)
        init_toolbar(self)
        InitShortcuts(self)
        
        self.__attach_events()
         
    def __attach_events(self):
        self.shell.Bind(wx.EVT_CHAR, self.OnKey)

    def start_thread_serial(self):
        """Start the receiver thread"""
        self.thread = threading.Thread(target=self.thread_listen_port)
        self.thread.setDaemon(1)
        self.alive.set()
        self.thread.start()
        self.serial.rts = True
        self.serial.dtr = True

    def stop_thread_serial(self):
        """Stop the receiver thread, wait until it's finished."""
        if self.thread is not None:
            self.alive.clear()          # clear alive event for thread
            self.thread.join()          # wait until thread has finished
            self.thread = None

    def read_cmd(self, data):
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
        self.serial_read_data(b)
    
        return GetCmdReturn(self.shell_text, data)

    def serial_read_data(self, data):
        """Handle input from the serial port."""
        print(self.show_cmd)
        #data = event.data
        if type(data) is bytes:
            print("Text red bytes = " + data.decode('UTF-8', 'replace'))
        else:
            print("Text red = " + data)
        
        if data == b'\x08': #backspace
            txt = self.shell.GetValue()
            cursor = self.shell.GetInsertionPoint()
            self.shell.SetValue(txt[:-1])
            self.shell_text = self.shell_text[:-1]
            self.shell.SetInsertionPoint(cursor)
        elif data == b'\x1b[K':
            pass
        else:
            self.shell_text += data.decode('UTF-8', 'ignore')
            if self.show_cmd == True:
                asyncio.run(self.shell.Asyncappend(data.decode('UTF-8', 'ignore')))

    def thread_listen_port(self):
        """\
        Thread that handles the incoming traffic. Does the basic input
        transformation (newlines) and call an serial_read_data
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
                self.serial_read_data(b)

    def actualize_status_bar(self):
        """Actualize the Status Bar

        :param evt: Event binded to trigger the function
        :type evt: wx.Event https://wxpython.org/Phoenix/docs/html/wx.Event.html
        """
        if self.connected:
            self.statusbar.SetStatusText("Status: %s %s %s"%("Connected",self.serial_manager.card, self.serial_manager.version), 1)
        else:
            self.statusbar.SetStatusText("Status: %s"%"Not Connected", 1)

    def OnChangeFocus(self, evt):
        """Allow to navigate in the differents region of the Frame after an event

        :param evt: Event binded to trigger the function
        :type evt: wx.Event https://wxpython.org/Phoenix/docs/html/wx.Event.html
        """
        widgets = [self.tree_panel, self.notebook.GetCurrentPage(), self.shell]
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
        page = self.notebook.GetCurrentPage()
        if page != None:
            page.ZoomIn()
        if self.shell.HasFocus() == True:
            self.shell.ZoomIn()

    def OnZoomOut(self, evt):
        """Zoom Out which affects the EditWindow panel

        :param evt: Event binded to trigger the function
        :type evt: wx.Event https://wxpython.org/Phoenix/docs/html/wx.Event.html
        """
        page = self.notebook.GetCurrentPage()
        if page != None:
            page.ZoomOut()
        if self.shell.HasFocus() == True:
            self.shell.ZoomOut()

    def OnStatus(self, evt):
        """Set the Focus on the Status Bar

        :param evt: Event binded to trigger the function
        :type evt: wx.Event https://wxpython.org/Phoenix/docs/html/wx.Event.html
        """
        self.statusbar.SetFocus()
        speak(self, self.statusbar.GetStatusText(1))

    def OnKey(self, evt):
        """\
        Key event handler. If the key is in the ASCII range, write it to the
        serial port. Newline handling is also done here.
        """
        code = evt.GetUnicodeKey()
        if code < 256:
            code = evt.GetKeyCode()
        if code == 13:                      # is it a newline? (check for CR which is the RETURN key)
            self.serial.write(b'\n')     # send LF
        char = chr(code)
        self.serial.write(char.encode('UTF-8', 'replace'))

class MyApp(wx.App):
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
        window = MainWindow("Blind-IDE V1.3.3", (800, 600))
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
            fonts = ["./FiraCode-Medium.ttf", "./FiraCode-Regular.ttf", \
                     "./FiraCode-Retina.ttf", "./FiraCode-Light.ttf"]
            Install_fonts(fonts)
        except:
            print("install ttf false.")
    app = MyApp()
    app.MainLoop()