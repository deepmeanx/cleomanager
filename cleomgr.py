import os
import pickle
import webbrowser
import shutil
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from pathlib import Path

root = tk.Tk()
cleo_state = IntVar()
if os.path.isdir("cleo"):
    print("cleo folder founded.")
else:
    Path("cleo").mkdir(exist_ok=True)
    Path("cleo/cleo_text").mkdir(exist_ok=True)
    messagebox.showinfo("Cleo", "The cleo folder is missing, they will be created.")

# functions
# =======================================================================================================================================

def check_cleo():
    if os.path.isfile("cleo.asi"):
        cleo_state.set(1)
    else:
        if os.path.isfile("disabledcleo"):
            print("cleo disabled")
        else:
            messagebox.showinfo("Cleo Missing", "The Cleo plugin is not detected in your game. Perhaps it is not installed?")
        cleo_state.set(0)    

def list_cleo_files():
    cleo_files = []
    for filename in os.listdir("cleo"):
        if filename.endswith(".cs"):
            cleo_files.append(filename)
    return cleo_files

def list_fxt_files():
    fxt_files = []
    for filename in os.listdir("cleo/cleo_text"):
        if filename.endswith(".fxt"):
            fxt_files.append(filename)
    return fxt_files

# about window
def about():
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

def launchgame():
    os.popen("gta_sa.exe")
    return

def on_cleo():
    if os.path.exists("disabledcleo"): 
        os.rename("disabledcleo", "cleo.asi") 
        print("KRNL:Cleo enabled.")
    else:
        print("KRNL:Cleo is already enabled.")

def off_cleo():
    if os.path.exists("cleo.asi"): 
        os.rename("cleo.asi", "disabledcleo") 
        print("KRNL:Cleo disabled.")
    else:
        print("KRNL:Cleo is already disabled.")

def do_action():
    if cleo_state.get() == 1:
        on_cleo()
        launchgame()
    else:
        off_cleo()
        launchgame()

def delete_item():
    selection = listbox.curselection()
    for i in reversed(selection):
        file_path = "cleo/" + listbox.get(i)
        print(file_path)
        os.remove(file_path)
        listbox.delete(i)
    selection = listbox1.curselection()
    for s in reversed(selection):
        file_path = "cleo/cleo_text/" + listbox1.get(s)
        os.remove(file_path)
        listbox1.delete(s)

def update_listbox_cleo():
    cleo_files = []
    fxt_files = []
    listbox.delete(0, END)
    listbox1.delete(0, END)  # fix typo
    for filename in os.listdir("cleo"):
        if filename.endswith(".cs"):
            cleo_files.append(filename)
    for filename in os.listdir("cleo/cleo_text"):
        if filename.endswith(".fxt"):
            fxt_files.append(filename)
    listbox.insert(END, *cleo_files)
    listbox1.insert(END, *fxt_files)
    return cleo_files

def addfile(file_type):
    filename = filedialog.askopenfilename(initialdir="/", title=f"Select .{file_type} file", filetypes=((f"{file_type.upper()} files", f"*.{file_type}"), ("All files", "*.*")))
    if filename:
        if file_type == "cs":
            shutil.copy(filename, "./cleo")
        elif file_type == "fxt":
            shutil.copy(filename, "./cleo/cleo_text")
        update_listbox_cleo()
    else:
        print("file not selected.")

def openfoldermod():
    os.startfile(os.getcwd())
    return
# =======================================================================================================================================

# buttons and listboxes
cleo_on = Radiobutton(root, text="Cleo On", variable=cleo_state, value=1)
cleo_off = Radiobutton(root, text="Cleo Off", variable=cleo_state, value=0)
btn = tk.Button(root, text="launch", command=do_action)
btn1 = tk.Button(root, text="")
btncs = tk.Button(root, text="Add .cs", command=lambda:addfile("cs"))
btnfxt = tk.Button(root, text="Add .fxt", command=lambda:addfile("fxt"))
btndelete = tk.Button(root, text="Delete Item", command=delete_item)
openfolderbtn = tk.Button(root, text="Game folder", command=openfoldermod)
aboutbtn = tk.Button(root, text="About", command=about)
listbox = tk.Listbox(root)
for file in list_cleo_files():
    listbox.insert(tk.END, file)
listbox1 = tk.Listbox(root)
for file in list_fxt_files():
    listbox1.insert(tk.END, file)

# button place
cleo_on.place(x=50, y=412)
cleo_off.place(x=120, y=412)
btn.place(x=2, y=410)
btncs.place(x=230, y=410)
btnfxt.place(x=350, y=410)
btndelete.place(x=280, y=410)
aboutbtn.place(x=500, y=410)
openfolderbtn.place(x=545, y=410)
listbox.place(x=0, y=0)
listbox.config(width=52, height=25)
listbox1.place(x=310, y=0)
listbox1.config(width=52, height=25)

# main window
root.geometry('625x440');
root.title('CLEO Manager');
root.resizable(False, False);
root.mainloop()