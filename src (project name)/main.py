import pygame

# 1. Setup
pygame.init()
screen = pygame.display.set_mode((600, 400))
font = pygame.font.SysFont("monospace", 20)
terminal_history = ["System initialized...", "User logged in.", "> Ready for input"]

# 2. Rendering Loop
def draw_terminal():
    screen.fill((0, 0, 0)) # Black background
    for i, line in enumerate(terminal_history):
        # Render text (Green on Black for retro feel)
        text_surface = font.render(line, True, (0, 255, 0))
        # Draw each line 25 pixels below the previous one
        screen.blit(text_surface, (10, 10 + (i * 25)))
    pygame.display.flip()
