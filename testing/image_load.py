import pygame
import sys

def main():
    print("Main started")
    pygame.init()

    font = pygame.font.SysFont("consolas", 20)
    char_width, char_height = font.size("A")
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Personal Finance")
    COLS =  screen_width // char_width
    ROWS =  screen_height // char_height
    history = []
    questions = []
    clock = pygame.time.Clock()
    running = True
    current_step = 0 
    current_input = ""  
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    current_input = current_input[:-1]
                elif event.key == pygame.K_RETURN:
                    print("User entered:", current_input)
                    current_input = ""
                else:
                    current_input += event.unicode

        screen.fill((30, 30, 30))

        
        text_surface = font.render(current_input, True, (200, 200, 200))
        screen.blit(text_surface, (10, 10))
        while running:
            active_question = F"{questions[current_step]}"
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

startinginput = input("Y/N to start finance program: ")
if startinginput.lower() == "y":
    main()
else:
    pygame.quit()
    sys.exit()



