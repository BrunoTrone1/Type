import requests
import random
import time
from tkinter import *
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

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
    cronometro()

def update(status):
    global start_time
    end_time = time.time()
    elapsed_time = round(end_time - start_time, 2)

    if status == -1:
        end_game()
    elif status == 0:
        combo_result()
    else:
        combo.set(0) 

    update_labels(elapsed_time)
    next_word()

def combo_result():
    if combo.get() > 20:
            comboResultLabel.config(text="¡Combo Dios!", foreground="magenta")
    elif combo.get() > 15:
        comboResultLabel.config(text="¡Ultra Combo!", foreground="pink")
    elif combo.get() > 10:
        comboResultLabel.config(text="¡Mega Combo!", foreground="orange")
    elif combo.get() > 5:
        comboResultLabel.config(text="¡Super Combo!", foreground="yellow")
    elif combo.get() > 0:
        comboResultLabel.config(text="¡Combo!", foreground="green")
    else:
        comboResultLabel.config(text="Combo", foreground="green")
    combo.set(combo.get() + 1)

def update_labels(elapsed_time):
    if combo.get() > 0:
        resultLabel.config(
            text=f"Correcto!\nTiempo: {elapsed_time} segundos.", 
            foreground="lightgreen",    
            anchor="center",   
            justify="center"
        )  
        puntaje.set(puntaje.get() + 10 + combo.get() * 2)
    else:
        resultLabel.config(
            text=f"Incorrecto!\nTiempo: {elapsed_time} segundos.", 
            foreground="red",
            anchor="center",
            justify="center"
            )
        puntaje.set(puntaje.get() - 25)

    puntajeLabel.config(text=f"Puntaje: {puntaje.get()}")
    comboLabel.config(text=f"Combo: {combo.get()}")

def cronometro():
    global start_time
    tiempo = time.time() - start_time
    cronometroLabel.config(text=f"Tiempo: {round(tiempo, 1)} segundos")
    if userEntry.get() != "ñ":
        tkWindow.after(100, cronometro)
    if tiempo >= 10:
        end_game()

def end_game():
    wordLabel.config(state="disabled", foreground="white")
    userEntry.config(state="disabled", foreground="white")
    userEntry.bind("<Return>", lambda e: None) 
    resultLabel.config(text="Juego terminado", foreground="blue")
    cronometroLabel.config(text="")
    puntajeLabel.config(text=f"Puntaje final: {puntaje.get()}")
    combo.set(0)  
    comboLabel.config(text=f"Combo final: {combo.get()}")
    userEntry.delete(0, END)

def toggle_fullscreen(event=None):
    global fullscreen_state
    fullscreen_state = not fullscreen_state
    tkWindow.attributes("-fullscreen", fullscreen_state)
    return "break"

def end_fullscreen(event=None):
    global fullscreen_state
    fullscreen_state = False
    tkWindow.attributes("-fullscreen", False)
    return "break"

# Obtener palabras
words_site =[("https://raw.githubusercontent.com/kkrypt0nn/wordlists/refs/heads/main/wordlists/languages/english.txt"), 
             ("https://raw.githubusercontent.com/kkrypt0nn/wordlists/refs/heads/main/wordlists/languages/spanish.txt"),
             ]
response = requests.get(words_site[0])
words = response.text.splitlines()

# Configuración de la ventana
tkWindow = ttk.Window(themename="vapor", title="Type")
tkWindow.attributes("-fullscreen", True)
tkWindow.title("Typing Game")
tkWindow.title('Python Typing Game')
tkWindow.bind("<F11>", toggle_fullscreen)
tkWindow.bind("<Escape>", end_fullscreen)

# Variables
puntaje = ttk.IntVar(value=0)
combo = ttk.IntVar(value=0)
current_word = ""
start_time = 0
fullscreen_state = True

# Etiquetas y entrada de texto
wordLabel = ttk.Label(tkWindow, text="", font=('Helvetica', 18))
wordLabel.pack(pady=10)

userEntry = ttk.Entry(tkWindow, font=('Helvetica', 18))
userEntry.pack(pady=10)
userEntry.bind("<Return>", word_generator)

resultLabel = ttk.Label(tkWindow, font=('Helvetica', 16))
resultLabel.pack(pady=10)

puntajeLabel = ttk.Label(tkWindow, font=('Helvetica', 14))
puntajeLabel.pack(pady=10)

comboLabel = ttk.Label(tkWindow, font=('Helvetica', 14))
comboLabel.pack(pady=10)

comboResultLabel = ttk.Label(tkWindow, font=('Helvetica', 14))
comboResultLabel.pack(pady=10)

cronometroLabel = ttk.Label(tkWindow, font=('Helvetica', 14))
cronometroLabel.pack(pady=10)

# Iniciar el juego
next_word()
tkWindow.mainloop()