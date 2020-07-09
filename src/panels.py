import wx

def Init_Panels(self):
    self.splitter_v = wx.SplitterWindow(self)
    self.splitter_h = wx.SplitterWindow(self.splitter_v)
    leftP = LeftPanel(self.splitter_h)
    rightP = RightPanel(self.splitter_v)
    bottomP = BottomPanel(self.splitter_h)
    self.splitter_v.SplitVertically(self.splitter_h, rightP)
    self.splitter_h.SplitHorizontally(leftP, bottomP)
    self.splitter_v.SetMinimumPaneSize(300)
    self.splitter_h.SetMinimumPaneSize(300)

class LeftPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)
        self.SetBackgroundColour("RED")
    
class RightPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.SetBackgroundColour("BLUE")

class BottomPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.SetBackgroundColour("Green")