import requests
import random
from tkinter import *
from functools import partial

#functions
def word_generator(event=None):
    user_word = userEntry.get()

    if user_word == "ñ":
        wordLabel.config(state="disabled", fg="white")
        userEntry.config(state="disabled", fg="white")
        resultLabel.config(text="Juego terminado", fg="blue")
        userEntry.delete(0, END)
        return

    if user_word == current_word:
        puntaje.set(puntaje.get() + 10)
        update()       

    else: 
        resultLabel.config(text="Incorrecto. La palabra era: " + current_word, fg="red")
        puntaje.set(puntaje.get() - 5)
        update()
        
def next_word():
    global current_word
    current_word = random.choice(words)
    wordLabel.config(text=current_word)
    userEntry.delete(0, END)

def update():
    puntajeLabel.config(text=f"Puntaje: {puntaje.get()}", fg="red")
    wordLabel.config(state="normal", fg="black")
    resultLabel.config(text="")
    userEntry.delete(0, END)
    next_word()

#words
words_site = "https://www.mit.edu/~ecprice/wordlist.10000"
response = requests.get(words_site)
words = response.text.splitlines()

#window
tkWindow = Tk()  
tkWindow.geometry('400x200')  
tkWindow.title('Python Typing Game')

#variables
puntaje = IntVar()
puntaje.set(0)
current_word = ""

#label
wordLabel = Label(tkWindow, text="", font= ('Helvetica', 18))
wordLabel.pack(pady=10)

userEntry = Entry(tkWindow, font= ('Helvetica', 18))
userEntry.pack(pady=10)
userEntry.bind("<Return>", word_generator)

resultLabel = Label(tkWindow, font= ('Helvetica', 14))
resultLabel.pack(pady=10)

puntajeLabel = Label(tkWindow, font= ('Helvetica', 14))
puntajeLabel.pack(pady=10)

#start
next_word()

#main loop
tkWindow.mainloop()

