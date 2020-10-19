import wx

def InitF6(main_window):
    """F6 to navigate between regions
    :param main_window: see InitShorcuts->param
    :type main_window: idem
    :return: entrie(here tuple) for AcceleratorTable
    :rtype: tuple(int, int, int)
    """        
    main_window.Bind(wx.EVT_MENU, main_window.OnChangeFocus, id=wx.ID_MOVE)
    return (wx.ACCEL_NORMAL,  wx.WXK_F6, wx.ID_MOVE)

def InitCTRL_plus(main_window):
    """Ctrl + = to zoom on the editor
    :param main_window: see InitShorcuts->param
    :type main_window: idem
    :return: entrie(here tuple) for AcceleratorTable
    :rtype: tuple(int, int, int)
    """
    main_window.Bind(wx.EVT_MENU, main_window.OnZoomIn, id=wx.ID_ZOOM_IN)
    return (wx.ACCEL_CTRL,  ord('='), wx.ID_ZOOM_IN)
        
def InitCTRL_moins(main_window):
    """Ctrl + - to zoom on the editor
    :param main_window: see InitShorcuts->param
    :type main_window: idem
    :return: entrie(here tuple) for AcceleratorTable
    :rtype: tuple(int, int, int)
    """
    main_window.Bind(wx.EVT_MENU, main_window.OnZoomOut, id=wx.ID_ZOOM_OUT)
    return (wx.ACCEL_CTRL,  ord('-'), wx.ID_ZOOM_OUT)        

def InitCTRL_fin(main_window):
    """Ctrl + fin to set focus on the status
    :param main_window: see InitShorcuts->param
    :type main_window: idem
    :return: entrie(here tuple) for AcceleratorTable
    :rtype: tuple(int, int, int)
    """
    main_window.Bind(wx.EVT_MENU, main_window.OnStatus, id=wx.ID_STATIC)
    return (wx.ACCEL_CTRL,  wx.WXK_END, wx.ID_STATIC)

def InitShortcuts(main_window):
    """Initiate shortcuts of the Application with wx.Accelerator Table
    
        :param main_window: parent class to bind events)
        :Type main_window: wx.main_window
    """
    accel_tbl = wx.AcceleratorTable([InitF6(main_window),
                                    InitCTRL_plus(main_window),
                                    InitCTRL_moins(main_window),
                                    InitCTRL_fin(main_window),
                                    ])
    main_window.SetAcceleratorTable(accel_tbl)      