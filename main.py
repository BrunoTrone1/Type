import requests
import random
import time
from tkinter import *

def word_generator(event=None):
    global start_time
    user_word = userEntry.get()

    if user_word == "ñ":
        end_game()
    elif user_word == current_word:
        update(0)
    else:
        update(1)

def next_word():
    global current_word, start_time
    current_word = random.choice(words)
    wordLabel.config(text=current_word)
    userEntry.delete(0, END)
    start_time = time.time()

def update(status):
    global start_time
    end_time = time.time()
    elapsed_time = round(end_time - start_time, 2)

    if status == -1:
        end_game()
    elif status == 0:
        combo.set(combo.get() + 1)
        resultLabel.config(text=f"Correcto.\nTiempo: {elapsed_time} segundos.", fg="green")
        puntaje.set(puntaje.get() + 10 + combo.get() * 2)
    else:
        resultLabel.config(text=f"Incorrecto.\nTiempo: {elapsed_time} segundos.", fg="red")
        puntaje.set(puntaje.get() - 5)
        combo.set(0)

    update_labels()
    next_word()

def update_labels():
    puntajeLabel.config(text=f"Puntaje: {puntaje.get()}")
    comboLabel.config(text=f"Combo: {combo.get()}")

def end_game():
    wordLabel.config(state="disabled", fg="white")
    userEntry.config(state="disabled", fg="white")
    resultLabel.config(text="Juego terminado", fg="blue")
    userEntry.delete(0, END)

# Obtener palabras
words_site = "https://www.mit.edu/~ecprice/wordlist.10000"
response = requests.get(words_site)
words = response.text.splitlines()

# Configuración de la ventana
tkWindow = Tk()
tkWindow.geometry('400x300')
tkWindow.title('Python Typing Game')

# Variables
puntaje = IntVar(value=0)
combo = IntVar(value=0)
current_word = ""
start_time = 0

# Etiquetas y entrada de texto
wordLabel = Label(tkWindow, text="", font=('Helvetica', 18))
wordLabel.pack(pady=10)

userEntry = Entry(tkWindow, font=('Helvetica', 18))
userEntry.pack(pady=10)
userEntry.bind("<Return>", word_generator)

resultLabel = Label(tkWindow, font=('Helvetica', 14))
resultLabel.pack(pady=10)

puntajeLabel = Label(tkWindow, font=('Helvetica', 14))
puntajeLabel.pack(pady=10)

comboLabel = Label(tkWindow, font=('Helvetica', 14))
comboLabel.pack(pady=10)

# Iniciar el juego
next_word()
tkWindow.mainloop()