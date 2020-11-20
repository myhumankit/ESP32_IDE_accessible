# TODO: Menu Help with shortcuts and link on wiki tuto HTML
import wx
import webbrowser


class HelpMenu(wx.Menu):
    def __init__(self, frame):
        wx.Menu.__init__(self, "Help")

        self.frame = frame

        self.item_list = []
        self.Append(wx.ID_ABOUT, "About")
        self.Append(wx.ID_SHORTCUT, "Shortcuts List")

    def __attach_events(self):
        self.Bind(wx.EVT_MENU, self.OnAbout, id=wx.ID_ABOUT)
        self.Bind(wx.EVT_MENU, self.OnHelp, id=wx.ID_HELP)

    def OnHelp(self, evt):
        # print("help")
        webbrowser.open("./Help/help.html")

    def OnAbout(self, evt):
        # print("about")
        webbrowser.open("./Help/about.html")
