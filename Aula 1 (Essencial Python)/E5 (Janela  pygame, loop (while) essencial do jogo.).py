import pygame

#pygame.init()

largura = 800
altura = 600

janela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("projeto pygame")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    janela.fill((255, 255, 255))

    pygame.draw.rect(janela, (255, 0, 0), (400, 300, 50, 50))

    pygame.display.update()