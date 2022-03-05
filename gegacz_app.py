import sys
import os
import ctypes
import multiprocessing
from tkinter import (
    Tk,
    Frame,
    Widget,
    Label,
    Button,
    font,
    YES,
    NO,
    TOP,
    BOTTOM,
    LEFT,
    RIGHT,
    BOTH,
    X,
    Y,
)
from PIL import ImageTk, Image, ImageOps
from playsound import playsound


def hide_console():
    """hide console window"""
    if os.name == "nt":
        ctypes.windll.user32.ShowWindow(
            ctypes.windll.kernel32.GetConsoleWindow(), 0
        )
    return None
    
    
class GuiClass(Frame):
    """gegacz app
    https://stackoverflow.com/questions/31360480/tkinter-label-image-without-border
    https://unsplash.com/photos/X7OdIjzkX48/download?force=true
    https://www.youtube.com/watch?v=fKKNPLowteY&list=PLk5NnKMbPNn-p4rgQRir2H49JB0ndzBYk&index=44
    https://stackoverflow.com/questions/57158779/how-to-stop-audio-with-playsound-module
    https://stackoverflow.com/questions/68704443/python-playsound-error-261-for-command-the-driver-cannot-recognize-the-specifie
    https://mp3cut.net/pl/
    https://stackoverflow.com/questions/41870727/pyinstaller-adding-data-files
    https://github.com/pyinstaller/pyinstaller/issues/4532
    https://stackoverflow.com/questions/27637197/tkinter-window-closes-automatically-after-python-program-has-run-in-pycharm
    https://stackoverflow.com/questions/32672596/pyinstaller-loads-script-multiple-times
    pyinstaller -F --add-data "resources/wyjasnianie_gegacza.mp3;resources" --add-data "resources/gegacz_wyjasniony.mp3;resources" --add-data "resources/hymn_gegaczy.mp3;resources" --add-data "resources/goose.jpg;resources" gegacz_app.py
    """
    def __init__(self, master):
        super().__init__(master)
        gegacz_img_path = self.resource_path(r'resources\goose.jpg')
        self.__original_img = Image.open(gegacz_img_path)
        self.__sound_process = None
        self.run_gui()
        
    def gegaj(self):
        print('[*] gegaj')
        if self.__sound_process is not None:
            self.__sound_process.terminate()
            
        # change label image
        img = ImageTk.PhotoImage(self.__original_img)
        self.gegacz_image.config(image=img)
        self.gegacz_image.image = img
        
        # play sound 
        sound_path = self.resource_path(r'resources\hymn_gegaczy.mp3')
        self.__sound_process = multiprocessing.Process(target=playsound, args=(sound_path,))
        self.__sound_process.start()
        return None
        
    def wyjasnij_gegacza(self):
        print('[*] wyjasnij gegacza')
        if self.__sound_process is not None:
            self.__sound_process.terminate()
            
        # change label image
        img = ImageOps.invert(self.__original_img)
        img = ImageTk.PhotoImage(img)
        self.gegacz_image.config(image=img)
        self.gegacz_image.image = img
        
        # play sound
        sound_path = self.resource_path(r'resources\wyjasnianie_gegacza.mp3')
        self.__sound_process = multiprocessing.Process(target=playsound, args=(sound_path,))
        self.__sound_process.start()
        return None
        
    def gegacz_wyjasniony(self):
        print('[*] gegacz_wyjasniony')
        if self.__sound_process is not None:
            self.__sound_process.terminate()
        sound_path = self.resource_path(r'resources\gegacz_wyjasniony.mp3')
        self.__sound_process = multiprocessing.Process(target=playsound, args=(sound_path,))
        self.__sound_process.start()
        return None
        
    def run_gui(self):
        """create widgets"""
        # *********** init gui ***********
        self.font = font.Font(family="Bahnschrift SemiLight Condensed", size=26, weight="normal")
        self.master.resizable(width=False, height=False)
        self.master.wm_title("gegacz app")
        self.pack()
        
        # *********** gegacz widgets ***********
        self.gegaj_button = Button(self.master, font=self.font, text="GĘGAJ", command=self.gegaj, justify="center")
        self.gegaj_button.pack(expand=NO, fill=X, side=TOP)
        
        self.gegacz_image = Label(self.master, borderwidth=0, highlightthicknes=0)
        self.gegacz_image.pack(expand=YES, fill=BOTH, side=TOP)
        img = ImageTk.PhotoImage(self.__original_img)
        self.gegacz_image.config(image=img)
        self.gegacz_image.image = img  # storing img in memory is needed
        
        self.wyjasnij_gegacza_button = Button(self.master, font=self.font, text="WYJAŚNIJ GĘGACZA", command=self.wyjasnij_gegacza, justify="center")
        self.wyjasnij_gegacza_button.pack(expand=NO, fill=X, side=TOP)
        self.gegacz_wyjasniony_button = Button(self.master, font=self.font, text="GĘGACZ WYJAŚNIONY", command=self.gegacz_wyjasniony, justify="center")
        self.gegacz_wyjasniony_button.pack(expand=NO, fill=X, side=TOP)
        
        # *********** lift, get focus ***********
        self.master.update()
        self.master.attributes("-topmost", True)
        self.master.lift()  # move window to the top
        self.master.focus_force()
        return None
        
    @staticmethod
    def resource_path(relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
        
        
if __name__ == "__main__":
    hide_console()
    multiprocessing.freeze_support()
    gui = GuiClass(master=Tk())
    gui.mainloop()
    