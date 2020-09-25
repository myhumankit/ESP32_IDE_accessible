from Packages import wx, random, os
from Constantes import *

import wx.stc as stc
import wx.py as pysh
import wx.lib.agw.flatnotebook as fnb

#TODO: continue les themes

def Init_Editor_base(editor):
    """Init settings for Editor

    :param editor: editorWindow
    :type editor: [type]
    """
    editor.SetIndentationGuides(stc.STC_IV_LOOKFORWARD)
    editor.SetEOLMode(stc.STC_EOL_CRLF)
    editor.setDisplayLineNumbers(True)
    editor.SetLexer(wx.stc.STC_LEX_PYTHON)
    #editor.SetFontQuality(stc.STC_EFF_QUALITY_LCD_OPTIMIZED)
    #editor.SetUseAntiAliasing(True)


def Change_Theme(editor, theme, py_style):
    """Chnage theme of the window

    :param editor: editwindow
    :type editor: [type]
    """
    editor.SetCaretForeground(theme[1][1])
    #default
    # editor.StyleSetSpec(stc.STC_STYLE_DEFAULT,'fore:#0000AA,back:#00000')
    # editor.StyleSetSpec(wx.stc.STC_STYLE_LINENUMBER,'fore:#FFFF00,back:#0000A')
    # editor.StyleSetSpec(wx.stc.STC_STYLE_BRACELIGHT,'fore:#FFFF00,back:#0000A')
    font = wx.Font(pointSize = 10,
                family = wx.FONTFAMILY_SWISS,
                style = wx.FONTSTYLE_SLANT,
                weight = wx.FONTWEIGHT_BOLD,  
                underline = False,
                faceName ="",
                encoding = 0)
    for i in stc_style:
        editor.StyleSetFont(i, font)
    for i in stc_style:
        editor.StyleSetBackground(i, theme[1][0])
    for i in stc_style:
        editor.StyleSetForeground(i, theme[1][1])
    #Lexer style
    x = 0
    for i in py_style:
        editor.StyleSetFont(i,font)
    for i in py_style:
        editor.StyleSetBackground(i, theme[1][0])
    for i in py_style:
        editor.StyleSetForeground(i, theme[0][x])
        print(editor.StyleGetForeground(i))
        x += 1