import os
import pygame
from color_palette.material_colors import (
    Red, Pink, Purple, DeepPurple, Indigo, Blue, LightBlue, Cyan, Teal,
    Green, LightGreen, Lime, Yellow, Amber, Orange, DeepOrange,
    Brown, Grey, BlueGrey, PALETTES
)

# Ausgabeordner
OUTPUT_DIR = "./source/boxes/"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Blockgröße
BLOCK_SIZE = 40

# Initialisierung
pygame.init()

def one_block_surface(color1, color2, size):
    """Erzeugt eine Surface mit einem diagonalen Farbverlauf."""
    surface = pygame.Surface((size, size))

    for y in range(size):
        for x in range(size):
            ratio = ((x / size) + (y / size)) / 2
            r = int(color1.value[0] * (1 - ratio) + color2.value[0] * ratio)
            g = int(color1.value[1] * (1 - ratio) + color2.value[1] * ratio)
            b = int(color1.value[2] * (1 - ratio) + color2.value[2] * ratio)
            surface.set_at((x, y), (r, g, b))

    return surface

# Erzeuge pro Palette ein Bild
for name, palette in PALETTES:
    color1 = palette._400
    color2 = palette._800

    surface = one_block_surface(color1, color2, BLOCK_SIZE)

    # Dateinamen aufbereiten
    filename = f"block_{name.lower().replace(' ', '_')}_{BLOCK_SIZE}x{BLOCK_SIZE}px.png"
    path = os.path.join(OUTPUT_DIR, filename)

    # Speichern
    pygame.image.save(surface, path)
    print(f"Gespeichert: {path}")

pygame.quit()
