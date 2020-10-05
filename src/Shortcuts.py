import wx

def InitF6(frame):
    """F6 to navigate between regions
    :param frame: see InitShorcuts->param
    :type frame: idem
    :return: entrie(here tuple) for AcceleratorTable
    :rtype: tuple(int, int, int)
    """        
    frame.Bind(wx.EVT_MENU, frame.OnChangeFocus, id=wx.ID_MOVE)
    return (wx.ACCEL_NORMAL,  wx.WXK_F6, wx.ID_MOVE)

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
        :Type frame: wx.Frame
    """
    accel_tbl = wx.AcceleratorTable([InitF6(frame),
                                    InitCTRL_plus(frame),
                                    InitCTRL_moins(frame),
                                    InitCTRL_fin(frame),
                                    ])
    frame.SetAcceleratorTable(accel_tbl)      