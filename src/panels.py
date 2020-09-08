import wx
import random
import wx.stc as stc
import os
import wx.py as pysh
import wx.lib.agw.flatnotebook as fnb
from Editor_Style import *
from Find_Replace import *

import codecs
import serial
import threading
import wxSerialConfigDialog

NEWLINE_CR = 0
NEWLINE_LF = 1
NEWLINE_CRLF = 2
ID_CLEAR = wx.NewId()
ID_SAVEAS = wx.NewId()
ID_SETTINGS = wx.NewId()
ID_TERM = wx.NewId()
ID_EXIT = wx.NewId()
ID_RTS = wx.NewId()
ID_DTR = wx.NewId()

#black #FFFF00 
#orange #FF9933
#white #FFFFFF
#violet #ea2cd8
#vert #07cc1e
#jaune #f0f20f
#bleu foncé #434885
th_dark = [
        '#f0f20f', #strings editor 0 
        '#07cc1e', #class editor 1
        '#ea2cd8', #word editor 2
        '#00ffdf', #character editor 3
        '#07cc1e', #def editor 4
        '#ea2cd8', #decorator editor 5
        '#FFFFFF', #default editor 6
        '#FFFFFF', #identifier editor 7
        '#FF9933', #Number editor 8
        '#ea2cd8', #Operator editor 9
        wx.YELLOW, #str EOL editor 11
        '#f0f20f', #triple editor 10
        '#f0f20f', #triple double editor 12
        '#ea2cd8', #word 2 13
        '#434885', #CommentLine 14
        '#f0f20f', #Comment block + strings 15
        ]

frame_dark = ["Black", #Background
           "White" #font linenumber
           ]

th_light = [
        '#44ea1e', #strings editor 0 
        '#d08c25', #class editor 1
        '#db62f2', #word editor 2
        '#131313', #character editor 3
        '#1626ff', #def editor 4
        '#1626ff', #decorator editor 5
        '#131313', #default editor 6
        '#131313', #identifier editor 7
        '#d08c25', #Number editor 8
        '#131313', #Operator editor 9
        '#44ea1e', #str EOL editor 11
        '#44ea1e', #triple editor 10
        '#44ea1e', #triple double editor 12
        '#db62f2', #word 2 13
        '#9798a3', #CommentLine 14
        '#44ea1e', #Comment block + strings 15
]
frame_light = ["White" , "Black"]

th_astro = [
        '#2e8942', #strings editor 0 
        '#d08c25', #class editor 1
        '#db62f2', #word editor 2
        '#131313', #character editor 3
        '#1626ff', #def editor 4
        '#1626ff', #decorator editor 5
        '#131313', #default editor 6
        '#131313', #identifier editor 7
        '#d08c25', #Number editor 8
        '#131313', #Operator editor 9
        '#2e8942', #str EOL editor 11
        '#2e8942', #triple editor 10
        '#2e8942', #triple double editor 12
        '#db62f2', #word 2 13
        '#9798a3', #CommentLine 14
        '#2e8942', #Comment block + strings 15
]
frame_astro = ["White", "Black"]

themes = [[th_dark, frame_dark],
          [th_light, frame_light],
          [th_astro, frame_astro]
          ]
 
py_style = [
            wx.stc.STC_P_STRING,
            wx.stc.STC_P_CLASSNAME,
            wx.stc.STC_P_WORD,
            wx.stc.STC_P_CHARACTER,
            wx.stc.STC_P_DEFNAME,
            wx.stc.STC_P_DECORATOR,
            wx.stc.STC_P_DEFAULT,
            wx.stc.STC_P_IDENTIFIER,
            wx.stc.STC_P_NUMBER,
            wx.stc.STC_P_OPERATOR,
            wx.stc.STC_P_STRINGEOL,
            wx.stc.STC_P_TRIPLE,
            wx.stc.STC_P_TRIPLEDOUBLE,
            wx.stc.STC_P_WORD2,
            wx.stc.STC_P_COMMENTLINE,
            wx.stc.STC_P_COMMENTBLOCK,
            ]

def Init_Panels(frame):
    """Inits the three differents regions(treeCtrl, Notebook, Shell) in the MainWindow
    
    :param frame: MainWindow or window to split
    :type frame: MainWindow or other panel
    """    
    style = wx.SP_3D | wx.SP_NO_XP_THEME | wx.SP_PERMIT_UNSPLIT | wx.SP_LIVE_UPDATE
    frame.splitter_v = wx.SplitterWindow(frame, style=style, name="Dimension")
    frame.splitter_h = wx.SplitterWindow(frame.splitter_v, style=style, name="DIMENSION ALL")
    frame.MyNotebook = NotebookPanel(frame.splitter_h, frame)
    frame.FileTree = FileTreePanel(frame.splitter_v, frame)
    frame.Shell = ShellPanel(frame.splitter_h, frame)
    frame.splitter_v.SplitVertically(frame.FileTree , frame.splitter_h, 200)
    frame.splitter_h.SplitHorizontally(frame.MyNotebook, frame.Shell, 400)

class MyEditor(pysh.editwindow.EditWindow):
    """Customizable Editor page

    :param pysh.edit ...: Editor Model customizable
    :type pysh: 
    """    
    def __init__(self, parent , topwindow):
        """ Constructor of a Tab from Notebook
        
        :param parent: NotebookPanel class
        """
        pysh.editwindow.EditWindow.__init__(self, parent=parent)
        self.topwindow = topwindow
        self.id = parent.tab_num
        self.filename = ""
        self.directory = ""
        self.saved = False
        self.last_save = ""
        self.theme = parent.theme
        self.findData = wx.FindReplaceData()
        self.txt = ""
        self.pos = 0
        self.size = 0
        
        
        print("PARENT THEME = " + str(parent.theme))
        self.SetMarginType(1, stc.STC_MARGIN_NUMBER)
        self.SetMarginWidth(1, 25)
        Init_Editor_base(self)
        Change_Theme(self, themes[self.theme], py_style)
        self.Bind(wx.EVT_TEXT, self.topwindow.ChangeStatus)
        self.Bind(wx.EVT_TEXT_ENTER, self.topwindow.ChangeStatus)
        
        ###############################################

    def BindFindEvents(self, win):
        win.Bind(wx.EVT_FIND, self.OnFind)
        win.Bind(wx.EVT_FIND_NEXT, self.OnFind)
        win.Bind(wx.EVT_FIND_REPLACE, self.OnFind)
        win.Bind(wx.EVT_FIND_REPLACE_ALL, self.OnFind)
        win.Bind(wx.EVT_FIND_CLOSE, self.OnFindClose)

    def OnShowFindReplace(self, evt=None):
        dlg = wx.FindReplaceDialog(self, self.findData, "Find & Replace", wx.FR_REPLACEDIALOG)

        self.BindFindEvents(dlg)
        dlg.Show(True)

    def OnFind(self, evt):
        self.txt = self.GetValue()
        map = {
            wx.wxEVT_COMMAND_FIND : "FIND",
            wx.wxEVT_COMMAND_FIND_NEXT : "FIND_NEXT",
            wx.wxEVT_COMMAND_FIND_REPLACE : "REPLACE",
            wx.wxEVT_COMMAND_FIND_REPLACE_ALL : "REPLACE_ALL",
            }

        et = evt.GetEventType()

        if et in map:
            evtType = map[et]
        if et in [wx.wxEVT_COMMAND_FIND_NEXT]:
            find_next(self, evt)
        if et in [wx.wxEVT_COMMAND_FIND_REPLACE]:
            replace(self, evt)
        if et in [wx.wxEVT_COMMAND_FIND_REPLACE_ALL]:
            while find_next(self, evt) == True:
                replace(self, evt)
        else:
            replaceTxt = ""

    def OnFindClose(self, evt):
        print("FindReplaceDialog closing...\n")
        evt.GetDialog().Destroy()

class NotebookPanel(fnb.FlatNotebook):
    def __init__(self, parent, topwindow):
        """ constructor to create a notebook multi-tabs
        
        :param parent: path of training
         '/ham' and '/spam'
        """
        style = fnb.FNB_FF2
        fnb.FlatNotebook.__init__(self, parent=parent, style=style, name="COUCOU")
        self.parent = parent
        self.topwindow = topwindow
        self.tab_num = 0
        self.data = ""
        self.dlg = None
        self.theme = 0
        self.SetTabAreaColour(wx.BLACK)
        Custom_Notebook(self, themes[self.theme][0])
        
class FileTreePanel(wx.GenericDirCtrl):
    def __init__(self, parent, frame):
        """constructor for the File/dir Controller on the left
        
        :param training_dir: path of training directory with subdirectories
         '/ham' and '/spam'
        """
        wx.GenericDirCtrl.__init__(self, parent = parent)
        self.frame = frame
        self.Bind(wx.EVT_DIRCTRL_FILEACTIVATED, self.OnOpenFile)
        font = wx.Font(pointSize = 20, family = wx.FONTFAMILY_SWISS, style = wx.FONTSTYLE_SLANT, weight = wx.FONTWEIGHT_BOLD,  
                      underline = False, faceName ="", encoding = 0)
        self.SetFont(font)
        theme = frame.MyNotebook.theme
        self.BackgroundColour = 'sky blue'
        #Custom_Tree_Ctrl(self, themes[theme][0])

    def OnOpenFile(self, evt):
        notebookP = self.frame.MyNotebook
        path = self.GetFilePath()
        file = os.path.split(path)
        directory = file[0]
        filename = file[1]
        filehandle = open(self.GetFilePath())
        # Check if a new tabe needs to be created to display contents of opened file
        if (notebookP.GetPageCount() == 1 
            and notebookP.GetCurrentPage().GetValue() == ""):
                notebookP.GetCurrentPage().SetValue(filehandle.read())
                notebookP.GetCurrentPage().filename = filename
                notebookP.GetCurrentPage().directory = directory
                notebookP.GetCurrentPage().last_save = notebookP.GetCurrentPage().GetValue()
                notebookP.GetCurrentPage().saved = True
        else:
            notebookP.tab_num += 1
            new_tab = MyEditor(notebookP)
            new_tab.filename = filename
            new_tab.directory = directory
            notebookP.AddPage(new_tab, filename, select = True)
            wx.CallAfter(new_tab.SetFocus)
            # Populate the tab with file contents
            new_tab.SetValue(filehandle.read())
            new_tab.last_save = new_tab.GetValue()
            new_tab.saved = True
            notebookP.SetPageText(notebookP.GetSelection(), filename)
            filehandle.close()
        
#TODO: add Set focus raccourci = maj + fin(flèche)
def MyStatusBar(frame):
    statusbar = frame.CreateStatusBar(2, style= wx.STB_ELLIPSIZE_MIDDLE)
    statusbar.SetBackgroundColour("RED")
    statusbar.SetStatusText("Status:%s"%frame.status_connection, 1)

class TerminalSetup:
    """
    Placeholder for various terminal settings. Used to pass the
    options to the TerminalSettingsDialog.
    """
    def __init__(self):
        self.echo = False
        self.unprintable = False
        self.newline = NEWLINE_CRLF

class ShellPanel(wx.TextCtrl):
    def __init__(self, parent, frame):
        """ inits Spamfilter with training data

        :param training_dir: path of training directory with subdirectories
         '/ham' and '/spam'
        """
        wx.TextCtrl.__init__(self, parent=parent, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.__set_properties__(frame)
        self.cursor = self.GetCaret()

    def __set_properties__(self, frame):
        self.top_window = frame
        self.SetName("Python Shell")
        self.SetFont(wx.Font(9, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, ""))
        #self.StyleSetBackground(wx.DIRCTRL_DEFAULT_STYLE, theme[0])
        #Change_Theme(self, themes[0], py_style)

    def append(self, text):
        #self.SetReadOnly(False)
        #self.SetValue(text)
        self.AddText(text)
        #self.SetReadOnly(True)