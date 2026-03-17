import pygame

pygame.init()
screen = pygame.display.set_mode((600, 400))
font = pygame.font.SysFont("monospace", 20)
terminal_history = ["System initialized...", "User logged in.", "> Ready for input"]


def draw_terminal():
    screen.fill((0, 0, 0)) 
    for i, line in enumerate(terminal_history):
        
        text_surface = font.render(line, True, (0, 255, 0))
      
        screen.blit(text_surface, (10, 10 + (i * 25)))
    pygame.display.flip()
