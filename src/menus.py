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
    MenuEdit.Append(wx.ID_UNDO, "&Redo\tCTRL+Z")
    MenuEdit.Append(wx.ID_SYNTAX_CHECK, "&Syntax Check")
    MenuEdit.Append(wx.ID_FIND, "&Find and/or Replace\tCTRL+F")
    MenuEdit.AppendSeparator()
    return MenuEdit

class TopMenu(wx.MenuBar):
    def __init__(self, parent):       
        wx.MenuBar.__init__(self, wx.ID_TOP)
        self.parent = parent
        self.MenuFile = create_File_Menu()
        self.MenuEdit = create_Edit_Menu()
        self.Append(self.MenuFile, "&File")
        self.Append(self.MenuEdit, "&Edit")
        self.Bind(wx.EVT_MENU,  self.OnExit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU,  self.OnOpen, id=wx.ID_OPEN)
        self.Bind(wx.EVT_MENU,  self.OnSaveAs, id=wx.ID_SAVEAS)
        self.Bind(wx.EVT_MENU,  self.OnCopy, id=wx.ID_COPY)
        self.Bind(wx.EVT_MENU,  self.OnPaste, id=wx.ID_PASTE)
        self.Bind(wx.EVT_MENU,  self.OnFindReplace, id=wx.ID_FIND)


    def OnExit(self, evt):
        self.Parent.Destroy()

    def OnSave(self, evt):
        notebookP = self.parent.MyNotebook
        # Check if save is required
        if (notebookP.GetCurrentPage().GetValue() 
            != notebookP.GetCurrentPage().last_save):
            notebookP.GetCurrentPage().saved = False

        # Check if Save should bring up FileDialog
        if (notebookP.GetCurrentPage().saved == False 
            and notebookP.GetCurrentPage().last_save == ""): 
            dialog = wx.FileDialog(self, 
                                   "Choose a file", 
                                   notebookP.GetCurrentPage().directory, 
                                   "", 
                                   "*", 
                                   wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
            if dialog.ShowModal() == wx.ID_OK:
                # Grab the content to be saved
                save_as_file_contents = notebookP.GetCurrentPage().GetValue()

                # Open, Write & Close File
                save_as_name = dialog.GetFilename()
                save_as_directory = dialog.GetDirectory()    
                filehandle=open(os.path.join(save_as_directory, save_as_name), 'w')
                filehandle.write(save_as_file_contents)
                filehandle.close()
                notebookP.SetPageText(notebookP.GetSelection(), save_as_name)
                notebookP.GetCurrentPage().filename = save_as_name
                notebookP.GetCurrentPage().directory = save_as_directory
                notebookP.GetCurrentPage().last_save = save_as_file_contents
                notebookP.GetCurrentPage().saved = True
        else:
            # Grab the content to be saved
            save_as_file_contents = notebookP.GetCurrentPage().GetValue()
            filehandle=open(os.path.join(notebookP.GetCurrentPage().directory, 
                                         notebookP.GetCurrentPage().filename), 'w')
            filehandle.write(save_as_file_contents)
            filehandle.close()
            notebookP.GetCurrentPage().last_save = save_as_file_contents
            notebookP.GetCurrentPage().saved = True

    def OnSaveAs(self, evt):
        notebookP = self.parent.MyNotebook
        dialog = wx.FileDialog(self, 
                               "Choose a file", 
                               notebookP.GetCurrentPage().directory, 
                               "", 
                               "*.py*", 
                               wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if dialog.ShowModal() == wx.ID_OK:
            # Grab the content to be saved
            save_as_file_contents = notebookP.GetCurrentPage().GetValue()
            # Open, Write & Close File
            save_as_name = dialog.GetFilename()
            save_as_directory = dialog.GetDirectory()
            filehandle=open(os.path.join(save_as_directory, save_as_name), 'w')
            filehandle.write(save_as_file_contents)
            filehandle.close()
            notebookP.SetPageText(notebookP.GetSelection(), save_as_name)
            notebookP.GetCurrentPage().filename = save_as_name
            notebookP.GetCurrentPage().directory = save_as_directory
            notebookP.GetCurrentPage().last_save = save_as_file_contents
            notebookP.GetCurrentPage().saved = True
        dialog.Destroy()

    def OnOpen(self, evt):
            notebookP = self.parent.MyNotebook
            dialog = wx.FileDialog(self, 
                               "Choose a File", 
                               notebookP.GetCurrentPage().directory, 
                               "", 
                               "*", 
                               wx.FD_OPEN)
            if dialog.ShowModal() == wx.ID_OK:
                filename = dialog.GetFilename()
                directory = dialog.GetDirectory()
                filehandle = open(os.path.join(directory, filename), 'r')
                # Check if a new tabe needs to be created to display contents of opened file
                if (notebookP.GetPageCount() == 1 
                    and notebookP.GetCurrentPage().GetValue() == ""):
                    notebookP.GetCurrentPage().SetValue(filehandle.read())
                    notebookP.GetCurrentPage().filename = filename
                    notebookP.GetCurrentPage().directory = directory
                    notebookP.GetCurrentPage().last_save = notebookP.GetCurrentPage().GetValue()
                    notebookP.GetCurrentPage().saved = True
                else:
                    print("")
                    new_tab = MyEditor(notebookP)
                    new_tab.filename = filename
                    new_tab.directory = directory
                    notebookP.AddPage(new_tab, filename, select = True)
                    wx.CallAfter(new_tab.SetFocus)
                # Populate the tab with file contents
                    new_tab.SetValue(filehandle.read())
                    new_tab.last_save = new_tab.GetValue()
                    new_tab.saved = True
                notebookP.SetPageText(notebookP.GetSelection(), filename)
                filehandle.close()
            dialog.Destroy()

    def OnCopy(self, event):
        self.parent.MyNotebook.GetCurrentPage().Copy()

    def OnPaste(self, event):
        self.parent.MyNotebook.GetCurrentPage().Paste()

    def OnRedo(self, event):
        self.parent.MyNotebook.GetCurrentPage().Redo()

    def OnUndo(self, event):
        self.parent.MyNotebook.GetCurrentPage().Undo()

    def OnFindReplace(self, event):
        notebookP = self.parent.MyNotebook
        notebookP.data = wx.FindReplaceData()   # initializes and holds search parameters
        notebookP.dlg = wx.FindReplaceDialog(notebookP.GetCurrentPage(), notebookP.data, 'Find')
        notebookP.dlg.Show()
        data = notebookP.GetCurrentPage().OnFindReplace()

class ToolBar(wx.ToolBar):
    def __init__(self, parent, ):       
        wx.ToolBar.__init__(self, parent=parent, style= wx.TB_RIGHT)
        self.CentreOnParent()
        self.parent = parent
        #self.AddTool(wx.ID_NEW, '', load_img('./img/save.png'))
        #self.AddTool(wx.ID_OPEN, '', load_img('./img/save.png'))
        #self.AddTool(wx.ID_SAVE, '', load_img('./img/save.png'))
        # self.AddTool(wx.ID_DOWNLOAD_RUN, '', load_img('./img/save.png'))
        # self.AddTool(wx.ID_DOWNLOAD_RUN, '', load_img('./img/save.png'))
        self.SetBackgroundColour("Orange")
        self.Realize()
        self.Bind(wx.EVT_MENU, self.OnAddPage, id=wx.ID_NEW)
        self.Bind(wx.EVT_MENU, parent.top_menu.OnOpen, id=wx.ID_OPEN)
        self.Bind(wx.EVT_MENU, parent.top_menu.OnSave, id=wx.ID_SAVE)

    def OnAddPage(self, event):
        new_tab = MyEditor(self.parent.MyNotebook)
        notebookP = self.parent.MyNotebook
        notebookP.AddPage(new_tab, "Tab %s" % notebookP.tab_num)
        notebookP.tab_num += 1    