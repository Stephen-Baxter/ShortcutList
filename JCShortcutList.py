#ShortcutList-Data--------------------------------------------------------------------#

SHORTCUT_LIST_DATA_ = {
    "Settings": 
    {
        "Program title (string: 'X')-----------------------": None,
        "Program icon path (string: 'X')-------------------": None,
        "Program window size (string: 'XXXxXXX')-----------": None,
        "Show scrollbar (boolean: True or False)-----------": None,
        "Start in fullscreen (boolean: True or False)------": None,
        "Background color (string: '#XXXXXX')--------------": None,
        "Button color (string: '#XXXXXX')------------------": None,
        "Border color (string: '#XXXXXX')------------------": None,
        "Highlight color (string: '#XXXXXX')---------------": None,
        "Background image path (string: 'X')---------------": None,
        "Background image fit (boolean: True or False)-----": None,
        "Font size (float: X.X)----------------------------": None,
        "Font type (string: 'X')---------------------------": None,
        "Shortcut button border (integer: X)---------------": None,
        "Shortcut button padding (integer: X)--------------": None,
        "Shortcut button aspectratio (float: X.X)----------": None,
        "Shortcut button image fit (boolean: True or False)": None,
        "Number of shortcuts on a row (integer: X)---------": None,
        "Play background music (boolean: True or False)----": None,
        "Repeat background music (boolean: True or False)--": None,
        "Background music path (string: 'X')---------------": None,
    },
    "Shortcuts":
    [
        {
            "Name (string: 'X')----------------": None,
            "Exe path (string: 'X')------------": [None],
            "Image path (string: 'X')----------": None,
            "Image fit (boolean: True or False)": None
        },
        
    ]
}

#-------------------------------------------------------------------------------------#

import tkinter as tk
from PIL import ImageTk, Image
import math, string
import subprocess
try: import pygame
except: print(f"NOTE: Pygame not found")

class SHORTCUT():
    def __init__(self_, data_, index_):
        self_.name =  data_["Name (string: 'X')----------------"] if type(data_["Name (string: 'X')----------------"]) == str else f"Shortcut {index_ + 1}"
        self_.exePath =  data_["Exe path (string: 'X')------------"]
        self_.imagePath = data_["Image path (string: 'X')----------"]
        self_.image = None
        self_.imageWidth = None
        self_.imageHeight = None
        self_.imageAspectRatio = None
        try:
            self_.image = Image.open(self_.imagePath)
            self_.imageWidth, self_.imageHeight = self_.image.size
            self_.imageAspectRatio = self_.imageHeight / self_.imageWidth
        except:
            print(f"NOTE: Image for shortcut {index_ + 1} not found - {self_.imagePath}")
        self_.imageFit = data_["Image fit (boolean: True or False)"] if type(data_["Image fit (boolean: True or False)"]) == bool else True

class SHORTCUT_LIST_DATA():
    def __init__(self_, data_):
        self_.programTitle = data_["Settings"]["Program title (string: 'X')-----------------------"] if type(data_["Settings"]["Program title (string: 'X')-----------------------"]) == str else "JCShortcutList"
        self_.programIconPath = data_["Settings"]["Program icon path (string: 'X')-------------------"]
        self_.programWindowSize = data_["Settings"]["Program window size (string: 'XXXxXXX')-----------"] if type(data_["Settings"]["Program window size (string: 'XXXxXXX')-----------"]) == str else "800x600"
        self_.backgroundColor = data_["Settings"]["Background color (string: '#XXXXXX')--------------"] if self_.IsHexString(data_["Settings"]["Background color (string: '#XXXXXX')--------------"]) else "#c0c0c0"
        self_.buttonColor = data_["Settings"]["Button color (string: '#XXXXXX')------------------"] if self_.IsHexString(data_["Settings"]["Button color (string: '#XXXXXX')------------------"]) else "#7fFF7f"
        self_.borderColor = data_["Settings"]["Border color (string: '#XXXXXX')------------------"] if self_.IsHexString(data_["Settings"]["Border color (string: '#XXXXXX')------------------"]) else "#3c3c3c"
        self_.highlightColor = data_["Settings"]["Highlight color (string: '#XXXXXX')---------------"] if self_.IsHexString(data_["Settings"]["Highlight color (string: '#XXXXXX')---------------"]) else "#ff7f7f"
        self_.backgroundImagePath = data_["Settings"]["Background image path (string: 'X')---------------"]
        self_.backgroundImageFit = data_["Settings"]["Background image fit (boolean: True or False)-----"] if type(data_["Settings"]["Background image fit (boolean: True or False)-----"]) == bool else True
        self_.backgroundImage = None
        self_.backgroundImageWidth = None
        self_.backgroundImageHeight = None
        self_.backgroundImageAspectRatio = None
        try: 
            self_.backgroundImage = Image.open(self_.backgroundImagePath)
            self_.backgroundImageWidth, self_.backgroundImageHeight = self_.backgroundImage.size
            self_.backgroundImageAspectRatio = self_.backgroundImageHeight / self_.backgroundImageWidth
        except:
            print(f"NOTE: Image for background not found - {self_.backgroundImagePath}")
        self_.fontSize = data_["Settings"]["Font size (float: X.X)----------------------------"] if type(data_["Settings"]["Font size (float: X.X)----------------------------"]) == float else 0.08
        self_.fontType = data_["Settings"]["Font type (string: 'X')---------------------------"]
        self_.buttonBorder = data_["Settings"]["Shortcut button border (integer: X)---------------"] if type(data_["Settings"]["Shortcut button border (integer: X)---------------"]) == int else 10
        self_.buttonPadding = data_["Settings"]["Shortcut button padding (integer: X)--------------"] if type(data_["Settings"]["Shortcut button padding (integer: X)--------------"]) == int else 10
        self_.buttonAspectRatio = data_["Settings"]["Shortcut button aspectratio (float: X.X)----------"] if type(data_["Settings"]["Shortcut button aspectratio (float: X.X)----------"]) == float else 1.5
        self_.buttonImageFit = data_["Settings"]["Shortcut button image fit (boolean: True or False)"] if type(data_["Settings"]["Shortcut button image fit (boolean: True or False)"]) == bool else None
        self_.numberOfShortcuts = len(data_["Shortcuts"])
        numberOfShortcutsOnARow = data_["Settings"]["Number of shortcuts on a row (integer: X)---------"] if type(data_["Settings"]["Number of shortcuts on a row (integer: X)---------"]) == int else 5
        self_.numberOfShortcutsOnARow = numberOfShortcutsOnARow if self_.numberOfShortcuts >= numberOfShortcutsOnARow else self_.numberOfShortcuts
        self_.numberOfShortcutsOnAColumn = math.ceil(self_.numberOfShortcuts / self_.numberOfShortcutsOnARow)
        self_.listOfButtons = []
        self_.listOfButtonsLeftoverSpace = None
        self_.currentButton = -1
        self_.previousButton = 0
        self_.listOfShortcuts = []
        for i in range(self_.numberOfShortcuts): self_.listOfShortcuts.append(SHORTCUT(data_["Shortcuts"][i], i))
        self_.isFullScreen = data_["Settings"]["Start in fullscreen (boolean: True or False)------"] if type(data_["Settings"]["Start in fullscreen (boolean: True or False)------"]) == bool else False
        self_.showScrollbar = data_["Settings"]["Show scrollbar (boolean: True or False)-----------"] if type(data_["Settings"]["Show scrollbar (boolean: True or False)-----------"]) == bool else True
        self_.playBackgroundMusic = data_["Settings"]["Play background music (boolean: True or False)----"] if type(data_["Settings"]["Play background music (boolean: True or False)----"]) == bool else False
        self_.repeatBackgroundMusic = data_["Settings"]["Repeat background music (boolean: True or False)--"] if type(data_["Settings"]["Repeat background music (boolean: True or False)--"]) == bool else False
        self_.backgroundMusicPath = data_["Settings"]["Background music path (string: 'X')---------------"]

    def IsHexString(self_, string_):
        if type(string_) != str: return False
        if string_[0] != "#": return False
        if len(string_) != 7: return False
        for i in range(1, len(string_)):
            if string_[i] not in string.hexdigits: return False
        return True
    
class WINDOW(tk.Tk):
    def __init__(self_, shortcut_list_data_):
        tk.Tk.__init__(self_)
        self_.title(shortcut_list_data_.programTitle)
        self_.geometry(shortcut_list_data_.programWindowSize)
        self_.attributes("-fullscreen", shortcut_list_data_.isFullScreen)
        try: self_.iconbitmap(shortcut_list_data_.programIconPath)
        except: print(f"NOTE: Icon not found - {shortcut_list_data_.programIconPath}")
        self_.canvas = tk.Canvas(self_, highlightthickness=0, background=shortcut_list_data_.backgroundColor)
        self_.frame = tk.Frame(self_.canvas, background=shortcut_list_data_.backgroundColor)
        self_.background = tk.Label(self_.frame, background=shortcut_list_data_.backgroundColor)
        self_.background.grid(sticky="nsew", rowspan=shortcut_list_data_.numberOfShortcutsOnAColumn, columnspan=shortcut_list_data_.numberOfShortcutsOnARow)
        self_.scrollbar = tk.Scrollbar(self_, orient="vertical", command=self_.canvas.yview)
        if shortcut_list_data_.showScrollbar: self_.scrollbar.pack(side="right", fill="y")
        self_.canvas.pack(side="left", fill="both", expand=True)
        self_.canvas.configure(yscrollcommand=self_.scrollbar.set)
        self_.frame_n_canvas_id = self_.canvas.create_window((0,0), window=self_.frame, anchor="nw")
        self_.oldWidth = 0
        self_.oldHeight = 0
        self_.oldBackboardYStart = 0
        self_.oldEventY = 0

def SetupBackgroundMusic(shortcut_list_data_):
    if shortcut_list_data_.playBackgroundMusic:
        pygame.mixer.init()
        try:
            pygame.mixer.music.load(shortcut_list_data_.backgroundMusicPath)
            if shortcut_list_data_.repeatBackgroundMusic: pygame.mixer.music.play(loops=-1)
            else: pygame.mixer.music.play(loops=0)
        except: print(f"NOTE: Audio file not found - {shortcut_list_data_.backgroundMusicPath}")

def ShutdounBackgroundMusic(shortcut_list_data):
    if shortcut_list_data.playBackgroundMusic:
        pygame.mixer.quit()

def HighlightButton(shortcut_list_data_):
    shortcut_list_data_.listOfButtons[shortcut_list_data_.previousButton].configure(background=shortcut_list_data_.borderColor, highlightbackground=shortcut_list_data_.borderColor)
    shortcut_list_data_.listOfButtons[shortcut_list_data_.currentButton].configure(background=shortcut_list_data_.highlightColor, highlightbackground=shortcut_list_data_.highlightColor)

def ButtonHighlightEnter(event_, shortcut_list_data_):
    for i in range(shortcut_list_data_.numberOfShortcuts):
        if event_.widget == shortcut_list_data_.listOfButtons[i]:
            shortcut_list_data_.previousButton = shortcut_list_data_.currentButton
            shortcut_list_data_.currentButton = i
            HighlightButton(shortcut_list_data_)
            break

def GetImageSize(image_fit_, image_ratio_, background_width_, background_height_):
    m = 1 if image_fit_ else -1
    imageHeight = imageWidth = startDrawingPointX = startDrawingPointY = 0
    if m*image_ratio_ > m*(background_height_ / background_width_):
        imageHeight = background_height_
        imageWidth = int(imageHeight / image_ratio_)
        startDrawingPointX = int((background_width_ - imageWidth) / 2)
    else:
        imageWidth = background_width_
        imageHeight = int(imageWidth * image_ratio_)
        startDrawingPointY = int((background_height_ - imageHeight) / 2)
    return imageWidth, imageHeight, startDrawingPointX, startDrawingPointY

def OnResizeAndScroll(event_, window_, shortcut_list_data_):
    newCanvasWidth = window_.canvas.winfo_width()
    newRootHeight = window_.winfo_height()

    backgroundBackboardHeight = 0
    backboardYStart = 0
    resized = False
    scrolled = False
    
    if window_.oldWidth != newCanvasWidth or window_.oldHeight != newRootHeight:
        window_.oldWidth = newCanvasWidth
        window_.oldHeight = newRootHeight
        
        padding = shortcut_list_data_.buttonPadding
        borderAndPadding = 2 * (shortcut_list_data_.buttonBorder + padding)
        newCanvasHeight = int((((newCanvasWidth / shortcut_list_data_.numberOfShortcutsOnARow) - borderAndPadding) * shortcut_list_data_.buttonAspectRatio + borderAndPadding) * shortcut_list_data_.numberOfShortcutsOnAColumn)
        buttonWidth = int(((newCanvasWidth / shortcut_list_data_.numberOfShortcutsOnARow) - borderAndPadding))
        buttonHeight = int(buttonWidth * shortcut_list_data_.buttonAspectRatio)

        paddingOffsetY = 0
        if newCanvasHeight >= newRootHeight:
            window_.canvas.yview_scroll(-window_.canvas.winfo_height(), "units")
            event_.y = 0
            backgroundBackboardHeight = newCanvasHeight
        else:
            realButtonHeight = newRootHeight / shortcut_list_data_.numberOfShortcutsOnAColumn - borderAndPadding
            paddingOffsetY = int((realButtonHeight - buttonHeight) / 2)
            backgroundBackboardHeight = newRootHeight
        
        window_.canvas.itemconfigure(window_.frame_n_canvas_id, width=newCanvasWidth, height=backgroundBackboardHeight)
        window_.canvas.configure(scrollregion=window_.canvas.bbox("all"))

        j = k = -1
        for i in range(shortcut_list_data_.numberOfShortcuts):
            if i % shortcut_list_data_.numberOfShortcutsOnARow == 0:
                j += 1
                k = -1
            k+=1
            shortcut_list_data_.listOfButtons[i].grid_forget()
            shortcut_list_data_.listOfButtons[i].grid(row=j, column=k, sticky="nsew", padx=padding, pady=padding+paddingOffsetY)
            imageFit = shortcut_list_data_.listOfShortcuts[i].imageFit
            if shortcut_list_data_.buttonImageFit != None: imageFit = shortcut_list_data_.buttonImageFit
            buttonImage = Image.new(mode="RGBA", size=(buttonWidth,buttonHeight), color=shortcut_list_data_.buttonColor)
            if shortcut_list_data_.listOfShortcuts[i].image != None:
                imageWidth, imageHeight, startDrawingPointX, startDrawingPointY = GetImageSize(imageFit, shortcut_list_data_.listOfShortcuts[i].imageAspectRatio, buttonWidth, buttonHeight)
                buttonImage.paste(shortcut_list_data_.listOfShortcuts[i].image.resize((imageWidth,imageHeight)), (startDrawingPointX, startDrawingPointY))
            shortcut_list_data_.listOfButtons[i].img1 = ImageTk.PhotoImage(buttonImage)
            shortcut_list_data_.listOfButtons[i].configure(image=shortcut_list_data_.listOfButtons[i].img1, font=(shortcut_list_data_.fontType, int(shortcut_list_data_.fontSize * buttonWidth)))

        resized = shortcut_list_data_.backgroundImage != None
    
    event_.y = event_.y if (event_.y <= 0) else window_.oldEventY
    window_.oldEventY = event_.y
    newBackboardYStart = -1 * event_.y
    
    if window_.oldBackboardYStart != newBackboardYStart and shortcut_list_data_.backgroundImage != None:
        window_.oldBackboardYStart = newBackboardYStart
        newCanvasHeight = window_.frame.winfo_height()
        backgroundBackboardHeight = 0
        if newCanvasHeight > newRootHeight:
            backgroundBackboardHeight = newCanvasHeight
            backboardYStart = int(newBackboardYStart)
        else:
            backgroundBackboardHeight = newRootHeight

        scrolled = shortcut_list_data_.backgroundImage != None

    if resized or scrolled:
        backgroundImageWidth, backgroundImageHeight, backgroundImageXStart, backgroundImageYStart = GetImageSize(shortcut_list_data_.backgroundImageFit, shortcut_list_data_.backgroundImageAspectRatio, newCanvasWidth, newRootHeight)
        backgroundBackboardImage = Image.new(mode="RGB", size=(newCanvasWidth,backgroundBackboardHeight), color=shortcut_list_data_.backgroundColor)
        backgroundBackboardImage.paste(shortcut_list_data_.backgroundImage.resize((backgroundImageWidth,backgroundImageHeight)), (backgroundImageXStart, backgroundImageYStart + backboardYStart))
        shortcut_list_data_.img1 = ImageTk.PhotoImage(backgroundBackboardImage)
        window_.background.configure(image=shortcut_list_data_.img1)

def EndJCShortcutListProgram(window_): window_.destroy()

def RunShortcut(window_, shortcut_list_data_):
    if shortcut_list_data_.currentButton > -1:
        EndJCShortcutListProgram(window_)
        try: subprocess.Popen(shortcut_list_data_.listOfShortcuts[shortcut_list_data_.currentButton].exePath, creationflags=0x00000008).pid
        except: subprocess.Popen(shortcut_list_data_.listOfShortcuts[shortcut_list_data_.currentButton].exePath).pid 
        #try: subprocess.Popen(shortcut_list_data_.listOfShortcuts[shortcut_list_data_.currentButton].exePath, creationflags=0x00000008).pid 
        #except: os.startfile(shortcut_list_data_.listOfShortcuts[shortcut_list_data_.currentButton].exePath) # using OS this runs shortcuts (.lnk files)"""

def OnMouseClick(window_, shortcut_list_data_):
    if shortcut_list_data_.currentButton > -1:
        buttonX = shortcut_list_data_.listOfButtons[shortcut_list_data_.currentButton].winfo_x()
        buttonY = shortcut_list_data_.listOfButtons[shortcut_list_data_.currentButton].winfo_y()
        buttonWidth = shortcut_list_data_.listOfButtons[shortcut_list_data_.currentButton].winfo_width()
        buttonHeight = shortcut_list_data_.listOfButtons[shortcut_list_data_.currentButton].winfo_height()
        pointerX = window_.frame.winfo_pointerx() - window_.frame.winfo_rootx()
        pointerY = window_.frame.winfo_pointery() - window_.frame.winfo_rooty()
        if buttonX <= pointerX <= buttonX+buttonWidth and buttonY <= pointerY <= buttonY+buttonHeight: RunShortcut(window_, shortcut_list_data_)

def ToggelFullscreen(window_, shortcut_list_data_):
    shortcut_list_data_.isFullScreen = not shortcut_list_data_.isFullScreen
    window_.attributes("-fullscreen", shortcut_list_data_.isFullScreen)

def Minimize(window_): window_.state("iconic")

def ToggelMaximize(window_):
    if window_.state() == "normal": 
        try: window_.state("zoomed")
        except: window_.attributes("-zoomed", True)
    else: window_.state("normal")

def LeftArrow(shortcut_list_data_):
    if shortcut_list_data_.currentButton == -1:
        shortcut_list_data_.currentButton = 0
    elif shortcut_list_data_.currentButton - 1 > -1:
        shortcut_list_data_.previousButton = shortcut_list_data_.currentButton
        shortcut_list_data_.currentButton -= 1
    else:
        shortcut_list_data_.previousButton = shortcut_list_data_.currentButton
        shortcut_list_data_.currentButton = shortcut_list_data_.numberOfShortcuts - 1
    HighlightButton(shortcut_list_data_)

def RightArrow(shortcut_list_data_):
    if shortcut_list_data_.currentButton + 1 < shortcut_list_data_.numberOfShortcuts:
        shortcut_list_data_.previousButton = shortcut_list_data_.currentButton
        shortcut_list_data_.currentButton += 1
    else:
        shortcut_list_data_.previousButton = shortcut_list_data_.currentButton
        shortcut_list_data_.currentButton = 0
    HighlightButton(shortcut_list_data_)

def UpArrow(shortcut_list_data_):
    if shortcut_list_data_.currentButton - shortcut_list_data_.numberOfShortcutsOnARow > -1:
        shortcut_list_data_.previousButton = shortcut_list_data_.currentButton
        shortcut_list_data_.currentButton -= shortcut_list_data_.numberOfShortcutsOnARow  
    else:
        shortcut_list_data_.previousButton = shortcut_list_data_.currentButton
        shortcut_list_data_.currentButton = 0
    HighlightButton(shortcut_list_data_)

def DownArrow(shortcut_list_data_):
    if shortcut_list_data_.currentButton == -1:
        shortcut_list_data_.currentButton = 0
    elif shortcut_list_data_.currentButton + shortcut_list_data_.numberOfShortcutsOnARow < shortcut_list_data_.numberOfShortcuts:
        shortcut_list_data_.previousButton = shortcut_list_data_.currentButton
        shortcut_list_data_.currentButton += shortcut_list_data_.numberOfShortcutsOnARow
    else:
        shortcut_list_data_.previousButton = shortcut_list_data_.currentButton
        shortcut_list_data_.currentButton = shortcut_list_data_.numberOfShortcuts - 1
    HighlightButton(shortcut_list_data_)

def MouseWheel(event_, window_):
    if window_.frame.winfo_height() > window_.winfo_height(): window_.canvas.yview_scroll(-1 * int(event_.delta/math.fabs(event_.delta)), "units")

def PageUp(window_, shortcut_list_data_):
    if window_.frame.winfo_height() > window_.winfo_height(): window_.canvas.yview_scroll(-1, "units")
    if shortcut_list_data_.currentButton == -1:
        shortcut_list_data_.currentButton = 0
        HighlightButton(shortcut_list_data_)

def PageDown(window_, shortcut_list_data_):
    if window_.frame.winfo_height() > window_.winfo_height() and shortcut_list_data_.currentButton != -1: window_.canvas.yview_scroll(1, "units")
    if shortcut_list_data_.currentButton == -1:
        shortcut_list_data_.currentButton = 0
        HighlightButton(shortcut_list_data_)

def main(data_):
    shortcutListData = SHORTCUT_LIST_DATA(data_)

    SetupBackgroundMusic(shortcutListData)
    window = WINDOW(shortcutListData)

    window.update()

    window.canvas.itemconfigure(window.frame_n_canvas_id, width=window.canvas.winfo_width(), height=window.winfo_height())
    
    for i in range(shortcutListData.numberOfShortcutsOnARow): window.frame.columnconfigure(i, weight=1)
    for i in range(shortcutListData.numberOfShortcutsOnAColumn): window.frame.rowconfigure(i, weight=1)
    for i in range(shortcutListData.numberOfShortcuts):
        shortcutListData.listOfButtons.append(tk.Label(window.frame, borderwidth=0, highlightthickness=shortcutListData.buttonBorder, relief="solid"))
        shortcutListData.listOfButtons[i].configure(background=shortcutListData.borderColor, highlightbackground=shortcutListData.borderColor)
        shortcutListData.listOfButtons[i].bind("<Enter>", lambda event: ButtonHighlightEnter(event, shortcutListData))
        if shortcutListData.listOfShortcuts[i].image == None: shortcutListData.listOfButtons[i].configure(text=shortcutListData.listOfShortcuts[i].name, compound='center')

    window.bind("<Escape>", lambda event: EndJCShortcutListProgram(window))
    window.bind("<Return>", lambda event: RunShortcut(window, shortcutListData))
    window.bind("<Button 1>", lambda event: OnMouseClick(window, shortcutListData))
    window.bind("<Button 3>", lambda event: OnMouseClick(window, shortcutListData))
    window.bind("<F11>", lambda event: ToggelFullscreen(window, shortcutListData))
    window.bind("<F1>", lambda event: Minimize(window))
    window.bind("<F2>", lambda event: ToggelMaximize(window))
    window.bind("<Configure>", lambda event: OnResizeAndScroll(event, window, shortcutListData))
    window.bind("<Left>", lambda event: LeftArrow(shortcutListData))
    window.bind("<Right>", lambda event: RightArrow(shortcutListData))
    window.bind("<Up>", lambda event: UpArrow(shortcutListData))
    window.bind("<Down>", lambda event: DownArrow(shortcutListData))
    window.bind("<Prior>", lambda event: PageUp(window, shortcutListData))
    window.bind("<Next>", lambda event: PageDown(window, shortcutListData))
    window.bind_all("<MouseWheel>", lambda event: MouseWheel(event, window))

    #window.wm_attributes("-alpha", 0.9)
    window.mainloop()

    ShutdounBackgroundMusic(shortcutListData)

if __name__ == "__main__": main(SHORTCUT_LIST_DATA_)