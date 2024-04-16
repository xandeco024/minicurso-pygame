import pygame

pygame.init()

largura = 800
altura = 600

tela = pygame.display.set_mode((largura, altura)) #cria a janela com o tamanho especificado
pygame.display.set_caption('projeto pygame') ##define o nome da janela

class Jogador:
    def __init__(self, usaSetas):
        self.largura = 50
        self.largura = 50
        self.altura = 100

        self.xInicial = 100
        self.yInicial = 100

        self.rect = pygame.Rect(self.xInicial, self.yInicial, self.largura, self.altura)
        self.cor = (135, 206, 235)

        self.movimento = [0, 0]
        self.velocidade = 10

        self.usaSetas = usaSetas

    def Desenhar(self):
        pygame.draw.rect(tela, self.cor, self.rect)

    def Movimento(self):

        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_a] == True:
            self.movimento[0] = -self.velocidade
        
        elif teclas[pygame.K_d] == True:
            self.movimento[0] = self.velocidade

        else:
            self.movimento[0] = 0

        if teclas[pygame.K_w] == True:
            self.movimento[1] = -self.velocidade

        elif teclas[pygame.K_s] == True:
            self.movimento[1] = self.velocidade

        else:
            self.movimento[1] = 0

        self.rect.x += self.movimento[0]
        self.rect.y += self.movimento[1]


jogadorClaudio = Jogador(False)

blocoRect = pygame.Rect(250, 200, 300, 200)

rodando = True
clock = pygame.time.Clock()

while rodando:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    jogadorClaudio.Movimento()
    #jogadorPedro.Movimento()

    tela.fill((255, 255, 255))

    if jogadorClaudio.rect.colliderect(blocoRect):

        jogadorClaudio.cor = (255, 0, 0)

        if jogadorClaudio.movimento[0] > 0:
            jogadorClaudio.rect.right = blocoRect.left
            jogadorClaudio.movimento[0] = 0

        elif jogadorClaudio.movimento[0] < 0:
            jogadorClaudio.rect.left = blocoRect.right
            jogadorClaudio.movimento[0] = 0

    else:
        jogadorClaudio.cor = (135, 206, 235)

    #escreve na tela o valor da variável movimento com o pygame.font
    fonte = pygame.font.Font(None, 100)
    texto = fonte.render(str(jogadorClaudio.movimento), True, (0, 0, 0))
    tela.blit(texto, (600, 250))

    pygame.draw.rect(tela, (0, 255, 0), blocoRect)
    jogadorClaudio.Desenhar()
    #jogadorPedro.Desenhar()

    pygame.display.update() #atualiza a tela