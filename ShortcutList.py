#   TITLE: ShortcutList
#
#---------------------------------------------------------------------------------------------#
#
#   CREATER: Stephen Baxter
#
#---------------------------------------------------------------------------------------------#
#
#   LICENSE:
#   MIT License
#
#   Copyright (c) 2021 Stephen Baxter (Nickname: Jak E Chronicle)
#   
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#   of this software and associated documentation files (the "Software"), to deal
#   in the Software without restriction, including without limitation the rights
#   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#   copies of the Software, and to permit persons to whom the Software is
#   furnished to do so, subject to the following conditions:
#   
#   The above copyright notice and this permission notice shall be included in all
#   copies or substantial portions of the Software.
#   
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#   SOFTWARE.
#
#---------------------------------------------------------------------------------------------#
#
#   IMPORTENT LINKS:
#   https://github.com/Stephen-Baxter
#   https://stephen-baxter.github.io
#   https://github.com/Stephen-Baxter/ShortcutList/tree/main
#   https://www.python.org/
#   https://www.python.org/downloads/
#
#---------------------------------------------------------------------------------------------#
#
#   CONTROLS:
#   Esc Key ============================================== Exit ShortcutList
#   F1 Function Key ====================================== Minimize window
#   F2 Function Key ====================================== Toggel maximize window
#   F11 Function Key ===================================== Toggel fullscreen
#   Arror Keys / Mouse movement ========================== Select shortcut
#   Enter Key / Left Mouse Button / Right Mouse Button === Launch selected shortcut
#   Mouse Scrollweel ===================================== Scolls window up or down
#
#----------------------------------------------------------------------------------------------#
#   DATA FORMAT:
#   
#   SHORTCUT_LIST_DATA_ = {
#       "settings": 
#       {
#           "program title (string)": "ShortcutList", # this is the name that will appears on the title bar
#           "program icon path (string)": "<dive letter>:/some file path/file.(exe or ico)", # this is the icon that will appears on the title bar
#           "background color (string)": "#000022",
#           "button color (string)": "#555555",
#           "highlight color (string)": "#FF0000",
#           "font size (float)": 0.08,
#           "font type (string)": "Helvetica",
#           "shortcut button padding (float)": 0.1,
#           "shortcut button aspect ratio (float)": 1.5,
#           "shortcut button image fit (boolean)": True,
#           "number of shortcuts on a row (integer)": 2
#       },
#       "sortcuts":
#       [
#           {
#               "name (string)": "First line of name\nNext line of name", # name will appear on shortcut button when image can not be found
#               "exe path (string)": '"<dive letter>:/some file path/file.exe"', # run a executable
#               "image path (string)": "<dive letter>:/some file path/file.<image extension>" # the image that will appear on shortcut button
#           },
#           {
#               "name (string)": "First line of name\nNext line of name",
#               "exe path (string)": '"<dive letter>:/some file path/file.exe" <some command(s)> "<dive letter>:/some file path/file.<some extension>"',  # run a executable with commands
#               "image path (string)": "<dive letter>:/some file path/file.<image extension>"
#           },
#           {
#               "name (string)": "First line of name\nNext line of name",
#               "exe path (string)": '"<dive letter>:/some file path/file.lnk"', # run a shortcut (i.e. .lnk file)
#               "image path (string)": "<dive letter>:/some file path/file.<image extension>"
#           }
#       ]
#   }
#
#----------------------------------------------------------------------------------------------#

import tkinter
from PIL import ImageTk, Image
import subprocess, os
import math, string

class GLOBAL():
    def __init__(self_):
        self_

    def IsHexString(self_, string_):
        if type(string_) != str: return False
        if string_[0] != "#" and len(string_) < 2: return False
        for i in range(1, len(string_)):
            if string_[i] not in string.hexdigits: return False
        return True

_ = GLOBAL()

class SHORTCUT():
    def __init__(self_, data_):
        self_.name =  data_["name (string)"]
        self_.exePath =  data_["exe path (string)"]
        self_.imagePath = data_["image path (string)"]

class SHORTCUT_LIST_DATA():
    def __init__(self_, data_):
        self_.programTitle = data_["settings"]["program title (string)"] if type(data_["settings"]["program title (string)"]) == str else "ShortcutList"
        self_.programIconPath = data_["settings"]["program icon path (string)"]
        self_.backgroundColor = data_["settings"]["background color (string)"] if _.IsHexString(data_["settings"]["background color (string)"]) else "#FFFFFF"
        self_.buttonColor = data_["settings"]["button color (string)"] if _.IsHexString(data_["settings"]["button color (string)"]) else "#FFFFFF"
        self_.highlightColor = data_["settings"]["highlight color (string)"] if _.IsHexString(data_["settings"]["highlight color (string)"]) else "#000000"
        self_.fontSize = data_["settings"]["font size (float)"] if type(data_["settings"]["font size (float)"]) == float else 0.08
        self_.fontType = data_["settings"]["font type (string)"] 
        self_.buttonPadding = data_["settings"]["shortcut button padding (float)"] if type(data_["settings"]["shortcut button padding (float)"]) == float else 0.1
        self_.buttonAspectRatio = data_["settings"]["shortcut button aspect ratio (float)"] if type(data_["settings"]["shortcut button aspect ratio (float)"]) == float else 1.5
        self_.buttonImageFit = data_["settings"]["shortcut button image fit (boolean)"] if type(data_["settings"]["shortcut button image fit (boolean)"]) == bool else True
        self_.numberOfShortcuts = len(data_["sortcuts"])
        self_.numberOfShortcutsOnARow = data_["settings"]["number of shortcuts on a row (integer)"] if self_.numberOfShortcuts >= data_["settings"]["number of shortcuts on a row (integer)"] else self_.numberOfShortcuts
        self_.listOfButtons = []
        self_.currentButton = -1
        self_.previousButton = 0
        self_.listOfShortcuts = []
        for i in range(len(data_["sortcuts"])): self_.listOfShortcuts.append(SHORTCUT(data_["sortcuts"][i]))
        self_.isFullScreen = False

def main(data_):
    shortcutListData = SHORTCUT_LIST_DATA(data_)

    window = tkinter.Tk()
    window.geometry("600x400")
    window.state("zoomed") 
    window.title(shortcutListData.programTitle)

    try: window.iconbitmap(shortcutListData.programIconPath)
    except: print(f"NOTE: Icon not found - {shortcutListData.programIconPath}")

    canvas = tkinter.Canvas(window)
    canvas.pack(side="left", fill="both", expand=1)
    canvas.configure(background=shortcutListData.backgroundColor)

    scrollbar = tkinter.Scrollbar(window, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    canvasFrame = tkinter.Frame(canvas)
    canvasFrame.configure(background=shortcutListData.backgroundColor)
    canvas.fram_n_canvas_iid = canvas.create_window((0,0), window=canvasFrame, anchor="nw")

    def EndShortcutListProgram(_):
        window.destroy()

    def RunShortcut(_):
        if shortcutListData.currentButton > -1:
            EndShortcutListProgram(_)
            try: subprocess.Popen(shortcutListData.listOfButtons[shortcutListData.currentButton].exePath, creationflags=0x00000008).pid 
            except: os.startfile(shortcutListData.listOfButtons[shortcutListData.currentButton].exePath) # using OS this runs shortcuts (.lnk files)

    def HighlightButton():
        shortcutListData.listOfButtons[shortcutListData.previousButton].configure(background=shortcutListData.backgroundColor)
        shortcutListData.listOfButtons[shortcutListData.currentButton].configure(background=shortcutListData.highlightColor)

    def ButtonHighlightEnter(event_):
        for i in range(shortcutListData.numberOfShortcuts):
            if event_.widget == shortcutListData.listOfButtons[i]:
                shortcutListData.previousButton = shortcutListData.currentButton
                shortcutListData.currentButton = i
                HighlightButton()
                break
            
    for i in range(shortcutListData.numberOfShortcutsOnARow): tkinter.Grid.columnconfigure(canvasFrame, i, weight=1)
    j = -1
    for i in range(shortcutListData.numberOfShortcuts):
        if i % shortcutListData.numberOfShortcutsOnARow == 0:
            j+=1
            tkinter.Grid.rowconfigure(canvasFrame, j, weight=1)
        shortcutListData.listOfButtons.append(tkinter.Button(canvasFrame, background=shortcutListData.backgroundColor, compound="center"))
        shortcutListData.listOfButtons[i].exePath = shortcutListData.listOfShortcuts[i].exePath
        shortcutListData.listOfButtons[i].bind("<Enter>", ButtonHighlightEnter)
        try: shortcutListData.listOfButtons[i].img = Image.open(shortcutListData.listOfShortcuts[i].imagePath)
        except:
            shortcutListData.listOfButtons[i].configure(text=shortcutListData.listOfShortcuts[i].name)
            print(f"NOTE: Image for shortcut {i+1} not found - {shortcutListData.listOfShortcuts[i].imagePath}")
        
    shortcutListData.numberOfButtonsOnAColumn = j + 1

    _.oldWidth = 0
    def Resize(event_):
        newWidth=event_.width
        if _.oldWidth != newWidth:
            newHeight = 0
            try: newHeight = int(newWidth * shortcutListData.buttonAspectRatio * shortcutListData.numberOfButtonsOnAColumn / shortcutListData.numberOfShortcutsOnARow)
            except: _
            canvas.itemconfigure(canvas.fram_n_canvas_iid, width=newWidth, height=newHeight)
            canvas.configure(scrollregion=canvas.bbox("all"))
            j = 0
            k = -1
            for i in range(shortcutListData.numberOfShortcuts):
                if i % shortcutListData.numberOfShortcutsOnARow == 0:
                    j = 0
                    k+=1
                buttonPaddingWidth = int(newWidth / shortcutListData.numberOfShortcutsOnARow * shortcutListData.buttonPadding)
                buttonPaddingHeigth = int(buttonPaddingWidth * shortcutListData.buttonAspectRatio)
                shortcutListData.listOfButtons[i].grid_forget()
                shortcutListData.listOfButtons[i].grid(row=k, column=j, sticky="nsew", padx=buttonPaddingWidth, pady=buttonPaddingHeigth)
                j+=1
                buttonWidth = int(newWidth / shortcutListData.numberOfShortcutsOnARow - 2 * buttonPaddingWidth)
                buttonHeight = int(buttonWidth * shortcutListData.buttonAspectRatio)
                buttonImage = Image.new(mode="RGB", size=(buttonWidth,buttonHeight), color=shortcutListData.buttonColor)
                shortcutListData.listOfButtons[i].img1 = ImageTk.PhotoImage(buttonImage)
                try:
                    shortcutImage = shortcutListData.listOfButtons[i].img
                    imageWidth, imageHeight = shortcutImage.size
                    imageAspectRatio = imageHeight / imageWidth
                    startDrawingPointX = 0
                    startDrawingPointY = 0
                    m = -1 if shortcutListData.buttonImageFit else 1
                    if m*imageAspectRatio > m*shortcutListData.buttonAspectRatio:
                        imageWidth = buttonWidth
                        imageHeight = int(imageWidth * imageAspectRatio)
                        startDrawingPointY = int((buttonHeight - imageHeight) / 2)
                    else:
                        imageHeight = buttonHeight
                        imageWidth = int(imageHeight / imageAspectRatio)
                        startDrawingPointX = int((buttonWidth - imageWidth) / 2)
                    shortcutImage = shortcutImage.resize((imageWidth,imageHeight))
                    buttonImage.paste(shortcutImage, (startDrawingPointX, startDrawingPointY))
                    shortcutListData.listOfButtons[i].img2 = ImageTk.PhotoImage(buttonImage)
                    shortcutListData.listOfButtons[i].configure(image=shortcutListData.listOfButtons[i].img2)
                except:
                    shortcutListData.listOfButtons[i].configure(image=shortcutListData.listOfButtons[i].img1, font=(shortcutListData.fontType, int(shortcutListData.fontSize * buttonWidth)))

    def MouseWheel(event_):
        if canvasFrame.winfo_height() > window.winfo_height(): canvas.yview_scroll(-1 * int(event_.delta/math.fabs(event_.delta)), "units")

    def LeftArrow(_):
        if shortcutListData.currentButton - 1 > -1:
            shortcutListData.previousButton = shortcutListData.currentButton
            shortcutListData.currentButton -= 1
            HighlightButton()

    def RightArrow(_):
        if shortcutListData.currentButton + 1 < shortcutListData.numberOfShortcuts:
            shortcutListData.previousButton = shortcutListData.currentButton
            shortcutListData.currentButton += 1
            HighlightButton()

    def UpArrow(_):
        if shortcutListData.currentButton - shortcutListData.numberOfShortcutsOnARow > -1:
            shortcutListData.previousButton = shortcutListData.currentButton
            shortcutListData.currentButton -= shortcutListData.numberOfShortcutsOnARow
            HighlightButton()

    def DownArrow(_):
        if shortcutListData.currentButton == -1:
            shortcutListData.currentButton = 0
            HighlightButton()
        elif shortcutListData.currentButton + shortcutListData.numberOfShortcutsOnARow < shortcutListData.numberOfShortcuts:
            shortcutListData.previousButton = shortcutListData.currentButton
            shortcutListData.currentButton += shortcutListData.numberOfShortcutsOnARow
            HighlightButton()
        else:
            shortcutListData.previousButton = shortcutListData.currentButton
            shortcutListData.currentButton = shortcutListData.numberOfShortcuts - 1
            HighlightButton()

    def ToggelFullscreen(_):
        shortcutListData.isFullScreen = not shortcutListData.isFullScreen
        window.attributes("-fullscreen", shortcutListData.isFullScreen)

    def Minimize(_):
        window.state("iconic")

    def ToggelMaximize(_):
        if window.state() == "normal": window.state("zoomed")
        else: window.state("normal")

    window.bind("<Left>", LeftArrow)
    window.bind("<Right>", RightArrow)
    window.bind("<Up>", UpArrow)
    window.bind("<Down>", DownArrow)
    window.bind("<Return>", RunShortcut) # Enter key
    window.bind("<Button 1>", RunShortcut) # Left mouse button
    window.bind("<Button 3>", RunShortcut) # Right mouse button
    window.bind("<F11>", ToggelFullscreen)
    window.bind("<F1>", Minimize)
    window.bind("<F2>", ToggelMaximize)
    window.bind("<Escape>", EndShortcutListProgram)
    canvas.bind("<Configure>", Resize)
    window.bind_all("<MouseWheel>", MouseWheel)

    window.mainloop()

#ShortcutList-Data--------------------------------------------------------------------#

SHORTCUT_LIST_DATA_ = {
    "settings": 
    {
        "program title": None,
        "program icon path": None,
        "background color": None,
        "button color": None,
        "highlight color": None,
        "font size": None,
        "font type": None,
        "shortcut button padding": None,
        "shortcut button aspect ratio": None,
        "shortcut button image fit": None,
        "number of shortcuts on a row": None
    },
    "sortcuts":
    [
        {
            "name": "",
            "exe path": '"C:/"',
            "image path": "C:/"
        }
    ]
}

#-------------------------------------------------------------------------------------#

if __name__ == "__main__": main(SHORTCUT_LIST_DATA_)
