""" Module wich contain classes related to the Shell Panel
"""

import wx
import json


class ShellPanel(wx.TextCtrl):
    """ Constructor method

        :param parent: in this case :class:wx.SplittedWindow
        :param frame: Main of the app :class:MainWindow
    """
    def __init__(self, parent, frame):
        """ Constructor method
         """
        wx.TextCtrl.__init__(self, parent=parent,
                             style=wx.TE_MULTILINE |
                             wx.TE_READONLY | wx.TE_RICH)
        self.__set_properties__(frame)

    def __set_properties__(self, frame):
        """ Method to define new attributes and set style
         """
        self.frame = frame
        self.SetName("Python Shell")
        self.theme_choice = frame.notebook.theme_choice
        self.custom_shell(self.theme_choice)

    def custom_shell(self, theme_choice):
        """Custom the Shell panel with the given theme_choice

        :param theme_choice: The theme selected
        :type theme_choice: str
        """
        try:
            file = open("./customize.json")
            theme = json.load(file)
            file.close()
            theme = theme[theme_choice]
            self.font = wx.Font(12, wx.MODERN, wx.NORMAL,
                                wx.NORMAL, 0, "Arial")
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

    def move_key_left(self):
        """ Move the cursor on the previous character
        """
        cursor = self.GetInsertionPoint()
        self.SetInsertionPoint(cursor - 1)

    def move_key_right(self):
        """ Move the cursor on the next character
        """
        cursor = self.GetInsertionPoint()
        self.SetInsertionPoint(cursor + 1)

    def remove_char(self):
        """ Remove the previous character
        """
        cursor = self.GetInsertionPoint()
        self.Remove(cursor - 1, cursor)

#TODO: My commands 
# class Mycommands():
#     def __init__(self, shell):
#         self.list_cmd = []
#         self.cursor = 0

#     def down(self):
#         print("")
