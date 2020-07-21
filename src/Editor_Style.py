import wx
import random
import wx.stc as stc
import os
import wx.py as pysh
import wx.lib.agw.flatnotebook as fnb

#TODO: continue les themes
#themes = [th_1, th_2, th_3, th_4, th_5]
#th = [default]
#th_1


#self.StyleSetSpec(wx.stc.STC_P_COMMENTLINE,"fore:#007F00")
#self.StyleSetSpec(stc.STC_STYLE_LINENUMBER, "fore:#ff007f, size:100")
#self.StyleSetBackground(wx.stc.STC_STYLE_DEFAULT, "Grey")

def Init_Editor_base(editor):
    """Init settings for Editor

    :param editor: editorWindow
    :type editor: [type]
    """    
    editor.setDisplayLineNumbers(True)
    editor.SetLexer(wx.stc.STC_LEX_PYTHON)
    editor.SetFontQuality(stc.STC_EFF_QUALITY_LCD_OPTIMIZED)
    editor.SetUseAntiAliasing(True)


#checker des styles 
def Change_lexer_style(editor):
    """Chnage theme of the editor

    :param editor: editwindow
    :type editor: [type]
    """    
    editor.StyleSetBold(wx.stc.STC_STYLE_DEFAULT, True)
    #editor.StyleSetForeground(wx.stc.STC_STYLE_DEFAULT,wx.Colour(0, 0, 0))
    editor.StyleSetForeground(wx.stc.STC_P_DEFNAME, wx.Colour(51, 51, 255))
    editor.StyleSetForeground(wx.stc.STC_P_STRING, wx.Colour(51, 51, 255))
    editor.StyleSetForeground(wx.stc.STC_P_CHARACTER, wx.Colour(51, 51, 255))
    editor.StyleSetForeground(wx.stc.STC_P_CLASSNAME, wx.Colour(51, 51, 255))
    editor.StyleSetForeground(wx.stc.STC_P_COMMENTBLOCK, wx.Colour(51, 51, 255))
    editor.StyleSetForeground(wx.stc.STC_P_COMMENTLINE, wx.Colour(51, 51, 255))
    editor.StyleSetForeground(wx.stc.STC_P_DECORATOR, wx.Colour(51, 51, 255))
    editor.StyleSetForeground(wx.stc.STC_P_IDENTIFIER, wx.Colour(51, 51, 255))
    editor.StyleSetForeground(wx.stc.STC_P_NUMBER, wx.Colour(51, 51, 255))
    editor.StyleSetForeground(wx.stc.STC_P_WORD, wx.Colour(51, 51, 255))
    
    #editor.StyleSetForeground(wx.stc.STC_STYLE_LINENUMBER,wx.Colour(0, 230, 250))