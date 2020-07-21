import wx
from Panels import *
from Utilitaries import load_img

wx.ID_REFLUSH_DIR = 250
wx.ID_EXAMPLES = 251
wx.ID_SYNTAX_CHECK = 252
wx.ID_DOWNLOAD_RUN = 253

def Init_Top_Menu(frame):
    """Inits and place the top menu

    :param frame: Mainwindow
    :type frame: Mainwindow
    """    
    frame.top_menu = TopMenu(frame)
    frame.SetMenuBar(frame.top_menu)

def Init_ToolBar(frame):
    """Inits and place the toolbar

    :param frame: Mainwindow
    :type frame: Mainwindow
    """    
    frame.ToolBar = ToolBar(frame)
    frame.SetToolBar(frame.ToolBar)

def create_File_Menu():
    """Inits a File menu and his buttons (Save, Open,...)

    :return: the File menu filled by buttons
    :rtype: wx.Menu see https://wxpython.org/Phoenix/docs/html/wx.Menu.html
    """    
    MenuFile = wx.Menu(style = wx.MENU_TEAROFF)
    MenuFile.Append(wx.ID_NEW, "&New\tCTRL+N")
    MenuFile.Append(wx.ID_SAVE, "&Save\tCTRL+S")
    MenuFile.Append(wx.ID_SAVEAS, "&Save as\tCTRL+A")
    MenuFile.Append(wx.ID_OPEN, "&Open\tCTRL+O")
    MenuFile.Append(wx.ID_REFLUSH_DIR, "&Reflush Directory")
    MenuFile.Append(wx.ID_EXAMPLES, "&Examples")
    MenuFile.Append(wx.ID_EXIT, "&Exit\tCTRL+Q")
    MenuFile.Append(wx.ID_CLOSE, "&Close\tCTRL+W")
    MenuFile.AppendSeparator()
    return MenuFile

def create_Edit_Menu():
    """Inits a Edit menu and his buttons (Copy, Paste, Find,...)

    :return: the Edit menu filled by buttons
    :rtype: wx.Menu see https://wxpython.org/Phoenix/docs/html/wx.Menu.html
    """    
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
    """TopMenu class which contains the Edit and File Menus

    :param wx.MenuBar: Parent class to contain menus see  https://wxpython.org/Phoenix/docs/html/wx.MenuBar.html
    """    
    def __init__(self, parent):
        """Constructor which append the Edit and File Menus on the Menubar and bind related events

        :param parent: Parent class (in this case MainWindow)
        :type parent: class Mainwindow
        """        
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
        self.Bind(wx.EVT_MENU,  self.OnAddPage, id=wx.ID_NEW)
        self.Bind(wx.EVT_MENU,  self.OnClosePage, id=wx.ID_CLOSE)

    def OnExit(self, evt):
        """Quit the app

        :param evt: always to get the macrocode
        :type evt: (wx.event ?)
        """        
        self.Parent.Destroy()

    def OnSave(self, evt):
        """Save the current page of the notebook

        :param evt: always to get the macrocode
        :type evt: (wx.event ?)
        """   
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
        """Open a wx.filedialog to Save as a file the text of the current editor

        :param evt: always to get the macrocode
        :type evt: (wx.event ?)
        """   
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
            """Open a wx.filedialog to open a file on a editor 

            :param evt: always to get the macrocode
            :type evt: (wx.event ?)
            """  
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
        """Copy the selection on the clipboard

        :param evt: always to get the macrocode
        :type evt: (wx.event ?)
        """  
        self.parent.MyNotebook.GetCurrentPage().Copy()

    def OnPaste(self, event):
        """Paste the content of the clipboard

        :param evt: always to get the macrocode
        :type evt: (wx.event ?)
        """  
        self.parent.MyNotebook.GetCurrentPage().Paste()

    def OnRedo(self, event):
        """Redo

        :param evt: always to get the macrocode
        :type evt: (wx.event ?)
        """  
        self.parent.MyNotebook.GetCurrentPage().Redo()

    def OnUndo(self, event):
        """Undo

        :param evt: always to get the macrocode
        :type evt: (wx.event ?)
        """  
        self.parent.MyNotebook.GetCurrentPage().Undo()

    def OnFindReplace(self, event):
        """Open a wx.FindReplaceDialog to find and/, replace text in the current editor

        :param evt: always to get the macrocode
        :type evt: (wx.event ?)
        """  
        notebookP = self.parent.MyNotebook
        notebookP.data = wx.FindReplaceData()   # initializes and holds search parameters
        notebookP.dlg = wx.FindReplaceDialog(notebookP.GetCurrentPage(), notebookP.data, 'Find')
        notebookP.dlg.Show()
        data = notebookP.GetCurrentPage().OnFindReplace()

    def OnAddPage(self, event):
        """Add a new page on the notebook

        :param evt: always to get the macrocode
        :type evt: (wx.event ?)
        """  
        new_tab = MyEditor(self.parent.MyNotebook)
        notebookP = self.parent.MyNotebook
        notebookP.tab_num += 1
        new_tab = notebookP.AddPage(new_tab, "Tab %s" % notebookP.tab_num)

    def OnClosePage(self, event):
        dataNoteBook = self.parent.MyNotebook
        page = dataNoteBook.GetCurrentPage()
        pageTitle = dataNoteBook.GetPageText()
        for index in range(dataNoteBook.GetPageCount()):
            print (dataNoteBook.GetPageText(index))
            if dataNoteBook.GetPageText(index) == pageTitle:
                dataNoteBook.DeletePage(index)
                break
class ToolBar(wx.ToolBar):
    """MOMENT : Derivated class to set A toolbar maybe we'll erase this derivated class

    :param wx.ToolBar: see https://wxpython.org/Phoenix/docs/html/wx.ToolBar.html
    """    
    def __init__(self, parent, ):
        """constructor for ToolBar 

        :param parent: Parent class generally the main window
        :type parent: MainWindow (generally)
        """           
        wx.ToolBar.__init__(self, parent=parent, style= wx.TB_RIGHT)
        self.CentreOnParent()
        self.parent = parent
        #self.AddTool(wx.ID_NEW, '', load_img('./img/save.png'))
        #self.AddTool(wx.ID_OPEN, '', load_img('./img/save.png'))
        #self.AddTool(wx.ID_SAVE, '', load_img('./img/save.png'))
        #self.AddTool(wx.ID_DOWNLOAD_RUN, '', load_img('./img/save.png'))
        #self.AddTool(wx.ID_DOWNLOAD_RUN, '', load_img('./img/save.png'))
        self.SetBackgroundColour("Orange")
        self.Realize()
        self.Bind(wx.EVT_MENU, parent.top_menu.OnAddPage, id=wx.ID_NEW)
        self.Bind(wx.EVT_MENU, parent.top_menu.OnOpen, id=wx.ID_OPEN)
        self.Bind(wx.EVT_MENU, parent.top_menu.OnSave, id=wx.ID_SAVE)