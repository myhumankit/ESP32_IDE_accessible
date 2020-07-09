import wx

wx.ID_REFLUSH_DIR = 250
wx.ID_EXAMPLES = 251
wx.ID_SYNTAX_CHECK = 252
wx.ID_DOWNLOAD_RUN = 253

def create_File_Menu():
    MenuFile = wx.Menu(style = wx.MENU_TEAROFF)
    MenuFile.Append(wx.ID_SAVE, "&Save\tCTRL+S")
    MenuFile.Append(wx.ID_SAVEAS, "&Save as")
    MenuFile.Append(wx.ID_OPEN, "&Open\tCTRL+O")
    MenuFile.Append(wx.ID_REFLUSH_DIR, "&Reflush Directory")
    MenuFile.Append(wx.ID_EXAMPLES, "&Examples")
    MenuFile.Append(wx.ID_EXIT, "&Exit\tCTRL+Q")
    MenuFile.AppendSeparator()
    return MenuFile

def create_Edit_Menu():
    MenuEdit = wx.Menu(style = wx.MENU_TEAROFF)
    MenuEdit.Append(wx.ID_COPY, "&Copy\tCTRL+C")
    MenuEdit.Append(wx.ID_CUT, "&Cut\tCTRL+X")
    MenuEdit.Append(wx.ID_PASTE, "&Paste\tCTRL+V")
    MenuEdit.Append(wx.ID_REDO, "&Redo\tCTRL+Z")
    MenuEdit.Append(wx.ID_SYNTAX_CHECK, "&Syntax Check")
    MenuEdit.Append(wx.ID_FIND, "&Find and/or Replace\tCTRL+F")
    MenuEdit.AppendSeparator()
    return MenuEdit

def create_TopMenu():
    MenuFile = create_File_Menu()
    MenuEdit = create_Edit_Menu()
    MenuTop = wx.MenuBar()
    MenuTop.Append(MenuFile, "&File")
    MenuTop.Append(MenuEdit, "&Edit")
    #TODO: add menu Tool later
    #MenuTop.Append(MenuTools, "&Tools")
    return MenuTop

class TopMenu(wx.MenuBar):
    def __init__(self, parent):       
        wx.MenuBar.__init__(self)
        self.controller = parent
        MenuFile = create_File_Menu()
        MenuEdit = create_Edit_Menu()
        self.Append(MenuFile, "&File")
        self.Append(MenuEdit, "&Edit")
        wx.EVT_MENU(parent, wx.ID_EXIT, self.OnExit)
        wx.EVT_MENU(parent, wx.ID_OPEN, self.OnOpen)
        wx.EVT_MENU(parent, wx.ID_SAVEAS, self.OnSaveAs)

    def OnExit(self, evt):
        self.Parent.Destroy()

    def OnSave(self, evt):
        print("save")

    def OnSaveAs(self, evt):
        with wx.FileDialog(self.Parent, "Save Python file", wildcard="Python files (*.py)|*.py",
                       style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind
        # save the current contents in the file
        pathname = fileDialog.GetPath()
        try:
            with open(pathname, 'w') as file:
                self.Parent.doSaveData(file)
        except IOError:
            wx.LogError("Cannot save current data in file '%s'." % pathname)

    def OnOpen(self, event):# ! if self.contentNotSaved:
        if wx.MessageBox("Current content has not been saved! Proceed?", "Please confirm",#alert the user that his job 
            wx.ICON_QUESTION | wx.YES_NO, self.Parent) == wx.NO:
                return OnSave()
        # otherwise ask the user what new file to open
        with wx.FileDialog(self.Parent, "Open Python file", wildcard="Python files (*.py)|*.py",
            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind
        # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            try:
                with open(pathname, 'r') as file:
                    self.Parent.doLoadDataOrWhatever(file)
            except IOError:
                wx.LogError("Cannot open file '%s'." % newfile)

def InitToolBar(frame):

    toolbar1 = frame.CreateToolBar(wx.TB_RIGHT| wx.TB_DOCKABLE|wx.TB_NODIVIDER)
    toolbar1.SetMargins(100,100)
    toolbar1.AddTool(wx.ID_NEW, '', wx.Bitmap('save.png'))
    toolbar1.AddTool(wx.ID_OPEN, '', wx.Bitmap('save.png'))
    toolbar1.AddTool(wx.ID_SAVE, '', wx.Bitmap('save.png'))
    toolbar1.AddTool(wx.ID_DOWNLOAD_RUN, '', wx.Bitmap('save.png'))
    toolbar1.AddTool(wx.ID_DOWNLOAD_RUN, '', wx.Bitmap('save.png'))
    toolbar1.Realize()
