import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tabbed App Example")

font = pygame.font.SysFont("consolas", 24)

# Tabs
TABS = ["HOME", "ADD", "VIEW", "SETTINGS"]
current_tab = "HOME"

clock = pygame.time.Clock()

# -------------------------
# Draw Tabs
# -------------------------
def draw_tabs():
    tab_width = WIDTH // len(TABS)

    for i, tab in enumerate(TABS):
        x = i * tab_width

        color = (70, 70, 70) if tab == current_tab else (40, 40, 40)
        pygame.draw.rect(screen, color, (x, 0, tab_width, 40))

        label = font.render(tab, True, (255, 255, 255))
        screen.blit(label, (x + 20, 8))


# -------------------------
# Tab Screens
# -------------------------
def draw_home():
    text = font.render("This is the HOME tab", True, (200, 200, 200))
    screen.blit(text, (50, 100))


def draw_add():
    text = font.render("This is the ADD tab", True, (200, 200, 200))
    screen.blit(text, (50, 100))


def draw_view():
    text = font.render("This is the VIEW tab", True, (200, 200, 200))
    screen.blit(text, (50, 100))


def draw_settings():
    text = font.render("This is the SETTINGS tab", True, (200, 200, 200))
    screen.blit(text, (50, 100))


# -------------------------
# Switch Tab Helper
# -------------------------
def switch_tab(new_tab):
    global current_tab
    current_tab = new_tab


# -------------------------
# Main Loop
# -------------------------
running = True
while running:
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Keyboard switching
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                switch_tab("HOME")
            elif event.key == pygame.K_2:
                switch_tab("ADD")
            elif event.key == pygame.K_3:
                switch_tab("VIEW")
            elif event.key == pygame.K_4:
                switch_tab("SETTINGS")

        # Mouse click switching
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if my < 40:  # clicking tab bar
                tab_width = WIDTH // len(TABS)
                index = mx // tab_width
                if index < len(TABS):
                    switch_tab(TABS[index])

    # Draw UI
    draw_tabs()

    # Render active tab
    if current_tab == "HOME":
        draw_home()
    elif current_tab == "ADD":
        draw_add()
    elif current_tab == "VIEW":
        draw_view()
    elif current_tab == "SETTINGS":
        draw_settings()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()