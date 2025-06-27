import tkinter as tk
from tkinter import messagebox

import pygame
from utilidades import estilos
from utilidades import imagenes
from utilidades import sonidos
from utilidades import cuestionarioPython

# Constantes para eventos de Tkinter
EVENT_ENTER = "<Enter>"
EVENT_LEAVE = "<Leave>"

# === Aplicación principal ===
class Aplicacion:
    # === Constructor de la clase Aplicacion: se ejecuta automáticamente al crear una instancia.
    #  Inicializa la ventana y las variables importantes--
    def __init__(self, root):
        # --- Ventana principal ---
        self.root = root
        self.root.title("Autoevaluación Python")
        self.root.state('zoomed')  # Pantalla completa
        self.root.update_idletasks()

        # --- Dimensiones de pantalla ---
        self.ancho_pantalla = self.root.winfo_width()
        self.alto_pantalla = self.root.winfo_height()

        # --- Estado del cuestionario ---
        self.puntaje = 0
        self.index = 0

        # --- Cargar preguntas desde cuestionarioPython ---
        # Selecciona 10 preguntas al azar
        self.preguntas = cuestionarioPython.obtener_preguntas_aleatorias(
            cuestionarioPython.preguntas, cantidad=10
        )

        # --- Animación: "Evalúa" y "TUS SABERES" ---
        self.evalua_id = None
        self.saberes_id = None
        self.evalua_initial_x = 0
        self.saberes_initial_x = 0
        self.animacion_step = 0
        self.animacion_duracion = 20
        self.font_size_evalua_inicio = 1
        self.font_size_evalua_final = 48
        self.font_size_saberes_inicio = 1
        self.font_size_saberes_final = 60
        self.pos_y_evalua_final = 0.1
        self.pos_y_saberes_final = 0.18

        # --- Animación: efecto máquina de escribir ---
        self.texto_quiz_completo = "¿Cuánto sabes de Python?"
        self.texto_quiz_actual_index = 0
        self.titulo_python_id = None

        # --- Resultados del cuestionario ---
        self.resultado_animacion_step = 0
        self.resultado_animacion_duracion = 20
        self.resultados_id = None
        self.felicitaciones_id = None
        self.puntaje_id = None

        # --- Iniciar pantalla de presentación ---
        self.mostrar_presentacion()

    # === Método para la limpieza de la interfaz ===
    def limpiar(self):
        """Elimina todos los widgets de la ventana principal."""
        for widget in self.root.winfo_children():
            widget.destroy()

    # === Metodo para la pantalla de presentación inicial ===
    def mostrar_presentacion(self):
        """Dibuja la portada del quiz with imágenes, texto animado y un botón de inicio."""
        self.limpiar()
        self.root.configure(bg=estilos.COLOR_OSCURO)

        # --- Canvas de fondo ---
        canvas = tk.Canvas(
            self.root,
            width=self.ancho_pantalla,
            height=self.alto_pantalla,
            highlightthickness=0,
            bg=estilos.COLOR_OSCURO
        )
        canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.canvas = canvas  # Guardamos para usarlo en animaciones

        # --- Imagen de fondo ---
        self.fondo_presentacion_img = imagenes.cargar_imagen(
            "fondoPrincipal.jpg", (self.ancho_pantalla, self.alto_pantalla)
        )
        if self.fondo_presentacion_img:
            canvas.create_image(0, 0, image=self.fondo_presentacion_img, anchor="nw")

        # --- Funciones auxiliares para coordenadas relativas ---
        def rel_x(val): return int(val * self.ancho_pantalla)
        def rel_y(val): return int(val * self.alto_pantalla)

        # --- Texto "Evalúa" ---
        self.evalua_id = canvas.create_text(
            self.evalua_initial_x, rel_y(0.0),
            text="Evalúa",
            font=(estilos.FONT_BRUSH_SCRIPT, self.font_size_evalua_inicio, "bold"),
            fill=estilos.COLOR_TEXTO_OSCURO,
            anchor="nw", angle=10
        )

        # --- Texto "TUS SABERES" ---
        self.saberes_initial_x = rel_x(0.10)
        self.saberes_id = canvas.create_text(
            self.saberes_initial_x, rel_y(0.08),
            text="TUS SABERES",
            font=("Impact", self.font_size_saberes_inicio),
            fill=estilos.COLOR_TEXTO_OSCURO,
            anchor="nw", angle=10
        )

        # --- Logo principal ---
        self.logo_photo = imagenes.cargar_imagen(
            "logoInformatorio.jpg", (500, 350)
        )
        if self.logo_photo:
            canvas.create_image(rel_x(0.48), rel_y(0.50),
                                 image=self.logo_photo, anchor="center")

        # --- Foto grupal del equipo ---
        self.group_photo = imagenes.cargar_imagen(
            "foto_grupal.jpg", (350, 250)
        )
        if self.group_photo:
            canvas.create_image(rel_x(0.8), rel_y(0.45), image=self.group_photo, anchor="center")

        # --- Texto "¿CUÁNTO SABES DE PYTHON?" (inicialmente vacío) ---
        self.titulo_python_id = canvas.create_text(
            rel_x(0.48), rel_y(0.3),text="", font=estilos.FONT_SUBTITULO, fill=estilos.COLOR_TEXTO_OSCURO,
            anchor="center")

       # --- Crear botón de inicio del cuestionario ---
        self.crear_boton_iniciar()

        # --- Crear pie de página con los nombres de los desarrolladores ---
        self.crear_footer()

        # --- Forzar actualización de todos los elementos renderizados ---
        self.root.update_idletasks()

        # --- Reiniciar paso de animación para el texto inicial ---
        self.animacion_step = 0

        # --- Iniciar animación de "Evalúa" y "TUS SABERES" ---
        self.animar_evalua_saberes()

        # --- Iniciar efecto máquina de escribir tras una pequeña pausa ---
        self.root.after(800, self.iniciar_typewriter_effect)

    # === Botón de inicio del cuestionario ===
    def crear_boton_iniciar(self):
        """Crea y configura el botón para iniciar el test con sonido."""
        btn = tk.Button(
            self.root,
            text="INICIAR CUESTIONARIO",
            font=estilos.FONT_BUTTON,
            bg=estilos.COLOR_BUTTON,
            fg="white",
            activebackground=estilos.COLOR_HOVER,
            activeforeground="white",
            command=lambda: (
                sonidos.reproducir_sonido("startup_sound.mp3"),
                self.mostrar_pregunta()
            )
        )
        btn.bind(EVENT_ENTER, self.on_enter_iniciar_btn)
        btn.bind(EVENT_LEAVE, self.on_leave_iniciar_btn)
        # Efecto hover
        btn.bind(EVENT_ENTER, self.on_enter_iniciar_btn)
        btn.bind(EVENT_LEAVE, self.on_leave_iniciar_btn)
        btn.bind(EVENT_LEAVE, self.on_leave_iniciar_btn)

        btn.place(relx=0.48, rely=0.65, anchor="center", width=350, height=60)
        return btn

    def crear_footer(self):
        """Agrega el pie de página los integrantes del equipo desarrollador."""
        footer_text = "Proyecto desarrollado por [Fortín Raquel], [Encina Andrés] y [Nasif Carina]"
        footer_label = tk.Label(
            text=footer_text,
            font=estilos.FONT_BUTTON,
            bg=estilos.COLOR_MEDIO,
            fg="#0d0c0c",
            relief="flat",
            anchor="center"
        )
        footer_label.place(relx=0.0, rely=0.96, relwidth=1.0, height=30)
    # === Métodos para el efecto máquina de escribir ===
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
            sonidos.reproducir_sonido("typewriter_click.mp3")
            self.texto_quiz_actual_index += 1
            self.root.after(80, self.escribir_titulo_python) # Velocidad del tecleo
        else:
            # Fin del efecto máquina de escribir
            return

    # ---  métodos para animar el texto : "Evalúa" y "TUS SABERES" ---
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
            if self.animacion_step == 0 or self.animacion_step == int(self.animacion_duracion / 2):
                sonidos.reproducir_sonido("evalua_sound.mp3")
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
        """Cambia el color del botón cuando el mouse ingresa al boton."""
        event.widget.config(bg=estilos.COLOR_EXITO, activebackground=estilos.COLOR_EXITO)

    def on_leave_iniciar_btn(self, event):
        """Restaura el color del botón cuando el mouse sale del boton."""
        event.widget.config(bg=estilos.COLOR_BUTTON)

    def mostrar_pregunta(self):
        """
        Muestra la siguiente pregunta del quiz.
        """
        if self.index >= len(self.preguntas):
            self.mostrar_resultado()
            return

        self.limpiar()
        self.root.configure(bg=estilos.COLOR_MEDIO)

        canvas_pregunta = tk.Canvas(self.root, width=self.ancho_pantalla, height=self.alto_pantalla,
                                   highlightthickness=0, bg=estilos.COLOR_MEDIO)
        canvas_pregunta.place(relx=0, rely=0, relwidth=1, relheight=1)

        # --- AGREGAR IMAGEN DE FONDO ---
        self.fondo_pregunta_img = imagenes.cargar_imagen("cuestionario.jpg", (self.ancho_pantalla, self.alto_pantalla))
        if self.fondo_pregunta_img:
            canvas_pregunta.create_image(0, 0, image=self.fondo_pregunta_img, anchor="nw")

        def rel_x_q(val): return int(val * self.ancho_pantalla)
        def rel_y_q(val): return int(val * self.alto_pantalla)

        pregunta_actual, opciones_actuales, _ = self.preguntas[self.index]

        # Ajustar el cuadro de la pregunta para que sea más ancho
        canvas_pregunta.create_rectangle(
            rel_x_q(0.1), rel_y_q(0.1), rel_x_q(0.9), rel_y_q(0.25),
            fill="#B366FF", outline="#90CAF9", width=2, tags="pregunta_box"
        )
        # Cambiar el color de la letra a un tono accesible
        canvas_pregunta.create_text(
            rel_x_q(0.5), rel_y_q(0.175),
            text=f"{self.index + 1}. {pregunta_actual}",
            font=estilos.FONT_SUBTITULO, fill="#333333",
            width=rel_x_q(0.75), anchor="center"
        )

        # Aumentar la separación vertical entre las opciones
        y_posiciones_opciones = [0.4, 0.58, 0.76]
        for i, pos in enumerate(y_posiciones_opciones):
            boton = tk.Button(
                self.root, text=opciones_actuales[i],
                font=estilos.FONT_BUTTON,
                bg="#BBDEFB", activebackground="#90CAF9",
                fg=estilos.COLOR_TEXTO_OSCURO, relief="flat",
                command=lambda idx=i: self.verificar(idx),
                wraplength=int(self.ancho_pantalla * 0.6)
            )
            boton.place(
                relx=0.3, rely=pos, anchor="w",
                width=int(self.ancho_pantalla * 0.6), height=80
            )

        # --- Crear botón de navegación (Siguiente/Finalizar) ---
        self.crear_boton_navegacion()

    def crear_boton_navegacion(self):
        """Muestra el botón 'Siguiente' o 'Finalizar' según la pregunta actual."""
        if self.index < len(self.preguntas) - 1:
            texto_boton = "Siguiente"
            comando = self.siguiente_pregunta
        else:
            texto_boton = "Finalizar"
            comando = self.mostrar_resultado

        btn_navegacion = tk.Button(
            self.root,
            text=texto_boton,
            font=estilos.FONT_BUTTON,
            bg=estilos.COLOR_BUTTON,
            fg="white",
            activebackground=estilos.COLOR_HOVER,
            activeforeground="white",
            command=comando
        )
        btn_navegacion.place(relx=0.75, rely=0.88, anchor="center", width=200, height=50)

    def siguiente_pregunta(self):
        """Muestra la siguiente pregunta solo si se ha respondido la actual."""
        if hasattr(self, 'respuesta_seleccionada'):
            if self.index < len(self.preguntas) - 1:
                self.index += 1
                del self.respuesta_seleccionada
                self.mostrar_pregunta()
        else:
            messagebox.showwarning("Advertencia", "Debes responder la pregunta antes de continuar.")

    def verificar(self, idx):
        """Verifica la respuesta seleccionada por el usuario."""
        if self.index >= len(self.preguntas):
            return
        self.respuesta_seleccionada = idx  # Guardar la respuesta seleccionada

        # Deshabilitar todos los botones de las opciones
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Button) and widget.cget("text") in self.preguntas[self.index][1]:
                widget.config(state="disabled")

        _, _, correcta = self.preguntas[self.index]
        if idx == correcta:
            self.puntaje += 1
            messagebox.showinfo("Respuesta Correcta", "¡Tu respuesta es correcta!")
        else:
            messagebox.showerror("Respuesta Incorrecta", f"Incorrecto. La respuesta correcta era: {self.preguntas[self.index][1][correcta]}")

    def reiniciar_quiz(self):
        self.puntaje = 0
        self.index = 0
        self.mostrar_presentacion()
    
    def mostrar_resultado(self):
        """Muestra la pantalla final con el título 'TUS RESULTADOS' animado y con confeti si aprueba."""
        self.limpiar()
        puntaje_porcentaje = int((self.puntaje / len(self.preguntas)) * 100)

        # Configuración de fondo
        self.root.configure(bg=estilos.COLOR_MEDIO)

        # Crear canvas para resultados
        canvas_resultado = tk.Canvas(self.root, width=self.ancho_pantalla, height=self.alto_pantalla,
                                   highlightthickness=0, bg=estilos.COLOR_MEDIO)
        canvas_resultado.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.canvas = canvas_resultado

        # Determinar si el usuario aprobó o desaprobó
        if puntaje_porcentaje >= 70:
            img_path = "felicidades.jpg"
            mensaje = "¡Felicidades, aprobaste!"
            # Mostrar imagen como fondo de todo el canvas ANTES del confeti
            resultado_img = imagenes.cargar_imagen(img_path, (self.ancho_pantalla, self.alto_pantalla))
            if resultado_img:
                canvas_resultado.create_image(0, 0, image=resultado_img, anchor="nw")
                self.resultado_img = resultado_img
            # Confeti
            import random
            colores = ["#FF5733", "#33FF57", "#3357FF", "#F7DC6F", "#AF7AC5", "#48C9B0", "#F1948A"]
            confetis = []
            for _ in range(40):
                x = random.randint(10, self.ancho_pantalla-10)
                y = random.randint(-200, 0)
                size = random.randint(8, 18)
                color = random.choice(colores)
                confeti = canvas_resultado.create_oval(x, y, x+size, y+size, fill=color, outline="")
                confetis.append((confeti, random.randint(2, 6)))
            def animar_confeti():
                for confeti, speed in confetis:
                    canvas_resultado.move(confeti, 0, speed)
                    _, _, _, _ = canvas_resultado.coords(confeti)
                    if canvas_resultado.coords(confeti)[1] > self.alto_pantalla:
                        canvas_resultado.move(confeti, 0, -self.alto_pantalla-20)
                self.root.after(30, animar_confeti)
            animar_confeti()
        else:
            img_path = "seguirIntentando.jpg"
            mensaje = "¡Sigue practicando, puedes mejorar!"
            # Mostrar imagen como fondo de todo el canvas
            resultado_img = imagenes.cargar_imagen(img_path, (self.ancho_pantalla, self.alto_pantalla))
            if resultado_img:
                canvas_resultado.create_image(0, 0, image=resultado_img, anchor="nw")
                self.resultado_img = resultado_img

        # Mensaje
        canvas_resultado.create_text(self.ancho_pantalla//2, 420, text=mensaje, font=estilos.FONT_SUBTITULO, fill="#333")
        # Puntaje
        puntaje_text = f"{puntaje_porcentaje}% Acertaste {self.puntaje} de {len(self.preguntas)} respuestas correctas"
        canvas_resultado.create_text(self.ancho_pantalla//2, 450, text=puntaje_text, font=estilos.FONT_SUBTITULO, fill="#222")

        # Botones
        self.btn_reiniciar = tk.Button(self.root, text="Reiniciar Quiz",
                                      font=estilos.FONT_BUTTON, bg=estilos.COLOR_EXITO, fg="white",
                                      command=self.reiniciar_quiz, relief="flat", bd=3)
        self.btn_salir = tk.Button(self.root, text="Salir",
                              font=estilos.FONT_BUTTON, bg=estilos.COLOR_ERROR, fg="white",
                              command=self.root.destroy, relief="flat", bd=3)

        self.btn_reiniciar.place(relx=0.4, rely=0.85, anchor="center", width=200, height=50)
        self.btn_reiniciar.bind(EVENT_ENTER, lambda e: e.widget.config(bg="#388E3C"))
        self.btn_reiniciar.bind(EVENT_LEAVE, lambda e: e.widget.config(bg=estilos.COLOR_EXITO))
        self.btn_salir.place(relx=0.6, rely=0.85, anchor="center", width=200, height=50)
        self.btn_salir.bind(EVENT_ENTER, lambda e: e.widget.config(bg="#B71C1C"))
        self.btn_salir.bind(EVENT_LEAVE, lambda e: e.widget.config(bg=estilos.COLOR_ERROR))
        self.btn_reiniciar.bind(EVENT_LEAVE, lambda e: e.widget.config(bg=estilos.COLOR_EXITO))
        self.btn_salir.bind(EVENT_ENTER, lambda e: e.widget.config(bg="#B71C1C"))
        self.btn_salir.bind(EVENT_LEAVE, lambda e: e.widget.config(bg=estilos.COLOR_ERROR))
        self.btn_salir.bind(EVENT_LEAVE, lambda e: e.widget.config(bg=estilos.COLOR_ERROR))

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
