import wx
from Menus import *
from Panels import * 

#TODO: change focus when new editor tab

wx.ID_MOVE = 455


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
        self.who_is_focus = 0
        #main_sizer = wx.BoxSizer(wx.VERTICAL)
        #main_sizer.Add(Init_Top_Menu(self), 0, wx.EXPAND)
        #self.SetIcon(wx.Icon("./img/Icone.png"))
        self.top_menu = Init_Top_Menu(self)
        Init_ToolBar(self)
        Init_Panels(self)
        InitShortcuts(self)
        
        
        #self.SetSizer(main_sizer)
        #main_sizer.Layout()

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
        window = MainWindow("Blind-IDE", (1920, 1080))
        window.Show()
        self.SetTopWindow(window)
        return True

app = Myapp()
app.MainLoop()