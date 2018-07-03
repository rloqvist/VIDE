from tkinter import filedialog, Tk, Frame, Text, DISABLED
from vide.gui import Editor
import os
import var

class MainWindow(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.filename = ''
        self.saved = True
        self.title('Vide %s' % self.filename)

        self.last_text_length = None
        self.geometry("800x600")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.editFrame = Frame(self)
        self.editFrame.grid(row=0, column=0, sticky="NWSE")

        self.editor = Editor(self.editFrame)
        self.editor.pack(expand=True, fill="both")

        self.bind("<Control-Key-s>", self.save_file)
        self.bind("<Control-Key-o>", self.open_file)
        self.bind("<F5>", self.run_file)

    def save_file(self, event):
        self.title('Vide %s' % self.filename)
        text = self.editor.text.get("1.0", "end")[:-1]
        if not self.filename:
            self.filename = filedialog.asksaveasfilename(initialdir=".", title="Select file", filetypes=(("All files","*.*"),("VAR files","*.vr")))
        with open(self.filename, 'w') as handle:
            handle.write(text)

    def open_file(self, event):
        self.filename = filedialog.askopenfilename(initialdir=".", title="Select file", filetypes=(("All files","*.*"),("VAR files","*.vr")))
        self.title('Vide %s' % self.filename)
        with open(self.filename, 'r') as handle:
            text = handle.read()
        self.editor.set_text(text)
        self.editor.text.focus()

    def run_file(self, event):
        if not self.saved:
            print("You must save first")
        if not self.filename:
            print("There is no filename specified")
        else:
            # redirect io for inline console
            cmd = "python3 var.py %s" % self.filename
            os.system(cmd)

    def check_edited(self):
        if self.last_text_length:
            text_length = len(self.editor.text.get("1.0", "end")[:-1])
            self.saved = text_length == self.last_text_length
            if not self.saved:
                self.last_text_length = text_length
                self.title('* Vide %s' % self.filename)
        else:
            self.last_text_length = len(self.editor.text.get("1.0", "end")[:-1])

if __name__ == "__main__":
    root = MainWindow()
    root.mainloop()
