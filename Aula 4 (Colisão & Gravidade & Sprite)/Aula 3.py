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

        self.sprite = pygame.image.load("Aula 4 (Colisão & Gravidade & Sprite)/sanic.png")
        self.sprite = pygame.transform.scale(self.sprite, (96, 96))
        self.correcao = [self.largura/2 - 48, self.altura - 96]
        self.olhandoParaDireita = True

        self.rect = pygame.Rect(self.xInicial, self.yInicial, self.largura, self.altura)
        self.cor = (135, 206, 235)

        self.movimento = [0 ,0]
        self.velocidade = 10

        self.usaSetas = usaSetas

    def Desenhar(self):
        tela.blit(self.sprite, (self.rect.x + self.correcao[0], self.rect.y + self.correcao[1]))

    def DesenharColisor(self):
        pygame.draw.rect(tela, self.cor, self.rect, 5)

    def Movimento(self, colisores = []):

        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_w] == True:
            self.movimento[1] = -self.velocidade

        elif teclas[pygame.K_s] == True:
            self.movimento[1] = self.velocidade

        else:
            self.movimento[1] = 0

        print(self.movimento)
        #aplica o movimento Y no jogador
        self.rect.y += self.movimento[1]

        for colisor in colisores:
            if self.rect.colliderect(colisor):
                print("colidiu")

                if self.movimento[1] > 0:
                    self.rect.bottom = colisor.top
                    self.movimento[1] = 0

                if self.movimento[1] < 0:
                    self.rect.top = colisor.bottom
                    self.movimento[1] = 0

        if teclas[pygame.K_a] == True:
            self.movimento[0] = -self.velocidade

            if self.olhandoParaDireita == True:
                self.sprite = pygame.transform.flip(self.sprite, True, False)
                self.olhandoParaDireita = False

        elif teclas[pygame.K_d] == True:
            self.movimento[0] = self.velocidade

            if self.olhandoParaDireita == False:
                self.sprite = pygame.transform.flip(self.sprite, True, False)
                self.olhandoParaDireita = True

        else:
            self.movimento[0] = 0

        #aplica o movimento X no jogador
        self.rect.x += self.movimento[0]

jogadorClaudio = Jogador(False)

chao = pygame.Rect(0, 300, 500, 100)

rodando = True
clock = pygame.time.Clock()

while rodando:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    jogadorClaudio.Movimento([chao])

    tela.fill((255, 255, 255))

    #desenha o chao provisório 
    pygame.draw.rect(tela, (0, 255, 0), chao) 

    jogadorClaudio.DesenharColisor()
    jogadorClaudio.Desenhar() 

    pygame.display.update() #atualiza a tela