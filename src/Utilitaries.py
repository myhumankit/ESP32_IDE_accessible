import wx

def load_img(path):
    return wx.Image(path,wx.BITMAP_TYPE_ANY).ConvertToBitmap()