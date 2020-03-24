from tkinter import *

root = Tk()
yDefilB = Scrollbar(root, orient='vertical')
yDefilB.grid(row=0, column=1, sticky='ns')

xDefilB = Scrollbar(root, orient='horizontal')
xDefilB.grid(row=1, column=0, sticky='ew')

listSel = Listbox(root,
     xscrollcommand=xDefilB.set,
     yscrollcommand=yDefilB.set)
listSel.grid(row=0, column=0, sticky='nsew')


listSel.insert(END, "a")
listSel.insert(END, "a")
listSel.insert(END, "a")
listSel.insert(END, "a")
listSel.insert(END, "a")
listSel.insert(END, "a")
listSel.insert(END, "a")
listSel.insert(END, "a")
listSel.insert(END, "a")
listSel.insert(END, "a")
listSel.insert(END, "a")
listSel.insert(END, "a")
listSel.insert(END, "a")
listSel.insert(END, "a")
listSel.insert(END, "a")
listSel.insert(END, "a")
listSel.insert(END, "a")
listSel.insert(END, "a")
listSel.insert(END, "a")
listSel.insert(END, "b")
root.mainloop()