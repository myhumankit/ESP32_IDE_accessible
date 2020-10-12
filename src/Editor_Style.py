"""
Module to Customize Panels with differents themes
"""

from Packages import wx, random, os
from Constantes import *

import wx.stc as stc
import wx.py as pysh
import wx.lib.agw.flatnotebook as fnb

#TODO: finir les thèmes

def Init_Editor_base(editor):
    """Init some settings for Editor Window

    :param editor: editorWindow
    :type editor: wx.py.editwindow.EditWindow
    """
    editor.SetIndentationGuides(stc.STC_IV_LOOKFORWARD)
    editor.SetEOLMode(stc.STC_EOL_CRLF)
    editor.setDisplayLineNumbers(True)
    editor.SetLexer(wx.stc.STC_LEX_PYTHON)
    editor.SetIndent(4)
    editor.SetTabIndents(4)
    editor.AutoCompleteDirectories()
    editor.AutoCompleteFileNames()
    #editor.SetFontQuality(stc.STC_EFF_QUALITY_LCD_OPTIMIZED)
    #editor.SetUseAntiAliasing(True)

def Change_Theme(editor, theme):
    """Change theme of the window

    :param editor: EditWindow to customize
    :type editor: wx.py.editwindow.EditWindow
    :param theme: Theme to apply on the EditWindow
    :type theme: list
    """
    editor.SetCaretForeground(theme[1][1])
    #default
    # editor.StyleSetSpec(stc.STC_STYLE_DEFAULT,'fore:#0000AA,back:#00000')
    # editor.StyleSetSpec(wx.stc.STC_STYLE_LINENUMBER,'fore:#FFFF00,back:#0000A')
    # editor.StyleSetSpec(wx.stc.STC_STYLE_BRACELIGHT,'fore:#FFFF00,back:#0000A')
    font = wx.Font(pointSize = 10,
                family = wx.FONTFAMILY_SWISS,
                style = wx.FONTSTYLE_SLANT,
                weight = wx.FONTWEIGHT_NORMAL,  
                underline = False,
                faceName ="Fira Code",
                encoding = 0)
    change_lexer_stcstyle(editor, theme, font)
    change_lexer_pystyle(editor, theme, font)

def change_lexer_stcstyle(editor, theme, font):
    """Change lexer words stc style by applying 
    the theme and the font gived in parameters

    :param editor: EditWindow to apply the style
    :type editor: wx.py.editwindow.EditWindow
    :param theme: Theme to apply on the EditWindow lexer
    :type theme: list
    :param font: font to apply on lexer
    :type font: wx.Font
    """
    for i in stc_style:
        editor.StyleSetFont(i, font)
    for i in stc_style:
        editor.StyleSetBackground(i, theme[1][0])
    for i in stc_style:
        editor.StyleSetForeground(i, theme[1][1])

    #Lexer style

def change_lexer_pystyle(editor, theme, font):
    """Change lexer python words by applying 
    the theme and the font gived in parameters

    :param editor: EditWindow to apply the style
    :type editor: wx.py.editwindow.EditWindow
    :param theme: Theme to apply on the EditWindow python lexer
    :type theme: list
    :param font: font to apply on lexer
    :type font: wx.Font
    """
    x = 0
    for i in py_style:
        editor.StyleSetFont(i,font)
    for i in py_style:
        editor.StyleSetBackground(i, theme[1][0])
    for i in py_style:
        editor.StyleSetForeground(i, theme[0][x])
        x += 1
        