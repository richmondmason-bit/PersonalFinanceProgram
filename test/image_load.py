import pygame 
import sys 

def main():

  #staring definitions and print statements to calrify start of program
    print("Main started")
    pygame.init()
    font = pygame.font.SysFont("consolas", 20)
    char_width,char_height = font.size("A")
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Personal Finance")
    COLS =  screen_width // char_width
    ROWS =  screen_height // char_height
    clock = pygame.time.Clock()
    running = True
    #while true statement for logic for open pygame window 
    while running: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        #rendering cosole area
        current_input = ""

        #screen settings 
        screen.fill((30, 30, 30)) 
        pygame.display.flip() 
        clock.tick(60)
    #close game if exited main loop
    pygame.quit()
    sys.exit()
#function to enter main
startinginput = input("Y/N to start finance program: ")
if startinginput.lower() == "y":
    main()
else:
    pygame.quit()
    sys.exit()

