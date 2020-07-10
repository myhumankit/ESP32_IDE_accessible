import wx
from Panels import *
from Utilitaries import load_img

wx.ID_REFLUSH_DIR = 250
wx.ID_EXAMPLES = 251
wx.ID_SYNTAX_CHECK = 252
wx.ID_DOWNLOAD_RUN = 253

def Init_Top_Menu(self):
    self.top_menu = TopMenu(self)
    self.SetMenuBar(self.top_menu)

def Init_ToolBar(self):
    self.ToolBar = ToolBar(self)
    self.SetToolBar(self.ToolBar)

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

class TopMenu(wx.MenuBar):
    def __init__(self, parent):       
        wx.MenuBar.__init__(self)
        self.parent = parent
        MenuFile = create_File_Menu()
        MenuEdit = create_Edit_Menu()
        self.Append(MenuFile, "&File")
        self.Append(MenuEdit, "&Edit")
        wx.EVT_MENU(parent, wx.ID_EXIT, self.OnExit)
        wx.EVT_MENU(parent, wx.ID_OPEN, self.OnOpen)
        wx.EVT_MENU(parent, wx.ID_SAVEAS, self.OnSaveAs)

    def OnExit(self, evt):
        """ Generates token frequency table from training emails
        :return:  dict{k,v}:  spam/ham frequencies
        k = (str)token, v = {spam_freq: , ham_freq:, prob_spam:, prob_ham:}
        """
        self.Parent.Destroy()

    def OnSave(self, evt):
        """ Generates token frequency table from training emails
        :return:  dict{k,v}:  spam/ham frequencies
        k = (str)token, v = {spam_freq: , ham_freq:, prob_spam:, prob_ham:}
        """
        print("save")

    def OnSaveAs(self, evt):
        """ Generates token frequency table from training emails
        :return:  dict{k,v}:  spam/ham frequencies
        k = (str)token, v = {spam_freq: , ham_freq:, prob_spam:, prob_ham:}
        """
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

class ToolBar(wx.ToolBar):
    def __init__(self, parent, ):       
        wx.ToolBar.__init__(self, parent=parent, style = wx.TB_RIGHT|wx.TE_HT_BEYOND )
        self.parent = parent
        self.SetMargins(100,100)
        self.AddTool(wx.ID_NEW, '', load_img('./img/save.png'))
        self.AddTool(wx.ID_OPEN, '', load_img('./img/save.png'))
        self.AddTool(wx.ID_SAVE, '', load_img('./img/save.png'))
        self.AddTool(wx.ID_DOWNLOAD_RUN, '', load_img('./img/save.png'))
        self.AddTool(wx.ID_DOWNLOAD_RUN, '', load_img('./img/save.png'))
        self.SetBackgroundColour("Orange")
        self.Realize()
        wx.EVT_MENU(parent, wx.ID_NEW, self.OnAddPage)

    def OnAddPage(self, event):
        new_tab = MyEditor(self.parent.MyNotebook)
        notebookP = self.parent.MyNotebook
        notebookP.AddPage(new_tab, "Tab %s" % notebookP.tab_num)
        notebookP.tab_num += 1    
