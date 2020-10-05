"""
Module which contains the DeviceTree class
which is builded in according with the contain of the card
"""

#!/usr/bin/env python

#!!!IN DEVELOPMENT with so much errors

import glob

from Packages import string, wx, os, sys, time
from Constantes import *

class DeviceTree(wx.TreeCtrl):
    def __init__(self, parent, frame, paths, name):
        tID = wx.NewId()
        # Use the WANTS_CHARS style so the panel doesn't eat the Return key.
        wx.TreeCtrl.__init__(self, parent)
        self.frame = frame
        path = os.getcwd()
        paths = paths
        #paths = glob.glob(path + "/*")
        #paths = os.listdir(os.getcwd())
        print("WARNINGG")
        print(paths)
        isz = (16,16)
        self.il = wx.ImageList(isz[0], isz[1])
        self.fldridx     = self.il.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER,      wx.ART_OTHER, isz))
        self.fldropenidx = self.il.Add(wx.ArtProvider.GetBitmap(wx.ART_FOLDER_OPEN, wx.ART_OTHER, isz))
        self.fileidx     = self.il.Add(wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, isz))
        self.smileidx    = self.il.Add(wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, isz))
        self.font = wx.Font(pointSize = 10, family = wx.FONTFAMILY_SWISS, style = wx.FONTSTYLE_SLANT, weight = wx.FONTWEIGHT_NORMAL,  
                      underline = False, faceName ="", encoding = 0)
        self.theme = frame.MyNotebook.theme
        self.root = self.AddRoot(name)

        self.SetImageList(self.il)
        self.SetItemData(self.root, None)
        self.SetItemImage(self.root, self.fldridx, wx.TreeItemIcon_Normal)
        self.SetItemImage(self.root, self.fldropenidx, wx.TreeItemIcon_Expanded)
        self.recurse_listdir(paths, self.root)
        self.Custom_Tree_Ctrl(themes[self.theme])
        self.__attach_events()

    def recurse_listdir(self, paths, root):
        for item in paths:
            if os.path.isdir(item):
                child = self.AppendItem(root, os.path.basename(item))
                new_paths = glob.glob(item + "/*")
                self.SetItemImage(child, self.fldridx, wx.TreeItemIcon_Normal)
                self.SetItemImage(child, self.fldropenidx, wx.TreeItemIcon_Expanded)
                self.recurse_listdir(new_paths, child)
            else:
                child = self.AppendItem(root, os.path.basename(item))
                self.SetItemImage(child, self.fldridx, wx.TreeItemIcon_Normal)
                self.SetItemImage(child, self.fldropenidx, wx.TreeItemIcon_Expanded)

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
            sys.stdout.write("OnActivate: %s\n" % self.GetItemText(self.item))