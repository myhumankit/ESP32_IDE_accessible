"""
    Contains functions to create all panels
"""

import wx
import Panels.Device_tree as Tree
from Panels.Notebook import NotebookPanel
from Panels.Shell import ShellPanel


def create_panels(frame):
    """Inits the differents regions(TreeView, Notebook, Shell) in the frame

    :param frame: MainWindow or window to split
    :type frame: MainWindow or other panel
    """

    style = wx.SP_3D | wx.SP_NO_XP_THEME | wx.SP_LIVE_UPDATE
    frame.splitter_v = wx.SplitterWindow(frame, style=style, name="Dimension")
    frame.splitter_h = wx.SplitterWindow(frame.splitter_v,
                                         style=style, name="DIMENSION ALL")
    frame.notebook = NotebookPanel(frame.splitter_h, frame)
    frame.device_tree = Tree.DeviceTree(frame.splitter_v, frame)
    frame.shell = ShellPanel(frame.splitter_h, frame)
    frame.splitter_v.SplitVertically(frame.device_tree, frame.splitter_h, 200)
    frame.splitter_h.SplitHorizontally(frame.notebook, frame.shell, 400)
    frame.splitter_h.SetMinimumPaneSize(20)
    frame.splitter_v.SetMinimumPaneSize(20)
    frame.statusbar = frame.CreateStatusBar(2, style=wx.STB_ELLIPSIZE_MIDDLE)
    frame.statusbar.SetBackgroundColour("Grey")
    frame.statusbar.SetStatusText("Status: Not Connected", 1)
