def move_key_left(shell):
    cursor = shell.GetInsertionPoint()
    shell.SetInsertionPoint(cursor - 1)


def move_key_right(shell):
    cursor = shell.GetInsertionPoint()
    shell.SetInsertionPoint(cursor + 1)


def cursor_at_end(shell, text):
    cursor = shell.GetInsertionPoint()
    maxi = len(text)
    return cursor == maxi


def remove_char(shell, frame):
    cursor = shell.GetInsertionPoint()
    shell.Remove(cursor - 1, cursor)
