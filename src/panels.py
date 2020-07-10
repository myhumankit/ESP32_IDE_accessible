import wx
import random
import wx.stc as stc

def Init_Panels(self):
    self.splitter_v = wx.SplitterWindow(self)
    self.splitter_h = wx.SplitterWindow(self.splitter_v)
    self.MyNotebook = NotebookPanel(self.splitter_h)
    self.FileTree = FileTreePanel(self.splitter_v)
    self.Shell = ShellPanel(self.splitter_h)
    self.splitter_v.SplitVertically(self.FileTree , self.splitter_h)
    self.splitter_h.SplitHorizontally(self.MyNotebook, self.Shell)
    self.splitter_v.SetMinimumPaneSize(50)
    self.splitter_h.SetMinimumPaneSize(50)

class MyEditor(stc.StyledTextCtrl):
    def __init__(self, parent):
        """ Constructor for Tab of Notebook
        
        :param parent: class parent (generally Frame or Panel)
        """
        stc.StyledTextCtrl.__init__(self, parent=parent, style=wx.TE_MULTILINE | wx.TE_WORDWRAP |wx.ALL|wx.EXPAND)
        colors = ["red", "blue", "gray", "yellow", "green"]
        self.SetBackgroundColour(random.choice(colors))
        #TODO: transform in class

class NotebookPanel(wx.Notebook):
    def __init__(self, parent):
        """ constructor to create a notebook multi-tabs
        
        :param training_dir: path of training directory with subdirectories
         '/ham' and '/spam'
        """
        wx.Notebook.__init__(self, parent=parent,style=wx.EXPAND|wx.ALL)
        self.tab_num = 1
        TabOne = MyEditor(self)
        self.SetBackgroundColour("Purple")
        self.AddPage(TabOne, "Tab 1", select=True)

class FileTreePanel(wx.Panel):
    def __init__(self, parent):
        """ inits Spamfilter with training data
        
        :param training_dir: path of training directory with subdirectories
         '/ham' and '/spam'
        """
        wx.Panel.__init__(self, parent=parent)
        self.SetBackgroundColour("BLUE")
        
class ShellPanel(wx.Panel):
    def __init__(self, parent):
        """ inits Spamfilter with training data
        
        :param training_dir: path of training directory with subdirectories
         '/ham' and '/spam'
        """
        wx.Panel.__init__(self, parent=parent)
        self.SetBackgroundColour("Green")