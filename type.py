import requests
import random
import time
from tkinter import *
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap import Progressbar

class Type(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=10)
        self.pack(fill=BOTH, expand=True)

        # Estado
        self.puntaje = ttk.IntVar(value=0)
        self.combo = ttk.IntVar(value=0)
        self.palabra_actual = ""
        self.tiempo_total = 5  # Tiempo total del cronómetro en segundos
        self.tiempo_inicio = 0
        self.pantalla_completa = False

        # Palabras
        self.palabras = self.obtener_palabras()
        

        # Interfaz
        self.crear_widgets()

        # Teclado
        self.bind("<F11>", self.cambiar_pantalla_completa)
        self.bind("<Escape>", self.salir_pantalla_completa)

    def obtener_palabras(self):
        fuente = [
            "https://raw.githubusercontent.com/kkrypt0nn/wordlists/refs/heads/main/wordlists/languages/english.txt",
            "https://raw.githubusercontent.com/kkrypt0nn/wordlists/refs/heads/main/wordlists/languages/spanish.txt"
        ]
        # Elegir una fuente aleatoria
        fuente = fuente[random.randint(0, len(fuente) - 1)]
        # Obtener palabras de la fuente
        respuesta = requests.get(fuente)
        return respuesta.text.splitlines()

    def crear_widgets(self):
        self.wordLabel = ttk.Label(self, font=('Helvetica', 18))
        self.wordLabel.pack(pady=10)

        self.userEntry = ttk.Entry(self, font=('Helvetica', 18))
        self.userEntry.pack(pady=10)
        self.userEntry.bind("<Return>", self.generador_palabra)

        self.resultLabel = ttk.Label(self, font=('Helvetica', 16))
        self.resultLabel.pack(pady=10)

        self.puntajeLabel = ttk.Label(self, font=('Helvetica', 14))
        self.puntajeLabel.pack(pady=10)

        self.comboLabel = ttk.Label(self, font=('Helvetica', 14))
        self.comboLabel.pack(pady=10)

        self.comboResultLabel = ttk.Label(self, font=('Helvetica', 14))
        self.comboResultLabel.pack(pady=10)

        self.cronometroLabel = ttk.Label(self, font=('Helvetica', 14))
        self.cronometroLabel.pack(pady=10)

        self.reiniciarButton = ttk.Button(self, text="Reiniciar", command=self.reiniciar, bootstyle="success", state=DISABLED)
        self.reiniciarButton.pack(pady=5)

        self.salirButton = ttk.Button(self, text="Salir", command=self.master.destroy, bootstyle="danger")
        self.salirButton.pack(pady=5) 

        self.progressbar = Progressbar(self, bootstyle="danger", maximum=self.tiempo_total)
        self.progressbar.pack(pady=10)

    def reiniciar(self):
        self.puntaje.set(0)
        self.combo.set(0)
        self.resultLabel.config(text="")
        self.wordLabel.config(text="")
        self.userEntry.config(state=NORMAL)
        self.userEntry.bind("<Return>", self.generador_palabra)
        self.userEntry.delete(0, END)
        self.siguiente_palabra
        self.userEntry.focus()

    def generador_palabra(self, event=None):
        palabra_usuario = self.userEntry.get()
        if palabra_usuario == self.palabra_actual and self.palabra_actual != "":
            self.actualizar(0)
        else:
            self.actualizar(1)
        

    def siguiente_palabra(self):
        self.palabra_actual = random.choice(self.palabras)
        self.wordLabel.config(text=self.palabra_actual)
        self.userEntry.config(state=NORMAL)
        self.userEntry.bind("<Return>", self.generador_palabra)
        self.userEntry.delete(0, END)
        self.userEntry.focus()
        self.tiempo_inicio = time.time()
        self.cronometro()

    def actualizar(self, estado):
        tiempo_transcurrido = time.time() - self.tiempo_inicio
        if estado == 0:
            self.resultado_combo()
        else:
            self.combo.set(0)
        
        self.actualizar_labels(tiempo_transcurrido)
        self.siguiente_palabra()

    def resultado_combo(self):
        if self.combo.get() > 100:
            txt, color = "¡Combo Legendario!", "gold"
        elif self.combo.get() > 75:
            txt, color = "¡Combo Mítico!", "crimson"
        elif self.combo.get() > 50:
            txt, color = "¡Combo Supremo!", "purple"
        elif self.combo.get() > 35:
            txt, color = "¡Combo Bestial!", "darkorange"
        elif self.combo.get() > 25:
            txt, color = "¡Combo Brutal!", "orangered"
        elif self.combo.get() > 15:
            txt, color = "¡Combo Imparable!", "deeppink"
        elif self.combo.get() > 10:
            txt, color = "¡Combo Furioso!", "tomato"
        elif self.combo.get() > 5:
            txt, color = "¡Combo Fuerte!", "yellow"
        elif self.combo.get() > 0:
            txt, color = "¡Combo!", "limegreen"
        else:
            txt, color = "Combo", "gray"
        
        self.comboResultLabel.config(text=txt, foreground=color)
        self.combo.set(self.combo.get() + 1)

    def actualizar_labels(self, tiempo_transcurrido):
        if self.userEntry.get() == self.palabra_actual and self.palabra_actual != "":
            msg, color  = f"Correcto!\nTiempo: {round(tiempo_transcurrido, 1)} segundos.", "lightgreen"
            self.puntaje.set(self.puntaje.get() + 10*self.combo.get())
        elif self.userEntry.get() == "":
            msg, color = "Escribe la palabra", "blue"
        else:
            msg, color = f"Incorrecto!\nTiempo: {round(tiempo_transcurrido, 1)} segundos.", "red"
            self.puntaje.set(self.puntaje.get() - 100)

        self.resultLabel.config(text=msg, foreground=color, anchor="center", justify="center")
        self.puntajeLabel.config(text=f"Puntaje: {self.puntaje.get()}")
        self.comboLabel.config(text=f"Combo: {self.combo.get()}")

    def cronometro(self):
        tiempo_transcurrido = time.time() - self.tiempo_inicio
        tiempo_restante = max(0, self.tiempo_total - tiempo_transcurrido)

        # Actualizar la barra de progreso
        self.progressbar["value"] = tiempo_restante

        # Actualizar la etiqueta del cronómetro
        self.cronometroLabel.config(text=f"Tiempo: {round(tiempo_restante, 1)} segundos.")

        if tiempo_restante > 0:
            self.after(100, self.cronometro)
        else:
            self.final()

    def final(self):
        self.wordLabel.config(state=DISABLED, foreground="white")
        self.userEntry.config(state=DISABLED, foreground="white")
        self.userEntry.bind("<Return>", lambda e: None)
        self.resultLabel.config(text="Juego terminado", foreground="blue")
        self.cronometroLabel.config(text="")
        self.puntajeLabel.config(text=f"Puntaje final: {self.puntaje.get()}")
        self.comboLabel.config(text=f"Combo final: {self.combo.get()}")
        self.userEntry.delete(0, END)
        self.reiniciarButton.config(state=NORMAL)
        self.reiniciarButton.bind("<Return>", self.reiniciar)

    def cambiar_pantalla_completa(self, event=None):
        self.fullscreen = not self.fullscreen
        self.master.attributes("-fullscreen", self.fullscreen)
        return "break"

    def salir_pantalla_completa(self, event=None):
        self.fullscreen = False
        self.master.attributes("-fullscreen", False)
        return "break"
    
if __name__ == "__main__":
    app = ttk.Window(title="Typing Game", themename="darkly")
    app.geometry("1920x1080")  # Ajusta el tamaño de la ventana a 1920x1080 píxeles
    Type(app)
    app.mainloop()
    
