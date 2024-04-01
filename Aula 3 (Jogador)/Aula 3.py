import pygame

pygame.init()

largura = 800
altura = 600

tela = pygame.display.set_mode((largura, altura)) #cria a janela com o tamanho especificado
pygame.display.set_caption('projeto pygame') ##define o nome da janela

class Jogador:
    def __init__(self, usaSetas):
        self.largura = 50
        self.altura = 100

        self.xInicial = 100
        self.yInicial = 100

        self.rect = pygame.Rect(self.xInicial, self.yInicial, self.largura, self.altura)
        self.cor = (135, 206, 235)

        self.velocidade = 10

        self.usaSetas = usaSetas

    def Desenhar(self):
        pygame.draw.rect(tela, self.cor, self.rect)

    def Movimento(self):

        teclas = pygame.key.get_pressed()

        if self.usaSetas:
            if teclas[pygame.K_UP] == True:
                self.rect.y -= self.velocidade

            if teclas[pygame.K_LEFT] == True:
                self.rect.x -= self.velocidade

            if teclas[pygame.K_DOWN] == True:
                self.rect.y += self.velocidade

            if teclas[pygame.K_RIGHT] == True:
                self.rect.x += self.velocidade
        else:
            if teclas[pygame.K_w] == True:
                self.rect.y -= self.velocidade

            if teclas[pygame.K_a] == True:
                self.rect.x -= self.velocidade

            if teclas[pygame.K_s] == True:
                self.rect.y += self.velocidade

            if teclas[pygame.K_d] == True:
                self.rect.x += self.velocidade

class JogadorSetinha:
    def __init__(self):
        self.largura = 50
        self.altura = 100

        self.xInicial = 100
        self.yInicial = 100

        self.rect = pygame.Rect(self.xInicial, self.yInicial, self.largura, self.altura)
        self.cor = (255, 206, 235)

        self.velocidade = 10

    def Desenhar(self):
        pygame.draw.rect(tela, self.cor, self.rect)

    def Movimento(self):

        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_UP] == True:
            self.rect.y -= self.velocidade

        if teclas[pygame.K_LEFT] == True:
            self.rect.x -= self.velocidade

        if teclas[pygame.K_DOWN] == True:
            self.rect.y += self.velocidade

        if teclas[pygame.K_RIGHT] == True:
            self.rect.x += self.velocidade

jogadorClaudio = Jogador(False)
jogadorPedro = Jogador(True)
jogadorBernardo = JogadorSetinha()

rodando = True
clock = pygame.time.Clock()

while rodando:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                print('espaço pressionado')

            if event.key == pygame.K_w:
                print('w pressionado')
            
            if event.key == pygame.K_a:
                print('a pressionado')

            if event.key == pygame.K_s:
                print('s pressionado')

            if event.key == pygame.K_d:
                print('d pressionado')
                
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                print('botão esquerdo do mouse pressionado')

            if event.button == 2:
                print('botão do meio do mouse pressionado')

            if event.button == 3:
                print('botão direito do mouse pressionado')

            #verificar WASD

    jogadorClaudio.Movimento()
    jogadorPedro.Movimento()

    tela.fill((255, 255, 255))

    jogadorClaudio.Desenhar()
    jogadorPedro.Desenhar()

    pygame.display.update() #atualiza a tela