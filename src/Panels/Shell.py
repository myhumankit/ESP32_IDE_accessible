import wx
import json


class ShellPanel(wx.TextCtrl):
    def __init__(self, parent, frame):
        """ inits Spamfilter with training data

        :param training_dir: path of training directory with subdirectories
         '/ham' and '/spam'
        """
        wx.TextCtrl.__init__(self, parent=parent,
                             style=wx.TE_MULTILINE |
                             wx.TE_READONLY | wx.TE_RICH)
        self.__set_properties__(frame)

    def InitShortcuts(self):
        """Initiate shortcuts of the Application with wx.Accelerator Table
            :param frame: parent class to bind events)
            :Type frame: wx.frame
         """
        accel_tbl = wx.AcceleratorTable([Init_paste(self),
                                        ])
        self.SetAcceleratorTable(accel_tbl)

    def Init_paste(self):
        frame.Bind(wx.EVT_MENU, frame.OnStatus, id=wx.ID_STATIC)
        return (wx.ACCEL_CTRL,  wx.WXK_END, wx.ID_STATIC)

    def __set_properties__(self, frame):
        self.frame = frame
        self.SetName("Python Shell")
        self.theme_choice = frame.notebook.theme_choice
        self.custom_shell(self.theme_choice)

    def custom_shell(self, theme_choice):
        try:
            file = open("./customize.json")
            theme = json.load(file)
            file.close()
            theme = theme[theme_choice]
            self.font = wx.Font(12, wx.MODERN, wx.NORMAL,
                                wx.NORMAL, 0, "Fira code")
            self.SetBackgroundColour(theme['Panels Colors']['Shell background'])
            self.SetFont(self.font)
            self.SetDefaultStyle(wx.TextAttr(
                theme['Panels Colors']['Text foreground'],
                theme['Panels Colors']['Shell background'],
                font=self.font))
            txt = self.GetValue()
            self.Clear()
            self.AppendText(txt)
        except Exception as e:
            print(e)
            # print("Can't customize shell")
            return

    def set_focus_shell(self, evt):
        self.SetFocus()


class Mycommands():
    def __init__(self, shell):
        self.list_cmd = []
        self.cursor = 0

    def down(self):
        print("")
