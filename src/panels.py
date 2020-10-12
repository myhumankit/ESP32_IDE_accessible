from Packages import random, os, codecs, threading, wxSerialConfigDialog, serial, asyncio, sys
import wx.stc as stc
import wx.py as pysh
import wx.lib.agw.flatnotebook as fnb
from Editor_Style import *
from Find_Replace import *
from Constantes import *
from Utilitaries import SendCmdAsync

def Init_Panels(frame):
    """Inits the three differents regions(treeCtrl, Notebook, Shell) in the MainWindow
    
    :param frame: MainWindow or window to split
    :type frame: MainWindow or other panel
    """    
    style = wx.SP_3D | wx.SP_NO_XP_THEME | wx.SP_PERMIT_UNSPLIT | wx.SP_LIVE_UPDATE
    frame.splitter_v = wx.SplitterWindow(frame, style=style, name="Dimension")
    frame.splitter_h = wx.SplitterWindow(frame.splitter_v, style=style, name="DIMENSION ALL")
    frame.MyNotebook = NotebookPanel(frame.splitter_h, frame)
    frame.FileTree = wx.Panel(frame.splitter_v)
    frame.Shell = ShellPanel(frame.splitter_h, frame)
    frame.splitter_v.SplitVertically(frame.FileTree , frame.splitter_h, 200)
    frame.splitter_h.SplitHorizontally(frame.MyNotebook, frame.Shell, 400)
    
    vbox = wx.BoxSizer(wx.VERTICAL)
    frame.device_tree = DeviceTree(frame.FileTree, frame, "", "Device")
    frame.workspace_tree = WorkspaceTree(frame.FileTree, frame)
    vbox.Add(frame.device_tree, 1, wx.EXPAND | wx.ALL)
    vbox.Add(frame.workspace_tree, 1, wx.EXPAND | wx.ALL)
    vbox.Add(ChooseWorkspace(frame.FileTree, frame), 1, wx.MINIMIZE)
    frame.FileTree.SetSizer(vbox)

class MyEditor(pysh.editwindow.EditWindow):
    """Customizable Editor page

    :param pysh.editwindow.EditWindow: see https://wxpython.org/Phoenix/docs/html/wx.py.html
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
        self.__set_style(parent)
        self.__attach_events()
        #self.write(text)
        self.SetValue(text)
    
    def __set_properties(self, parent, topwindow, on_card):
        """Set the properties and declare the variables of the instance
        
        :param parent: NotebookPanel class
        :type parent: NotebookPanel class
        :param topwindow: the MainWindow in this case
        :type parent: MainWindow class
        """
        self.topwindow = topwindow
        self.id = parent.tab_num
        self.filename = ""
        self.directory = ""
        self.saved = False
        self.last_save = ""
        self.theme = parent.theme
        self.findData = wx.FindReplaceData()
        self.txt = ""
        self.pos = 0
        self.size = 0
        self.on_card = on_card

    def __set_style(self, parent):
        """Load the first style of the editor

        :param parent: Notebook Panel
        :type parent: Notebook class
        """
        print("PARENT THEME = " + str(parent.theme))
        self.SetMarginType(1, stc.STC_MARGIN_NUMBER)
        self.SetMarginWidth(1, 25)
        Init_Editor_base(self)
        Change_Theme(self, themes[self.theme])

    def __attach_events(self):
        """
        Bind events related to this class
        """
        self.Bind(wx.EVT_TEXT, self.topwindow.ChangeStatus)
        self.Bind(wx.EVT_TEXT_ENTER, self.topwindow.ChangeStatus)
        
    def BindFindEvents(self, win):
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
        """Show the Find and Replace dialog and call the BindFindEvents method

        :param evt: , defaults to None
        :type evt: wx.Event, optional
        """
        dlg = wx.FindReplaceDialog(self, self.findData, "Find & Replace", wx.FR_REPLACEDIALOG)

        self.BindFindEvents(dlg)
        dlg.Show(True)

    def OnFind(self, evt):
        """Method to find a string on the current tab editor

        :param evt: Event which decide to what execute
        :type evt: wx.Event
        """
        self.txt = self.GetValue()
        map = {
            wx.wxEVT_COMMAND_FIND : "FIND",
            wx.wxEVT_COMMAND_FIND_NEXT : "FIND_NEXT",
            wx.wxEVT_COMMAND_FIND_REPLACE : "REPLACE",
            wx.wxEVT_COMMAND_FIND_REPLACE_ALL : "REPLACE_ALL",
            }

        et = evt.GetEventType()

        if et in map:
            evtType = map[et]
        if et in [wx.wxEVT_COMMAND_FIND_NEXT]:
            find_next(self, evt)
        if et in [wx.wxEVT_COMMAND_FIND_REPLACE]:
            replace(self, evt)
        if et in [wx.wxEVT_COMMAND_FIND_REPLACE_ALL]:
            while find_next(self, evt) == True:
                replace(self, evt)
        else:
            replaceTxt = ""

    def OnFindClose(self, evt):
        """Close the find and replace dialog

        :param evt: Event to close the dialog
        :type evt: wx.Event
        """
        print("FindReplaceDialog closing...\n")
        evt.GetDialog().Destroy()

class NotebookPanel(fnb.FlatNotebook):
    """Customized Notebook class

    :param fnb.FlatNotebook: A class of notebook to derivate
    :type fnb.FlatNotebook: wx.lib.agw.flatnotebook.FlatNotebook
    """
    def __init__(self, parent, topwindow):
        """ constructor to create a notebook multi-tabs
        
        :param parent: Splitter window (unused in methods, just to init)
        :type parent: wx.SplitterWindow
        :param topwindow: MainWindow to use her attibuts
        :type parent: MainWindow class
        
        """
        style = fnb.FNB_FF2 | wx.FULL_REPAINT_ON_RESIZE | fnb.FNB_COLOURFUL_TABS
        fnb.FlatNotebook.__init__(self, parent=parent, style=style, name="COUCOU")
        self.__set_properties(parent, topwindow)
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        self.Bind(wx.EVT_PAINT, self.on_paint)
    
    def on_paint(self, event):
        """Paint a gradient color on the Notebook background

        :param event: Event to repaint the notebook background
        :type event: wx.Event
        """
        self.dc = wx.PaintDC(self)
        x = 0
        y = 0
        w, h = self.GetSize()
        self.dc.GradientFillLinear((x, y, w, h), themes[self.theme][1][4],themes[self.theme][1][5])

    def __set_properties(self, parent, topwindow):
        """Set the properties and declare the variables of the instance
        
        :param parent: Splitter window (unused)
        :type parent: wx.SplitterWindow
        :param topwindow: the MainWindow in this case
        :type parent: MainWindow class
        """
        
        self.parent = parent
        self.topwindow = topwindow
        self.tab_num = 0
        self.data = ""
        self.dlg = None
        self.theme = 0
        self.Custom_Notebook(themes[self.theme])
        
    def Custom_Notebook(self, theme):
        """Custom the Notebook according to the theme passed on args

        :param theme: The theme to apply
        :type theme: list
        """
        self.SetActiveTabColour(theme[1][1])
        self.SetTabAreaColour(theme[1][3])
        self.SetActiveTabTextColour(theme[1][0])
        self.SetNonActiveTabTextColour(theme[1][7])
        
class FileTreePanel(wx.GenericDirCtrl):
    def __init__(self, parent, frame):
        """constructor for the File/dir Controller on the left
        
        :param training_dir: path of training directory with subdirectories
         '/ham' and '/spam'
        """
        wx.GenericDirCtrl.__init__(self, parent = parent)
        
        self.__set_properties(frame)
        self.__attach_events()
        self.ReCreateTree()

    def __set_properties(self, frame):
        self.frame = frame
        self.theme = frame.MyNotebook.theme
        self.tree = self.GetTreeCtrl()
        self.font = wx.Font(pointSize = 10, family = wx.FONTFAMILY_SWISS, style = wx.FONTSTYLE_SLANT, weight = wx.FONTWEIGHT_BOLD,  
                      underline = False, faceName ="Fira Code", encoding = 0)
        self.Custom_Tree_Ctrl(themes[self.theme])

    def __attach_events(self):
        self.Bind(wx.EVT_DIRCTRL_FILEACTIVATED, self.OnOpenFile)
        
    def Custom_Tree_Ctrl(self, theme):
        self.tree.SetBackgroundColour(theme[1][1])
        self.tree.SetFont(self.font)

    def OnOpenFile(self, evt):
        notebookP = self.frame.MyNotebook
        path = self.GetFilePath()
        file = os.path.split(path)
        directory = file[0]
        filename = file[1]
        filehandle = open(self.GetFilePath())
        # Check if a new tabe needs to be created to display contents of opened file
        if (notebookP.GetPageCount() == 1 
            and notebookP.GetCurrentPage().GetValue() == ""):
                notebookP.GetCurrentPage().SetValue(filehandle.read())
                notebookP.GetCurrentPage().filename = filename
                notebookP.GetCurrentPage().directory = directory
                notebookP.GetCurrentPage().last_save = notebookP.GetCurrentPage().GetValue()
                notebookP.GetCurrentPage().saved = True
        else:
            notebookP.tab_num += 1
            new_tab = MyEditor(notebookP, self.frame, "", False)
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
        
class WorkspaceTree(wx.GenericDirCtrl):
    def __init__(self, parent, frame):
        """constructor for the File/dir Controller on the left
        
        :param training_dir: path of training directory with subdirectories
         '/ham' and '/spam'
        """
        wx.GenericDirCtrl.__init__(self, parent = parent, style = wx.ALIGN_CENTER)
        
        self.__set_properties(frame)
        self.__attach_events()
        print(self.GetDefaultPath())

    def __set_properties(self, frame):
        self.frame = frame
        self.theme = frame.MyNotebook.theme
        self.tree = self.GetTreeCtrl()
        self.font = wx.Font(pointSize = 12, family = wx.FONTFAMILY_SWISS, style = wx.FONTSTYLE_SLANT, weight = wx.FONTWEIGHT_NORMAL,  
                      underline = False, faceName ="Fira Code", encoding = 0)
        self.Custom_Tree_Ctrl(themes[self.theme])

    def __attach_events(self):
        self.Bind(wx.EVT_DIRCTRL_FILEACTIVATED, self.OnOpenFile)
        
    def Custom_Tree_Ctrl(self, theme):
        self.tree.SetBackgroundColour(theme[1][1])
        self.tree.SetFont(self.font)

    def OnOpenFile(self, evt):
        notebookP = self.frame.MyNotebook
        path = self.GetFilePath()
        file = os.path.split(path)
        directory = file[0]
        filename = file[1]
        filehandle = open(self.GetFilePath())
        # Check if a new tabe needs to be created to display contents of opened file
        if (notebookP.GetPageCount() == 1 
            and notebookP.GetCurrentPage().GetValue() == ""):
                notebookP.GetCurrentPage().SetValue(filehandle.read())
                notebookP.GetCurrentPage().filename = filename
                notebookP.GetCurrentPage().directory = directory
                notebookP.GetCurrentPage().last_save = notebookP.GetCurrentPage().GetValue()
                notebookP.GetCurrentPage().saved = True
        else:
            notebookP.tab_num += 1
            new_tab = MyEditor(notebookP, self.frame, "", False)
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
        
class ChooseWorkspace(wx.DirPickerCtrl):
    def __init__(self, parent, frame):
        wx.DirPickerCtrl.__init__(self, parent, message="Hello")

        self.__set_properties(frame)
        self.Bind(wx.EVT_DIRPICKER_CHANGED, self.changeWorkspace)
    
    def __set_properties(self, frame):
        self.SetLabelText("Set your Workspace")
        self.frame = frame
    
    def changeWorkspace(self, evt):
        path = self.GetPath()
        self.frame.workspace_tree.SetPath(path)
        self.frame.workspace_tree.SetFocus()

def MyStatusBar(frame):
    statusbar = frame.CreateStatusBar(2, style= wx.STB_ELLIPSIZE_MIDDLE)
    statusbar.SetBackgroundColour("Grey")
    if frame.connected:
        statusbar.SetStatusText("Status: Connected", 1)
    else: 
        statusbar.SetStatusText("Status: Not Connected", 1)
    return statusbar

class TerminalSetup:
    """
    Placeholder for various terminal settings. Used to pass the
    options to the TerminalSettingsDialog.
    """
    def __init__(self):
        self.echo = False
        self.unprintable = False
        self.newline = NEWLINE_CRLF

class ShellPanel(wx.TextCtrl):
    def __init__(self, parent, frame):
        """ inits Spamfilter with training data

        :param training_dir: path of training directory with subdirectories
         '/ham' and '/spam'
        """
        wx.TextCtrl.__init__(self, parent=parent, style=wx.TE_MULTILINE | wx.TE_READONLY |wx.TE_RICH2)

        self.__set_properties__(frame)

    def __set_properties__(self, frame):
        self.top_window = frame
        self.SetName("Python Shell")
        self.theme = frame.MyNotebook.theme
        self.Custom_Shell(themes[self.theme])

    def Custom_Shell(self, theme):
        self.SetBackgroundColour("white")
        self.font = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, "Fira code")
        self.SetFont(self.font)
        #font = wx.Font(pointSize = 10, family = wx.FONTFAMILY_SWISS, style = wx.FONTSTYLE_SLANT, weight = wx.FONTWEIGHT_BOLD,  
        #              underline = False, faceName ="", encoding = 0)
        #self.SetFont(font)
    
    async def Asyncappend(self, data):
        self.AppendText(data)
        
class DeviceTree(wx.TreeCtrl):
    def __init__(self, parent, frame, paths, name):
        tID = wx.NewId()
        # Use the WANTS_CHARS style so the panel doesn't eat the Return key.
        wx.TreeCtrl.__init__(self, parent)
        self.frame = frame
        paths = paths
        isz = (16,16)
        self.il = wx.ImageList(isz[0], isz[1])
        self.fldridx     = self.il.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER,      wx.ART_OTHER, isz))
        self.fldropenidx = self.il.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_OTHER, isz))
        self.fileidx     = self.il.Add(wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, isz))
        self.font = wx.Font(pointSize = 12, family = wx.FONTFAMILY_SWISS, style = wx.FONTSTYLE_SLANT, weight = wx.FONTWEIGHT_NORMAL,  
                      underline = False, faceName ="Fira Code", encoding = 0)
        self.theme = frame.MyNotebook.theme
        self.root = self.AddRoot(name)

        self.SetImageList(self.il)
        self.SetItemData(self.root, None)
        self.SetItemImage(self.root, self.fldridx, wx.TreeItemIcon_Normal)
        self.SetItemImage(self.root, self.fldropenidx, wx.TreeItemIcon_Expanded)
        self.Custom_Tree_Ctrl(themes[self.theme])
        self.__attach_events()

    def __attach_events(self):
        self.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.OnItemExpanded, self)
        self.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.OnItemCollapsed, self)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, self)
        self.Bind(wx.EVT_TREE_BEGIN_LABEL_EDIT, self.OnBeginEdit, self)
        self.Bind(wx.EVT_TREE_END_LABEL_EDIT, self.OnEndEdit, self)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnActivate, self)

        self.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDClick)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)
        
    def Custom_Tree_Ctrl(self, theme):
        self.SetBackgroundColour(theme[1][1])
        self.SetFont(self.font)

    def OnRightDown(self, event):
        pt = event.GetPosition();
        item, flags = self.HitTest(pt)
        if item:
            sys.stdout.write("OnRightClick: %s, %s, %s\n" %
                               (self.GetItemText(item), type(item), item.__class__))
            self.SelectItem(item)

    def OnRightUp(self, event):
        pt = event.GetPosition();
        item, flags = self.HitTest(pt)
        if item:
            sys.stdout.write("OnRightUp: %s (manually starting label edit)\n"
                               % self.GetItemText(item))
            self.EditLabel(item)

    def OnBeginEdit(self, event):
        sys.stdout.write("OnBeginEdit\n")
        # show how to prevent edit...
        item = event.GetItem()
        if item and self.GetItemText(item) == "The Root Item":
            wx.Bell()
            sys.stdout.write("You can't edit this one...\n")

            # Lets just see what's visible of its children
            cookie = 0
            root = event.GetItem()
            (child, cookie) = self.GetFirstChild(root)

            while child.IsOk():
                sys.stdout.write("Child [%s] visible = %d" %
                                   (self.GetItemText(child),
                                    self.IsVisible(child)))
                (child, cookie) = self.GetNextChild(root, cookie)

            event.Veto()

    def OnEndEdit(self, event):
        sys.stdout.write("OnEndEdit: %s %s\n" %
                           (event.IsEditCancelled(), event.GetLabel()) )
        # show how to reject edit, we'll not allow any digits
        for x in event.GetLabel():
            if x in string.digits:
                sys.stdout.write("You can't enter digits...\n")
                event.Veto()
                return

    def OnLeftDClick(self, event):
        pt = event.GetPosition();
        item, flags = self.HitTest(pt)
        if item:
            sys.stdout.write("OnLeftDClick: %s\n" % self.GetItemText(item))
            parent = self.GetItemParent(item)
            if parent.IsOk():
                self.SortChildren(parent)
        event.Skip()

    def OnItemExpanded(self, event):
        item = event.GetItem()

    def OnItemCollapsed(self, event):
        item = event.GetItem()

    def OnSelChanged(self, event):
        self.item = event.GetItem()
        if self.item:
            sys.stdout.write("OnSelChanged: %s\n" % self.GetItemText(self.item))
            #items = self.GetSelections()
            #print(map(self.GetItemText, items))
        event.Skip()

    def OnActivate(self, event):
        if self.item:
            if self.GetItemImage(self.item, which=wx.TreeItemIcon_Normal):
                print("FILE")
                #TODO: Create path to open,
                self.path = ""
                self.root_it = self.GetRootItem()
                name = self.GetItemText(self.item)

                self.Get_Path_Item(self.item, name)
                print("Path = ", self.path)
                self.frame.show_cmd = False
                asyncio.run(SendCmdAsync(self.frame, "a = open('%s').read()\r\n"%self.path))
                asyncio.run(SendCmdAsync(self.frame, "print(a)\r\n"))
                res = self.frame.ReadCmd("print(a)")
                asyncio.run(SendCmdAsync(self.frame, "a.close()\r\n"))
                notebookP = self.frame.MyNotebook
                notebookP.tab_num += 1
                new_tab = MyEditor(notebookP, self.frame, str(res), True)
                new_tab.filename = name
                new_tab.directory = self.path
                new_tab = notebookP.AddPage(new_tab, "Tab %s" % notebookP.tab_num, select=True)
                self.frame.show_cmd = True
            sys.stdout.write("OnActivate: %s\n" % name)
            
    def Get_Path_Item(self, item, name):
        parent_it = self.GetItemParent(item)
        list = []
        while parent_it != self.root_it:
            list.insert(0, self.GetItemText(parent_it))
            parent_it = self.GetItemParent(parent_it)
        list.insert(0, self.GetItemText(parent_it))
        for i in list:
            if i == "Device":
                i = "."
            self.path += i + "/"
        self.path += name
