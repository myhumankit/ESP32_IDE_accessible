import random, os, codecs, threading, asyncio, sys, json
import Panels.wxSerialConfigDialog
import Panels.Device_tree as Tree

import wx.stc as stc
import wx.py as pysh
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
    style = wx.SP_3D | wx.SP_NO_XP_THEME | wx.SP_PERMIT_UNSPLIT | wx.SP_LIVE_UPDATE
    main_window.splitter_v = wx.SplitterWindow(main_window, style=style, name="Dimension")
    main_window.splitter_h = wx.SplitterWindow(main_window.splitter_v, style=style, name="DIMENSION ALL")
    main_window.notebook = NotebookPanel(main_window.splitter_h, main_window)
    main_window.device_tree = Tree.DeviceTree(main_window.splitter_v, main_window, "", "")
    main_window.shell = ShellPanel(main_window.splitter_h, main_window)
    main_window.splitter_v.SplitVertically(main_window.device_tree , main_window.splitter_h, 200)
    main_window.splitter_h.SplitHorizontally(main_window.notebook, main_window.shell, 400)

class MyEditor(pysh.editwindow.EditWindow):
    """Customizable Editor page

    :param pysh.editwindow.EditWindow: see https://wxpython.org/Phoenix/docs/html/wx.py.html
    :type pysh.editwindow.EditWindow: wx.py.editwindow.EditWindow
    """

    def __init__(self, parent, topwindow, text, on_card):
        """ Constructor to init a Tab on the Notebook
        
        :param parent: NotebookPanel class
        :type parent: NotebookPanel class
        :param topwindow: the MainWindow in this case
        :type parent: MainWindow class
        """

        pysh.editwindow.EditWindow.__init__(self, parent=parent)

        self.__set_properties(parent, topwindow, on_card)
        self.__set_style(parent)
        self.__attach_events()
        #self.write(text)
        self.SetValue(text)
    
    def __set_properties(self, parent, topwindow, on_card):
        """Set the properties and declare the variables of the instance
        
        :param parent: NotebookPanel class
        :type parent: NotebookPanel class
        :param topwindow: the MainWindow in this case
        :type parent: MainWindow class
        """
        self.topwindow = topwindow
        self.id = parent.tab_num + 1
        self.filename = ""
        self.directory = ""
        self.saved = False
        self.last_save = ""
        self.theme_choice = parent.theme_choice
        self.findData = wx.FindReplaceData()
        self.txt = ""
        self.pos = 0
        self.size = 0
        self.on_card = on_card

    def __set_style(self, parent):
        """Load the first style of the editor

        :param parent: Notebook Panel
        :type parent: Notebook class
        """
        ##print("PARENT THEME = " + str(parent.theme))
        self.SetMarginType(1, stc.STC_MARGIN_NUMBER)
        self.SetMarginWidth(1, 25)
        init_editor_style(self)
        customize_editor(self, self.theme_choice)

    def __attach_events(self):
        """
        Bind events related to this class
        """
        self.Bind(wx.EVT_TEXT, self.topwindow.actualize_status_bar)
        self.Bind(wx.EVT_TEXT_ENTER, self.topwindow.actualize_status_bar)
        
    def bind_find_events(self, win):
        """Bind events of the find and replace dialog

        :param win: the main main_window
        :type win: MainWindow class
        """
        win.Bind(wx.EVT_FIND, self.OnFind)
        win.Bind(wx.EVT_FIND_NEXT, self.OnFind)
        win.Bind(wx.EVT_FIND_REPLACE, self.OnFind)
        win.Bind(wx.EVT_FIND_REPLACE_ALL, self.OnFind)
        win.Bind(wx.EVT_FIND_CLOSE, self.OnFindClose)

    def OnShowFindReplace(self, evt=None):
        """Show the Find and Replace dialog and call the bind_find_events method

        :param evt: , defaults to None
        :type evt: wx.Event, optional
        """
        dlg = wx.FindReplaceDialog(self, self.findData, "Find & Replace", wx.FR_REPLACEDIALOG)

        self.bind_find_events(dlg)
        dlg.Show(True)

    def OnFind(self, evt):
        """Method to find a string on the current tab editor

        :param evt: Event which decide to what execute
        :type evt: wx.Event
        """
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
        """Close the find and replace dialog

        :param evt: Event to close the dialog
        :type evt: wx.Event
        """
        #print("FindReplaceDialog closing...\n")
        evt.GetDialog().Destroy()

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
        style = fnb.FNB_FF2 | wx.FULL_REPAINT_ON_RESIZE | fnb.FNB_COLOURFUL_TABS
        fnb.FlatNotebook.__init__(self, parent=parent, style=style, name="COUCOU")

        self.__set_properties(parent, topwindow)
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.Bind(wx.EVT_PAINT, self.on_paint)

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
            self.SetActiveTabColour(theme['Background tab area'])
            self.SetTabAreaColour(theme['Background tab area'])
            self.SetActiveTabTextColour(theme['Active tab text'])
            self.SetNonActiveTabTextColour(theme['Active tab text'])
        except Exception:
            print("Can't Customize Notebook")

    def set_focus_editor(self, evt):
        try:
            page = self.GetCurrentPage()
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
        wx.TextCtrl.__init__(self, parent=parent, style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.__set_properties__(main_window)

    def __set_properties__(self, main_window):
        self.main_window = main_window
        self.SetName("Python Shell")
        self.theme_choice = main_window.notebook.theme_choice
        #self.custom_shell("Dark Theme")

    def custom_shell(self, choice_theme):
        try:
            file = open("./customize.json")
            theme = json.load(file)
            file.close()
            theme = theme[self.theme_choice]
            self.font = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, "Fira code")
            self.SetBackgroundColour(theme['Panels Colors']['Shell background'])
            self.SetDefaultStyle(wx.TextAttr(theme['Panels Colors']['Text foreground'], font=self.font))
            self.SetFont(self.font)
        except Exception as e:
            print(e)
            #print("Can't customize shell")
            return        
        #font = wx.Font(pointSize = 10, family = wx.FONTFAMILY_SWISS, style = wx.FONTSTYLE_SLANT, weight = wx.FONTWEIGHT_BOLD,  
        #              underline = False, faceName ="Fira Code", encoding = 0)
    
    def set_focus_shell(self, evt):
        self.SetFocus()
