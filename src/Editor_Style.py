import wx
import random
import wx.stc as stc
import os
import wx.py as pysh
import wx.lib.agw.flatnotebook as fnb

#TODO: continue les themes

stc_style = [stc.STC_STYLE_BRACEBAD,
             stc.STC_STYLE_BRACELIGHT,
             stc.STC_STYLE_CALLTIP,
             stc.STC_STYLE_CONTROLCHAR,
             stc.STC_STYLE_DEFAULT,
             stc.STC_STYLE_FOLDDISPLAYTEXT,
             stc.STC_STYLE_INDENTGUIDE,
             stc.STC_STYLE_LASTPREDEFINED,
             stc.STC_STYLE_MAX
             ]

def Init_Editor_base(editor):
    """Init settings for Editor

    :param editor: editorWindow
    :type editor: [type]
    """
    editor.SetIndentationGuides(stc.STC_IV_LOOKFORWARD)
    editor.SetEOLMode(stc.STC_EOL_CRLF)
    editor.setDisplayLineNumbers(True)
    editor.SetLexer(wx.stc.STC_LEX_PYTHON)
    editor.SetFontQuality(stc.STC_EFF_QUALITY_LCD_OPTIMIZED)
    editor.SetUseAntiAliasing(True)

def Custom_Tree_Ctrl(tree, theme):
    tree.StyleSetBackground(wx.DIRCTRL_DEFAULT_STYLE, 'Black')
    
def Custom_Notebook(notebook, theme):
    notebook.SetBackgroundColour('Black')

#checker des styles 
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