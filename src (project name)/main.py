import pygame
import sys
pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Personal Finanace")
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
    screen.fill((30, 30, 30)) 
    pygame.display.flip()
    clock.tick(60)
if input("")
#main
def main():
    print("Personal Finance")
    
    while True:
       print("main worked")

if __name__ == "__main__":
    main()
