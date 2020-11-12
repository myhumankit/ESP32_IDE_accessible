import wx, os, sys, time, serial, asyncio

from my_serial import put_cmd
from all_panels import *
from utilitaries import *

from constantes import *
from firmware import UpdateFirmwareDialog, FirmwareThread, BurnFrame

from Menus.Tools_menu import ToolsMenu
from Menus.File_menu import FileMenu
from Menus.Edit_menu import EditMenu
from Menus.Help_menu import HelpMenu

def init_top_menu(main_window):
    """Inits an instance of customized TopMenu class and places it on the main_window

    :param main_window: main_window which will contains the MenuBar
    :type main_window: wx.main_window https://wxpython.org/Phoenix/docs/html/wx.main_window.html
    """

    main_window.top_menu = TopMenu(main_window)
    main_window.SetMenuBar(main_window.top_menu)

    return main_window.top_menu

def init_toolbar(main_window):
    """Inits an instance of the customized ToolBar class and places it on the main_window

    :param main_window: main_window which will contains the ToolBar
    :type main_window: wx.main_window https://wxpython.org/Phoenix/docs/html/wx.main_window.html
    """  
    
    main_window.ToolBar = ToolBar(main_window)
    main_window.SetToolBar(main_window.ToolBar)

class TopMenu(wx.MenuBar):
    """TopMenu class derivated of wx.MenuBar which contains the Edit and File Menus

    :param wx.MenuBar: Class to derivate
    :type wx.MenuBar: wx.MenuBar see  https://wxpython.org/Phoenix/docs/html/wx.MenuBar.html
    """
    def __init__(self, main_window):
        """Constructor which append the Edit and File Menus on the Menubar and bind related events

        :param main_window: main_window class (in this case MainWindow)
        :type main_window: MainWindow(here Mainwindow class derivated of wx.main_window)
        """
        wx.MenuBar.__init__(self)
        self.main_window = main_window
        self.__set_properties(main_window) #:Set properties and variables linked to the class
        self.__attach_events__() #:Bind events relatives to this class

    def __set_properties(self, main_window):
        """
        Set properties and define variables of the objet instantiated
        """
        self.MenuFile = FileMenu(self.main_window)
        self.MenuEdit = EditMenu(self.main_window)
        self.MenuTools = ToolsMenu(self.main_window)
        self.MenuHelp = HelpMenu(self.main_window)
        self.SetBackgroundColour("Black")
        self.SetForegroundColour("White")

        self.Append(self.MenuFile, "&File")
        self.Append(self.MenuEdit, "&Edit")
        self.Append(self.MenuTools, "Tools")
        self.Append(self.MenuHelp,"Help")
        
    def __attach_events__(self):
        """
        Bind events with the objet instantiated
        """
        self.Bind(wx.EVT_MENU,  self.MenuFile.OnExit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU,  self.MenuFile.OnOpen, id=wx.ID_OPEN)
        self.Bind(wx.EVT_MENU,  self.MenuFile.OnSaveAs, id=wx.ID_SAVEAS)
        self.Bind(wx.EVT_MENU,  self.MenuFile.OnSave, id=wx.ID_SAVE)
        self.Bind(wx.EVT_MENU,  self.MenuFile.OnAddPage, id=wx.ID_NEW)
        self.Bind(wx.EVT_MENU,  self.MenuFile.OnClosePage, id=wx.ID_CLOSE)
        self.Bind(wx.EVT_MENU,  self.MenuEdit.OnCopy, id=wx.ID_COPY)
        self.Bind(wx.EVT_MENU,  self.MenuEdit.OnPaste, id=wx.ID_PASTE)
        self.Bind(wx.EVT_MENU,  self.MenuEdit.OnCut, id=wx.ID_CUT)
        self.Bind(wx.EVT_MENU,  self.MenuEdit.OnFindReplace, id=wx.ID_FIND)
        self.Bind(wx.EVT_MENU,  self.MenuEdit.OnSyntaxCheck, id=wx.ID_SYNTAX_CHECK)
        self.Bind(wx.EVT_MENU, self.MenuTools.OnPortSettings, id=wx.ID_SETTINGS)
        self.Bind(wx.EVT_MENU, self.MenuTools.Ondownload, id=wx.ID_DOWNLOAD)
        self.Bind(wx.EVT_MENU, self.MenuTools.OnRun, id=wx.ID_EXECUTE)
        self.Bind(wx.EVT_MENU, self.MenuTools.OnStop, id=wx.ID_STOP)
        self.Bind(wx.EVT_MENU, self.MenuTools.OnBurnFirmware, id=wx.ID_BURN_FIRMWARE)
        self.Bind(wx.EVT_MENU,  self.MenuTools.OnChangeTheme, \
         id=wx.ID_LIGHT_THEME)
        self.Bind(wx.EVT_MENU,  self.MenuTools.OnChangeTheme, \
         id=wx.ID_DARK_THEME)
        self.Bind(wx.EVT_MENU,  self.MenuTools.OnChangeTheme, \
         id=wx.ID_ASTRO_THEME)
        self.Bind(wx.EVT_MENU, self.MenuTools.OnDisconnect, id=wx.ID_CANCEL)

class ToolBar(wx.ToolBar):
    """A custom class derivated from wx.ToolBar to access quickly on some commands

    :param wx.ToolBar: see https://wxpython.org/Phoenix/docs/html/wx.ToolBar.html
    """    
    def __init__(self, main_window):
        """constructor for ToolBar 

        :param main_window: main_window class generally the main window
        :type main_window: MainWindow (generally)
        """           
        wx.ToolBar.__init__(self, parent=main_window, style= wx.TB_RIGHT | wx.TB_DOCKABLE | wx.FULL_REPAINT_ON_RESIZE)
        self.CentreOnParent()
        self.main_window = main_window
        
        self.add_tools()
        self.__set_properties()
        self.__attach_events(main_window.top_menu)

    def add_tools(self):
        """
        Fill the objet created with tools buttons
        """
        self.AddTool(wx.ID_NEW, '', load_img('./img/newfile.png'), shortHelp="New")
        self.AddTool(wx.ID_OPEN, '', load_img('./img/fileopen.png'), shortHelp="Open")
        self.AddTool(wx.ID_SAVE, '', load_img('./img/save.png'), shortHelp="Save")
        self.AddTool(wx.ID_EXECUTE, '', load_img('./img/downloadandrun.png'), shortHelp="Run")
        self.AddTool(wx.ID_STOP, '', load_img('./img/stop.png'), shortHelp="Stop")
        self.AddTool(wx.ID_UNDO, '', load_img('./img/undo.png'), shortHelp="Undo")
        self.AddTool(wx.ID_REDO, '', load_img('./img/redo.png'), shortHelp="Redo")
        self.AddTool(wx.ID_SYNTAX_CHECK, '', load_img('./img/syntaxCheck.png'), shortHelp="Check syntax")
        self.AddTool(wx.ID_CLEAR, '', load_img('./img/clear.png'), shortHelp="Clear")

    def __set_properties(self):
        """Set properties and declare variables of the instance
        """  
        self.Realize()
        self.SetBackgroundColour("black")

    def __attach_events(self, top_menu):
        """Bind the events related with this class

        :param main_window: often the MainWindow
        :type main_window: MainWindow class
        """
        self.Bind(wx.EVT_MENU, top_menu.MenuFile.OnAddPage, id=wx.ID_NEW)
        self.Bind(wx.EVT_MENU, top_menu.MenuFile.OnOpen, id=wx.ID_OPEN)
        self.Bind(wx.EVT_MENU, top_menu.MenuFile.OnSave, id=wx.ID_SAVE)
        self.Bind(wx.EVT_MENU, top_menu.MenuTools.OnRun, id=wx.ID_EXECUTE)
        self.Bind(wx.EVT_MENU, top_menu.MenuTools.OnStop, id=wx.ID_STOP)
        self.Bind(wx.EVT_MENU, top_menu.MenuEdit.OnSyntaxCheck, id=wx.ID_SYNTAX_CHECK)
        self.Bind(wx.EVT_MENU, self.OnClear, id=wx.ID_CLEAR)
        self.Bind(wx.EVT_MENU, top_menu.MenuEdit.OnUndo, id=wx.ID_UNDO)
        self.Bind(wx.EVT_MENU, top_menu.MenuEdit.OnRedo, id=wx.ID_REDO)
        
    def OnClear(self, event):
        """Clear the shell panel

        :param evt: Event to trigger the method
        :type evt: wx.Event
        """  
        self.main_window.shell.Clear()
        my_speak(self.main_window, "Terminal Cleared")