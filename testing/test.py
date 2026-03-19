import pygame
import sys

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    font = pygame.font.SysFont("consolas", 18)
    
    # --- 1. THE HISTORY LIST ---
    # This stores everything that already happened. 
    # Because we only "append" to it, the user can't change old lines.
    history = ["System: Welcome to your Finance Tracker."]
    
    # --- 2. THE QUESTION SEQUENCE ---
    # A list of what the program will ask in order.
    questions = ["Enter Date (MM/DD):", "Enter Category:", "Enter Amount:"]
    current_step = 0  # Tracks which question we are on (0, 1, or 2)
    
    user_text = ""
    running = True

    while running:
        # We define the "Active Question" based on our current step
        active_question = f"PROG: {questions[current_step]}"
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # When Enter is pressed:
                    # A) Add the question and the answer to history so they stay visible
                    history.append(active_question)
                    history.append(f"USER: {user_text}")
                    
                    # B) Move to the next question in the list
                    # The % len(questions) makes it loop back to the start after the last question
                    current_step = (current_step + 1) % len(questions)
                    
                    # C) Clear the input for the next answer
                    user_text = "" 
                
                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    # --- 3. INPUT FILTERING ---
                    # Only add the character if it's a real letter/number (ignores Shift, Ctrl, etc.)
                    if event.unicode.isprintable():
                        user_text += event.unicode

        screen.fill((30, 30, 30))

        # --- 4. THE DYNAMIC Y-OFFSET ---
        # We start at the top (y=20) and move down for every line in history
        y_pos = 20
        for line in history:
            # Render old messages in a darker gray so they look "inactive"
            old_surf = font.render(line, True, (120, 120, 120))
            screen.blit(old_surf, (20, y_pos))
            y_pos += 25 # Move the "pen" down for the next line

        # --- 5. THE ACTIVE AREA ---
        # Draw the current question in a bright color
        prompt_surf = font.render(active_question, True, (0, 255, 100))
        screen.blit(prompt_surf, (20, y_pos))
        
        # Draw what the user is currently typing below the question
        input_surf = font.render(f"> {user_text}", True, (255, 255, 255))
        screen.blit(input_surf, (20, y_pos + 25))

        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

main()
