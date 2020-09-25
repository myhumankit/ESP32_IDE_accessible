from Packages import wx, speech
def load_img(path):
    return wx.Image(path,wx.BITMAP_TYPE_ANY).ConvertToBitmap()

def speak(frame, txt):
    if frame.voice_on:
        speech.say(txt)
