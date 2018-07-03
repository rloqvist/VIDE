from tkinter import *
from vide.gui import Editor

def callback(event):
    content = editor.text.get("1.0", "end")[:-1]
    '''
    with open("runfile.py", "w") as dump:
        dump.write(content)
    '''
    print(content)

root = Tk()

root.columnconfigure(0, weight=1)
#root.columnconfigure(1, weight=13)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=13)

editFrame = Frame(root)
textFrame = Frame(root)

#lftGrid.grid(row=0, column=0, sticky="NWSE")
editFrame.grid(row=0, column=0, sticky="NWSE")
textFrame.grid(row=1, column=0)


editor = Editor(editFrame)
output = Text(textFrame, wrap="word", state=DISABLED, width=650)

editor.pack(expand=True, fill="both")
output.pack(fill="both")

root.geometry("800x600")

root.bind("<Control-Key-s>", callback)

#print(dir())

root.mainloop()
