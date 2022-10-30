
from tkinter import filedialog
from tkinter import * 
import sqlite3
import tkinter as tk
from tkinter import ttk

connection = sqlite3.connect('notes.sqlite')

def createfiler():
    saver = filedialog.asksaveasfilename(initialdir="",filetypes=(("txt","*.txt"),))
    filename = saver
    file = open(filename, "w")
    file.write(textbox2.get(1.0,END))
    file.close()
  

def openfiler():
    file = filedialog.askopenfilename(initialdir="", filetypes = (("txt","*.txt"),)) 
    with open(file, "r") as data:
        textbox2.delete('1.0', END)
        textbox2.insert(END,data.read())

def sql():
    file = filedialog.askopenfilename(initialdir="",filetypes=(("txt","*.txt"),))
    with open(file, "r") as data:
        filename = file.split("/")
        newfile = filename[-1]
        sql = f"INSERT INTO notes (filename,notes) VALUES ('{newfile}','{data.read()}')"
        connection.execute(sql)
        connection.commit()

def butopen():
    filechosen = DBfiles.get()
    print(filechosen)
    sql = "SELECT * FROM notes"
    curser = connection.execute(sql)
    for row in curser:
       print(row)
       if row[0]==(filechosen):
            textbox2.delete('1.0', END)
            textbox2.insert(END,row[1])
    connection.commit()
    top.destroy()
        

def sqlopen():
    files2 = []
    sql = "SELECT * FROM notes"
    data = connection.execute(sql)
    for row in data:
        files2.append(row[0])
    global top
    top = Toplevel(root)
    top.title("SQL Files")
    top.geometry("1000x240")
    label1 = Label(top, text = "Please Select The Note You Would Like To Open")
    n = tk.StringVar()
    global DBfiles
    DBfiles = ttk.Combobox(top, width = 27, textvariable = n)
    DBfiles['values'] = files2
    button1 = Button(top,text = "Open", command = butopen)
    label1.pack()
    button1.pack()
    DBfiles.pack()
    DBfiles.current()

root = Tk()

root.title("Note Taker")

root.geometry("640x360")

mainmenu = Menu(root)
root.config(menu = mainmenu)
submenu = Menu(mainmenu)

mainmenu.add_cascade(label = "file", menu = submenu)
submenu.add_command(label ="open file", command = openfiler)
submenu.add_separator()
submenu.add_command(label = "create file", command = createfiler)
submenu.add_separator()
submenu.add_command(label = "back up file to DB", command = sql)
submenu.add_separator()
submenu.add_command(label = "Open file from DB", command = sqlopen)


textbox2 = Text(root,width=100,height=100)
textbox2.pack()

root.mainloop()
