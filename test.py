from tkinter import *

def appel_bouton():
	print("ok")

root = Tk()


photo = PhotoImage(file='image/pion.png')

img = PhotoImage(file='image/pion.png')

button = Button(root, image=img, background="white", command=appel_bouton, padx=30, pady=30)
button.grid()

b = Button(root, image=None, text="haha", background="black", padx=30, pady=30, command=lambda: appel_bouton())

b["image"] = img
b.grid()

b["text"] = "azerty"
print(b.cget("text"))

root.mainloop()

