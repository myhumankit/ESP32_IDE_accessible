"""
Module to Customize Panels with differents themes
"""

import wx, random, os, json
from constantes import *

import wx.stc as stc
import wx.py as pysh
import wx.lib.agw.flatnotebook as fnb

def change_theme_choice(main_window, theme_name):
    main_window.notebook.theme_choice = theme_name
    main_window.shell.theme_choice = theme_name
    main_window.device_tree.theme_choice = theme_name

def init_editor_style(editor):
    """Init some settings for Editor Window

    :param editor: editorWindow
    :type editor: wx.py.editwindow.EditWindow
    """
    font = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, "Fira code")

    editor.SetIndentationGuides(stc.STC_IV_LOOKFORWARD)
    editor.SetEOLMode(stc.STC_EOL_CRLF)
    #editor.setDisplayLineNumbers(True)
    editor.SetLexer(wx.stc.STC_LEX_PYTHON)
    editor.SetIndent(4)
    editor.SetTabIndents(4)
    editor.AutoCompleteDirectories()
    editor.AutoCompleteFileNames()
    editor.SetFont(font)
    
    #editor.SetFontQuality(stc.STC_EFF_QUALITY_LCD_OPTIMIZED)
    #editor.SetUseAntiAliasing(True)

def customize_editor(editor, theme_choice):
    """Change theme of the Editor panel

    :param editor: EditWindow to customize
    :type editor: wx.py.editwindow.EditWindow
    :param theme: Theme to apply on the EditWindow
    :type theme: str
    """

    try:
        file = open("./customize.json")
        theme = json.load(file)
        theme = theme[theme_choice]
        file.close()
        editor.SetCaretForeground(theme['Caret']['Foreground'])
        ##print(theme[0][1])
        #default
        # editor.StyleSetSpec(stc.STC_STYLE_DEFAULT,'fore:#0000AA,back:#00000')
        # editor.StyleSetSpec(wx.stc.STC_STYLE_LINENUMBER,'fore:#FFFF00,back:#0000A')
        # editor.StyleSetSpec(wx.stc.STC_STYLE_BRACELIGHT,'fore:#FFFF00,back:#0000A')
        font = wx.Font(pointSize = 10,
                    family = wx.FONTFAMILY_DEFAULT,
                    style = wx.FONTSTYLE_NORMAL,
                    weight = wx.FONTWEIGHT_NORMAL,  
                    underline = False,
                    faceName ="Fira Code",
                    encoding = 0)
        customize_lexer_stcstyle(editor, theme['Panels Colors'], font)
        customize_lexer_pystyle(editor, theme, font)
    except Exception:
        #print("Can't customize Editor")
        return

def customize_lexer_stcstyle(editor, theme, font):
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
        editor.StyleSetBackground(i, theme['Text background'])
    for i in stc_style:
        editor.StyleSetForeground(i, theme['Text foreground'])

def customize_lexer_pystyle(editor, theme, font):
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
    keys = []

    for i in py_style:
        editor.StyleSetFont(i,font)
    for i in py_style:
        editor.StyleSetBackground(i, theme['Panels Colors']['Text background'])
    for i in py_style:
        editor.StyleSetForeground(i, theme['Panels Colors']['Text foreground'])
    for f in theme['LexerStyleEditor']:
        keys.append(f)
    for i in py_style:
        editor.StyleSetForeground(i, theme['LexerStyleEditor'][keys[x]])
        x += 1
