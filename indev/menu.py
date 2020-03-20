from tkinter import *

#Nouvelle partie
#Charger une partie
fen = Tk()
fen.overrideredirect(True)

positionRight = int(fen.winfo_screenwidth() / 3 - fen.winfo_reqwidth() / 3)
positionDown = int(fen.winfo_screenheight() / 3 - fen.winfo_reqheight() / 2)
fen.geometry("+{}+{}".format(positionRight, positionDown))


background = PhotoImage(file="background.png")

menu = Canvas(fen, border=-5, background="black", width=background.width(), height=background.height())
menu.create_image(0, 0, image=background, anchor=NW)
menu.pack(fill=BOTH)

button1 = Button(fen, text = "Quit", command = fen.quit, anchor = W)
button1.configure(width = 10, activebackground = "#33B5E5", relief = FLAT)
button1_window = menu.create_window(10, 10, anchor=NW, window=button1)


fen.after(15000, menu.destroy)
#fen.after(5000, lambda: fen.overrideredirect(False))
fen.mainloop()