import pygame

class InteractiveBox:
    HANDLE_SIZE = 8

    def __init__(self, rect, color=(255, 100, 100)):
        self.rect = pygame.Rect(rect)
        self.color = color
        self.hovered = False
        self.selected_handle = None  # z.B. "topleft", "bottomright", etc.

    def draw(self, surface):
        # Hauptbox
        pygame.draw.rect(surface, self.color, self.rect)

        # Wenn Maus in Nähe: Anfasser anzeigen
        if self.hovered:
            for pos in self._handle_positions().values():
                pygame.draw.rect(surface, (255, 255, 255), (*pos, self.HANDLE_SIZE, self.HANDLE_SIZE))

    def update(self, mouse_pos):
        # Hover prüfen
        self.hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.hovered:
            for name, pos in self._handle_positions().items():
                handle_rect = pygame.Rect(*pos, self.HANDLE_SIZE, self.HANDLE_SIZE)
                if handle_rect.collidepoint(event.pos):
                    self.selected_handle = name
                    print(f"Handle {name} ausgewählt")

        elif event.type == pygame.MOUSEBUTTONUP:
            self.selected_handle = None

        elif event.type == pygame.MOUSEMOTION and self.selected_handle:
            self._resize(event.rel)

    def _resize(self, delta):
        dx, dy = delta
        if self.selected_handle == "bottomright":
            self.rect.width += dx
            self.rect.height += dy
        elif self.selected_handle == "topleft":
            self.rect.x += dx
            self.rect.y += dy
            self.rect.width -= dx
            self.rect.height -= dy
        # Weitere Handles möglich...

    def _handle_positions(self):
        return {
            "topleft": (self.rect.left - self.HANDLE_SIZE // 2, self.rect.top - self.HANDLE_SIZE // 2),
            "topright": (self.rect.right - self.HANDLE_SIZE // 2, self.rect.top - self.HANDLE_SIZE // 2),
            "bottomleft": (self.rect.left - self.HANDLE_SIZE // 2, self.rect.bottom - self.HANDLE_SIZE // 2),
            "bottomright": (self.rect.right - self.HANDLE_SIZE // 2, self.rect.bottom - self.HANDLE_SIZE // 2),
        }

pygame.init()
screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()

box = InteractiveBox((100, 100, 120, 80))

running = True
while running:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        box.handle_event(event)

    box.update(mouse_pos)

    screen.fill((30, 30, 30))
    box.draw(screen)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

