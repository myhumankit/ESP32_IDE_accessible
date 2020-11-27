"""
    Module wich contains the HelpMenu class
"""
import wx
import webbrowser
import os


class HelpMenu(wx.Menu):
    """Inits a instance of a wx.Menu to create a Help menu
        and his buttons (About, Shortcuts list, Tutorial,...)

    :return: the Theme menu filled by buttons
    :rtype: wx.Menu see https://wxpython.org/Phoenix/docs/html/wx.Menu.html
    """
    def __init__(self, frame):
        """ Constructor method

        :param frame: main window
        :type frame: MainWindow
        """
        wx.Menu.__init__(self, "Help")

        self.frame = frame

        self.item_list = []
        self.Append(wx.ID_ABOUT, "About")
        self.Append(wx.ID_SHORTCUT, "Shortcuts List")
        self.Append(wx.ID_ABORT, "Documentation")
        self.__attach_events()

    def __attach_events(self):
        """ Link events and methods with menu buttons
        """
        self.Bind(wx.EVT_MENU, self.OnAbout, id=wx.ID_ABOUT)
        self.Bind(wx.EVT_MENU, self.OnHelp, id=wx.ID_SHORTCUT)
        self.Bind(wx.EVT_MENU, self.OnDocumentation, id=wx.ID_ABORT)

    def OnHelp(self, evt):
        """ Open a webrowser and display the shortcuts list
        """
        if os.getcwd().find("dist") >= 1:
            webbrowser.open(os.getcwd()+"\\..\\..\\docs\\Help\\output\\shortcuts.html")
        else:
            webbrowser.open(os.getcwd()+"\\docs\\Help\\output\\shortcuts.html")

    def OnAbout(self, evt):
        """ Open a webrowser and display the about
        """
        print("about")
        if os.getcwd().find("dist") >= 1:
            webbrowser.open(os.getcwd()+"../../docs/Help/output/shortcuts.html")
        else:
            webbrowser.open(os.getcwd()+"./docs/Help/output/shortcuts.html")

    def OnDocumentation(self, evt):
        """ Open a webrowser and display the docs
        """
        if os.getcwd().find("dist") >= 1:
            webbrowser.open(os.getcwd()+"../../docs/_build/html/index.html")
        else:
            webbrowser.open(os.getcwd()+"./docs/_build/html/index.html")
