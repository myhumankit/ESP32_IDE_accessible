""" Module wich contains the classes and functions related to the editor tab panel
"""

import keyword
import wx
import wx.stc as stc
import wx.py as pysh
from editor_style import customize_editor, init_editor_style
from Utils.find_replace import find_next, replace


class Styled_Editor(pysh.editwindow.EditWindow):
    """Customizable Editor page

    :param pysh.editwindow.EditWindow:
     see https://wxpython.org/Phoenix/docs/html/wx.py.html
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
        self.set_style(parent)
        self.__attach_events()
        self.custom_stc()
        self.SetValue(text)

    def custom_stc(self):
        """Custom the editwindow instance based on the model of the wxDemo StyledCtrl2.py
         """
        self.CmdKeyAssign(ord('+'), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMIN)
        self.CmdKeyAssign(ord('-'), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMOUT)

        self.SetKeyWords(0, " ".join(keyword.kwlist))

        self.SetProperty("fold", "1")
        self.SetProperty("tab.timmy.whinge.level", "1")
        self.SetMargins(0, 0)

        self.SetViewWhiteSpace(False)
        self.SetMarginType(2, stc.STC_MARGIN_SYMBOL)
        self.SetMarginMask(2, stc.STC_MASK_FOLDERS)
        self.SetMarginSensitive(2, True)
        self.SetMarginWidth(2, 12)

        # Like a flattened tree control using circular headers and curved joins
        self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN,
                          stc.STC_MARK_CIRCLEMINUS,          "white", "#404040")
        self.MarkerDefine(stc.STC_MARKNUM_FOLDER,
                          stc.STC_MARK_CIRCLEPLUS,           "white", "#404040")
        self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB,
                          stc.STC_MARK_VLINE,                "white", "#404040")
        self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL,
                          stc.STC_MARK_LCORNERCURVE,         "white", "#404040")
        self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND,
                          stc.STC_MARK_CIRCLEPLUSCONNECTED,  "white", "#404040")
        self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID,
                          stc.STC_MARK_CIRCLEMINUSCONNECTED, "white", "#404040")
        self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL,
                          stc.STC_MARK_TCORNERCURVE,         "white", "#404040")

        self.Bind(stc.EVT_STC_UPDATEUI, self.OnUpdateUI)
        self.Bind(stc.EVT_STC_MARGINCLICK, self.OnMarginClick)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyPressed)

    def OnKeyPressed(self, event):
        """Manage the keyboard events related to the tab
         """
        if self.CallTipActive():
            self.CallTipCancel()
        key = event.GetKeyCode()

        if key == 32 and event.ControlDown():
            pos = self.GetCurrentPos()

            # Tips
            if event.ShiftDown():
                self.CallTipSetBackground("yellow")
                self.CallTipShow(pos, 'lots of of text: blah, blah, blah\n\n'
                                 'show some suff, maybe parameters..\n\n'
                                 'fubar(param1, param2)')
            # Code completion
            else:

                kw = keyword.kwlist[:]
                kw.append("zzzzzz?2")
                kw.append("aaaaa?2")
                kw.append("__init__?3")
                kw.append("zzaaaaa?2")
                kw.append("zzbaaaa?2")
                kw.append("this_is_a_longer_value")
                # kw.append("this_is_a_much_much_much_much_much_much_much_longer_value")

                kw.sort()  # Python sorts are case sensitive
                self.AutoCompSetIgnoreCase(False)  # so this needs to match

                # Images are specified with a appended "?type"
                for i in range(len(kw)):
                    if kw[i] in keyword.kwlist:
                        kw[i] = kw[i] + "?1"

                self.AutoCompShow(0, " ".join(kw))
        else:
            event.Skip()

    def OnUpdateUI(self, evt):
        """ Manage the syntax highlight on the braces
         """
        # check for matching braces
        braceAtCaret = -1
        braceOpposite = -1
        charBefore = None
        caretPos = self.GetCurrentPos()

        if caretPos > 0:
            charBefore = self.GetCharAt(caretPos - 1)
            styleBefore = self.GetStyleAt(caretPos - 1)

        # check before
        if charBefore and chr(charBefore) in "[]{}()" and styleBefore == stc.STC_P_OPERATOR:
            braceAtCaret = caretPos - 1

        # check after
        if braceAtCaret < 0:
            charAfter = self.GetCharAt(caretPos)
            styleAfter = self.GetStyleAt(caretPos)

            if charAfter and chr(charAfter) in "[]{}()" and styleAfter == stc.STC_P_OPERATOR:
                braceAtCaret = caretPos

        if braceAtCaret >= 0:
            braceOpposite = self.BraceMatch(braceAtCaret)

        if braceAtCaret != -1 and braceOpposite == -1:
            self.BraceBadLight(braceAtCaret)
        else:
            self.BraceHighlight(braceAtCaret, braceOpposite)

    def OnMarginClick(self, evt):
        """ Fold the tab content if an event is happened
         """
        if evt.GetMargin() == 2:
            if evt.GetShift() and evt.GetControl():
                self.FoldAll()
            else:
                lineClicked = self.LineFromPosition(evt.GetPosition())

                if self.GetFoldLevel(lineClicked) & stc.STC_FOLDLEVELHEADERFLAG:
                    if evt.GetShift():
                        self.SetFoldExpanded(lineClicked, True)
                        self.Expand(lineClicked, True, True, 1)
                    elif evt.GetControl():
                        if self.GetFoldExpanded(lineClicked):
                            self.SetFoldExpanded(lineClicked, False)
                            self.Expand(lineClicked, False, True, 0)
                        else:
                            self.SetFoldExpanded(lineClicked, True)
                            self.Expand(lineClicked, True, True, 100)
                    else:
                        self.ToggleFold(lineClicked)

    def FoldAll(self):
        """ Fold all the tab content
         """
        lineCount = self.GetLineCount()
        expanding = True

        # find out if we are folding or unfolding
        for lineNum in range(lineCount):
            if self.GetFoldLevel(lineNum) & stc.STC_FOLDLEVELHEADERFLAG:
                expanding = not self.GetFoldExpanded(lineNum)
                break

        lineNum = 0

        while lineNum < lineCount:
            level = self.GetFoldLevel(lineNum)
            if level & stc.STC_FOLDLEVELHEADERFLAG and \
               (level & stc.STC_FOLDLEVELNUMBERMASK) == stc.STC_FOLDLEVELBASE:

                if expanding:
                    self.SetFoldExpanded(lineNum, True)
                    lineNum = self.Expand(lineNum, True)
                    lineNum = lineNum - 1
                else:
                    lastChild = self.GetLastChild(lineNum, -1)
                    self.SetFoldExpanded(lineNum, False)

                    if lastChild > lineNum:
                        self.HideLines(lineNum+1, lastChild)

            lineNum = lineNum + 1

    def Expand(self, line, doExpand, force=False, visLevels=0, level=-1):
        """ Expand the tab content
         """
        lastChild = self.GetLastChild(line, level)
        line = line + 1

        while line <= lastChild:
            if force:
                if visLevels > 0:
                    self.ShowLines(line, line)
                else:
                    self.HideLines(line, line)
            else:
                if doExpand:
                    self.ShowLines(line, line)

            if level == -1:
                level = self.GetFoldLevel(line)

            if level & stc.STC_FOLDLEVELHEADERFLAG:
                if force:
                    if visLevels > 1:
                        self.SetFoldExpanded(line, True)
                    else:
                        self.SetFoldExpanded(line, False)

                    line = self.Expand(line, doExpand, force, visLevels-1)

                else:
                    if doExpand and self.GetFoldExpanded(line):
                        line = self.Expand(line, True, force, visLevels-1)
                    else:
                        line = self.Expand(line, False, force, visLevels-1)
            else:
                line = line + 1

        return line

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
        self.parent = parent

    def set_style(self, parent):
        """Load the first style of the editor

        :param parent: Notebook Panel
        :type parent: Notebook class
        """
        self.setDisplayLineNumbers(True)
        self.CmdKeyAssign(ord('='), stc.STC_KEYMOD_CTRL, stc.STC_CMD_ZOOMIN)
        self.CmdKeyAssign(ord('6'), stc.STC_KEYMOD_CTRL, stc.STC_CMD_ZOOMOUT)
        init_editor_style(self)
        customize_editor(self, self.theme_choice)

    def __attach_events(self):
        """
         Bind events related to this class
         """
        self.Bind(wx.EVT_TEXT, self.topwindow.actualize_status_bar)

    def bind_find_events(self, win):
        """Bind events of the find and replace dialog

         :param win: the main frame
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
        dlg = wx.FindReplaceDialog(
            self, self.findData, "Find & Replace", wx.FR_REPLACEDIALOG)

        self.bind_find_events(dlg)
        dlg.Show(True)

    def OnFind(self, evt):
        """Method to find a string on the current tab editor

         :param evt: Event which decide to what execute
         :type evt: wx.Event
         """
        self.txt = self.GetValue()
        et = evt.GetEventType()

        if et in [wx.wxEVT_COMMAND_FIND_NEXT]:
            find_next(self, evt)
        if et in [wx.wxEVT_COMMAND_FIND_REPLACE]:
            replace(self, evt)
        if et in [wx.wxEVT_COMMAND_FIND_REPLACE_ALL]:
            while find_next(self, evt) is True:
                replace(self, evt)

    def OnFindClose(self, evt):
        """Close the find and replace dialog

         :param evt: Event to close the dialog
         :type evt: wx.Event
         """
        # print("FindReplaceDialog closing...\n")
        evt.GetDialog().Destroy()

