import random, os, codecs, threading, asyncio, sys, json
import Panels.wxSerialConfigDialog
import Panels.Device_tree as Tree

import wx.stc as stc
from Panels.Editor import MyEditor
import wx.lib.agw.flatnotebook as fnb
from editor_style import *
from find_replace import *
from constantes import *
from my_serial import SendCmdAsync, put_cmd

#TODO: rajouter le path workspace dans le json

def create_panels(main_window):
    """Inits the three differents regions(treeCtrl, Notebook, Shell) in the MainWindow
    
    :param main_window: MainWindow or window to split
    :type main_window: MainWindow or other panel
    """    
    style = wx.SP_3D | wx.SP_NO_XP_THEME | wx.SP_LIVE_UPDATE
    main_window.splitter_v = wx.SplitterWindow(main_window, style=style, name="Dimension")
    main_window.splitter_h = wx.SplitterWindow(main_window.splitter_v, style=style, name="DIMENSION ALL")
    main_window.notebook = NotebookPanel(main_window.splitter_h, main_window)
    main_window.device_tree = Tree.DeviceTree(main_window.splitter_v, main_window, "", "")
    main_window.shell = ShellPanel(main_window.splitter_h, main_window)
    main_window.splitter_v.SplitVertically(main_window.device_tree , main_window.splitter_h, 200)
    main_window.splitter_h.SplitHorizontally(main_window.notebook, main_window.shell, 400)
    main_window.splitter_h.SetMinimumPaneSize(20)
    main_window.splitter_v.SetMinimumPaneSize(20)
    

class NotebookPanel(fnb.FlatNotebook):
    """Customized Notebook class

    :param fnb.FlatNotebook: A class of notebook to derivate
    :type fnb.FlatNotebook: wx.lib.agw.flatnotebook.FlatNotebook
    """
    def __init__(self, parent, topwindow):
        """ constructor to create a notebook multi-tabs
        
        :param parent: Splitter window (unused in methods, just to init)
        :type parent: wx.SplitterWindow
        :param topwindow: MainWindow to use her attibuts
        :type parent: MainWindow class
        
        """
        style = fnb.FNB_FF2 | wx.FULL_REPAINT_ON_RESIZE | fnb.FNB_BACKGROUND_GRADIENT
        fnb.FlatNotebook.__init__(self, parent=parent, style=style, name="COUCOU")

        self.SetGradientColours(wx.BLACK, wx.WHITE, wx.BLACK)
        self.SetAGWWindowStyleFlag(fnb.FNB_X_ON_TAB | fnb.FNB_DROPDOWN_TABS_LIST | fnb.FNB_RIBBON_TABS)
        self.__set_properties(parent, topwindow)
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(fnb.EVT_FLATNOTEBOOK_PAGE_CHANGED, self.set_focus_editor)
        self.Bind(fnb.EVT_FLATNOTEBOOK_PAGE_CHANGING, self.set_focus_editor)
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.set_focus_editor)
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.set_focus_editor)
        self.custom_notebook("Dark Theme")

    def on_paint(self, event):
        """Paint a gradient color on the Notebook background

        :param event: Event to repaint the notebook background
        :type event: wx.Event
        """
        x = 0
        y = 0
        w, h = self.GetSize()
        try:
            self.dc = wx.PaintDC(self)
            file = open('./customize.json')
            theme = json.load(file)
            theme = theme[self.theme_choice]
            file.close()
            self.dc.GradientFillLinear((x, y, w, h), \
                theme['Panels Colors']['Background notebook gradient 2'], \
                theme['Panels Colors']['Background notebook gradient 1'])
        except Exception as e:
            print("Can't custom notebook background :", e)

    def __set_properties(self, parent, topwindow):
        """Set the properties and declare the variables of the instance
        
        :param parent: Splitter window (unused)
        :type parent: wx.SplitterWindow
        :param topwindow: the MainWindow in this case
        :type parent: MainWindow class
        """
        
        self.parent = parent
        self.topwindow = topwindow
        self.tab_num = 0
        self.data = ""
        self.dlg = None
        self.theme_choice = 'Dark Theme'
        
    def custom_notebook(self, theme):
        """Custom the Notebook according to the theme passed on args

        :param theme: The theme to apply
        :type theme: list
        """
        try:
            file = open("./customize.json")
            theme = json.load(file)
            file.close()
            theme = theme['Dark Theme']['Panels Colors']
            self.SetTabAreaColour("#D3D3D3")
            self.SetActiveTabColour(theme['Background active tab area'])
            #self.SetTabAreaColour(theme['Background tab area'])
            self.SetActiveTabTextColour(theme['Active tab text'])
            self.SetNonActiveTabTextColour(theme['Active tab text'])
        except Exception:
            print("Can't Customize Notebook")

    def set_focus_editor(self, evt):
        try:
            page = self.GetCurrentPage()
            page = self.GetTabArea()
            page.SetFocus()
        except Exception as e:
            print(e)

def create_status_bar(main_window):
    statusbar = main_window.CreateStatusBar(2, style= wx.STB_ELLIPSIZE_MIDDLE)
    statusbar.SetBackgroundColour("Grey")
    if main_window.connected:
        statusbar.SetStatusText("Status: Connected", 1)
    else: 
        statusbar.SetStatusText("Status: Not Connected", 1)
    return statusbar

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
    def __init__(self, parent, main_window):
        """ inits Spamfilter with training data

        :param training_dir: path of training directory with subdirectories
         '/ham' and '/spam'
        """
        wx.TextCtrl.__init__(self, parent=parent, style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_RICH)
        self.__set_properties__(main_window)

    def __set_properties__(self, main_window):
        self.main_window = main_window
        self.SetName("Python Shell")
        self.theme_choice = main_window.notebook.theme_choice
        self.custom_shell("Dark Theme")

    def custom_shell(self, choice_theme):
        try:
            file = open("./customize.json")
            theme = json.load(file)
            file.close()
            theme = theme[self.theme_choice]
            self.font = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, "Fira code")
            self.SetBackgroundColour(theme['Panels Colors']['Shell background'])
            self.SetFont(self.font)
            self.SetDefaultStyle(wx.TextAttr(theme['Panels Colors']['Text foreground'],theme['Panels Colors']['Shell background'], font=self.font))
            txt = self.GetValue()
            self.Clear()
            self.AppendText(txt)
        except Exception as e:
            print(e)
            #print("Can't customize shell")
            return        
        #font = wx.Font(pointSize = 10, family = wx.FONTFAMILY_SWISS, style = wx.FONTSTYLE_SLANT, weight = wx.FONTWEIGHT_BOLD,  
        #              underline = False, faceName ="Fira Code", encoding = 0)
    
    def set_focus_shell(self, evt):
        self.SetFocus()
