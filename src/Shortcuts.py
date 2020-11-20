import wx

wx.ID_VOCAL = wx.NewId()
wx.ID_EDITOR_FOCUS = wx.NewId()
wx.ID_SHELL_FOCUS = wx.NewId()
wx.ID_TREE_FOCUS = wx.NewId()


def stopvocal(frame):
    print("GROSSSSS")
    if not frame.speak_on:
        frame.speak_on = True
    else:
        frame.speak_on = False


def InitCTRL(frame):
    """F6 to navigate between regions
    :param frame: see InitShorcuts->param
    :type frame: idem
    :return: entrie(here tuple) for AcceleratorTable
    :rtype: tuple(int, int, int)
    """
    frame.Bind(wx.EVT_MENU, lambda x: stopvocal(frame), id=wx.ID_VOCAL)
    return (wx.ACCEL_CTRL,  ord('m'), wx.ID_VOCAL)


def InitF6(frame):
    """F6 to navigate between regions
    :param frame: see InitShorcuts->param
    :type frame: idem
    :return: entrie(here tuple) for AcceleratorTable
    :rtype: tuple(int, int, int)
    """
    frame.Bind(wx.EVT_MENU, frame.OnUpFocus, id=wx.ID_CONVERT)
    return (wx.ACCEL_NORMAL,  wx.WXK_F6, wx.ID_CONVERT)


def InitF9(frame):
    """F6 to navigate between regions
    :param frame: see InitShorcuts->param
    :type frame: idem
    :return: entrie(here tuple) for AcceleratorTable
    :rtype: tuple(int, int, int)
    """
    frame.Bind(wx.EVT_MENU, frame.device_tree.set_focus_tree,
               id=wx.ID_TREE_FOCUS)
    return (wx.ACCEL_NORMAL,  wx.WXK_F9, wx.ID_TREE_FOCUS)


def InitF10(frame):
    """F6 to navigate between regions
    :param frame: see InitShorcuts->param
    :type frame: idem
    :return: entrie(here tuple) for AcceleratorTable
    :rtype: tuple(int, int, int)
    """
    frame.Bind(wx.EVT_MENU, frame.set_focus_editor, id=wx.ID_EDITOR_FOCUS)
    return (wx.ACCEL_NORMAL,  wx.WXK_F10, wx.ID_EDITOR_FOCUS)


def InitF11(frame):
    """F6 to navigate between regions
    :param frame: see InitShorcuts->param
    :type frame: idem
    :return: entrie(here tuple) for AcceleratorTable
    :rtype: tuple(int, int, int)
    """
    frame.Bind(wx.EVT_MENU, frame.shell.set_focus_shell, id=wx.ID_SHELL_FOCUS)
    return (wx.ACCEL_NORMAL,  wx.WXK_F11, wx.ID_SHELL_FOCUS)


def InitMajF6(frame):
    """F6 to navigate between regions (previous)
    :param frame: see InitShorcuts->param
    :type frame: idem
    :return: entrie(here tuple) for AcceleratorTable
    :rtype: tuple(int, int, int)
    """
    frame.Bind(wx.EVT_MENU, frame.OnDownFocus, id=wx.ID_MOVE_FRAME)
    return (wx.ACCEL_SHIFT,  wx.WXK_F6, wx.ID_MOVE_FRAME)


def InitMajF10(frame):
    """Simulate a right click
    :param frame: see InitShorcuts->param
    :type frame: idem
    :return: entrie(here tuple) for AcceleratorTable
    :rtype: tuple(int, int, int)
    """
    frame.Bind(wx.EVT_MENU, frame.right_click_shortcut, id=wx.ID_JUSTIFY_RIGHT)
    return (wx.ACCEL_SHIFT,  wx.WXK_F10, wx.ID_JUSTIFY_RIGHT)


def InitCTRL_plus(frame):
    """Ctrl + = to zoom on the editor
    :param frame: see InitShorcuts->param
    :type frame: idem
    :return: entrie(here tuple) for AcceleratorTable
    :rtype: tuple(int, int, int)
    """
    frame.Bind(wx.EVT_MENU, frame.OnZoomIn, id=wx.ID_ZOOM_IN)
    return (wx.ACCEL_CTRL,  ord('='), wx.ID_ZOOM_IN)


def InitCTRL_moins(frame):
    """Ctrl + - to zoom on the editor
    :param frame: see InitShorcuts->param
    :type frame: idem
    :return: entrie(here tuple) for AcceleratorTable
    :rtype: tuple(int, int, int)
    """
    frame.Bind(wx.EVT_MENU, frame.OnZoomOut, id=wx.ID_ZOOM_OUT)
    return (wx.ACCEL_CTRL,  ord('-'), wx.ID_ZOOM_OUT)


def InitCTRL_fin(frame):
    """Ctrl + fin to set focus on the status
    :param frame: see InitShorcuts->param
    :type frame: idem
    :return: entrie(here tuple) for AcceleratorTable
    :rtype: tuple(int, int, int)
    """
    frame.Bind(wx.EVT_MENU, frame.OnStatus, id=wx.ID_STATIC)
    return (wx.ACCEL_CTRL,  wx.WXK_END, wx.ID_STATIC)


def InitShortcuts(frame):
    """Initiate shortcuts of the Application with wx.Accelerator Table

        :param frame: parent class to bind events)
        :Type frame: wx.frame
    """
    accel_tbl = wx.AcceleratorTable([InitF6(frame),
                                    InitF9(frame),
                                    InitF10(frame),
                                    InitF11(frame),
                                    InitCTRL(frame),
                                    InitCTRL_plus(frame),
                                    InitCTRL_moins(frame),
                                    InitCTRL_fin(frame),
                                    InitMajF6(frame),
                                    InitMajF10(frame)
                                    ])
    frame.SetAcceleratorTable(accel_tbl)
