import wx
import random
import wx.stc as stc
import os
import wx.py as pysh
import wx.lib.agw.flatnotebook as fnb
from Editor_Style import *

def Init_Panels(frame):
    """Inits the three differents regions(treeCtrl, Notebook, Shell) in the MainWindow
        ------------------
        |  |             |
        |  |     1       |
        | 3|-------------|
        |  |     2       |
        |  |             |
        ------------------
    :param frame: MainWindow or window to split
    :type frame: MainWindow or other panel
    """    
    style = wx.SP_3D | wx.SP_NO_XP_THEME | wx.SP_PERMIT_UNSPLIT | wx.SP_LIVE_UPDATE
    frame.splitter_v = wx.SplitterWindow(frame, style=style)
    frame.splitter_h = wx.SplitterWindow(frame.splitter_v, style=style)
    frame.MyNotebook = NotebookPanel(frame.splitter_h)
    frame.FileTree = FileTreePanel(frame.splitter_v)
    frame.Shell = ShellPanel(frame.splitter_h)
    frame.splitter_v.SplitVertically(frame.FileTree , frame.splitter_h, 200)
    frame.splitter_h.SplitHorizontally(frame.MyNotebook, frame.Shell, 400)

class MyEditor(pysh.editwindow.EditWindow):
    """Customizable Editor page

    :param pysh.edit ...: Editor Model customizable
    :type pysh: 
    """    
    def __init__(self, parent):
        """ Constructor of a Tab from Notebook
        
        :param parent: NotebookPanel class
        """
        pysh.editwindow.EditWindow.__init__(self, parent=parent)
        self.id = parent.tab_num
        self.setDisplayLineNumbers(True)
        self.SetLexer(wx.stc.STC_LEX_PYTHON)
        self.SetFontQuality(stc.STC_EFF_QUALITY_LCD_OPTIMIZED)
        self.SetUseAntiAliasing(True)
        self.filename = ""
        self.directory = ""
        self.saved = False
        self.last_save = ""
        Init_Editor_base(self)
        Change_lexer_style(self)
        #self.StyleClearAll()

    def OnFindReplace(self):
        print(self.GetValue())

class NotebookPanel(fnb.FlatNotebook):
    def __init__(self, parent):
        """ constructor to create a notebook multi-tabs
        
        :param parent: path of training
         '/ham' and '/spam'
        """
        style = fnb.FNB_NO_TAB_FOCUS | fnb.FNB_FF2
        fnb.FlatNotebook.__init__(self, parent=parent, style=style)
        self.parent = parent
        self.tab_num = 0
        self.data = ""
        self.dlg = None
        
#          self.m_auinotebook1.Bind( wx.aui.EVT_AUINOTEBOOK_PAGE_CLOSED, self.OnAuiNotebookPageClose )

# def OnAuiNotebookPageClose( self, event ):
#     auinotebook = event.GetEventObject()
#     page_idx = event.GetSelection()
#     auinotebook.RemovePage(page_idx)
#     auinotebook.DeletePage(page_idx)

class FileTreePanel(wx.GenericDirCtrl):
    def __init__(self, parent):
        """constructor for the File/dir Controller on the left
        
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