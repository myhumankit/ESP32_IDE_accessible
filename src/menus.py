"""
    Contains functions to create all panels
"""

import wx

from Utils.utilitaries import load_img
from Utils.voice_synthese import my_speak
from Menus.Tools_menu import ToolsMenu
from Menus.File_menu import FileMenu
from Menus.Edit_menu import EditMenu
from Menus.Help_menu import HelpMenu


def init_top_menu(frame):
    """Inits an instance of customized TopMenu class and places it on the frame

    :param frame: frame which will contains the MenuBar
    :type frame: wx.frame https://wxpython.org/Phoenix/docs/html/wx.frame.html
    """

    frame.top_menu = TopMenu(frame)
    frame.SetMenuBar(frame.top_menu)

    return frame.top_menu


def init_toolbar(frame):
    """Inits an instance of the customized ToolBar class and places it on the frame

    :param frame: frame which will contains the ToolBar
    :type frame: wx.frame https://wxpython.org/Phoenix/docs/html/wx.frame.html
    """

    frame.ToolBar = ToolBar(frame)
    frame.SetToolBar(frame.ToolBar)


class TopMenu(wx.MenuBar):
    """TopMenu class derivated of wx.MenuBar which contains the Edit and File Menus

    :param wx.MenuBar: Class to derivate
    :type wx.MenuBar: :class:wx.MenuBar see
     https://wxpython.org/Phoenix/docs/html/wx.MenuBar.html
    """

    def __init__(self, frame):
        """Constructor which append the Edit and File Menus on the Menubar
           and bind related events

        :param frame: frame class (in this case MainWindow)
        :type frame: MainWindow(here Mainwindow class derivated of wx.frame)
        """

        wx.MenuBar.__init__(self)
        self.frame = frame
        self.__set_properties(frame)
        self.__attach_events__()

    def __set_properties(self, frame):
        """
        Set properties and define variables of the objet instantiated
        """

        self.MenuFile = FileMenu(self.frame)
        self.MenuEdit = EditMenu(self.frame)
        self.MenuTools = ToolsMenu(self.frame)
        self.MenuHelp = HelpMenu(self.frame)

        self.SetBackgroundColour("Black")
        self.SetForegroundColour("White")
        self.Append(self.MenuFile, "&File")
        self.Append(self.MenuEdit, "&Edit")
        self.Append(self.MenuTools, "Tools")
        self.Append(self.MenuHelp, "Help")

    def __attach_events__(self):
        """
        Bind events with the objet instantiated
        """

        MenuFile = self.MenuFile
        MenuEdit = self.MenuEdit
        MenuTools = self.MenuTools
        MenuTheme = self.MenuTools.themes_submenu

        self.Bind(wx.EVT_MENU, MenuFile.OnExit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, MenuFile.OnOpen, id=wx.ID_OPEN)
        self.Bind(wx.EVT_MENU, MenuFile.OnSaveAs, id=wx.ID_SAVEAS)
        self.Bind(wx.EVT_MENU, MenuFile.OnSave, id=wx.ID_SAVE)
        self.Bind(wx.EVT_MENU, MenuFile.OnAddPage, id=wx.ID_NEW)
        self.Bind(wx.EVT_MENU, MenuFile.OnClosePage, id=wx.ID_CLOSE)
        self.Bind(wx.EVT_MENU, MenuEdit.OnCopy, id=wx.ID_COPY)
        self.Bind(wx.EVT_MENU, MenuEdit.OnPaste, id=wx.ID_PASTE)
        self.Bind(wx.EVT_MENU, MenuEdit.OnCut, id=wx.ID_CUT)
        self.Bind(wx.EVT_MENU, MenuEdit.OnFindReplace, id=wx.ID_FIND)
        self.Bind(wx.EVT_MENU, MenuEdit.OnSyntaxCheck, id=wx.ID_SYNTAX_CHECK)
        self.Bind(wx.EVT_MENU, MenuTools.OnPortSettings, id=wx.ID_SETTINGS)
        self.Bind(wx.EVT_MENU, MenuTools.OnUpload, id=wx.ID_DOWNLOAD)
        self.Bind(wx.EVT_MENU, MenuTools.OnRun, id=wx.ID_EXECUTE)
        self.Bind(wx.EVT_MENU, MenuTools.OnStop, id=wx.ID_STOP)
        self.Bind(wx.EVT_MENU, MenuTools.OnBurnFirmware, id=wx.ID_BURN_FIRMWARE)
        self.Bind(wx.EVT_MENU, MenuTheme.OnChangeTheme, id=wx.ID_LIGHT_THEME)
        self.Bind(wx.EVT_MENU, MenuTheme.OnChangeTheme, id=wx.ID_DARK_THEME)
        self.Bind(wx.EVT_MENU, MenuTheme.OnChangeTheme, id=wx.ID_NVDA_THEME)
        self.Bind(wx.EVT_MENU, self.MenuTools.OnDisconnect, id=wx.ID_CANCEL)
        self.Bind(wx.EVT_MENU, self.MenuTools.OnRefreshTreeView, id=wx.ID_REFRESH)


class ToolBar(wx.ToolBar):
    """A custom class derivated from wx.ToolBar to access quickly on some commands

    :param wx.ToolBar:
    see https://wxpython.org/Phoenix/docs/html/wx.ToolBar.html
    """

    def __init__(self, frame):
        """constructor for ToolBar

        :param frame: frame class generally the main window
        :type frame: MainWindow (generally)
        """

        wx.ToolBar.__init__(self, parent=frame, style=wx.TB_RIGHT |
                            wx.TB_DOCKABLE | wx.FULL_REPAINT_ON_RESIZE)
        self.frame = frame

        self.add_tools()
        self.__set_properties()
        self.__attach_events(frame.top_menu)
        self.CentreOnParent()

    def __set_properties(self):
        """Set properties and declare variables of the instance
        """

        self.Realize()
        self.SetBackgroundColour("black")

    def __attach_events(self, top_menu):
        """Bind the events related with this class

        :param frame: often the MainWindow
        :type frame: MainWindow class
        """

        self.Bind(wx.EVT_MENU, top_menu.MenuFile.OnAddPage, id=wx.ID_NEW)
        self.Bind(wx.EVT_MENU, top_menu.MenuFile.OnOpen, id=wx.ID_OPEN)
        self.Bind(wx.EVT_MENU, top_menu.MenuFile.OnSave, id=wx.ID_SAVE)
        self.Bind(wx.EVT_MENU, top_menu.MenuTools.OnRun, id=wx.ID_EXECUTE)
        self.Bind(wx.EVT_MENU, top_menu.MenuTools.OnStop, id=wx.ID_STOP)
        self.Bind(wx.EVT_MENU, top_menu.MenuEdit.OnSyntaxCheck,
                  id=wx.ID_SYNTAX_CHECK)
        self.Bind(wx.EVT_MENU, self.OnClear, id=wx.ID_CLEAR)
        self.Bind(wx.EVT_MENU, top_menu.MenuEdit.OnUndo, id=wx.ID_UNDO)
        self.Bind(wx.EVT_MENU, top_menu.MenuEdit.OnRedo, id=wx.ID_REDO)

    def add_tools(self):
        """
        Fill the objet created with tools buttons
        """

        self.AddTool(wx.ID_NEW, '', load_img('./img/newfile.png'), shortHelp="New")
        self.AddTool(wx.ID_OPEN, '', load_img('./img/fileopen.png'), shortHelp="Open")
        self.AddTool(wx.ID_SAVE, '', load_img('./img/save.png'), shortHelp="Save")
        self.AddTool(wx.ID_EXECUTE, '', load_img('./img/downloadandrun.png'),
                     shortHelp="Run")
        self.AddTool(wx.ID_STOP, '', load_img('./img/stop.png'), shortHelp="Stop")
        self.AddTool(wx.ID_UNDO, '', load_img('./img/undo.png'), shortHelp="Undo")
        self.AddTool(wx.ID_REDO, '', load_img('./img/redo.png'), shortHelp="Redo")
        self.AddTool(wx.ID_SYNTAX_CHECK, '', load_img('./img/syntaxCheck.png'),
                     shortHelp="Check syntax")
        self.AddTool(wx.ID_CLEAR, '', load_img('./img/clear.png'), shortHelp="Clear")

    def OnClear(self, event):
        """Clear the shell panel

        :param evt: Event to trigger the method
        :type evt: wx.Event
        """

        self.frame.shell.Clear()
        my_speak(self.frame, "Terminal Cleared")
