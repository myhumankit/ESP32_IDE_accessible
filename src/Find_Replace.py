import wx

def find_next(editor, evt):
    findTxt = evt.GetFindString()
    editor.pos = editor.txt.find(findTxt, editor.pos)
    if editor.pos == -1:
        print("String not found")
        editor.pos = 0
        editor.ClearSelections()
        return False
    editor.size = len(findTxt)
    editor.SetSelection(editor.pos, editor.pos+editor.size)
    editor.pos += editor.size
    return True

def replace(editor, evt):
    if editor.GetSelectedText() == "":
        return
    replaceTxt = evt.GetReplaceString()
    editor.size = len(replaceTxt)
    start = editor.GetSelectionStart()
    end = editor.GetSelectionEnd()
    editor.Replace(start, end, replaceTxt)
    editor.txt = editor.GetValue()