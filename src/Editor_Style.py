"""
Module to Customize Panels with differents themes
"""

import wx
import json
import wx.stc as stc

from constantes import stc_style, py_style


def change_theme_choice(frame, theme_name):
    """ Change the theme attribut on all panels

    :param frame: main window
    :type frame: :class: MainWindow
    :param theme_name: theme selected
    :type theme_name: str
    """

    frame.notebook.theme_choice = theme_name
    frame.shell.theme_choice = theme_name
    frame.device_tree.theme_choice = theme_name


def init_editor_style(editor):
    """Init some settings for Editor Window

    :param editor: editorWindow
    :type editor: wx.py.editwindow.EditWindow
    """

    font = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL, 0, "Arial")
    editor.SetIndentationGuides(stc.STC_IV_LOOKFORWARD)
    if editor.parent.colorized:
        editor.SetLexer(wx.stc.STC_LEX_PYTHON)
    editor.SetIndent(4)
    editor.SetTabIndents(4)
    editor.AutoCompleteDirectories()
    editor.AutoCompleteFileNames()
    editor.SetFont(font)


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
        font = wx.Font(pointSize=10,
                       family=wx.FONTFAMILY_DEFAULT,
                       style=wx.FONTSTYLE_NORMAL,
                       weight=wx.FONTWEIGHT_NORMAL,
                       underline=False,
                       faceName="Arial",
                       encoding=0)
        customize_lexer_stcstyle(editor, theme['Panels Colors'], font)
        customize_lexer_pystyle(editor, theme, font)
    except Exception as e:
        text = "Can't customize Editor\nError: %s" % e
        print(text)
        editor.frame.shell.AppendText(text)


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
        editor.StyleSetFont(i, font)
    for i in py_style:
        editor.StyleSetBackground(i, theme['Panels Colors']['Text background'])
    for i in py_style:
        editor.StyleSetForeground(i, theme['Panels Colors']['Text foreground'])
    if editor.parent.colorized:
        for f in theme['LexerStyleEditor']:
            keys.append(f)
        for i in py_style:
            editor.StyleSetForeground(i, theme['LexerStyleEditor'][keys[x]])
            x += 1


def activate_highlighted_syntax(notebook, theme_menu):
    """Enable/disable the syntax highlight

    :param notebook: Notebook panel
    :type notebook: :class: Panels.NotebookPanel
    :param theme_menu: themes menu
    :type theme_menu: :class:Tools.ThemeMenu
    """

    page = notebook.GetCurrentPage()
    if notebook.colorized:
        notebook.colorized = False
        if page:
            customize_editor(page, notebook.theme_choice)
            theme_menu.syntax_on_item.SetItemLabel("Syntax Highlight Disabled")
    else:
        notebook.colorized = True
        if page:
            customize_editor(page, notebook.theme_choice)
            theme_menu.syntax_on_item.SetItemLabel("Syntax Highlight Enabled")
