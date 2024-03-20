#Aula 2: Conhecendo o pygame.
#Compreendendo o loop principal, desenhos e eventos.

#Importando a biblioteca pygame
import pygame

#Inicializando os módulos do pygame (como se você estivesse ligando os interruptores da sua casa, os eletrodomesticos e etc... antes de começar a utiliza-la)
pygame.init()

#Definindo a largura e altura da tela
largura = 800
altura = 600

#Criando a tela e definindo o titulo.
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('projeto pygame')

#criando jogador
jogadorXInicial = 100
jogadorYInicial = 100

jogadorLargura = 32
jogadorAltura = 64

jogadorRect = pygame.Rect(jogadorXInicial, jogadorYInicial, jogadorLargura, jogadorAltura) #cria um retangulo que representa o jogador
jogadorCor = (200, 105, 19)

jogadorVelocidade = 10
forcaPulo = 10

movimentoJogador = [0, 0]

gravidade = 0.5

noChao = False

chaoRect = pygame.Rect(0, 500, 800, 100)
blocoRect = pygame.Rect(250, 300, 300, 100)

#Criando o loop principal
rodando = True

clock = pygame.time.Clock()
fps = 60

while rodando: #enquanto rodando for verdadeiro, o jogo continuará rodando.

    clock.tick(fps)

    #Verificando se o usuário clicou no botão de fechar a janela
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False #se clicou no botão de fechar a janela, rodando se torna falso e o jogo para de rodar.

    teclas = pygame.key.get_pressed() #pega todas as teclas, que estão sendo pressionadas ou não

    if teclas[pygame.K_a] == True: #se a tecla esquerda estiver sendo pressionada
        movimentoJogador[0] = -jogadorVelocidade

    elif teclas[pygame.K_d] == True: #se a tecla direita estiver sendo pressionada
        movimentoJogador[0] = jogadorVelocidade

    else:
        movimentoJogador[0] = 0

    if teclas[pygame.K_SPACE] == True and noChao == True:
        movimentoJogador[1] -= forcaPulo
        noChao = False
        print('pulou')


    #como será um jogo de plataforma, o jogador não se moverá livremente no eixo Y. tornando desnecessária essa parte do código.
    '''if teclas[pygame.K_UP] == True: #se a tecla cima estiver sendo pressionada
        movimentoJogador[1] = -velocidadeJogador

    elif teclas[pygame.K_DOWN] == True: #se a tecla baixo estiver sendo pressionada
        movimentoJogador[1] = velocidadeJogador

    else:
        movimentoJogador[1] = 0'''

    jogadorRect.x += movimentoJogador[0]

    if jogadorRect.colliderect(blocoRect) == True:
        jogadorCor = (0, 0, 255)

        if movimentoJogador[0] > 0: #colisão com a direita
            jogadorRect.x = blocoRect.x - jogadorRect.width
            movimentoJogador[0] = 0

        elif movimentoJogador[0] < 0: #esquerda
            jogadorRect.x = blocoRect.x + blocoRect.width
            movimentoJogador[0] = 0

    if not noChao:
        movimentoJogador[1] += gravidade

    jogadorRect.y += movimentoJogador[1]

    if jogadorRect.colliderect(blocoRect) == True:
        jogadorCor = (0, 0, 255)

        if movimentoJogador[1] > 0: #colisão com o chão
            jogadorRect.y = blocoRect.y - jogadorRect.height
            movimentoJogador[1] = 0

        elif movimentoJogador[1] < 0: #colisão com o teto
            jogadorRect.y = blocoRect.y + blocoRect.height
            movimentoJogador[1] = 0

    if jogadorRect.colliderect(chaoRect) == True:
        jogadorCor = (255, 0, 0)
        
        if movimentoJogador[1] > 0:
            jogadorRect.y = chaoRect.y - jogadorRect.height
            movimentoJogador[1] = 0   
            noChao = True #se o jogador está no chão, noChao é verdadeiro.

    print(movimentoJogador)

    tela.fill((255, 255, 255))

    pygame.draw.rect(tela, (100, 255, 100), chaoRect)
    pygame.draw.rect(tela, (100, 255, 255), blocoRect)

    pygame.draw.rect(tela, jogadorCor, jogadorRect)

    pygame.display.update()