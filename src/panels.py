import wx
import random
import wx.stc as stc
import os
import wx.py as pysh

def Init_Panels(self):
    self.splitter_v = wx.SplitterWindow(self, style=wx.SP_3D)
    self.splitter_h = wx.SplitterWindow(self.splitter_v, size=self.GetBestSize())
    self.MyNotebook = NotebookPanel(self.splitter_h)
    self.FileTree = FileTreePanel(self.splitter_v)
    self.Shell = ShellPanel(self.splitter_h)
    self.splitter_v.SplitVertically(self.FileTree , self.splitter_h, 200)
    self.splitter_h.SplitHorizontally(self.MyNotebook, self.Shell, 400)

class MyEditor(pysh.editwindow.EditWindow):
    def __init__(self, parent):
        """ Constructor for Tab of Notebook
        
        :param parent: class parent (generally Frame or Panel)
        """
        pysh.editwindow.EditWindow .__init__(self, parent=parent)
        #TODO: s'occuper du focus wx.CallAfter(self.SetFocus)
        self.setDisplayLineNumbers(True)
        self.filename = ""
        self.directory = ""
        self.saved = False
        self.last_save = ""
        #self.StyleSetBackground(wx.stc.STC_STYLE_DEFAULT, "Grey")
    def OnFindReplace(self):
        print(self.GetValue())

class NotebookPanel(pysh.editor.EditorNotebook):
    def __init__(self, parent):
        """ constructor to create a notebook multi-tabs
        
        :param training_dir: path of training directory with subdirectories
         '/ham' and '/spam'
        """
        pysh.editor.EditorNotebook.__init__(self, parent=parent)
        self.parent = parent
        self.tab_num = 0
        self.data = ""
        self.dlg = None
        TabOne = MyEditor(self)
        self.SetForegroundColour("Black")
        self.SetBackgroundColour("Grey")
        self.AddPage(TabOne, "Tab 1", select=True)

class FileTreePanel(wx.GenericDirCtrl):
    def __init__(self, parent):
        """ inits Spamfilter with training data
        
        :param training_dir: path of training directory with subdirectories
         '/ham' and '/spam'
        """
        wx.GenericDirCtrl.__init__(self, parent = parent)
        
class ShellPanel(pysh.editor.Shell):
    def __init__(self, parent):
        """ inits Spamfilter with training data
        
        :param training_dir: path of training directory with subdirectories
         '/ham' and '/spam'
        """
        pysh.editor.Shell.__init__(self, parent=parent)