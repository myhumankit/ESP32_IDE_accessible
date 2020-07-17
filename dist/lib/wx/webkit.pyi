# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# This file is generated by wxPython's PI generator.  Do not edit by hand.
#
# The *.pyi files are used by PyCharm and other development tools to provide
# more information, such as PEP 484 type hints, than it is able to glean from
# introspection of extension types and methods.  They are not intended to be
# imported, executed or used for any other purpose other than providing info
# to the tools. If you don't use use a tool that makes use of .pyi files then
# you can safely ignore this file.
#
# See: https://www.python.org/dev/peps/pep-0484/
#      https://www.jetbrains.com/help/pycharm/2016.1/type-hinting-in-pycharm.html
#
# Copyright: (c) 2020 by Total Control Software
# License:   wxWindows License
#---------------------------------------------------------------------------


"""
The :ref:`wx.webkit.wxWebKitCtrl` and related classes are provided mainly for
backwards compatibility only. New code would be more future-proof by using the
``wx.html2`` module.  The classes in this module are light wrappers around
the OSX WebKit control and is not implemented on any other platform.
"""
#-- begin-_webkit --#

import wx
#-- end-_webkit --#
#-- begin-webkit --#
WEBKIT_STATE_START = 0
WEBKIT_STATE_NEGOTIATING = 0
WEBKIT_STATE_REDIRECTING = 0
WEBKIT_STATE_TRANSFERRING = 0
WEBKIT_STATE_STOP = 0
WEBKIT_STATE_FAILED = 0
WEBKIT_NAV_LINK_CLICKED = 0
WEBKIT_NAV_BACK_NEXT = 0
WEBKIT_NAV_FORM_SUBMITTED = 0
WEBKIT_NAV_RELOAD = 0
WEBKIT_NAV_FORM_RESUBMITTED = 0
WEBKIT_NAV_OTHER = 0
wxEVT_WEBKIT_STATE_CHANGED = 0
wxEVT_WEBKIT_BEFORE_LOAD = 0
wxEVT_WEBKIT_NEW_WINDOW = 0
WebKitCtrlNameStr = ""

class WebKitCtrl(wx.Control):
    """
    WebKitCtrl()
    WebKitCtrl(parent, winid=wx.ID_ANY, strURL="", pos=wx.DefaultPosition, size=wx.DefaultSize, style=0, validator=wx.DefaultValidator, name=WebKitCtrlNameStr)
    
    This control is a native wrapper around the Safari web browsing
    engine.
    """

    def __init__(self, *args, **kw):
        """
        WebKitCtrl()
        WebKitCtrl(parent, winid=wx.ID_ANY, strURL="", pos=wx.DefaultPosition, size=wx.DefaultSize, style=0, validator=wx.DefaultValidator, name=WebKitCtrlNameStr)
        
        This control is a native wrapper around the Safari web browsing
        engine.
        """

    def Create(self, parent, winid=wx.ID_ANY, strURL="", pos=wx.DefaultPosition, size=wx.DefaultSize, style=0, validator=wx.DefaultValidator, name=WebKitCtrlNameStr):
        """
        Create(parent, winid=wx.ID_ANY, strURL="", pos=wx.DefaultPosition, size=wx.DefaultSize, style=0, validator=wx.DefaultValidator, name=WebKitCtrlNameStr) -> bool
        """

    def LoadURL(self, url):
        """
        LoadURL(url)
        """

    def CanGoBack(self):
        """
        CanGoBack() -> bool
        """

    def CanGoForward(self):
        """
        CanGoForward() -> bool
        """

    def GoBack(self):
        """
        GoBack() -> bool
        """

    def GoForward(self):
        """
        GoForward() -> bool
        """

    def Reload(self):
        """
        Reload()
        """

    def Stop(self):
        """
        Stop()
        """

    def CanGetPageSource(self):
        """
        CanGetPageSource() -> bool
        """

    def GetPageSource(self):
        """
        GetPageSource() -> String
        """

    def SetPageSource(self, source, baseUrl=wx.EmptyString):
        """
        SetPageSource(source, baseUrl=wx.EmptyString)
        """

    def GetPageURL(self):
        """
        GetPageURL() -> String
        """

    def SetPageTitle(self, title):
        """
        SetPageTitle(title)
        """

    def GetPageTitle(self):
        """
        GetPageTitle() -> String
        """

    def SetTitle(self, title):
        """
        SetTitle(title)
        """

    def GetTitle(self):
        """
        GetTitle() -> String
        """

    def GetSelection(self):
        """
        GetSelection() -> String
        """

    def CanIncreaseTextSize(self):
        """
        CanIncreaseTextSize() -> bool
        """

    def IncreaseTextSize(self):
        """
        IncreaseTextSize()
        """

    def CanDecreaseTextSize(self):
        """
        CanDecreaseTextSize() -> bool
        """

    def DecreaseTextSize(self):
        """
        DecreaseTextSize()
        """

    def Print(self, showPrompt=False):
        """
        Print(showPrompt=False)
        """

    def MakeEditable(self, enable=True):
        """
        MakeEditable(enable=True)
        """

    def IsEditable(self):
        """
        IsEditable() -> bool
        """

    def RunScript(self, javascript):
        """
        RunScript(javascript) -> String
        """

    def SetScrollPos(self, pos):
        """
        SetScrollPos(pos)
        """

    def GetScrollPos(self):
        """
        GetScrollPos() -> int
        """

    @staticmethod
    def GetClassDefaultAttributes(variant=wx.WINDOW_VARIANT_NORMAL):
        """
        GetClassDefaultAttributes(variant=wx.WINDOW_VARIANT_NORMAL) -> wx.VisualAttributes
        """
    PageSource = property(None, None)
    PageTitle = property(None, None)
    PageURL = property(None, None)
    ScrollPos = property(None, None)
    Selection = property(None, None)
    Title = property(None, None)
# end of class WebKitCtrl


class WebKitBeforeLoadEvent(wx.CommandEvent):
    """
    WebKitBeforeLoadEvent(win=0)
    """

    def __init__(self, win=0):
        """
        WebKitBeforeLoadEvent(win=0)
        """

    def IsCancelled(self):
        """
        IsCancelled() -> bool
        """

    def Cancel(self, cancel=True):
        """
        Cancel(cancel=True)
        """

    def GetURL(self):
        """
        GetURL() -> String
        """

    def SetURL(self, url):
        """
        SetURL(url)
        """

    def SetNavigationType(self, navType):
        """
        SetNavigationType(navType)
        """

    def GetNavigationType(self):
        """
        GetNavigationType() -> int
        """
    NavigationType = property(None, None)
    URL = property(None, None)
# end of class WebKitBeforeLoadEvent


class WebKitStateChangedEvent(wx.CommandEvent):
    """
    WebKitStateChangedEvent(win=0)
    """

    def __init__(self, win=0):
        """
        WebKitStateChangedEvent(win=0)
        """

    def GetState(self):
        """
        GetState() -> int
        """

    def SetState(self, state):
        """
        SetState(state)
        """

    def GetURL(self):
        """
        GetURL() -> String
        """

    def SetURL(self, url):
        """
        SetURL(url)
        """
    State = property(None, None)
    URL = property(None, None)
# end of class WebKitStateChangedEvent


class WebKitNewWindowEvent(wx.CommandEvent):
    """
    WebKitNewWindowEvent(win=0)
    """

    def __init__(self, win=0):
        """
        WebKitNewWindowEvent(win=0)
        """

    def GetURL(self):
        """
        GetURL() -> String
        """

    def SetURL(self, url):
        """
        SetURL(url)
        """

    def GetTargetName(self):
        """
        GetTargetName() -> String
        """

    def SetTargetName(self, name):
        """
        SetTargetName(name)
        """
    TargetName = property(None, None)
    URL = property(None, None)
# end of class WebKitNewWindowEvent

USE_WEBKIT = 0

EVT_WEBKIT_BEFORE_LOAD = wx.PyEventBinder( wxEVT_WEBKIT_BEFORE_LOAD, 1 )
EVT_WEBKIT_STATE_CHANGED = wx.PyEventBinder( wxEVT_WEBKIT_STATE_CHANGED, 1 )
EVT_WEBKIT_NEW_WINDOW = wx.PyEventBinder( wxEVT_WEBKIT_NEW_WINDOW, 1 )
#-- end-webkit --#
