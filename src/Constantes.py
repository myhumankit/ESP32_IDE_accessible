"""Constantes Module to stock main constants"""
from packages import os, wx

import wx.stc as stc

rootDirectoryPath  =os.path.expanduser("~")
rootDirectoryPath  =rootDirectoryPath.replace("\\","/")
currentTempPath="%s/AppData/Local/uPyCraft/temp/"%rootDirectoryPath

SERIALRX = wx.NewEventType() #:create a serial data received event
EVT_SERIALRX = wx.PyEventBinder(SERIALRX, 0) #:bind to serial data receive events

wx.ID_RUN = wx.NewId()
wx.ID_RENAME = wx.NewId()
wx.ID_DIRECTORY = wx.NewId()
wx.ID_SHORTCUT = wx.NewId()
wx.ID_CONNECT = wx.NewId() #: New id to Connect the card
wx.ID_REFLUSH_DIR = wx.NewId() #: New id to Connect the card
wx.ID_EXAMPLES = wx.NewId() #: New id to Connect the card
wx.ID_SYNTAX_CHECK = wx.NewId()
wx.ID_DOWNLOAD_RUN = wx.NewId()
wx.ID_SETTINGS = wx.NewId()
wx.ID_SERIAL = wx.NewId()
wx.ID_BOARD = wx.NewId()
wx.ID_DOWNLOAD = wx.NewId()
wx.ID_DOWNLOAD_RUN = wx.NewId()
wx.ID_BURN_FIRMWARE = wx.NewId()
wx.ID_INIT = wx.NewId()
wx.ID_ESP32_CHOICE = wx.NewId()
wx.ID_PYBOARD_CHOICE = wx.NewId()
wx.ID_DARK_THEME = wx.NewId()
wx.ID_LIGHT_THEME = wx.NewId()
wx.ID_ASTRO_THEME = wx.NewId()
wx.ID_MOVE = wx.NewId()
ID_CLEAR = wx.NewId()
ID_SAVEAS = wx.NewId()
ID_SETTINGS = wx.NewId()
ID_TERM = wx.NewId()
ID_EXIT = wx.NewId()
ID_RTS = wx.NewId()
ID_DTR = wx.NewId()

SERIALRX = wx.NewEventType()
# bind to serial data receive events
EVT_SERIALRX = wx.PyEventBinder(SERIALRX, 0)

NEWLINE_CR = 0
NEWLINE_LF = 1
NEWLINE_CRLF = 2


#black #FFFF00 
#orange #FF9933
#white #FFFFFF
#violet #ea2cd8
#vert #07cc1e
#jaune #f0f20f
#bleu foncé #434885

th_dark = [
        '#f0f20f', #:strings editor 0 
        '#07cc1e', #:class editor 1
        '#ea2cd8', #:word editor 2
        '#00ffdf', #:character editor 3
        '#07cc1e', #:def editor 4
        '#ea2cd8', #:decorator editor 5
        '#FFFFFF', #:default editor 6
        '#FFFFFF', #:identifier editor 7
        '#FF9933', #:Number editor 8
        '#ea2cd8', #:Operator editor 9
        wx.YELLOW, #:str EOL editor 11
        '#f0f20f', #:triple editor 10
        '#f0f20f', #:triple double editor 12
        '#ea2cd8', #:word 2 13
        '#434885', #:CommentLine 14
        '#f0f20f', #:Comment block + strings 15
        ]

frame_dark = ["Black", #:Background
           "White", #:font linenumber
           "Grey", #:Background for Tree Ctrl
           "grey" ,#:Back Tab Area
           "grey",#:DCPaint
           "black", #:DcPaint
           "white", #:Active tab text
           "black", #:Non active tab text
           ]

th_light = [
        '#44ea1e', #strings editor 0 
        '#d08c25', #class editor 1
        '#db62f2', #word editor 2
        '#131313', #character editor 3
        '#1626ff', #def editor 4
        '#1626ff', #decorator editor 5
        '#131313', #default editor 6
        '#131313', #identifier editor 7
        '#d08c25', #Number editor 8
        '#131313', #Operator editor 9
        '#44ea1e', #str EOL editor 11
        '#44ea1e', #triple editor 10
        '#44ea1e', #triple double editor 12
        '#db62f2', #word 2 13
        '#9798a3', #CommentLine 14
        '#44ea1e', #Comment block + strings 15
]
frame_light = ["White" , "Black"]

#: Themes lists with sub_themes[lexer, frames]
# themes = [[th_dark, frame_dark],
#           [th_light, frame_light],]
 
#: List about lexer styles
py_style = [
            wx.stc.STC_P_STRING,
            wx.stc.STC_P_CLASSNAME,
            wx.stc.STC_P_WORD,
            wx.stc.STC_P_CHARACTER,
            wx.stc.STC_P_DEFNAME,
            wx.stc.STC_P_DECORATOR,
            wx.stc.STC_P_DEFAULT,
            wx.stc.STC_P_IDENTIFIER,
            wx.stc.STC_P_NUMBER,
            wx.stc.STC_P_OPERATOR,
            wx.stc.STC_P_STRINGEOL,
            wx.stc.STC_P_TRIPLE,
            wx.stc.STC_P_TRIPLEDOUBLE,
            wx.stc.STC_P_WORD2,
            wx.stc.STC_P_COMMENTLINE,
            wx.stc.STC_P_COMMENTBLOCK,
            ]

#: List about stc.editwindow styles
stc_style = [stc.STC_STYLE_BRACEBAD,
             stc.STC_STYLE_BRACELIGHT,
             stc.STC_STYLE_CALLTIP,
             stc.STC_STYLE_CONTROLCHAR,
             stc.STC_STYLE_DEFAULT,
             #stc.STC_STYLE_FOLDDISPLAYTEXT,
             stc.STC_STYLE_INDENTGUIDE,
             stc.STC_STYLE_LASTPREDEFINED,
             stc.STC_STYLE_MAX
             ]