"""Module which contains functions to find and replace
"""


def find_next(editor, evt):
    """
    Useful function to find the next occurence of a word on the EditWindow panel

    :param editor: EditWindow to apply the function
    :type editor: wx.py.editwindow.EditWindow
    :param evt: Evt which contains the string to find
    :type evt: wx.Event
    :return: True if the string is found, False if not
    :rtype: Boolean
    """

    findTxt = evt.GetFindString()
    editor.pos = editor.txt.find(findTxt, editor.pos)
    if editor.pos == -1:
        editor.pos = 0
        editor.ClearSelections()
        return False
    editor.size = len(findTxt)
    editor.SetSelection(editor.pos, editor.pos+editor.size)
    editor.pos += editor.size
    return True


def replace(editor, evt):
    """
    Useful function to replace a the selected text by an other word
    on the EditWindow panel

    :param editor: EditWindow to apply the function
    :type editor: wx.py.editwindow.EditWindow
    :param evt: Evt which contains the string to replace
    :type evt: wx.Event
    :return: True if something is replaced, False if not
    :rtype: Boolean
    """

    if editor.GetSelectedText() == "":
        return False
    replaceTxt = evt.GetReplaceString()
    editor.size = len(replaceTxt)
    start = editor.GetSelectionStart()
    end = editor.GetSelectionEnd()
    editor.Replace(start, end, replaceTxt)
    editor.txt = editor.GetValue()
    return True
