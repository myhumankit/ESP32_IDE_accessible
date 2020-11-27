""" Module which contains the classes related to the TreeView
"""

import wx
import json
import os
import sys
from Utils.voice_synthese import my_speak
from Serial_manager.send_infos import put_cmd
import time


class DeviceTree(wx.TreeCtrl):
    """[summary]

    :param wx.TreeCtrl: Class to derivate 
    :type wx.TreeCtrl: :class:wx.TreeCtrl
    """
    def __init__(self, parent, frame):
        """Constructor method

        :param parent: parent of the instance
        :type parent: :class:
        :param frame: main window if the application
        :type frame: :class:MainWindow
        """
        wx.TreeCtrl.__init__(self, parent)
        self.frame = frame
        isz = (16, 16)
        self.il = wx.ImageList(isz[0], isz[1])
        self.fldridx = self.il.Add(wx.ArtProvider.GetBitmap(
            wx.ART_FOLDER_OPEN, wx.ART_OTHER, isz))
        self.fldropenidx = self.il.Add(wx.ArtProvider.GetBitmap(
            wx.ART_FOLDER_OPEN, wx.ART_OTHER, isz))
        self.fileidx = self.il.Add(wx.ArtProvider.GetBitmap(
            wx.ART_NORMAL_FILE, wx.ART_OTHER, isz))
        self.font = wx.Font(pointSize=12,
                            family=wx.FONTFAMILY_SWISS,
                            style=wx.FONTSTYLE_SLANT,
                            weight=wx.FONTWEIGHT_NORMAL,
                            underline=False,
                            faceName="Arial", encoding=0)
        self.theme_choice = frame.notebook.theme_choice
        self.main_root = self.AddRoot("")
        self.device = self.AppendItem(self.main_root, "Device")
        self.sd = self.AppendItem(self.main_root, "Librairies")
        self.workspace = self.AppendItem(self.main_root, "Workspace")
        self.Expand(self.main_root)

        self.SetImageList(self.il)
        self.SetItemData(self.device, None)
        self.SetItemImage(self.device, self.fldridx, wx.TreeItemIcon_Normal)
        self.SetItemImage(self.device, self.fldropenidx,
                          wx.TreeItemIcon_Expanded)
        self.custom_tree_ctrl()
        self.__attach_events()

    def fill_workspace(self, item, path):
        """Manage the creation of the treeview item selected (recursive)

        :param section: section to build
        :type section: wx.TreeItem
        :param path: path to analyse
        :type path: str
        """
        for a, directories, files in os.walk(path):
            for dire in directories:
                child = self.AppendItem(item, dire)
                self.SetItemImage(child, self.fldridx, wx.TreeItemIcon_Normal)
                self.SetItemImage(child, self.fldropenidx,
                                  wx.TreeItemIcon_Expanded)
                self.fill_workspace(child, path + "/" + dire)
            for file in files:
                child = self.AppendItem(item, file)
                self.SetItemImage(child, self.fileidx, wx.TreeItemIcon_Normal)
                self.SetItemImage(child, self.fileidx, wx.TreeItemIcon_Expanded)

    def __attach_events(self):
        """ Bind events with methods
         """
        self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnActivate, self)
        self.Bind(wx.EVT_RIGHT_DCLICK, self.OnClipboardMenu)
        self.Bind(wx.EVT_RIGHT_UP, self.OnClipboardMenu)
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, self)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.Bind(wx.EVT_RIGHT_UP, self.OnClipboardMenu)

    def custom_tree_ctrl(self):
        """Custom the treeView with the theme selected
         """
        try:
            file = open("./customize.json")
            theme = json.load(file)
            theme = theme[self.theme_choice]
            file.close()

            self.SetBackgroundColour(
                theme['Panels Colors']['Filetree background'])
            self.SetForegroundColour(theme['Panels Colors']['Text foreground'])
            self.SetFont(self.font)
        except Exception as e:
            print(e)

    def OnRightDown(self, event):
        pt = event.GetPosition()
        item, flags = self.HitTest(pt)

        if item:
            sys.stdout.write("OnRightClick: %s, %s, %s\n" %
                             (self.GetItemText(item),
                              type(item), item.__class__))
            self.SelectItem(item)

    def OnRightUp(self, event):
        pt = event.GetPosition()
        item, flags = self.HitTest(pt)
        if item:
            sys.stdout.write("OnRightUp: %s (manually starting label edit)\n"
                             % self.GetItemText(item))
            self.EditLabel(item)

    def OnSelChanged(self, event):
        self.item = event.GetItem()
        if self.item:
            sys.stdout.write("OnSelChanged: %s\n" % self.GetItemText(self.item))
            # items = self.GetSelections()
            # print(map(self.GetItemText, items))

    def OnActivate(self, event):
        """ Execute the function related to click or a Enter press on the item selected
         """
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
        list_files = []
        if self.GetItemText(item) == "Device":
            self.path = "."
            return self.path
        while parent_it != self.device:
            list_files.insert(0, self.GetItemText(parent_it))
            parent_it = self.GetItemParent(parent_it)
        list_files.insert(0, self.GetItemText(parent_it))
        for i in list_files:
            if i == "Device":
                i = "."
            self.path += i + "/"
        self.path += name
        return self.path

    def open_file(self):
        """
        Open the file given
         """
        name = self.GetItemText(self.item)
        self.get_path_item(self.item, name)
        self.frame.exec_cmd("\r\n")
        self.frame.show_cmd = False
        self.frame.exec_cmd("info = os.stat('%s')\r\n" % self.path)
        size = self.frame.exec_cmd("info[6]\r\n")
        self.frame.exec_cmd("del info\r\n")
        self.frame.exec_cmd("impossible = open('%s','r')\r\n" % self.path)
        print("SIZE", size)
        cmd = "print(impossible.read())\r\n"
        put_cmd(self.frame, cmd)
        self.frame.open_file = True
        start_time = time.time()
        end_time = 0
        while (len(self.frame.open_file_txt) - len(cmd) - 1) < int(size) and end_time < 10:
            end_time = time.time() - start_time
        print("Size_opened:", len(self.frame.open_file_txt))
        if end_time >= 10:
            self.frame.shell.AppendText("Can't Open file")
            put_cmd(self.frame, "impossible.close()\r\n")
            return
        self.frame.open_file = False
        put_cmd(self.frame, "impossible.close()\r\n")
        res = self.frame.open_file_txt[len(cmd) - 1:]
        res = res.split('\n>>> ')[0]
        res = res.replace('\r', '')
        notebookP = self.frame.notebook
        notebookP.new_page(name, self.path, res, True)
        self.frame.open_file_txt = ""
        self.frame.show_cmd = True

    def define_workspace(self):
        """
        Define the workspace treeview and call :function:fill_workspace()
         """
        dialog = wx.DirDialog(self.frame,
                              "Choose a Worspace",
                              "",
                              wx.FD_OPEN)
        dialog.CenterOnParent()
        if dialog.ShowModal() == wx.ID_OK:
            path = dialog.GetPath()
            self.fill_workspace(self.workspace, path)

    def OnClipboardMenu(self, evt):
        """
        Create an instance of the :class:ClipboardMenuDevice and display it
         """
        img = self.GetItemImage(self.item)
        if img == self.fldridx or img == self.fldropenidx:
            print("DIR")
            menu = ClipboardMenuDevice(True, self.frame, self.item)
            self.frame.PopupMenu(menu)
            menu.Destroy()
        else:
            print("File")
            menu = ClipboardMenuDevice(False, self.frame, self.item)
            self.frame.PopupMenu(menu)
            menu.Destroy()


class ClipboardMenuDevice(wx.Menu):
    """
    Create an instance of the :class:ClipboardMenuDevice and display it
     """

    def __init__(self, is_dir, frame, item):
        """Constructor method

        :param is_dir: flag is directory or file ?
        :type is_dir: bool
        :param frame: main window
        :type frame: :class:MainWindow
        :param item: item right-click pressed
        :type item: wx.TreeItemId
        """
        wx.Menu.__init__(self)
        self.is_dir_menu = is_dir
        self.frame = frame
        self.device_tree = frame.device_tree
        self.item = item
        self.__set_properties(frame)
        self.__attach_events()

    def __set_properties(self, frame):
        """
        Set attributs of the instance
         """
        if self.is_dir_menu:
            self.Append(wx.ID_NEW, "&New file")
            self.Append(wx.ID_DIRECTORY, "&New Directory")
            self.Append(wx.ID_DELETE, "&Delete")
        else:
            self.Append(wx.ID_RUN, "&Run")
            self.Append(wx.ID_OPEN, "&Open")
            self.Append(wx.ID_CLOSE, "&Close")
            self.Append(wx.ID_DELETE, "&Delete")
            self.Append(wx.ID_DEFAULT, "&Default Run")
            self.Append(wx.ID_RENAME, "&Rename")

    def __attach_events(self):
        """
        Link events related of the menu with methods
         """
        if self.is_dir_menu:
            self.Bind(wx.EVT_MENU, self.OnNewFile, id=wx.ID_NEW)
            self.Bind(wx.EVT_MENU, self.OnNewdir, id=wx.ID_DIRECTORY)
            self.Bind(wx.EVT_MENU, self.OnDelete, id=wx.ID_DELETE)
        else:

            self.Bind(wx.EVT_MENU, self.OnRun, id=wx.ID_RUN)
            self.Bind(wx.EVT_MENU, self.frame.device_tree.OnActivate,
                      id=wx.ID_OPEN)
            self.Bind(wx.EVT_MENU, self.OnDelete, id=wx.ID_DELETE)
            self.Bind(wx.EVT_MENU, self.OnDefaultRun, id=wx.ID_DEFAULT)
            self.Bind(wx.EVT_MENU, self.OnRename, id=wx.ID_RENAME)

    def OnRun(self, evt):
        """
        Execute the device item selected (file)
         """
        self.device_tree.path = ""
        self.device_tree.root_it = self.device_tree.GetRootItem()
        name = self.device_tree.GetItemText(self.item)
        self.device_tree.get_path_item(self.item, name)
        put_cmd(self.device_tree.frame, "\r\n")
        time.sleep(0.1)
        self.frame.exec_cmd("exec(open('%s').read())\r\n" %
                            self.device_tree.path)

    def OnNewdir(self, evt):
        """
        Create a new directory in the device item selected (directory)
         """
        self.device_tree.path = ""
        self.device_tree.root_it = self.device_tree.GetRootItem()
        name = self.device_tree.GetItemText(self.item)
        self.device_tree.get_path_item(self.item, name)
        ok = False
        txt = "Select the name of the new directory"
        self.frame.exec_cmd("\r\n")
        self.frame.show_cmd = False
        while not ok:
            with wx.TextEntryDialog(self.frame, txt) as dlg:
                dlg.CenterOnParent()
                result = dlg.ShowModal()
                if result == wx.ID_OK or evt is not None:
                    path = self.device_tree.path + "/" + dlg.GetValue()
                    self.frame.exec_cmd("os.mkdir('%s')\r\n" % path)
                    treeModel(self.frame)
                    ok = True
                else:
                    ok = True
        self.frame.show_cmd = True

    def OnDelete(self, evt):
        """
        Delete the device item selected
         """
        self.device_tree.path = ""
        self.device_tree.root_it = self.device_tree.GetRootItem()
        name = self.device_tree.GetItemText(self.item)
        self.device_tree.get_path_item(self.item, name)
        if self.is_dir_menu:
            self.frame.exec_cmd("\r\n\r\n")
            self.frame.exec_cmd("os.rmdir('%s')\r\n" % self.device_tree.path)
        else:
            self.frame.exec_cmd("os.remove('%s')\r\n" % self.device_tree.path)
        self.device_tree.Delete(self.item)

    def OnDefaultRun(self, evt):
        """
        Create a main.py or fill it with a python line to execute the device item selected
         """
        self.device_tree.path = ""
        self.device_tree.root_it = self.device_tree.GetRootItem()
        name = self.device_tree.GetItemText(self.item)
        self.device_tree.get_path_item(self.item, name)
        setDefaultProg(self.frame, self.device_tree.path)
        treeModel(self.frame)

    def OnNewFile(self, evt):
        """
        Execute the device item selected
         """
        self.device_tree.path = ""
        name = self.device_tree.GetItemText(self.item)
        self.device_tree.get_path_item(self.item, name)
        ok = False
        txt = "Select the name of the new file"
        self.frame.exec_cmd("\r\n")
        self.frame.show_cmd = False
        while not ok:
            with wx.TextEntryDialog(self.frame, txt) as dlg:
                dlg.CenterOnParent()
                result = dlg.ShowModal()
                if result == wx.ID_OK or evt is not None:
                    path = self.device_tree.path + "/" + dlg.GetValue()
                    self.frame.exec_cmd("myfile = open('%s', 'w')\r\n" % path)
                    self.frame.exec_cmd("myfile.close()\r\n")
                    ok = True
                    treeModel(self.frame)
                else:
                    ok = True
        self.frame.show_cmd = True

    def OnRename(self, evt):
        """
        Rename the device item selected(file and dir)
         """
        self.device_tree.path = ""
        name = self.device_tree.GetItemText(self.item)
        path_actual = self.device_tree.get_path_item(self.item, name)
        ok = False
        txt = "Rename the file"
        message = "Rename"
        self.frame.exec_cmd("\r\n")
        self.frame.show_cmd = False
        while not ok:
            with wx.TextEntryDialog(self.frame, txt, message) as dlg:
                dlg.CenterOnParent()
                result = dlg.ShowModal()
                if result == wx.ID_OK:
                    new_name = dlg.GetValue()
                    self.device_tree.SetItemText(self.item, new_name)
                    self.device_tree.path = ""
                    new_path = self.device_tree.get_path_item(self.item, new_name)
                    self.frame.exec_cmd("os.rename('%s', '%s')\r\n" % (path_actual, new_path))
                    ok = True
                    time.sleep(10)
                    treeModel(self.frame)
                else:
                    ok = True
        self.frame.show_cmd = True


def setDefaultProg(frame, filename):
    """Extension of the method OnDefaultRun

    :param frame: Main window
    :type frame: :class: MainWindow
    :param filename: path of the file to run by default
    :type filename: str
    """
    frame.exec_cmd("\r\n")
    frame.show_cmd = False
    ProgMsg = ""
    cmd = "myfile=open(\'main.py\',\'w\')\r\n"
    ProgMsg = frame.exec_cmd(cmd)
    if ProgMsg.find("Traceback") >= 0 or ProgMsg.find("... ") >= 0:
        frame.exec_cmd("\x03")
        return
    cmd = "myfile.write(\"exec(open(\'%s\').read(),globals())\")\r\n" % str(
        filename)
    ProgMsg = frame.exec_cmd(cmd)
    if ProgMsg.find("Traceback") >= 0 or ProgMsg.find("... ") >= 0:
        frame.exec_cmd("\x03")
        return
    cmd = "myfile.close()\r\n"
    ProgMsg = frame.exec_cmd(cmd)
    if ProgMsg.find("Traceback") >= 0 or ProgMsg.find("... ") >= 0:
        frame.exec_cmd("\x03")
        return
    frame.show_cmd = True


def getFileTree(frame, dir):
    """
        Get the TreeView structure (recursive way)
    """
    frame.cmd_return = ""
    frame.get_cmd = True
    frame.exec_cmd("\r\n")
    result = frame.exec_cmd("os.listdir(\'%s\')\r\n" % dir)
    if result == "err":
        return result
    filemsg = result[result.find("["):result.find("]")+1]

    ret = json.loads("{}")
    ret[dir] = []
    if filemsg == "[]":
        return ret
    filelist = []
    filemsg = filemsg.split("'")

    for i in filemsg:
        if i.find("[") >= 0 or i.find(",") >= 0 or i.find("]") >= 0:
            pass
        else:
            filelist.append(i)
    for i in filelist:
        res = frame.exec_cmd("os.stat(\'%s\')\r\n" % (dir + "/" + i))
        if res == "err":
            return res
        isdir = res.split("\n")[1]
        isdir = isdir.split(", ")
        try:
            adir = isdir[0]
            if adir.find("(") >= 0:
                adir = adir[1:]
            if adir.find(")") >= 0:
                adir = adir[:-1]
            if int(adir) == 0o040000:
                if i == "System Volume Information":
                    pass
                else:
                    ret[dir].append(getFileTree(frame, dir+"/"+i))
            else:
                ret[dir].append(i)
        except Exception as e:
            print("Error Build TreeView: ", e)
            return "err"
    return ret


def treeModel(frame):
    """
    Build the TreeView
    """
    frame.show_cmd = False
    frame.reflushTreeBool = True
    frame.cmd_return = ""
    frame.device_tree.DeleteChildren(frame.device_tree.device)
    res = json.loads("{}")
    res = getFileTree(frame, ".")

    if res == "err":
        frame.cmd_return = ""
        return
    try:
        ReflushTree(frame, frame.device_tree.device, res['.'])
    except Exception as e:
        print("Error Build TreeView", e)
    frame.cmd_return = ""
    frame.show_cmd = True


def ReflushTree(frame, device, msg):
    """Create the branches of the treeview(recursive)

    :param frame: main window
    :type frame: MainWindow
    :param device: item to add
    :type device: wx.TreeItemId 
    :param msg: back of infos of the file or directory analysed
    :type msg: str or list or dict
    """
    if msg == "err":
        return
    tree = frame.device_tree
    if type(msg) is str:  # : fichier
        child = tree.AppendItem(device, msg)
        tree.SetItemImage(child, tree.fileidx, wx.TreeItemIcon_Normal)
        tree.SetItemImage(child, tree.fileidx, wx.TreeItemIcon_Expanded)

    elif type(msg) is dict:  # : dossier
        for i in msg:
            k = eval("%s" % msg[i])
            i = i.split("/")
            child = tree.AppendItem(device, i[len(i) - 1])
            tree.SetItemImage(child, tree.fldridx, wx.TreeItemIcon_Normal)
            tree.SetItemImage(child, tree.fldropenidx, wx.TreeItemIcon_Expanded)
            ReflushTree(frame, child, k)
    elif type(msg) is list:  # :liste de fichiers
        for i in msg:
            if type(i) is str:
                ReflushTree(frame, device, i)
            elif type(i) is dict:
                ReflushTree(frame, device, i)
            else:
                pass

# TODO: move this function on Editor


def save_on_card(frame, page):
    """ Save the tab on the device connected

    :param frame: main window
    :type frame: :class:MainWindow
    :param page: tab to save
    :type page: :class:StyledEditor
    """
    # Check if save is required
    if (page.GetValue() != page.last_save):
        page.saved = False
        # Grab the content to be saved
        save_as_file_content = page.GetValue()
        frame.exec_cmd("\r\n")
        frame.show_cmd = False
        cmd = "f = os.remove('%s')\r\n" % (page.directory)
        frame.exec_cmd(cmd)
        cmd = "f = open('%s', 'wb')\r\n" % (page.directory)
        frame.exec_cmd(cmd)
        cmd = "f.write(%s)\r\n" % save_as_file_content.encode('utf8')
        frame.exec_cmd(cmd)
        cmd = "f.close()\r\n"
        frame.exec_cmd(cmd)
        page.last_save = save_as_file_content
        page.saved = True
        wx.CallAfter(frame.shell.AppendText, "Content Saved\n")
        my_speak(frame, "Content Saved")
        frame.show_cmd = True
