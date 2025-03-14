import requests
import random
import time
from tkinter import *
from functools import partial

#functions
def word_generator(event=None, combo=None):
    global start_time
    user_word = userEntry.get()

    if user_word == "ñ":
        update(-1)  

    if user_word == current_word:
        update(0)       

    else: 
        update(1)
        
def next_word():
    global current_word, start_time
    current_word = random.choice(words)
    wordLabel.config(text=current_word)
    userEntry.delete(0, END)
    start_time = time.time()

def update(int):
    global start_time
    if int == -1:
        wordLabel.config(state="disabled", fg="white")
        userEntry.config(state="disabled", fg="white")
        resultLabel.config(text="Juego terminado", fg="blue")
        userEntry.delete(0, END)
        return

    if int == 0:
        end_time = time.time()
        elapsed_time = round(end_time - start_time, 2)
        combo.set(combo.get() + 1)
        comboLabel.config(text=f"Combo: {combo.get()}", fg="green")
        resultLabel.config(text="Correcto.\n Tiempo: " + str(elapsed_time) + " segundos.", fg="green")
        puntaje.set(puntaje.get() + 10 +  combo.get() * 2)
        puntajeLabel.config(text=f"Puntaje: {puntaje.get()}", fg="green")
        wordLabel.config(state="normal", fg="black")
        userEntry.delete(0, END)

    if int == 1:
        end_time = time.time()
        elapsed_time = round(end_time - start_time, 2)
        resultLabel.config(text="Incorrecto.\n Tiempo: " + str(elapsed_time) + " segundos.", fg="red")
        puntaje.set(puntaje.get() - 5)
        puntajeLabel.config(text=f"Puntaje: {puntaje.get()}", fg="red")
        wordLabel.config(state="normal", fg="black")
        combo.set(0)
        comboLabel.config(text=f"Combo: {combo.get()}", fg="red")
        userEntry.delete(0, END)

    next_word()

#words
words_site = "https://www.mit.edu/~ecprice/wordlist.10000"
response = requests.get(words_site)
words = response.text.splitlines()

#window
tkWindow = Tk()  
tkWindow.geometry('400x300')  
tkWindow.title('Python Typing Game')

#variables
puntaje = IntVar()
puntaje.set(0)
current_word = ""
combo = IntVar()
combo.set(0)
start_time = 0

#label
wordLabel = Label(tkWindow, text="", font= ('Helvetica', 18))
wordLabel.pack(pady=10)

userEntry = Entry(tkWindow, font= ('Helvetica', 18))
userEntry.pack(pady=10)
userEntry.bind("<Return>", word_generator, combo)

resultLabel = Label(tkWindow, font= ('Helvetica', 14))
resultLabel.pack(pady=10)

puntajeLabel = Label(tkWindow, font= ('Helvetica', 14))
puntajeLabel.pack(pady=10)

comboLabel = Label(tkWindow, font= ('Helvetica', 14))
comboLabel.pack(pady=10)

#start
next_word()

#main loop
tkWindow.mainloop()

