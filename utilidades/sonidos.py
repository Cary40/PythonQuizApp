import pygame

try:
    pygame.mixer.init()
except pygame.error as e:
    print(f"Error al inicializar pygame.mixer: {e}")

def reproducir_sonido(nombre_archivo):
    ruta = "sonidos/" + nombre_archivo
    try:
        sonido = pygame.mixer.Sound(ruta)
        sonido.play()
    except pygame.error as e:
        print(f"Error al reproducir el sonido: {e}")
