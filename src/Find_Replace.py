import wx

class Find_Replace_dlg(wx.FindReplaceDialog):
    def __init__(self, parent, data):
        wx.FindReplaceDialog.__init__(parent, data, title="Find/Replace")
        self.BackgroundColour = "Red"