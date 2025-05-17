import pygame
from material_colors import (
    Red, Pink, Purple, DeepPurple, Indigo, Blue, LightBlue, Cyan,
    Teal, Green, LightGreen, Lime, Yellow, Amber, Orange, DeepOrange,
    Brown, Grey, BlueGrey, PALETTES
)



def calc_size_for_single(enum_cls, cols, box_w, box_h, margin, title_h):
    n = len(enum_cls)
    rows = (n + cols - 1)//cols
    w = cols*(box_w+margin)+margin
    h = title_h + rows*(box_h+margin)+margin
    return w, h

def calc_size_for_all(palettes, cols, box_w, box_h, margin, title_h, section_title_h):
    y = margin
    max_w = 0
    for name, enum_cls in palettes:
        n = len(enum_cls)
        rows = (n + cols -1)//cols
        w = cols*(box_w+margin)+margin
        h = section_title_h + rows*(box_h+margin)+margin
        max_w = max(max_w, w)
        y += h
    return max_w, min(y, 900)

def preview():
    pygame.init()
    BOX_W, BOX_H = 200, 150
    MARGIN = 5
    COLUMNS = 5
    TITLE_H = 40
    SECTION_TITLE_H = 25
    FONT = pygame.font.SysFont("Arial", 14)
    TXT_COL = (255,255,255)
    BG = (30,30,30)

    current = 0
    show_all = False
    need_resize = True

    screen = pygame.display.set_mode((800,600))
    clock = pygame.time.Clock()

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                return
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_RIGHT and not show_all:
                    current = (current+1)%len(PALETTES); need_resize = True
                if ev.key == pygame.K_LEFT and not show_all:
                    current = (current-1)%len(PALETTES); need_resize = True
                if ev.key == pygame.K_a:
                    show_all = not show_all; need_resize = True
                if ev.key in (pygame.K_ESCAPE, pygame.K_q):
                    pygame.quit()
                    return

        if need_resize:
            if show_all:
                w,h = calc_size_for_all(PALETTES, COLUMNS, BOX_W, BOX_H, MARGIN, TITLE_H, SECTION_TITLE_H)
            else:
                _, enum_cls = PALETTES[current]
                w,h = calc_size_for_single(enum_cls, COLUMNS, BOX_W, BOX_H, MARGIN, TITLE_H)
            screen = pygame.display.set_mode((w, h))
            need_resize = False

        screen.fill(BG)
        if show_all:
            y_off = MARGIN
            for name, enum_cls in PALETTES:
                # Section title
                screen.blit(FONT.render(name, True, TXT_COL), (MARGIN, y_off))
                y_off += SECTION_TITLE_H
                for idx, col in enumerate(enum_cls):
                    row, col_i = divmod(idx, COLUMNS)
                    x = MARGIN + col_i*(BOX_W+MARGIN)
                    y = y_off + row*(BOX_H+MARGIN)
                    pygame.draw.rect(screen, col.value, (x,y,BOX_W,BOX_H))
                    # Volles Label
                    label = f"colors.{enum_cls.__name__}.{col.name}"
                    screen.blit(FONT.render(label, True, TXT_COL), (x+5, y+5))
                y_off += ((len(enum_cls)+COLUMNS-1)//COLUMNS)*(BOX_H+MARGIN) + MARGIN
        else:
            name, enum_cls = PALETTES[current]
            screen.blit(FONT.render(
                f"{name}  (←/→ wechseln, A=alle, Q/ESC=Exit)",
                True, TXT_COL),
                (MARGIN, MARGIN)
            )
            for idx, col in enumerate(enum_cls):
                row, col_i = divmod(idx, COLUMNS)
                x = MARGIN + col_i*(BOX_W+MARGIN)
                y = TITLE_H + row*(BOX_H+MARGIN)
                pygame.draw.rect(screen, col.value, (x,y,BOX_W,BOX_H))
                # Volles Label
                label = f"colors.{enum_cls.__name__}.{col.name}"
                screen.blit(FONT.render(label, True, TXT_COL), (x+5, y+5))

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    preview()
