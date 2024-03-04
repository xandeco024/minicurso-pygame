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
jogadorYInicial = 100

jogadorLargura = 50
jogadorAltura = 100

jogadorRect = pygame.Rect(jogadorXInicial, jogadorYInicial, jogadorLargura, jogadorAltura) #cria um retangulo que representa o jogador
jogadorCor = (200, 105, 19)

#Criando o loop principal
rodando = True

clock = pygame.time.Clock()
fps = 180

while rodando: #enquanto rodando for verdadeiro, o jogo continuará rodando.

    #Verificando se o usuário clicou no botão de fechar a janela
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False #se clicou no botão de fechar a janela, rodando se torna falso e o jogo para de rodar.

    teclas = pygame.key.get_pressed() #pega todas as teclas, que estão sendo pressionadas ou não

    if teclas[pygame.K_LEFT] == True: #se a tecla esquerda estiver sendo pressionada
        jogadorRect.x -= 2 #mova o jogador para a esquerda

    if teclas[pygame.K_RIGHT] == True: #se a tecla direita estiver sendo pressionada
        jogadorRect.x += 2 #mova o jogador para a direita

    if teclas[pygame.K_UP] == True: #se a tecla cima estiver sendo pressionada
        jogadorRect.y -= 2 #mova o jogador para cima

    if teclas[pygame.K_DOWN] == True: #se a tecla baixo estiver sendo pressionada
        jogadorRect.y += 2 #mova o jogador para baixo


    #Preenchendo a tela com a cor branca, como apagando uma lousa.
    tela.fill((255, 255, 255))

    #Desenhando um retangulo na tela
    pygame.draw.rect(tela, jogadorCor, jogadorRect) #desenha na TELA, com a COR DO JOGADOR, um RETANGULO na POSIÇÃO DO JOGADOR, com sua ALTURA E LARGURA.

    #Atualizando a tela (como se você estivesse virando a pagina de um caderno)
    pygame.display.update()