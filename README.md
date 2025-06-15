# PythonQuizApp

¡Bienvenido a **PythonQuizApp**!  
Una aplicación interactiva desarrollada en Python, con interfaz gráfica (Tkinter), para autoevaluar tus conocimientos sobre el lenguaje Python a través de preguntas y respuestas, animaciones, efectos visuales y de sonido.

---

## Características

- Interfaz gráfica amigable con animaciones (Tkinter)
- Preguntas de opción múltiple sobre conceptos clave de Python
- Efectos de sonido en eventos y resultados (usando pygame)
- Imágenes ilustrativas y fondos personalizados
- Puntuación automática y feedback inmediato
- Pantalla de resultados con animaciones (confeti, felicitaciones)
- Fácil de ejecutar en cualquier sistema con Python 3.x

---

## Instalación

1. **Clona este repositorio:**
   ```bash
   git clone https://github.com/Cary40/PythonQuizApp.git
   cd PythonQuizApp
   ```

2. **(Opcional) Crea un entorno virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```
   Si `requirements.txt` no existe, instala manualmente:
   ```bash
   pip install pillow pygame
   ```

   - **Dependencias utilizadas:**
     - `tkinter` (incluido en la mayoría de distribuciones estándar de Python)
     - `pillow` (`PIL`) para manejo de imágenes
     - `pygame` para efectos de sonido

---

## Ejecución

Desde la carpeta principal del proyecto, ejecuta:

```bash
python Quiz.py
```

> **Nota:**  
> Asegúrate de tener la carpeta `sonidos` con los archivos `.mp3` y la carpeta `imagenes` con los recursos gráficos necesarios.

---

## Estructura del Proyecto

- `Quiz.py` : Archivo principal de la aplicación
- `/imagenes/` : Carpeta con imágenes y fondos que usa la interfaz
- `/sonidos/` : Carpeta con efectos de sonido (ej: `aplausos.mp3`, `evalua_sound.mp3`, `startup_sound.mp3`, `typewriter_click.mp3`)
- `Interfaz 35 preg y resp con V-F.pdf` y `Interfaz Autoevaluacion Python.pdf`: Documentos de referencia del diseño/interfaz

---

## Créditos

Proyecto desarrollado por:
- Fortín Raquel
- Encina Andres
- Nasif Carina

---

## Contribución

¿Quieres mejorar PythonQuizApp?  
1. Haz un fork del repositorio
2. Crea una rama: `git checkout -b nueva-funcionalidad`
3. Realiza tus cambios y commitea
4. Abre un Pull Request

---

## Licencia

Este proyecto está bajo la licencia MIT.

---

¡Diviértete aprendiendo y autoevaluándote en Python con PythonQuizApp!
