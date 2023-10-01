from doctest import master
import os
import pickle
import webbrowser
import shutil
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from pathlib import Path

class CleoManager:
    def __init__(self, root):
        self.root = tk.Tk()
        self.cleo_state = tk.IntVar()
        self.master = root
        self.listbox = tk.Listbox(self.root)
        self.listbox1 = tk.Listbox(self.root)
        self.btn = tk.Button(self.root, text="launch", command=self.do_action)
        self.btncs = tk.Button(self.root, text="Add .cs", command=lambda: self.addfile("cs"))
        self.btnfxt = tk.Button(self.root, text="Add .fxt", command=lambda: self.addfile("fxt"))
        self.btndelete = tk.Button(self.root, text="Delete Item", command=self.delete_item)
        self.openfolderbtn = tk.Button(self.root, text="Game folder", command=self.openfoldermod)
        self.aboutbtn = tk.Button(self.root, text="About", command=self.about)
        if os.path.isdir("cleo"):
            print("cleo folder founded.")
        else:
            Path("cleo").mkdir(exist_ok=True)
            Path("cleo/cleo_text").mkdir(exist_ok=True)
            messagebox.showinfo("Cleo", "The cleo folder is missing, they will be created.")

    def run(self):
        # setting up the main window
        self.root.geometry('625x440')
        self.root.title('CLEO Manager')
        self.root.resizable(False, False)

        # placing buttons and listboxes
        cleo_on = tk.Radiobutton(self.root, text="Cleo On", variable=self.cleo_state, value=1)
        cleo_off = tk.Radiobutton(self.root, text="Cleo Off", variable=self.cleo_state, value=0)
        cleo_on.place(x=50, y=412)
        cleo_off.place(x=120, y=412)
        self.btn.place(x=2, y=410)
        self.btncs.place(x=230, y=410)
        self.btnfxt.place(x=350, y=410)
        self.btndelete.place(x=280, y=410)
        self.aboutbtn.place(x=500, y=410)
        self.openfolderbtn.place(x=545, y=410)
        self.listbox.place(x=0, y=0)
        self.listbox.config(width=52, height=25)
        self.listbox1.place(x=310, y=0)
        self.listbox1.config(width=52, height=25)

        # running the main loop
        self.root.mainloop()

        # functions
# =======================================================================================================================================
    def list_cleo_files(self):
        cleo_files = []
        for filename in os.listdir("cleo"):
            if filename.endswith(".cs"):
                cleo_files.append(filename)
        return cleo_files

    def list_fxt_files(self):
        fxt_files = []
        for filename in os.listdir("cleo/cleo_text"):
            if filename.endswith(".fxt"):
                fxt_files.append(filename)
        return fxt_files
    
    def check_cleo(self): 
        if os.path.isfile("cleo.asi"):
             self.cleo_state.set(1)
        else:
            if os.path.isfile("disabledcleo"):
                print("cleo disabled")
            else:
                messagebox.showinfo("Cleo Missing", "The Cleo plugin is not detected in your game. Perhaps it is not installed?")
            self.cleo_state.set(0)
            return
        
    # about window
    def about(self):
        aboutwind = tk.Toplevel()
        aboutwind.title("About")
        aboutwind.geometry('220x140')
        aboutwind.resizable(False, False)

        label1 = tk.Label(aboutwind, text="GTA SA Cleo Manager")
        label1.place(x=45, y=20)

        label2 = tk.Label(aboutwind, text="by deepmeanx")
        label2.place(x=65, y=40)

        label3 = tk.Label(aboutwind, text="check my github:")
        label3.place(x=60, y=60)

        website = tk.Label(aboutwind, text="github.com/deepmeanx", fg="blue", cursor="hand2")
        website.place(x=45, y=80)

        def exittop():
            aboutwind.destroy()

        btnexitnya = tk.Button(aboutwind, text="I'm just learning python, don't judge strictly", command=exittop)
        btnexitnya.place(x=0, y=105)

        def callback(event):
            webbrowser.open_new("https://github.com/deepmeanx")

        website.bind("<Button-1>", callback)
        aboutwind.mainloop()

    def launchgame(self):
        os.popen("gta_sa.exe")
        return

    def on_cleo(self):
        if os.path.exists("disabledcleo"):
            os.rename("disabledcleo", "cleo.asi")
            print("KRNL:Cleo enabled.")
        else:
            print("KRNL:Cleo is already enabled.")

    def off_cleo(self):
        if os.path.exists("cleo.asi"):
            os.rename("cleo.asi", "disabledcleo")
            print("KRNL:Cleo disabled.")
        else:
            print("KRNL:Cleo is already disabled.")

    def do_action(self):
        if self.cleo_state.get() == 1:
            self.on_cleo()
            self.launchgame()
        else:
            self.off_cleo()
            self.launchgame()

    def delete_item(self):
        selection = self.listbox.curselection()
        for i in reversed(selection):
            file_path = "cleo/" + self.listbox.get(i)
            print(file_path)
            os.remove(file_path)
            self.listbox.delete(i)
        selection = self.listbox1.curselection()
        for s in reversed(selection):
            file_path = "cleo/cleo_text/" + self.listbox1.get(s)
            os.remove(file_path)
            self.listbox1.delete(s)

    def update_listbox_cleo(self):
        cleo_files = []
        fxt_files = []
        self.listbox.delete(0, END)
        self.listbox1.delete(0, END)
        for filename in os.listdir("cleo"):
            if filename.endswith(".cs"):
                cleo_files.append(filename)
        for filename in os.listdir("cleo/cleo_text"):
            if filename.endswith(".fxt"):
                fxt_files.append(filename)
        self.listbox.insert(END, *cleo_files)
        self.listbox1.insert(END, *fxt_files)
        return cleo_files

    def addfile(self, file_type):
        filename = filedialog.askopenfilename(initialdir="/", title=f"Select .{file_type} file", filetypes=((f"{file_type.upper()} files", f"*.{file_type}"), ("All files", "*.*")))
        if filename:
            if file_type == "cs":
                shutil.copy(filename, "./cleo")
            elif file_type == "fxt":
                shutil.copy(filename, "./cleo/cleo_text")
            self.update_listbox_cleo()
        else:
            print("file not selected.")

    def openfoldermod(self):
        os.startfile(os.getcwd())
        return
    # =======================================================================================================================================

if __name__ == "__main__":
    cleo_manager = CleoManager(master)
    cleo_manager.check_cleo()
    cleo_manager.update_listbox_cleo()
    cleo_manager.run()