import pygame

pygame.init()

largura = 1280
altura = 720

tela = pygame.display.set_mode((largura, altura)) #cria a janela com o tamanho especificado
pygame.display.set_caption('projeto pygame') ##define o nome da janela

gravidade = 0.9

class Jogador:
    def __init__(self, colisores, mundo):
        self.largura = 50
        self.altura = 100

        self.xInicial = 128
        self.yInicial = 640

        self.colisores = colisores
        self.mundo = mundo

        self.sprite = pygame.image.load("REPOSICAO SCRIPT ALUNOS/steve.png")
        self.sprite = pygame.transform.scale(self.sprite, (48, 96))
        self.correcao = [self.largura/2 - 24, self.altura - 96]
        self.olhandoParaDireita = True

        self.rect = pygame.Rect(self.xInicial, self.yInicial, self.largura, self.altura)
        self.cor = (135, 206, 235)

        self.movimento = [0 ,0]
        self.velocidade = 10
        self.forcaPulo = 15
        self.estaNoChao = False
        self.pulos = 2
        self.rect.x += self.velocidade

        self.moedas = 0

        self.dano = 1
        self.vidaMaxima = 5
        self.vidaAtual = self.vidaMaxima
        self.podeSerControlado = True
        self.levandoDano = False
        self.temporizadorKnockback = 0

        self.hurtSFX = pygame.mixer.Sound("Aula 9 (SOM)/SFX/dano.wav")
        self.dieSFX = pygame.mixer.Sound("Aula 9 (SOM)/SFX/inimigoMorte.wav")
        self.jumpSFX = pygame.mixer.Sound("Aula 9 (SOM)/SFX/pulo.wav")

    def Desenhar(self, superficie):
        superficie.blit(self.sprite, (self.rect.x + self.correcao[0], self.rect.y + self.correcao[1]))

    def DesenharColisor(self, superficie):
        pygame.draw.rect(superficie, self.cor, self.rect, 5)

    def Movimento(self):

        teclas = pygame.key.get_pressed()

        '''if teclas[pygame.K_w] == True:
            self.movimento[1] = -self.velocidade

        elif teclas[pygame.K_s] == True:
            self.movimento[1] = self.velocidade

        else:
            self.movimento[1] = 0'''
        
        #aplica o movimento Y no jogador
        self.rect.y += self.movimento[1]
        self.movimento[1] += gravidade

        for colisor in self.colisores:
            if self.rect.colliderect(colisor):

                if self.movimento[1] > 0:
                    self.rect.bottom = colisor.top
                    self.movimento[1] = 0
                    self.estaNoChao = True
                    self.pulos = 2

                if self.movimento[1] < 0:
                    self.rect.top = colisor.bottom
                    self.movimento[1] = 0

        if self.podeSerControlado == True:
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

        for colisor in self.colisores:
            if self.rect.colliderect(colisor):
                if self.movimento[0] > 0:
                    self.rect.right = colisor.left
                    self.movimento[0] = 0

                elif self.movimento[0] < 0:
                    self.rect.left = colisor.right
                    self.movimento[0] = 0

    def Pulo(self):
        if self.pulos > 0 and self.podeSerControlado == True:
            self.movimento[1] = -self.forcaPulo
            self.estaNoChao = False
            self.pulos -= 1
            self.jumpSFX.play()

    def RestringirAoMundo(self):
        larguraMundo = self.mundo.get_width()
        alturaMundo = self.mundo.get_height()

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > larguraMundo:
            self.rect.right = larguraMundo

        if self.rect.top < 0:
            self.rect.top = 0

        if self.rect.bottom > alturaMundo:
            self.rect.bottom = alturaMundo

    def LevarDano(self, dano):
        self.vidaAtual -= dano
        self.levandoDano = True
        self.podeSerControlado = False

        self.hurtSFX.play()

        self.movimento[1] = -10

        if self.olhandoParaDireita == True:
            self.movimento[0] = -10

        else:
            self.movimento[0] = 10

    def Morrer(self):
        self.rect.x = self.xInicial
        self.rect.y = self.yInicial
        self.vidaAtual = self.vidaMaxima
        self.levandoDano = False
        self.podeSerControlado = True
        self.temporizadorKnockback = 0
        self.dieSFX.play()

    def Atirar(self, objetos):
        projetil = ProjetilJogador(self, objetos)
        objetos.Adicionar(projetil)
        
    def Atualizar(self):
        self.Movimento()
        self.RestringirAoMundo()

        if self.levandoDano == True:
            self.temporizadorKnockback += 1

            if self.temporizadorKnockback > 8:
                self.levandoDano = False
                self.podeSerControlado = True
                self.temporizadorKnockback = 0

        if self.vidaAtual <= 0:
            self.Morrer()

class Tilemap:
    def __init__(self, colisores, mapa):
        self.colisores = colisores

        self.tamanhoTile = 64 #define a altura e largura de cada tile (porque é um quadrado)

        self.texturas = [
            '',
            pygame.transform.scale(pygame.image.load("REPOSICAO SCRIPT ALUNOS/grama.png"), (self.tamanhoTile, self.tamanhoTile)),
            pygame.transform.scale(pygame.image.load("REPOSICAO SCRIPT ALUNOS/terra.png"), (self.tamanhoTile, self.tamanhoTile))
        ]

        self.mapa = mapa

        self.superficieTilemap = pygame.Surface((len(self.mapa[0]) * self.tamanhoTile, len(self.mapa) * self.tamanhoTile))
        self.superficieTilemap.set_colorkey((0, 0, 0))


    def CriarTilemap(self):
        for linha in range(len(self.mapa)):
            for coluna in range(len(self.mapa[0])):
                if self.mapa[linha][coluna] != 0:
                    self.superficieTilemap.blit(self.texturas[self.mapa[linha][coluna]], (coluna * self.tamanhoTile, linha * self.tamanhoTile))
                    self.colisores.append(pygame.Rect(coluna * self.tamanhoTile, linha * self.tamanhoTile, self.tamanhoTile, self.tamanhoTile))

    def Desenhar(self, superficie):
        superficie.blit(self.superficieTilemap, (0, 0))

class CameraQueSegue():
    def __init__(self, alvo, superficieMundo):
        self.alvo = alvo
        self.superficieMundo = superficieMundo

        self.rect = pygame.Rect(0, 0, largura, altura)

        self.larguraMundo = superficieMundo.get_width() # 6400
        self.alturaMundo = superficieMundo.get_height() # 3200

    def Atualizar(self):
        self.rect.center = self.alvo.rect.center

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > self.larguraMundo:
            self.rect.right = self.larguraMundo

        if self.rect.top < 0:
            self.rect.top = 0

        if self.rect.bottom > self.alturaMundo:
            self.rect.bottom = self.alturaMundo

    def Mostrar(self, superficie):
        superficieCamera = self.superficieMundo.subsurface(self.rect)
        superficie.blit(superficieCamera, (0, 0))

class Espinho():
    def __init__(self, jogador, x, y):
        self.jogador = jogador
        
        self.largura = 64
        self.altura = 64

        self.sprite = pygame.image.load("Aula 6 (Camera e Combate 1)/espinho.png")
        self.sprite = pygame.transform.scale(self.sprite, (self.largura, self.altura))

        self.rect = pygame.Rect(x, y, self.largura, self.altura)

        self.dano = 1

    def Atualizar(self):
        if self.jogador.rect.colliderect(self.rect):
            self.jogador.LevarDano(self.dano) #faz o jogador levar 1 de dano.

    def Desenhar(self, superficie):
        superficie.blit(self.sprite, (self.rect.x, self.rect.y))

class Grupo:
    def __init__(self):
        self.lista = []

    def Adicionar(self, objeto):
        self.lista.append(objeto)

    def Remover(self, objeto):
        self.lista.remove(objeto)

    def Atualizar(self):
        for objeto in self.lista:
            if hasattr(objeto, 'Atualizar'):
                objeto.Atualizar()

    def Desenhar(self, superficie):
        for objeto in self.lista:
            if hasattr(objeto, 'Desenhar'):
                objeto.Desenhar(superficie)

class InimigoPatrulhador:
    def __init__(self, x, y, distancia, objetos):
        self.largura = 64
        self.altura = 128
        self.xInicial = x
        self.yInicial = y

        self.objetos = objetos

        self.rect = pygame.Rect(self.xInicial, self.yInicial, self.largura, self.altura)

        self.vida = 3
        self.dano = 1

        self.spriteOriginal = pygame.image.load("Aula 7 (Combate 2)/zombie.png")
        self.spriteOriginal = pygame.transform.scale(self.spriteOriginal, (self.largura, self.altura))

        self.spriteDano = pygame.image.load("Aula 7 (Combate 2)/zombie dano.png")
        self.spriteDano = pygame.transform.scale(self.spriteDano, (self.largura, self.altura))

        self.sprite = self.spriteOriginal

        self.indo = True
        self.velocidade = 3
        self.distancia = distancia

        self.temporizadorDano = 0
        self.levandoDano = False

        self.hurtSFX = pygame.mixer.Sound("Aula 9 (SOM)/SFX/dano.wav")
        self.dieSFX = pygame.mixer.Sound("Aula 9 (SOM)/SFX/inimigoMorte.wav")

    def Desenhar(self, superficie):
        superficie.blit(self.sprite, (self.rect.x, self.rect.y))

    def Atualizar(self):
        self.Movimento()

        for objeto in self.objetos.lista:
            if isinstance(objeto, Jogador):
                if self.rect.colliderect(objeto.rect):
                    objeto.LevarDano(self.dano)

        if self.vida <= 0:
            self.dieSFX.play()
            self.objetos.Remover(self)

        if self.levandoDano == True:
            self.temporizadorDano += 1

            if self.temporizadorDano > 10:
                self.sprite = self.spriteOriginal
                self.levandoDano = False
                self.temporizadorDano = 0

    def Movimento(self):
        if self.indo == True:
            self.rect.x += self.velocidade

            if self.rect.x >= self.xInicial + self.distancia:
                self.indo = False
                self.sprite = pygame.transform.flip(self.sprite, True, False)

        else:
            self.rect.x -= self.velocidade

            if self.rect.x <= self.xInicial:
                self.indo = True
                self.sprite = pygame.transform.flip(self.sprite, True, False)
        
    def LevarDano(self, dano):
        self.vida -= dano
        self.sprite = self.spriteDano
        self.levandoDano = True
        self.temporizadorDano = 0
        self.hurtSFX.play()

class ProjetilJogador:
    def __init__(self, jogador, objetos):
        self.largura = 32
        self.altura = 32

        self.jogador = jogador
        self.objetos = objetos

        self.rect = pygame.Rect(self.jogador.rect.x, self.jogador.rect.y, self.largura, self.altura)

        if self.jogador.olhandoParaDireita == True:
            self.direcao = 1

        else:
            self.direcao = -1

        #self.dano

        self.velocidade = 20
        self.tempoDeVida = 600

        self.sprite = pygame.image.load("Aula 7 (Combate 2)/projetil.png")
        self.sprite = pygame.transform.scale(self.sprite, (self.largura, self.altura))

        self.projectileSFX = pygame.mixer.Sound("Aula 9 (SOM)/SFX/tiro.wav")
        self.projectileSFX.play()

    def Desenhar(self, superficie):
        superficie.blit(self.sprite, (self.rect.x, self.rect.y))

    def Atualizar(self):
        if self.direcao == 1:
            self.rect.x += self.velocidade
        elif self.direcao == -1:
            self.rect.x -= self.velocidade

        self.tempoDeVida -= 1

        if self.tempoDeVida <= 0:
            print("i morreu")
            self.objetos.Remover(self)

        for objeto in self.objetos.lista:
            if isinstance(objeto, InimigoPatrulhador):
                if self.rect.colliderect(objeto.rect):
                    print("bateu!")
                    objeto.LevarDano(self.jogador.dano)
                    self.objetos.Remover(self)

class HUD:
    def __init__(self, jogador):
        self.jogador = jogador

        self.coracaoSprite = pygame.image.load("Aula 8 (HUD)/coracao.png")
        self.coracaoRect = pygame.Rect(32, 32, 64, 64)
        self.coracaoSprite = pygame.transform.scale(self.coracaoSprite, (64, 64))

        self.fonte = pygame.font.Font("Aula 8 (HUD)/Kenney Pixel Square.ttf", 32)

        self.moedaSprite = pygame.image.load("Aula 8 (HUD)/moeda.png")
        self.moedaSprite = pygame.transform.scale(self.moedaSprite, (64, 64))

    def Mostrar(self, superficie):
        for i in range(self.jogador.vidaAtual):
            superficie.blit(self.coracaoSprite, (self.coracaoRect.x + i * 96, self.coracaoRect.y))
        
        superficie.blit(self.moedaSprite, (32, 128))

        textoMoedas = self.fonte.render(str(self.jogador.moedas), False, (255, 255, 255))
        superficie.blit(textoMoedas, (100, 132))

class Moeda:
    def __init__(self, x, y, objetos):
        self.largura = 32
        self.altura = 32

        self.sprite = pygame.image.load("Aula 8 (HUD)/moeda.png")
        self.sprite = pygame.transform.scale(self.sprite, (self.largura, self.altura))

        self.objetos = objetos

        self.moedaEfeitoSonoro = pygame.mixer.Sound("Aula 9 (SOM)/SFX/moeda.wav")

        for objeto in self.objetos.lista:
            if isinstance(objeto, Jogador):
                self.jogador = objeto

        self.rect = pygame.Rect(x, y, self.largura, self.altura)

    def Desenhar(self, superficie):
        superficie.blit(self.sprite, self.rect)

    def Atualizar(self):
        if self.rect.colliderect(self.jogador.rect):
            self.jogador.moedas += 1
            self.moedaEfeitoSonoro.play()
            self.objetos.Remover(self)

class Portal:
    def __init__(self, x, y, jogador, faseDestino, gerenciadorDeFases):
        self.largura = 64
        self.altura = 128

        self.rect = pygame.Rect(x, y, self.largura, self.altura)
        self.corRect = (128, 0, 128)

        self.jogador = jogador
        self.faseDestino = faseDestino
        self.gerenciadorDeFases = gerenciadorDeFases

    def Desenhar(self, superficie):
        pygame.draw.rect(superficie, self.corRect, self.rect)
        #futuramente trocar por sprite do portal

    def Atualizar(self):
        if self.rect.colliderect(self.jogador.rect):
            self.gerenciadorDeFases.CarregarFase(self.faseDestino)

class Fase1:
    def __init__(self, gerenciadorDeFases):
        self.superficieMundo = pygame.Surface((64*100, 64*50))
        self.colisores = []
        self.grupoObjetos = Grupo()

        self.gerenciadorDeFases = gerenciadorDeFases

        self.jogador = Jogador(self.colisores, self.superficieMundo)
        self.grupoObjetos.Adicionar(self.jogador)

        self.mapa = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
            [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
            [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
            [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
            [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
            [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
            [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
            [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
            [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
            [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]
        ]

        self.tilemap = Tilemap(self.colisores, self.mapa)
        self.tilemap.CriarTilemap()
        self.grupoObjetos.Adicionar(self.tilemap)

        self.inimigo1 = InimigoPatrulhador(576, 832, 196, self.grupoObjetos)
        self.grupoObjetos.Adicionar(self.inimigo1)

        self.moeda1 = Moeda(576, 768, self.grupoObjetos)
        self.grupoObjetos.Adicionar(self.moeda1)

        self.portal = Portal(576, 832, self.jogador, "fase2", self.gerenciadorDeFases)
        self.grupoObjetos.Adicionar(self.portal)

        self.camera = CameraQueSegue(self.jogador, self.superficieMundo)
        self.grupoObjetos.Adicionar(self.camera)

        self.hud = HUD(self.jogador)
        self.grupoObjetos.Adicionar(self.hud)

        self.mixer = pygame.mixer

        self.mixer.music.load("Aula 9 (SOM)/BGM/musica1.mp3")
        self.mixer.music.set_volume(0.1)
        self.mixer.music.play(-1)

    def Atualizar(self):
        self.grupoObjetos.Atualizar()

    def Desenhar(self, superficie):
        superficie.fill((0, 0, 0))
        self.superficieMundo.fill((135, 206, 250))

        self.grupoObjetos.Desenhar(self.superficieMundo)

        self.camera.Mostrar(superficie)
        self.hud.Mostrar(superficie)

class Fase2:
    def __init__(self, gerenciadorDeFases):
        self.superficieMundo = pygame.Surface((64*100, 64*50))
        self.colisores = []
        self.grupoObjetos = Grupo()

        self.gerenciadorDeFases = gerenciadorDeFases

        self.jogador = Jogador(self.colisores, self.superficieMundo)
        self.grupoObjetos.Adicionar(self.jogador)

        self.mapa = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,1,0,0,0,0,0,0,2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
            [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
            [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
            [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
            [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
            [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
            [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
            [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
            [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2],
            [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]
        ]

        self.tilemap = Tilemap(self.colisores, self.mapa)
        self.tilemap.CriarTilemap()
        self.grupoObjetos.Adicionar(self.tilemap)

        self.inimigo1 = InimigoPatrulhador(576, 832, 196, self.grupoObjetos)
        self.grupoObjetos.Adicionar(self.inimigo1)

        self.moeda1 = Moeda(576, 768, self.grupoObjetos)
        self.grupoObjetos.Adicionar(self.moeda1)

        self.camera = CameraQueSegue(self.jogador, self.superficieMundo)
        self.grupoObjetos.Adicionar(self.camera)

        self.hud = HUD(self.jogador)
        self.grupoObjetos.Adicionar(self.hud)

        self.mixer = pygame.mixer

        self.mixer.music.load("Aula 9 (SOM)/BGM/musica1.mp3")
        self.mixer.music.set_volume(0.1)
        self.mixer.music.play(-1)

    def Atualizar(self):
        self.grupoObjetos.Atualizar()

    def Desenhar(self, superficie):
        superficie.fill((0, 0, 0))
        self.superficieMundo.fill((135, 206, 250))

        self.grupoObjetos.Desenhar(self.superficieMundo)

        self.camera.Mostrar(superficie)
        self.hud.Mostrar(superficie)

class GerenciadorDeFases:
    def __init__(self, faseInicial):
        self.faseAtual = self.CarregarFase(faseInicial)

    def CarregarFase(self, fase):

        if fase == "fase1":
            self.faseAtual = Fase1(self)

        elif fase == "fase2":
            self.faseAtual = Fase2(self)
        
        return self.faseAtual

gerenciadorDeFases = GerenciadorDeFases("fase1")

rodando = True
clock = pygame.time.Clock()

while rodando:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                gerenciadorDeFases.faseAtual.jogador.Pulo()

            if event.key == pygame.K_q:
                gerenciadorDeFases.faseAtual.jogador.Atirar(gerenciadorDeFases.faseAtual.grupoObjetos)

    gerenciadorDeFases.faseAtual.Atualizar()
    gerenciadorDeFases.faseAtual.Desenhar(tela)

    pygame.display.update() #atualiza a tela