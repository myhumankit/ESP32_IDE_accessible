import wx
from Menus import *
from Panels import * 

#TODO: change focus when new editor tab

def InitShortcuts(self):
    randomId = wx.NewId()
    self.Bind(wx.EVT_MENU, self.OnChangeFocus, id=randomId)
    change_focus = (wx.ACCEL_NORMAL,  wx.WXK_F6, randomId )
    accel_tbl = wx.AcceleratorTable([change_focus])
    self.SetAcceleratorTable(accel_tbl)
        
class MainWindow(wx.Frame):
    """Main window of the application"""
    def __init__(self, name):
        """ inits Spamfilter with training data
        
        :param name of the window: path of training directory with subdirectories
         '/ham' and '/spam'
        """       
        wx.Frame.__init__(self, None, 1, title = name, size = (1600,900))
        self.who_is_focus = 0

        Init_Top_Menu(self)
        Init_ToolBar(self)
        Init_Panels(self)
        InitShortcuts(self)

    def OnChangeFocus(self, event):
        widgets = [self.FileTree, self.MyNotebook.GetCurrentPage(), self.Shell]
        widgets[self.who_is_focus].SetFocus()
        if self.who_is_focus < 2:
            self.who_is_focus += 1
        else:
            self.who_is_focus = 0
            
class Myapp(wx.App):
    """ inits The Minimal App"""
    def OnInit(self):
        window = MainWindow("Blind-IDE")
        window.Show()
        self.SetTopWindow(window)
        return True

app = Myapp()
app.MainLoop()