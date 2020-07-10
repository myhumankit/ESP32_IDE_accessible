import wx
from Menus import *
from Panels import * 

class MainWindow(wx.Frame):
    """A naive Bayesian spam filter"""
    def __init__(self, name):
        """ inits Spamfilter with training data
        
        :param training_dir: path of training directory with subdirectories
         '/ham' and '/spam'
        """       
        wx.Frame.__init__(self, None, 1, title = name, size = (800,400))
        Init_Top_Menu(self)
        Init_ToolBar(self)
        Init_Panels(self)

class Myapp(wx.App):
    """ inits Spamfilter with training data"""
    def OnInit(self):
        """ inits Spamfilter with training data
        
        :param training_dir: path of training directory with subdirectories
         '/ham' and '/spam'
        """
        window = MainWindow("Menus")
        window.Show()
        self.SetTopWindow(window)
        return True

app = Myapp()
app.MainLoop()