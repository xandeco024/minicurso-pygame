#Aula 1: Conhecendo o pygame.
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
jogadorYInicial = 300

jogadorLargura = 50
jogadorAltura = 100

jogadorRect = pygame.Rect(jogadorXInicial, jogadorYInicial, jogadorLargura, jogadorAltura) #cria um retangulo que representa o jogador
jogadorCor = (200, 105, 19)

jogadorVelocidade = 10
jogadorEixos = [0, 0]

forcaPulo = 20
noChao = False

gravidade = 1


blocoRect = pygame.Rect(0, 500, 700, 100)
blocoCor = (100, 100, 255)

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

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and noChao == True:
                #pula
                noChao = False
                jogadorEixos[1] -= forcaPulo

    teclas = pygame.key.get_pressed() #pega todas as teclas, que estão sendo pressionadas ou não

    if teclas[pygame.K_RIGHT] == True: #se a tecla direita estiver sendo pressionada
        #jogadorRect.x += jogadorVelocidade #mova o jogador para a direita
        jogadorEixos[0] = jogadorVelocidade

    elif teclas[pygame.K_LEFT] == True: #se a tecla esquerda estiver sendo pressionada
        #jogadorRect.x -= jogadorVelocidade #mova o jogador para a esquerda
        jogadorEixos[0] = -jogadorVelocidade

    else:
        jogadorEixos[0] = 0

    '''if teclas[pygame.K_SPACE] == True and noChao == True:
        #pula
        noChao = False
        jogadorEixos[1] -= forcaPulo'''

    '''if teclas[pygame.K_UP] == True: #se a tecla cima estiver sendo pressionada
        #jogadorRect.y -= jogadorVelocidade #mova o jogador para cima
        jogadorEixos[1] = -jogadorVelocidade

    elif teclas[pygame.K_DOWN] == True: #se a tecla baixo estiver sendo pressionada
        #jogadorRect.y += jogadorVelocidade #mova o jogador para baixo
        jogadorEixos[1] = jogadorVelocidade

    else:
        jogadorEixos[1] = 0'''

    jogadorRect.x += jogadorEixos[0]

    if jogadorRect.colliderect(blocoRect):
        if jogadorEixos[0] > 0:
            jogadorRect.right = blocoRect.left
        elif jogadorEixos[0] < 0:
            jogadorRect.left = blocoRect.right    
 
    if not noChao:
        jogadorEixos[1] += gravidade

    jogadorRect.y += jogadorEixos[1]

    if jogadorRect.colliderect(blocoRect):
        if jogadorEixos[1] > 0:
            jogadorRect.bottom = blocoRect.top
            jogadorEixos[1] = 0
            noChao = True
        elif jogadorEixos[1] < 0:
            jogadorRect.top = blocoRect.bottom


    if jogadorRect.colliderect(blocoRect):
        jogadorCor = (255, 0, 0)

    else:
        jogadorCor = (200, 105, 19)

    #print(jogadorEixos)
    print(noChao)

    #Preenchendo a tela com a cor branca, como apagando uma lousa.
    tela.fill((255, 255, 255))

    pygame.draw.rect(tela, blocoCor, blocoRect)

    #Desenhando um retangulo na tela
    pygame.draw.rect(tela, jogadorCor, jogadorRect) #desenha na TELA, com a COR DO JOGADOR, um RETANGULO na POSIÇÃO DO JOGADOR, com sua ALTURA E LARGURA.

    #Atualizando a tela (como se você estivesse virando a pagina de um caderno)
    pygame.display.update()