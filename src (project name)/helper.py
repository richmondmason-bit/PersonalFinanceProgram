#savings goal tracker and income entries and expense entries 
import matplotlib.pyplot as plt
import pygame
import sys
import io

def generate_pie_chart_image(values, labels, colors):
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.pie(values, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax.axis('equal') # Ensures the pie chart is circular

    # Save to a buffer and convert to a Pygame surface
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    buf.seek(0)
    plt.close(fig) # Close the figure to avoid memory leaks
    return pygame.image.load(buf, 'chart.png')

# Example usage in a Pygame loop:
pygame.init()
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("Matplotlib Pie Chart in Pygame")

# Data
chart_values = [35, 25, 25, 15]
chart_labels = ["Apples", "Bananas", "Cherries", "Dates"]
chart_colors = ["red", "gold", "lightskyblue", "lightcoral"]

# Generate the image surface
pie_chart_surface = generate_pie_chart_image(chart_values, chart_labels, chart_colors)
pie_chart_rect = pie_chart_surface.get_rect(center=(200, 200))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255)) 
    screen.blit(pie_chart_surface, pie_chart_rect) 
    
    pygame.display.flip()

pygame.quit()
