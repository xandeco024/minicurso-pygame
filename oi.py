import pygame

#pygame.init()

largura = 800
altura = 600

flags = pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE
janela = pygame.display.set_mode((largura, altura), flags)
pygame.display.set_caption("projeto pygame")

jogadorLargura = 200
jogadorAltura = 100

jogadorX = 0
jogadorY = 0

jogadorCor = (255, 0, 0) #RGB, de 0 a 255

jogadorRect = pygame.Rect(jogadorX, jogadorY, jogadorLargura, jogadorAltura)

rodando = True

while rodando == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    pygame.draw.rect(janela, jogadorCor, jogadorRect)

    pygame.display.update()

    