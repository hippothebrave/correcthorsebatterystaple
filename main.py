import random
from tkinter import *
from tkinter import ttk
import pyperclip

# GLOBAL VARIABLES
words = []
wordframes = []
cur_col = 0
cur_row = 1
with open('google-10000-english-usa-no-swears.txt', 'r') as words_file:
    for word in words_file:
        words.append(word.strip())

# FUNCTIONS
def return_word():
    """Select a random word and return it."""
    return words[random.randint(0, len(words))]

# FIXME - there's a visible flash as items are re-added to the grid
def regrid(*args):
    """Add all wordframes back into the grid to account for deletions"""
    global cur_row
    global cur_col
    cur_col, cur_row = 0, 1
    for i in range(len(wordframes)):
        wordframes[i].grid(row=cur_row,column=cur_col)
        if(cur_col == 3):
            cur_row += 1
        cur_col = (cur_col+1) % 4

def add_wordframe(*args):
    """Add a wordframe - a frame with a word and a refresh and delete button"""
    # declare that I'm using global vars
    global cur_row
    global cur_col

    # create the frame, add it to grid, update cur_col and cur_row
    wf = ttk.Frame(content, padding=(5), borderwidth=2, relief='solid', width=150, height=75)
    wordframes.append(wf)
    wf.grid(column=cur_col,row=cur_row,pady=5)
    if(cur_col == 3):
        cur_row += 1
    cur_col = (cur_col+1) % 4
    # wf.grid_propagate(False)
    wf.columnconfigure(0,weight=3,minsize=75)
    wf.columnconfigure(1,weight=1,minsize=75)
    wf.rowconfigure(0,weight=1)
    wf.rowconfigure(1,weight=1)

    # word label
    wf_word_text = StringVar()
    wf_word_text.set(return_word())
    wf_word = ttk.Label(wf, textvariable=wf_word_text, wraplength=75)
    wf_word.grid(column=0,row=0,rowspan=2,sticky=(W))

    # refresh button
    wf_refresh = ttk.Button(wf, text="Refresh", command=lambda : wf_word_text.set(return_word()))
    wf_refresh.grid(column=1,row=0,sticky=(E))

    # delete button
    wf_delete = ttk.Button(wf, text="Delete", command=lambda: del_wordframe(wf))
    wf_delete.grid(column=1,row=1,sticky=(E))

"""
# FIXME
def resize_wordframes(*args):
    if (root.winfo_width() / 5) > 150:
        for wf in wordframes:
            wf.configure(width=(root.winfo_width() / 5))
    else:
        for wf in wordframes:
            wf.configure(width=150)
"""

def del_wordframe(wordframe):
    wordframe.grid_forget()
    wordframes.remove(wordframe)
    regrid()
    wordframe.destroy()

def copy_passcode():
    passcode = []
    for wf in wordframes:
        for label in wf.grid_slaves(0,0):
            passcode.append(label['text'])
    print("".join(passcode))
    pyperclip.copy("".join(passcode))
    copy_label_contents.set("Copied!")
    copy_label.after(2000, clear_text)

def clear_text():
    copy_label_contents.set("")

# INTERFACE
    # window
root = Tk()
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
root.title("Correct Horse Battery Staple - Password Generator")
icon = PhotoImage(file='comic_snapshot_2.png')
root.iconphoto(True,icon)

    # frame
content = ttk.Frame(root,padding=(5,10), borderwidth=3,relief="groove")
content.grid(column=0, row=0, sticky=(N,E,S,W))
content.grid_columnconfigure(0, weight=1, minsize=200)
content.grid_columnconfigure(1, weight=1, minsize=200)
content.grid_columnconfigure(2, weight=1, minsize=200)
content.grid_columnconfigure(3, weight=1, minsize=200)
content.grid_rowconfigure(0, weight=1, minsize=10)
content.grid_rowconfigure(1, weight=1)

    # title
title_img = ttk.Label(content, image=icon)
title_img.grid(column=1,row=0,sticky=(E))
title_text = ttk.Label(content, text="Correct Horse Battery Staple",
                  anchor='n',font=('TkHeadingFont',20))
title_text.grid(column=2,row=0,columnspan=2,sticky=(E,W))

    # "copied" text
copy_label_contents = StringVar()
copy_label = ttk.Label(content, textvariable=copy_label_contents)
copy_label_contents.set("")
copy_label.grid(column=4,row=99,sticky=(W))

    # "add wordframe" button
add_btn = ttk.Button(content, text="+", command=add_wordframe)
add_btn.grid(column=4,row=100,sticky=(W))

    # "copy" button
copy_btn = ttk.Button(content, text="copy", command=copy_passcode)
copy_btn.grid(column=4,row=101,sticky=(W))


# EVENT LOOP
root.mainloop()
