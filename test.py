from tkinter import *
from functools import partial

def printDetails(usernameEntry) :
    usernameText = usernameEntry.get()
    print("user entered :", usernameText)
    return

#window
tkWindow = Tk()  
tkWindow.geometry('400x150')  
tkWindow.title('Python Examples')

#label
usernameLabel = Label(tkWindow, text="Enter your name")
#entry for user input
usernameEntry = Entry(tkWindow)

#define callable function with printDetails function and usernameEntry argument
printDetailsCallable = partial(printDetails, usernameEntry)

#submit button
submitButton = Button(tkWindow, text="Submit", command=printDetailsCallable)

#place label, entry, and button in grid
usernameLabel.grid(row=0, column=0)
usernameEntry.grid(row=0, column=1) 
submitButton .grid(row=1, column=1)  

#main loop
tkWindow.mainloop()