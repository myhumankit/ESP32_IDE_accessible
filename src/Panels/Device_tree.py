import wx, asyncio, json, os, sys, string
from utilitaries import SendCmdAsync, put_cmd, get_cmd_result
from all_panels import MyEditor

class DeviceTree(wx.TreeCtrl):
    def __init__(self, parent, main_window, paths, name):
        tID = wx.NewId()
        # Use the WANTS_CHARS style so the panel doesn't eat the Return key.
        wx.TreeCtrl.__init__(self, parent)
        self.main_window = main_window
        paths = paths
        isz = (16,16)
        self.il = wx.ImageList(isz[0], isz[1])
        self.fldridx     = self.il.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER,      wx.ART_OTHER, isz))
        self.fldropenidx = self.il.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_OTHER, isz))
        self.fileidx     = self.il.Add(wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, isz))
        self.font = wx.Font(pointSize = 12, family = wx.FONTFAMILY_SWISS, style = wx.FONTSTYLE_SLANT, weight = wx.FONTWEIGHT_NORMAL,
                      underline = False, faceName ="Fira Code", encoding = 0)
        self.theme_choice = main_window.notebook.theme_choice
        self.main_root = self.AddRoot("")
        self.device = self.AppendItem(self.main_root, "Device")
        self.sd = self.AppendItem(self.main_root, "Sd")
        self.workspace = self.AppendItem(self.main_root, "Workspace")
        self.Expand(self.main_root)

        self.SetImageList(self.il)
        self.SetItemData(self.device, None)
        self.SetItemImage(self.device, self.fldridx, wx.TreeItemIcon_Normal)
        self.SetItemImage(self.device, self.fldropenidx, wx.TreeItemIcon_Expanded)
        self.custom_tree_ctrl()
        self.__attach_events()

    def fill_workspace(self, device, path):
        for a, directories, files in os.walk(path):  
            for dire in directories:
                child = self.AppendItem(device, dire)
                self.SetItemImage(child, self.fldridx, wx.TreeItemIcon_Normal)
                self.SetItemImage(child, self.fldropenidx, wx.TreeItemIcon_Expanded)
                self.fill_workspace(child, path + "/" + dire)
            for file in files:
                child = self.AppendItem(device, file)
                self.SetItemImage(child, self.fileidx, wx.TreeItemIcon_Normal)
                self.SetItemImage(child, self.fileidx, wx.TreeItemIcon_Expanded)

    def __attach_events(self):
        self.Bind(wx.EVT_TREE_ITEM_EXPANDED, self.OnItemExpanded, self)
        self.Bind(wx.EVT_TREE_ITEM_COLLAPSED, self.OnItemCollapsed, self)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, self)
        self.Bind(wx.EVT_TREE_BEGIN_LABEL_EDIT, self.OnBeginEdit, self)
        self.Bind(wx.EVT_TREE_END_LABEL_EDIT, self.OnEndEdit, self)
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnActivate, self)
        self.Bind(wx.EVT_RIGHT_DCLICK, self.OnClipboardMenu)
        self.Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDClick)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.Bind(wx.EVT_RIGHT_UP, self.OnClipboardMenu)
        
    def custom_tree_ctrl(self):
        """Custom the tree controller

        :param theme: theme to apply on the tree
        :type theme: list
        """
        try:
            file = open("./customize.json")
            theme = json.load(file)
            theme = theme[self.theme_choice]
            file.close()

            self.SetBackgroundColour(theme['Panels Colors']['Filetree background'])
            self.SetForegroundColour(theme['Panels Colors']['Text foreground'])
            self.SetFont(self.font)
        except Exception as e:
            print(e)

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
            device = event.GetItem()
            (child, cookie) = self.GetFirstChild(device)

            while child.IsOk():
                sys.stdout.write("Child [%s] visible = %d" %
                                   (self.GetItemText(child),
                                    self.IsVisible(child)))
                (child, cookie) = self.GetNextChild(device, cookie)

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
        pt = event.GetPosition()
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
            ##print(map(self.GetItemText, items))
        event.Skip()

    def OnActivate(self, event):
        self.path = ""
        if self.item:
            if self.item == self.workspace:
                self.define_workspace()
            elif self.GetItemImage(self.item, which=wx.TreeItemIcon_Normal):
               self.open_file()
        sys.stdout.write("OnActivate: %s\n" % self.path)
         
    def get_path_item(self, item, name):
        """Catch the path name of an item in the tree

        :param item: Item to find path
        :type item: wx.ItemId
        :param name: Name of the item
        :type name: str
        """
        parent_it = self.GetItemParent(item)
        list = []
        while parent_it != self.device:
            list.insert(0, self.GetItemText(parent_it))
            parent_it = self.GetItemParent(parent_it)
        list.insert(0, self.GetItemText(parent_it))
        for i in list:
            if i == "Device":
                i = "."
            self.path += i + "/"
        self.path += name

    def open_file(self):
        """
        docstring
        """
        #print("FILE")
        name = self.GetItemText(self.item)
        self.get_path_item(self.item, name)
        #print("Path = ", self.path)
        self.main_window.q_serial.put("a = open('%s','r')\r\n" % self.path)
        self.main_window.q_serial.put("#print(a.read())\r\n")
        res = self.main_window.result
        self.main_window.q_serial.put("a.close()\r\n")
        self.main_window.shell_text = ""
        notebookP = self.main_window.notebook
        new_tab = MyEditor(notebookP, self.main_window, str(res), True)
        new_tab.filename = name
        new_tab.directory = self.path
        new_tab = notebookP.AddPage(new_tab, "%s" % name, select=True)
        notebookP.tab_num = notebookP.GetPageCount()

    def define_workspace(self):
        notebookP = self.main_window.notebook
        dialog = wx.DirDialog(self.main_window, 
                        "Choose a Worspace", 
                        "",  
                        wx.FD_OPEN)
        dialog.CenterOnParent()
        if dialog.ShowModal() == wx.ID_OK:
            path = dialog.GetPath()
            self.fill_workspace(self.workspace, path)

    def OnClipboardMenu(self, evt):
        img = self.GetItemImage(self.item)
        if img == self.fldridx or img == self.fldropenidx:
            #print("DIR")
            menu = ClipboardMenuDevice(True, self.main_window, self.item)
            self.main_window.PopupMenu(menu)
            menu.Destroy()
        else:
            #print("File")
            menu = ClipboardMenuDevice(False, self.main_window, self.item)
            self.main_window.PopupMenu(menu)
            menu.Destroy()

    def set_focus_tree(self, evt):
        self.SetFocus()
class ClipboardMenuDevice(wx.Menu):
    """[summary]

    :param wx: [description]
    :type wx: [type]
    """
    def __init__(self, is_dir, main_window, item):
        wx.Menu.__init__(self)
        self.is_dir_menu = is_dir
        self.main_window = main_window
        self.device_tree = main_window.device_tree
        self.item = item
        self.__set_properties(main_window)
        self.__attach_events()

    def __set_properties(self, main_window):
        if self.is_dir_menu:
            self.Append(wx.ID_NEW, "&New file")
            self.Append(wx.ID_DIRECTORY, "&New Directory")
        else:
            self.Append(wx.ID_RUN, "&Run")
            self.Append(wx.ID_OPEN, "&Open")
            self.Append(wx.ID_CLOSE, "&Close")
            self.Append(wx.ID_DELETE, "&Delete")
            self.Append(wx.ID_DEFAULT, "&Default Run")
            self.Append(wx.ID_RENAME, "&Rename")

    #TODO: FAIRE TOUS LES EVENTS
    def __attach_events(self):
        self.Bind(wx.EVT_MENU, self.OnNewdir, id=wx.ID_DIRECTORY)
        self.Bind(wx.EVT_MENU, self.OnRun, id=wx.ID_RUN)
        self.Bind(wx.EVT_MENU, self.main_window.device_tree.OnActivate, id=wx.ID_OPEN)
        self.Bind(wx.EVT_MENU, self.OnClose, id=wx.ID_CLOSE)
        self.Bind(wx.EVT_MENU, self.OnDelete, id=wx.ID_DELETE)
        self.Bind(wx.EVT_MENU, self.OnDefaultRun, id=wx.ID_DEFAULT)

    def OnRun(self, evt):
        self.device_tree.path = ""
        self.device_tree.root_it = self.device_tree.GetRootItem()
        name = self.device_tree.GetItemText(self.item)
        self.device_tree.get_path_item(self.item, name)
        self.main_window.q_serial.put("exec(open('%s').read())\r\n"%self.device_tree.path)

    def OnNewdir(self, evt):
        self.device_tree.path = ""
        self.device_tree.root_it = self.device_tree.GetRootItem()
        name = self.device_tree.GetItemText(self.item)
        self.device_tree.get_path_item(self.item, name)
        ok = False
        while not ok:
            with wx.TextEntryDialog(self.main_window, "Select the name of the new directory") as dlg:
                dlg.CenterOnParent()
                result = dlg.ShowModal()
                if result == wx.ID_OK or evt is not None:
                    path = self.device_tree.path + "/" + dlg.GetValue()
                    self.main_window.q_serial.put( "os.mkdir('%s',0755)\r\n"%self.device_tree.path)
                    ok = True
                    treeModel(self.main_window)
                else:
                    ok = True

    def OnClose(self, evt):
        #CHECK SI UNE PAGE AVEC LE NOM DU PATH EST OUVERTE DANS L'EDITEUR
        path = self.item.GetPath()
        #print(path)

    def OnDelete(self, evt):
        self.device_tree.path = ""
        self.device_tree.root_it = self.device_tree.GetRootItem()
        name = self.device_tree.GetItemText(self.item)
        self.device_tree.get_path_item(self.item, name)
        self.main_window.q_serial.put( "os.remove('%s')\r\n"%self.device_tree.path)
        treeModel(self.main_window)

    def OnDefaultRun(self, evt):
        self.device_tree.path = ""
        self.device_tree.root_it = self.device_tree.GetRootItem()
        name = self.device_tree.GetItemText(self.item)
        self.device_tree.get_path_item(self.item, name)
        setDefaultProg(self.main_window, self.device_tree.path)
        treeModel(self.main_window)

    def OnNewFile(self, evt):
        self.device_tree.path = ""
        self.device_tree.root_it = self.device_tree.GetRootItem()
        name = self.device_tree.GetItemText(self.item)
        self.device_tree.get_path_item(self.item, name)
        ok = False
        while not ok:
            with wx.TextEntryDialog(self.main_window, "Select the name of the new file") as dlg:
                dlg.CenterOnParent()
                result = dlg.ShowModal()
                if result == wx.ID_OK or evt is not None:
                    path = self.device_tree.path + "/" + dlg.GetValue()
                    self.main_window.q_serial.put( "myfile = open('%s', 'w')\r\n"%self.device_tree.path)
                    self.main_window.q_serial.put( "myfile.close()\r\n")
                    ok = True
                    treeModel(self.main_window)
                else:
                    ok = True

def setDefaultProg(main_window,filename):
    #print("setDefaultProg:%s"%filename)
    main_window.show_cmd = False
    ProgMsg= ""
    cmd = "myfile=open(\'main.py\',\'w\')\r\n"
    ProgMsg = get_cmd_result(main_window, cmd)
    if ProgMsg.find("Traceback")>=0 or ProgMsg.find("... ")>=0:
        main_window.q_serial.put("\x03")
        return
    cmd = "myfile.write(\"exec(open(\'%s\').read(),globals())\")\r\n"%str(filename)
    ProgMsg = get_cmd_result(main_window, cmd)
    if ProgMsg.find("Traceback")>=0 or ProgMsg.find("... ")>=0:
        main_window.q_serial.put("\x03")
        return
    cmd = "myfile.close()\r\n"
    ProgMsg = get_cmd_result(main_window, cmd)
    if ProgMsg.find("Traceback")>=0 or ProgMsg.find("... ")>=0:
        main_window.q_serial.put("\x03")
        return
    main_window.show_cmd = True

def getFileTree(main_window, dir):
        #print("GET FILE TREE : %s"%(dir))
        main_window.cmd_return = ""
        main_window.get_cmd = True
        result = get_cmd_result(main_window, "os.listdir(\'%s\')\r\n"%dir)
        if result=="err":
            return result
        filemsg=result[result.find("["):result.find("]")+1]
        #print("FILEMSG = " + filemsg)

        ret=json.loads("{}")
        ret[dir]=[]
        if filemsg=="[]":
            return ret
        filelist=[]
        filemsg=filemsg.split("'")
        
        for i in filemsg:
            if i.find("[")>=0 or i.find(",")>=0 or i.find("]")>=0:
                pass
            else:
                filelist.append(i)
        #print("FILE LIST =" ,filelist)
        for i in filelist:
            res = get_cmd_result(main_window, "os.stat(\'%s\')\r\n"%(dir + "/" + i))
            if res == "err":
                return res
            isdir=res.split("\n")[1]
            isdir=isdir.split(", ")
            #print("ISDIR = ", isdir)
            try:
                adir = isdir[0]
                if adir.find("(")>=0:
                    adir = adir[1:]
                if adir.find(")")>=0:
                    adir = adir[:-1]
                #print("ADIR = ", adir)
                if int(adir)==0o040000:
                    if i=="System Volume Information":
                        pass
                    else:
                        ret[dir].append(getFileTree(main_window, dir+"/"+i))
                else:
                    ret[dir].append(i)
            except Exception as e:
                #print("ERROr: " + e)
                return "err"
        return ret

def treeModel(main_window):
        main_window.show_cmd = False
        main_window.reflushTreeBool= True
        main_window.cmd_return = ""
        main_window.device_tree.DeleteChildren(main_window.device_tree.device)
        res=json.loads("{}")
        res=getFileTree(main_window, ".")

        if res=="err":
            main_window.cmd_return = ""
            return
        #print("RESSSSSSS")
        #print(res)
        try:
            ReflushTree(main_window,main_window.device_tree.device,res['.'])
        except Exception as e:
            print(e)
        main_window.cmd_return =""
        main_window.show_cmd = True
    
def ReflushTree(main_window, device, msg):
        if msg=="err":
            #print("soucii")
            return
        #print("reflushTree=====================%s"%msg)
        #print("MSG " + str(msg))
        tree = main_window.device_tree
        if type(msg) is str: #: fichier
            child = tree.AppendItem(device, msg)
            tree.SetItemImage(child, tree.fileidx, wx.TreeItemIcon_Normal)
            tree.SetItemImage(child, tree.fileidx, wx.TreeItemIcon_Expanded)
            
        elif type(msg) is dict: #: dossier
            for i in msg:
                k=eval("%s"%msg[i])
                i=i.split("/")
                child = tree.AppendItem(device, i[1])
                tree.SetItemImage(child, tree.fldridx, wx.TreeItemIcon_Normal)
                tree.SetItemImage(child, tree.fldropenidx, wx.TreeItemIcon_Expanded)
                ReflushTree(main_window, child, k)
        elif type(msg) is list: #:liste de fichiers
            for i in msg:
                if type(i) is str:
                    ReflushTree(main_window, device, i)
                elif type(i) is dict:
                    ReflushTree(main_window, device, i)           
                else:
                    pass

def save_on_card(main_window, page):
    #print(page.directory)
    #print(page.filename)
    notebookP = main_window.notebook

    # Check if save is required
    if (page.GetValue() != page.last_save):
        page.saved = False
        # Grab the content to be saved
        save_as_file_content = page.GetValue()
        #print("|+|",save_as_file_content, "|+|")
        main_window.show_cmd = False
        cmd = "f = os.remove('%s')\r\n" % (page.directory + "/" + page.filename)
        main_window.q_serial.put(cmd)
        cmd = "f = open('%s', 'wb')\r\n" % (page.directory + "/" + page.filename)
        main_window.q_serial.put(cmd)
        cmd = "f.write(%s)\r\n" % save_as_file_content
        main_window.q_serial.put(cmd)
        cmd = "f.close()\r\n"
        main_window.q_serial.put(cmd)
        page.last_save = save_as_file_content
        page.saved = True
        treeModel(main_window)
        main_window.shell.AppendText("Content Saved\n")
        self.main_window.q_serial.put("Content Saved")
