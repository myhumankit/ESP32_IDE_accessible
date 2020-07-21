import wx
from Menus import *
from Panels import * 

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
        :rtype: tuple 
        """        
        randomId = wx.NewId()
        frame.Bind(wx.EVT_MENU, frame.OnChangeFocus, id=randomId)
        return (wx.ACCEL_NORMAL,  wx.WXK_F6, randomId )
    accel_tbl = wx.AcceleratorTable([InitF6(frame)])
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
        #self.SetIcon(wx.Icon("./img/Icone.png"))
        self.AcceleratorTable
        Init_Top_Menu(self)
        Init_ToolBar(self)
        Init_Panels(self)
        InitShortcuts(self)

    def OnChangeFocus(self, event):
        """Allow to navigate in the differents region of the Frame after an event

        :param event: Passive arg but important for binding events
        :type event: None
        """        
        widgets = [self.FileTree, self.MyNotebook.GetCurrentPage(), self.Shell]
        widgets[self.who_is_focus].SetFocus()
        if self.who_is_focus < 2:
            self.who_is_focus += 1
        else:
            self.who_is_focus = 0
            
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