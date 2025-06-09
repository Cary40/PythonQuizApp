import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import pygame.mixer # Importamos el módulo de sonido de Pygame

# --- Colores Globales para consistencia ---
COLOR_FONDO_OSCURO = "#AAAAAA" # Gris muy oscuro para el fondo principal
COLOR_FONDO_MEDIO = "#c9c3c3"  # Un gris un poco más claro para otras secciones
COLOR_TEXTO_CLARO = "white"    # Para textos sobre fondos oscuros
COLOR_TEXTO_OSCURO = "black"   # Para textos sobre fondos claros
COLOR_ACCENT = "#00c3ff"       # Azul vibrante (ej. para botones)
COLOR_ACCENT_HOVER = "#0099cc" # Azul más oscuro para hover de botones
COLOR_EXITO = "#4CAF50"        # Verde para éxito
COLOR_ERROR = "#D32F2F"        # Rojo para error

# --- Función para reproducir sonido con Pygame ---
def reproducir_sonido(ruta_sonido):
    """
    Reproduce un archivo de sonido usando pygame.mixer.
    La reproducción es no bloqueante.
    Soporta formatos como .wav y .mp3.
    """
    ruta_completa = os.path.join("sonidos", ruta_sonido)
    if os.path.exists(ruta_completa):
        try:
            # Crea un objeto Sound y lo reproduce.
            # play() es no bloqueante, lo que significa que el programa continúa inmediatamente.
            sound_obj = pygame.mixer.Sound(ruta_completa)
            sound_obj.play()
        except pygame.error as e:
            print(f"❌ Error al reproducir sonido con Pygame: {e}")
            print(f"Asegúrate de que el archivo '{ruta_sonido}' existe y es compatible (wav, mp3).")
    else:
        print(f"⚠ Archivo de sonido no encontrado: {ruta_completa}")

# === Verificar si la imagen existe antes de cargarla ===
def cargar_imagen(ruta, tamaño=None):
    """
    Carga una imagen desde la carpeta 'imagenes' y la redimensiona si se especifica un tamaño.
    Retorna un PhotoImage o None si la imagen no se encuentra.
    """
    ruta_completa = os.path.join("imagenes", ruta)
    if os.path.exists(ruta_completa):
        try:
            imagen = Image.open(ruta_completa)
            if tamaño:
                # Usar Image.Resampling.LANCZOS para mejor calidad de redimensionamiento
                imagen = imagen.resize(tamaño, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(imagen)
        except Exception as e:
            print(f"❌ Error al cargar la imagen {ruta_completa}: {e}")
            return None
    else:
        print(f"⚠ Imagen no encontrada: {ruta_completa}")
        return None

# === Datos del cuestionario ===
preguntas = [
    ("¿Qué es Python?", ["Un lenguaje de programación interpretado y de alto nivel", "Un sistema operativo", "Un navegador web"], 0),
    ("¿Cómo se imprime texto en Python?", ["mostrar()", "echo", "print()"], 2),
    ("¿Qué es una tupla en Python?", ["Una colección ordenada e inmutable de elementos", "Una colección desordenada de elementos únicos", "Una colección ordenada y mutable de elementos"], 0),
    ("¿Cuál de las siguientes palabras clave se usa para definir una función en Python?", ["function", "def", "func"], 1),
    ("¿Qué tipo de dato representa números enteros en Python?", ["float", "str", "int"], 2)
]

# === Aplicación principal ===
class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("Autoevaluación Python")

        # Se inicializa el módulo de sonido de Pygame.
        try:
            pygame.mixer.init()
        except pygame.error as e:
            print(f"❌ Error al inicializar pygame.mixer: {e}")
            print("Es posible que necesites instalar librerías adicionales de audio en tu sistema (ej. para mp3).")
        # --- FIN INICIALIZACIÓN ---


        # Configurar la ventana para que ocupe toda la pantalla
        self.root.state('zoomed')
        self.root.update_idletasks() # Forzar actualización para obtener dimensiones correctas
        self.ancho_pantalla = self.root.winfo_width()
        self.alto_pantalla = self.root.winfo_height()

        self.puntaje = 0
        self.index = 0

        # --- Variables añadidas para el Efecto Máquina de Escribir ---
        self.texto_quiz_completo = "¿Cuánto sabes de Python?"
        self.texto_quiz_actual_index = 0
        self.titulo_python_id = None # Para almacenar el ID del texto en el canvas
        # --- Fin de variables para Efecto Máquina de Escribir ---

        # --- Variables para las animaciones de "Evalúa" y "TUS SABERES" ---
        self.evalua_id = None
        self.saberes_id = None
        # Necesitamos guardar las posiciones X iniciales para 'coords()'
        self.evalua_initial_x = 0
        self.saberes_initial_x = 0

        self.animacion_step = 0
        self.animacion_duracion = 20 # Número de frames para la animación
        self.font_size_evalua_inicio = 1 # Tamaño de fuente inicial (invisible)
        self.font_size_evalua_final = 48
        self.font_size_saberes_inicio = 1
        self.font_size_saberes_final = 60
        self.pos_y_evalua_final = 0.1
        self.pos_y_saberes_final = 0.18
        # --- Fin variables animación textos ---

        self.mostrar_presentacion()

    def limpiar(self):
        """Elimina todos los widgets de la ventana principal."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def mostrar_presentacion(self):
        """Muestra la pantalla de presentación del quiz."""
        self.limpiar()

        # Establecer el color de fondo de la ventana principal
        self.root.configure(bg=COLOR_FONDO_OSCURO)

        # Crear un Canvas que cubra toda la ventana para superponer elementos
        canvas = tk.Canvas(self.root, width=self.ancho_pantalla, height=self.alto_pantalla,
                           highlightthickness=0, bg=COLOR_FONDO_OSCURO)
        canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.canvas = canvas # Guardar referencia al canvas para usarla en el método de animación

        # Helper para convertir coordenadas relativas a absolutas para el canvas
        def rel_x(val): return int(val * self.ancho_pantalla)
        def rel_y(val): return int(val * self.alto_pantalla)

        # === Elementos de Texto (Inicialmente para animación) ===
        # "Evalúa" - Se crea con tamaño de fuente y posición inicial para animar
        self.evalua_initial_x = rel_x(0.10) # Guarda la posición X inicial
        self.evalua_id = canvas.create_text(self.evalua_initial_x, rel_y(0.0), text="Evalúa", # Empieza más arriba
                                           font=("Brush Script MT", self.font_size_evalua_inicio, "bold"),
                                           fill=COLOR_TEXTO_OSCURO, anchor="nw", angle=10)
        # "TUS SABERES" - Se crea con tamaño de fuente y posición inicial para animar
        self.saberes_initial_x = rel_x(0.10) # Guarda la posición X inicial
        self.saberes_id = canvas.create_text(self.saberes_initial_x, rel_y(0.08), text="TUS SABERES", # Empieza más arriba
                                            font=("Impact", self.font_size_saberes_inicio),
                                            fill=COLOR_TEXTO_OSCURO, anchor="nw", angle=10)


        # === Logo y Texto de Informatorio ===
        self.logo_photo = cargar_imagen("logo.jpg", (500, 350))
        if self.logo_photo:
            canvas.create_image(rel_x(0.48), rel_y(0.50), image=self.logo_photo, anchor="center")

        # === Imagen Grupal ===
        self.group_photo = cargar_imagen("foto_grupal.jpg", (350, 250))
        if self.group_photo:
            canvas.create_image(rel_x(0.8), rel_y(0.45), image=self.group_photo, anchor="center")

        # === EL TEXTO "¿CUÁNTO SABES DE PYTHON?" ===
        self.titulo_python_id = canvas.create_text(rel_x(0.48), rel_y(0.3), text="", # Inicialmente vacío
                                                   font=("Helvetica", 28, "bold"), fill=COLOR_TEXTO_OSCURO, anchor="center")

        # === Botón para iniciar el test ===
        btn_iniciar = tk.Button(self.root, text="INICIAR CUESTIONARIO",
                                font=("Arial", 22, "bold"), bg=COLOR_ACCENT, fg="white",
                                activebackground=COLOR_ACCENT_HOVER, activeforeground="white",
                                # --- CAMBIO AQUÍ: Llamamos al sonido ANTES de mostrar la primera pregunta ---
                                command=lambda: (reproducir_sonido("startup_sound.mp3"), self.mostrar_pregunta()),
                                relief="raised", bd=3)
        btn_iniciar.place(relx=0.5, rely=0.85, anchor="center", width=400, height=80)

        # --- Efecto Hover para el botón INICIAR CUESTIONARIO ---
        btn_iniciar.bind("<Enter>", self.on_enter_iniciar_btn)
        btn_iniciar.bind("<Leave>", self.on_leave_iniciar_btn)

        # === Footer ===
        footer_text = "Proyecto desarrollado por [Tu Nombre 1], [Tu Nombre 2] y [Nasif Carina]"
        footer_label = tk.Label(self.root,
                                text=footer_text,
                                font=("Arial", 12),
                                bg=COLOR_FONDO_MEDIO,
                                fg="#0d0c0c",
                                relief="flat",
                                anchor="center")
        footer_label.place(relx=0.0, rely=0.96, relwidth=1.0, height=30)

        self.root.update_idletasks() # Asegurarse de que todos los elementos se dibujen

        # --- Iniciar Animaciones de Títulos y Efecto Máquina de Escribir ---
        self.animacion_step = 0 # Reiniciar para la animación de "Evalúa" y "TUS SABERES"
        self.animar_evalua_saberes() # Iniciar la animación de los títulos
        # Después de la animación de los títulos, o con un ligero retraso, inicia el efecto de máquina de escribir
        self.root.after(800, self.iniciar_typewriter_effect) # Retraso para que la animación de "Evalúa" termine primero

    def iniciar_typewriter_effect(self):
        """Inicia el efecto de máquina de escribir para el título de Python."""
        self.texto_quiz_actual_index = 0 # Reiniciar el índice al mostrar la presentación
        self.escribir_titulo_python()

    # --- Métodos para el Efecto Máquina de Escribir ---
    def escribir_titulo_python(self):
        """Implementa el efecto de máquina de escribir para el título del quiz."""
        if self.texto_quiz_actual_index < len(self.texto_quiz_completo):
            texto_a_mostrar = self.texto_quiz_completo[:self.texto_quiz_actual_index + 1]
            self.canvas.itemconfig(self.titulo_python_id, text=texto_a_mostrar)
            # Reproducir sonido de clic de máquina de escribir
            reproducir_sonido("typewriter_click.mp3") 
            self.texto_quiz_actual_index += 1
            self.root.after(80, self.escribir_titulo_python) # Velocidad del tecleo
        else:
            pass

    # --- Nuevos métodos para animar "Evalúa" y "TUS SABERES" ---
    def animar_evalua_saberes(self):
        if self.animacion_step <= self.animacion_duracion:
            current_font_size_evalua = self.font_size_evalua_inicio + (
                self.font_size_evalua_final - self.font_size_evalua_inicio
            ) * (self.animacion_step / self.animacion_duracion)

            current_font_size_saberes = self.font_size_saberes_inicio + (
                self.font_size_saberes_final - self.font_size_saberes_inicio
            ) * (self.animacion_step / self.animacion_duracion)

            current_pos_y_evalua = (self.pos_y_evalua_final) * (self.animacion_step / self.animacion_duracion)
            current_pos_y_saberes = (self.pos_y_saberes_final) * (self.animacion_step / self.animacion_duracion)

            self.canvas.itemconfig(self.evalua_id,
                                   font=("Brush Script MT", int(current_font_size_evalua), "bold"))
            self.canvas.coords(self.evalua_id, self.evalua_initial_x, int(current_pos_y_evalua * self.alto_pantalla))

            self.canvas.itemconfig(self.saberes_id,
                                   font=("Impact", int(current_font_size_saberes)))
            self.canvas.coords(self.saberes_id, self.saberes_initial_x, int(current_pos_y_saberes * self.alto_pantalla))

            # Reproducir sonido al inicio de la animación de "Evalúa" y "TUS SABERES"
            if self.animacion_step == 0:
                reproducir_sonido("evalua_sound.mp3") 
            elif self.animacion_step == int(self.animacion_duracion / 2): # A mitad de la animación, para "TUS SABERES"
                reproducir_sonido("evalua_sound.mp3") # Usando el mismo sonido para "TUS SABERES"

            self.animacion_step += 1
            self.root.after(20, self.animar_evalua_saberes)
        else:
            # Ajuste final de fuente y posición
            self.canvas.itemconfig(self.evalua_id,
                                   font=("Brush Script MT", self.font_size_evalua_final, "bold"))
            self.canvas.coords(self.evalua_id, self.evalua_initial_x, int(self.pos_y_evalua_final * self.alto_pantalla))

            self.canvas.itemconfig(self.saberes_id,
                                   font=("Impact", self.font_size_saberes_final))
            self.canvas.coords(self.saberes_id, self.saberes_initial_x, int(self.pos_y_saberes_final * self.alto_pantalla))


    # --- Métodos para el Efecto Hover del botón ---
    def on_enter_iniciar_btn(self, event):
        """Cambia el color del botón cuando el mouse entra."""
        event.widget.config(bg=COLOR_EXITO, activebackground=COLOR_EXITO)

    def on_leave_iniciar_btn(self, event):
        """Restaura el color del botón cuando el mouse sale."""
        event.widget.config(bg=COLOR_ACCENT)

    def mostrar_pregunta(self):
        """
        Muestra la siguiente pregunta del quiz.
        El sonido startup_sound.mp3 YA NO se reproduce aquí.
        """

        if self.index >= len(preguntas):
            self.mostrar_resultado()
            return

        self.limpiar()
        self.root.configure(bg=COLOR_FONDO_MEDIO)

        canvas_pregunta = tk.Canvas(self.root, width=self.ancho_pantalla, height=self.alto_pantalla,
                                   highlightthickness=0, bg=COLOR_FONDO_MEDIO)
        canvas_pregunta.place(relx=0, rely=0, relwidth=1, relheight=1)

        def rel_x_q(val): return int(val * self.ancho_pantalla)
        def rel_y_q(val): return int(val * self.alto_pantalla)

        pregunta_actual, opciones_actuales, _ = preguntas[self.index]

        canvas_pregunta.create_rectangle(rel_x_q(0.1), rel_y_q(0.1), rel_x_q(0.9), rel_y_q(0.25),
                                         fill="#E3F2FD", outline="#90CAF9", width=2, tags="pregunta_box")
        canvas_pregunta.create_text(rel_x_q(0.5), rel_y_q(0.175), text=f"{self.index + 1}. {pregunta_actual}",
                                    font=("Arial", 22, "bold"), fill=COLOR_TEXTO_OSCURO,
                                    width=rel_x_q(0.75), anchor="center")

        y_posiciones_opciones = [0.4, 0.55, 0.7]

        for i, pos in enumerate(y_posiciones_opciones):
            boton = tk.Button(self.root, text=opciones_actuales[i],
                              font=("Arial", 16, "bold"),
                              bg="#BBDEFB", activebackground="#90CAF9", fg=COLOR_TEXTO_OSCURO, relief="flat",
                              command=lambda idx=i: self.verificar(idx),
                              wraplength=int(self.ancho_pantalla * 0.6))
            boton.place(relx=0.5, rely=pos, anchor="center", width=int(self.ancho_pantalla * 0.7), height=80)

    def verificar(self, seleccion):
        """Verifica la respuesta seleccionada por el usuario."""
        _, _, correcta = preguntas[self.index]
        if seleccion == correcta:
            self.puntaje += 1
            # Aquí podrías agregar un sonido para respuesta correcta, por ejemplo:
            # reproducir_sonido("correct_answer.mp3")
            messagebox.showinfo("✅ Respuesta Correcta", "¡Tu respuesta es correcta!")
        else:
            # Aquí podrías agregar un sonido para respuesta incorrecta, por ejemplo:
            # reproducir_sonido("incorrect_answer.mp3")
            messagebox.showerror("❌ Respuesta Incorrecta", f"Incorrecto. La respuesta correcta era: {preguntas[self.index][1][correcta]}")

        self.index += 1
        self.root.after(500, self.mostrar_pregunta)

    def mostrar_resultado(self):
        """Muestra la pantalla final con el puntaje del quiz."""
        self.limpiar()
        puntaje_porcentaje = int((self.puntaje / len(preguntas)) * 100)

        mensaje_principal = "¡Felicitaciones!" if puntaje_porcentaje >= 70 else "Sigue intentándolo..."
        mensaje_secundario = f"Obtuviste {self.puntaje} de {len(preguntas)} respuestas correctas.\nTu puntaje final es: {puntaje_porcentaje}%"

        # Fondo para la pantalla de resultados 
        self.root.configure(bg=COLOR_FONDO_OSCURO)

        # Crear un frame para el resultado para centrarlo y darle un fondo claro
        frame_resultado = tk.Frame(self.root, bg="#E0F2F7", bd=5, relief="raised")
        frame_resultado.place(relx=0.5, rely=0.5, anchor="center",
                              width=self.ancho_pantalla * 0.6, height=self.alto_pantalla * 0.5)

        label_principal = tk.Label(frame_resultado, text=mensaje_principal,
                                   font=("Arial", 36, "bold"), fg="#004D40", bg="#E0F2F7")
        label_principal.pack(pady=20)

        label_secundario = tk.Label(frame_resultado, text=mensaje_secundario,
                                    font=("Arial", 20), fg="#263238", bg="#E0F2F7")
        label_secundario.pack(pady=10)

        # Botones para reiniciar y salir
        btn_reiniciar = tk.Button(frame_resultado, text="Reiniciar Quiz",
                                  font=("Arial", 18, "bold"), bg=COLOR_EXITO, fg="white",
                                  command=self.reiniciar_quiz, relief="flat", bd=3)
        btn_reiniciar.pack(pady=20)

        btn_salir = tk.Button(frame_resultado, text="Salir",
                              font=("Arial", 18, "bold"), bg=COLOR_ERROR, fg="white",
                              command=self.root.destroy, relief="flat", bd=3)
        btn_salir.pack(pady=10)

    def reiniciar_quiz(self):
        """Reinicia el quiz a su estado inicial."""
        self.puntaje = 0
        self.index = 0
        self.mostrar_presentacion()

# === Ejecutar aplicación ===
if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacion(root)
    root.mainloop()

    # --- ¡IMPORTANTE! Limpiar mixer de Pygame al cerrar la aplicación ---
    # Esto libera los recursos de audio.
    try:
        pygame.mixer.quit()
    except Exception as e:
        print(f"Error al cerrar pygame.mixer: {e}")
    # --- FIN LIMPIEZA ---