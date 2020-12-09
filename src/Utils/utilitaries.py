"""
    Useful functions
"""

import wx
import os


def load_img(path):
    """Convert a picture to display it

    :param path: path of the picture
    :type path: str
    :return: Bitmap image
    :rtype: wx.Bitmap
    """
    return wx.Image(path, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
