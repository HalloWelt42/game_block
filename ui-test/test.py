import sys
import pygame
from pygame.locals import DOUBLEBUF, OPENGL
import imgui
from imgui.integrations.pygame import PygameRenderer
from OpenGL.GL import glClear, GL_COLOR_BUFFER_BIT, glClearColor

def main():
    # Initialisierung von Pygame und Fenster
    pygame.init()
    size = (800, 600)
    pygame.display.set_mode(size, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("ImGui mit Pygame")

    # Hintergrundfarbe setzen
    glClearColor(0.1, 0.1, 0.1, 1)

    # ImGui-Kontext erstellen (nach Fensterinitialisierung!)
    imgui.create_context()

    # Renderer für Pygame initialisieren
    impl = PygameRenderer()

    # UI-Zustand
    counter = 0
    show_demo = False

    clock = pygame.time.Clock()
    running = True

    while running:
        # Ereignisse abfragen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            impl.process_event(event)

        impl.process_inputs()

        # 🔧 Wichtiger Fix: DisplaySize manuell setzen
        io = imgui.get_io()
        io.display_size = pygame.display.get_surface().get_size()

        # Frame vorbereiten
        imgui.new_frame()
        glClear(GL_COLOR_BUFFER_BIT)

        # ImGui Fenster
        imgui.begin("Hallo Welt Fenster")
        imgui.text("Hallo von PyImGui mit Pygame!")
        if imgui.button("Klicke mich!"):
            counter += 1
        imgui.same_line()
        imgui.text(f"Zähler: {counter}")
        _, show_demo = imgui.checkbox("Demo Fenster anzeigen", show_demo)
        imgui.end()

        # Optional: Demo-Fenster von ImGui
        if show_demo:
            imgui.show_demo_window()

        # Rendern
        imgui.render()
        impl.render(imgui.get_draw_data())

        pygame.display.flip()
        clock.tick(60)

    # Aufräumen
    impl.shutdown()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
