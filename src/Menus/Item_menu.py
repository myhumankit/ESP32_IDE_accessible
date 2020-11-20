import wx
import json


def create_Menu_item(parentMenu, id_id, text, submenu, theme_name):

    item = wx.MenuItem(id=id_id, text=text, helpString=text, subMenu=submenu)
    wx.Menu
    try:
        file = open("./customize.json")
        theme = json.load(file)
        file.close()
        theme = theme[theme_name]
        return item
    except Exception as e:
        print(e)
        # print("Can't customize ItemMenu")
        return item
