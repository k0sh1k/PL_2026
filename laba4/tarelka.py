import pygame

pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("НЛО без огней")

# Цвета
SKY = (15, 15, 30)      # Очень темный синий
METAL = (170, 170, 180) # Светлый металл
GLASS = (100, 200, 255) # Голубое стекло

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(SKY)

    # 1. Купол (кабина)
    pygame.draw.ellipse(screen, GLASS, (150, 115, 100, 60))
    
    # 2. Основной корпус (диск)
    pygame.draw.ellipse(screen, METAL, (100, 140, 200, 50))
    
    # 3. Тень на корпусе для объема (необязательно, но так симпатичнее)
    pygame.draw.ellipse(screen, (100, 100, 110), (100, 140, 200, 50), 2)

    pygame.display.flip()

pygame.quit()
