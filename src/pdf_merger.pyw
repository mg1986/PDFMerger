# Author: Matthew Gray
# Copyright (C) 2017 Matthew Gray
# Last Modified: 03/25/2018
# pdf_merger.py - Merges all PDFs from a directory into one output PDF file.

import datetime
import filecmp
import glob
import os
import shutil
import threading
from tkinter import *
import tkFileDialog

from PyPDF2 import PdfFileMerger

# Starts new thread using input function as thread target
def start_thread(function):
    t = threading.Thread(target=function)
    t.start()

# Print message to PDFMerger application message box    
def print_to_textbox(message):
    message_box.insert(END, message + "\n")

# Clear PDFMerger application message box    
def clear_textbox():
    message_box.delete('1.0', END)

# Center popup box relative to root    
def center_popup(toplevel):
    root.update_idletasks()
    toplevel.update_idletasks()
    w = toplevel.winfo_width()
    h = toplevel.winfo_height()
    x = root.winfo_width()/2 + root.winfo_x()-132
    y = root.winfo_height()/2 + root.winfo_y()-55
    toplevel.geometry("%dx%d+%d+%d" % (w, h, x, y))
  
# About popup
def about_popup():
    
    separator = "-------------------------------------------------\n"
    title_message = " Title: PDFMerger\n"
    copyright_message = "Copyright (C) 2018 Matthew Gray\n"
    description_message = "Description: Merges all PDFs from a directory into one output PDF file."
    about_message = title_message + separator+ copyright_message + separator + description_message
    
    toplevel = Toplevel(padx=5, pady=5, takefocus=True)
    toplevel.wm_title("About")
    label = Label(toplevel, text=about_message)
    label.grid(row=0, column=2)
    center_popup(toplevel)
    toplevel.grab_set()

# Confirm PDF Merge popup
def confirm_popup():
    
    confirm_message = "Are you sure you want merge these PDFs?"
    
    toplevel = Toplevel(padx=5, pady=5, takefocus=True)
    toplevel.wm_title("Confirm Merge")
    label = Label(toplevel, text=confirm_message)
    label.grid(row=0, column=1)
    yes_button = Button(master=toplevel, text="Yes", command=lambda: confirm_sync(toplevel))
    yes_button.grid(row=2, column=1)
    no_button = Button(master=toplevel, text="No", command=toplevel.destroy)
    no_button.grid(row=3, column=1)
    center_popup(toplevel)
    toplevel.grab_set()

# Executes main when confirm PDF Merge button clicked
def confirm_sync(toplevel):
    toplevel.destroy()
    start_thread(main)
    
# Stores the path of a user selected directory to a variable
def browse_directory(pdf_directory_path):

    directory_path = tkFileDialog.askdirectory()
    pdf_directory_path.set(directory_path)
   
    if len(pdf_directory_path.get()) > 0 :
        pdf_directory_exists = os.path.exists(pdf_directory_path.get()) and os.path.isdir(pdf_directory_path.get())
        if pdf_directory_exists:
            pdf_merge_button.config(state=ACTIVE)

# Merges all pdf files from pdf_directory based on their natural sort order      
def pdf_merge(pdf_directory):

    os.chdir(pdf_directory)
    pdf_list = glob.glob("*.pdf")

    merger = PdfFileMerger()

    for pdf in natural_sort(pdf_list):
        print_to_textbox(pdf)
        merger.append(pdf)

    merger.write("merge.pdf")

# Naturally sorts strings
def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)

# Main method - Calls pdf_merge method     
def main():

    clear_textbox()

    pdf_directory = str(pdf_directory_path.get())

    start_time = datetime.datetime.now()
    print_to_textbox("PDF Merge start: " + str(start_time))
    print_to_textbox("------------------------------------------------------------")
    
    pdf_merge(pdf_directory)

    end_time = datetime.datetime.now()
    print_to_textbox("------------------------------------------------------------")
    print_to_textbox("PDF Merge took: " + str(end_time - start_time) + " to finish")

### Configure GUI
root = Tk()
root.title("PDF Merger")

# Add menu bar
menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="About", command=about_popup)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.destroy)
menubar.add_cascade(label="File", menu=filemenu)

# String variable used to hold pdf directory path
pdf_directory_path = StringVar()

# PDF Directory browse button
pdf_directory_button = Button(text="PDF Directory", command= lambda: browse_directory(pdf_directory_path))
pdf_directory_button.grid(row=0, column=3)

# PDF Directory path label
pdf_directory_label = Label(master=root, textvariable=pdf_directory_path)
pdf_directory_label.grid(row=1, column=3)

# PDF Merge button - Starts pdf merge process after confirm merge popup button confirmed
pdf_merge_button = Button(text="Merge PDFs", state=DISABLED, command=confirm_popup)
pdf_merge_button.grid(row=9, column=3)

# Displays messages to application user                 
message_box = Text(master=root)
message_box.grid(row=11, column=3)

# Set menubar object as root menu
root.config(menu=menubar)
root.update()

# Center root menu on application startup
root.update_idletasks()
w = root.winfo_reqwidth()
h = root.winfo_reqheight()
x = (root.winfo_screenwidth() - w) / 2
y = (root.winfo_screenheight() - h) / 2
root.geometry("%dx%d+%d+%d" % (w, h, x, y))

# Tkinter application main loop
mainloop()
