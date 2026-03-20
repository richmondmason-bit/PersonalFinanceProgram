import pygame
import sys

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    font = pygame.font.SysFont("consolas", 18)

    image = pygame.image.load("testing/Pictures/1615991837602.png").convert_alpha()
    image = pygame.transform.scale(image, (426,240))

    state = "MENU"
    character_limit = 20
    history = ["Welcome to Finance Tracker.", "[1] Add Transaction", "[2] View Total"]
    transactions = []
    current_entry = {}
    user_text = ""
    running = True

    icon_surface = pygame.image.load("testing/Pictures/1615991837602.png").convert_alpha()

    while running:
        if state == "MENU":
            active_question = "SELECT (1 or 2):"
        elif state == "GET_NAME":
            active_question = "ENTER ITEM NAME:"
        elif state == "GET_AMOUNT":
            active_question = f"AMOUNT FOR {current_entry.get('name', '')}:"
        elif state == "CONFIRM":
            active_question = f"SAVE {current_entry.get('name')} (${current_entry.get('amount')})? (y/n):"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    cmd = user_text.strip().lower()
                    history.append(f"{active_question} {user_text}")

                   
                    if len(user_text) > character_limit:
                        history.append("Error: input has too many characters")
                        user_text = ""
                        continue

                    if state == "MENU":
                        if cmd == "1":
                            state = "GET_NAME"
                        elif cmd == "2":
                            total = sum(t['amount'] for t in transactions)
                            history.append(f"TOTAL SPENT: ${total:.2f}")
                        else:
                            history.append("Invalid. Press 1 or 2.")

                    elif state == "GET_NAME":
                        current_entry['name'] = user_text
                        state = "GET_AMOUNT"

                    elif state == "GET_AMOUNT":
                        try:
                            current_entry['amount'] = float(user_text)
                            state = "CONFIRM"
                        except ValueError:
                            history.append("Error: Please enter a number.")

                    elif state == "CONFIRM":
                        if cmd == "y":
                            transactions.append(current_entry.copy())
                            history.append("TRANSACTION SAVED.")
                        else:
                            history.append("CANCELLED.")
                        state = "MENU"
                        current_entry = {}
                        history.append("[1] Add Transaction, [2] View Total")

                    user_text = ""
                    if len(history) > 15:
                        history.pop(0)

                elif event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]

                else:
                    if event.unicode.isprintable():
                        if len(user_text) < character_limit:
                            user_text += event.unicode
                        else:
                            history.append("Error: input has too many characters")

        screen.fill((30, 30, 30))
        screen.blit(image, (350, 20))

        y_pos = 20
        for line in history:
            color = (0, 255, 255) if ">>>" in line else (120, 120, 120)
            surf = font.render(line, True, color)
            screen.blit(surf, (20, y_pos))
            y_pos += 25

        prompt_surf = font.render(active_question, True, (0, 255, 100))
        screen.blit(prompt_surf, (20, y_pos))

        input_surf = font.render(f"> {user_text}", True, (255, 255, 255))
        screen.blit(input_surf, (20, y_pos + 25))

        try:
            icon_surface = pygame.image.load("testing/Pictures/1615991837602.png")
        except pygame.error as message:
            print(f"Cannot load image: {message}")
            icon_surface = None

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()