import tkinter as Tkinter

from tkinter import *

class NoBorderWindow(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.little = Tk()
        self.little.geometry("0x0")
        self.little.lift(aboveThis=self)
        self.little.bind("<Map>", self.apparition)
        self.little.bind("<Unmap>", self.disparition)
        self.overrideredirect(True)
        self.lift()
        self.attributes('-topmost', True)

        self.background_image = PhotoImage(file="background.png")
        menu = Canvas(self, border=-5, background="black", width=self.background_image.width(), height=self.background_image.height())
        menu.create_image(0, 0, image=self.background_image, anchor=NW)
        menu.pack(fill=BOTH)

        centrer_fenetre(self.little)
        centrer_fenetre(self)




    def apparition(self, e):
        self.wm_deiconify()
        self.lift()
    def disparition(self, e):
        self.wm_withdraw()
        self.lift()

def centrer_fenetre(fen):
    fen.update_idletasks()
    width = fen.winfo_width()
    height = fen.winfo_height()
    x = (fen.winfo_screenwidth() // 2) - (width // 2)
    y = (fen.winfo_screenheight() // 2) - (height // 2)
    fen.geometry('{}x{}+{}+{}'.format(width, height, x, y))

class App:
    def __init__(self):
        self.root = Tkinter.Tk()
        self.root.geometry("0x0")
        fen = self.root
        positionRight = int(fen.winfo_screenwidth() / 3 - fen.winfo_reqwidth() / 3)
        positionDown = int(fen.winfo_screenheight() / 3 - fen.winfo_reqheight() / 2)
        fen.geometry("+{}+{}".format(positionRight, positionDown))
        self.window = Tkinter.Toplevel()
        fen = self.window
        fen.geometry("100x100")
        positionRight = int(fen.winfo_screenwidth() / 3 - fen.winfo_reqwidth() / 3)
        positionDown = int(fen.winfo_screenheight() / 3 - fen.winfo_reqheight() / 2)
        fen.geometry("+{}+{}".format(positionRight, positionDown))
        fen.lift
        self.window.overrideredirect(True)
        Tkinter.Label(self.window, text="Additional window").pack()
        self.root.bind("<Unmap>", self.OnUnMap)
        self.root.bind("<Map>", self.OnMap)
        self.root.mainloop()
    def OnMap(self, e):
        self.window.wm_deiconify()
    def OnUnMap(self, e):
        self.window.wm_withdraw()

app = NoBorderWindow()
app.little.title("Chesscraft")
app.mainloop()