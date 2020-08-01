#!/usr/bin/env python2.6
# encoding: ISO-8859-1
"""
Basic Splitter Panel Skeleton.py
"""

import sys
import os
import time
import wx


def timenow():
    return time.time()

########################################################################

class VSplitterPanel(wx.Panel):
    """ Constructs a Vertical splitter window with left and right panels"""
    #----------------------------------------------------------------------
    def __init__(self, parent, color):
        """Constructor"""
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(color)
        #splitter = wx.SplitterWindow(self, style = wx.SP_3D| wx.SP_LIVE_UPDATE)
        leftPanel = wx.Panel()
        #rightPanel = wx.Panel(splitter)
        leftPanel.SetBackgroundColour('SEA GREEN')
        #rightPanel.SetBackgroundColour('STEEL BLUE')

        #splitter.SplitVertically(leftPanel, rightPanel) 
        PanelSizer=wx.BoxSizer(wx.VERTICAL)
        PanelSizer.Add(leftPanel, 1, wx.EXPAND | wx.ALL)
        self.SetSizer(PanelSizer)
########################################################################

class HSplitterPanel(wx.Panel):
    """ Constructs a Horizontal splitter window with top and bottom panels"""
    #----------------------------------------------------------------------
    def __init__(self, parent, color):
        """Constructor"""
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(color)
        splitter = wx.SplitterWindow(self, style = wx.SP_3D| wx.SP_LIVE_UPDATE)
        TopPanel = wx.Panel(splitter)
        BottomPanel = wx.Panel(splitter)
        TopPanel.SetBackgroundColour('YELLOW GREEN')
        BottomPanel.SetBackgroundColour('SLATE BLUE')


        splitter.SplitHorizontally(TopPanel, BottomPanel) 
        PanelSizer=wx.BoxSizer(wx.VERTICAL)
        PanelSizer.Add(splitter, 1, wx.EXPAND | wx.ALL)
        self.SetSizer(PanelSizer)
########################################################################

class MainFrame(wx.Frame):
    """Constructor"""
    #----------------------------------------------------------------------
    def __init__(self, parent, id):
        wx.Frame.__init__(self, None, title="Basic Splitter Panel Skeleton",size=(800,600))
        t0=timenow()
        self.sb=self.CreateStatusBar()
        ################################################################
        # Define mainsplitter as child of Frame and add H and VSplitterPanel as children
        mainsplitter = wx.SplitterWindow(self, style = wx.SP_3D| wx.SP_LIVE_UPDATE)
        splitterpanel1 = HSplitterPanel(mainsplitter,'LIGHT BLUE')
        splitterpanel2 = VSplitterPanel(mainsplitter,'LIGHT BLUE') 
        mainsplitter.SplitVertically(splitterpanel2, splitterpanel1)
        MainSizer = wx.BoxSizer(wx.VERTICAL)
        MainSizer.Add(mainsplitter, 1, wx.EXPAND | wx.ALL)
        self.SetSizer(MainSizer)
        #################################################################
        self.sb.SetStatusText('Initialized in  %6.4f secs'%(timenow()-t0))
        self.Refresh()
        self.Show()

#---------------------------------------------------------------------- 


if __name__ == '__main__':
    app = wx.App()
    MainFrame(None, -1)
    app.MainLoop()
