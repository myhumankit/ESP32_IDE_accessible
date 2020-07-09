import wx

from menus import *
from panels import *

def Init_Top_Menu(self):
    self.top_menu = TopMenu(self)
    self.SetMenuBar(self.top_menu)

class MainWindow(wx.Frame):
    def __init__(self, name):       
        wx.Frame.__init__(self, None, 1, title = name, size = (1900,1200))
        Init_Top_Menu(self)
        InitToolBar(self)
        Init_Panels(self)

class Myapp(wx.App):
    def OnInit(self):
        window = MainWindow("Menus")
        window.Show()
        self.SetTopWindow(window)
        return True

app = Myapp()
app.MainLoop()