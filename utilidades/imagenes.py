from PIL import Image, ImageTk

def cargar_imagen(nombre_archivo, tamano=None):
    """
    Abre una imagen desde la carpeta 'imagenes' ubicada en la raíz del proyecto.
    Si se indica un tamaño, redimensiona la imagen antes de devolverla.
    Devuelve un objeto PhotoImage listo para usar con Tkinter, o None (nada) si no se pudo cargar.
    """
    ruta = "imagenes/" + nombre_archivo

    try:
        imagen = Image.open(ruta)
        if tamano:
            imagen = imagen.resize(tamano, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(imagen)
    except Exception as e:
        print(f"Error al cargar la imagen {ruta}: {e}")
        return None

