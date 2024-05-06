import pygame

pygame.init()

windowWitdh = 800
windowHeight = 600

screen = pygame.display.set_mode((windowWitdh, windowHeight)) #cria a janela com o tamanho especificado
pygame.display.set_caption('projeto pygame') ##define o nome da janela

gravity = 0.9
collisions = []

class Player:
    def __init__(self):
        self.width = 50
        self.height = 100

        self.initialX = 100
        self.initialY = 100

        self.sprite = pygame.image.load("REPOSICAO SCRIPT ALUNOS/steve.png")
        self.sprite = pygame.transform.scale(self.sprite, (48, 96))
        self.spriteCorrection = [self.width/2 - 24, self.height - 96]
        self.facingRight = True

        self.rect = pygame.Rect(self.initialX, self.initialY, self.width, self.height)
        self.colliderColor = (135, 206, 235)

        self.movementAxis = [0 ,0]
        self.movementSpeed = 10
        self.jumpForce = 15
        self.grounded = False
        self.jumpAmount = 2
        self.rect.x += self.movementSpeed

    def Draw(self):
        screen.blit(self.sprite, (self.rect.x + self.spriteCorrection[0], self.rect.y + self.spriteCorrection[1]))

    def DrawCollider(self):
        pygame.draw.rect(screen, self.colliderColor, self.rect, 5)

    def Movement(self, colliders = []):

        keys = pygame.key.get_pressed()

        '''if teclas[pygame.K_w] == True:
            self.movimento[1] = -self.velocidade

        elif teclas[pygame.K_s] == True:
            self.movimento[1] = self.velocidade

        else:
            self.movimento[1] = 0'''
        
        #aplica o movimento Y no jogador
        self.rect.y += self.movementAxis[1]
        self.movementAxis[1] += gravity

        for colisor in colliders:
            if self.rect.colliderect(colisor):

                if self.movementAxis[1] > 0:
                    self.rect.bottom = colisor.top
                    self.movementAxis[1] = 0
                    self.grounded = True
                    self.jumpAmount = 2

                if self.movementAxis[1] < 0:
                    self.rect.top = colisor.bottom
                    self.movementAxis[1] = 0

        if keys[pygame.K_a] == True:
            self.movementAxis[0] = -self.movementSpeed

            if self.facingRight == True:
                self.sprite = pygame.transform.flip(self.sprite, True, False)
                self.facingRight = False

        elif keys[pygame.K_d] == True:
            self.movementAxis[0] = self.movementSpeed

            if self.facingRight == False:
                self.sprite = pygame.transform.flip(self.sprite, True, False)
                self.facingRight = True

        else:
            self.movementAxis[0] = 0

        #aplica o movimento X no jogador
        self.rect.x += self.movementAxis[0]

        for colisor in colliders:
            if self.rect.colliderect(colisor):
                if self.movementAxis[0] > 0:
                    self.rect.right = colisor.left
                    self.movementAxis[0] = 0

                elif self.movementAxis[0] < 0:
                    self.rect.left = colisor.right
                    self.movementAxis[0] = 0

    def Jump(self):
        if self.jumpAmount > 0:
            self.movementAxis[1] = -self.jumpForce
            self.grounded = False
            self.jumpAmount -= 1

class Tilemap:
    def __init__(self):
        self.tileSize = 64 #define a altura e largura de cada tile (porque é um quadrado)

        self.textures = [
            '',
            pygame.transform.scale(pygame.image.load("REPOSICAO SCRIPT ALUNOS/grama.png"), (self.tileSize, self.tileSize)),
            pygame.transform.scale(pygame.image.load("REPOSICAO SCRIPT ALUNOS/terra.png"), (self.tileSize, self.tileSize))
        ]

        self.map = [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [1,1,1,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,1,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
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


        self.tilemapSurface = pygame.Surface((len(self.map[0]) * self.tileSize, len(self.map) * self.tileSize))
        self.tilemapSurface.set_colorkey((0, 0, 0))


    def CreateTilemap(self):
        for row in range(len(self.map)):
            for column in range(len(self.map[0])):
                if self.map[row][column] != 0:
                    self.tilemapSurface.blit(self.textures[self.map[row][column]], (column * self.tileSize, row * self.tileSize))
                    collisions.append(pygame.Rect(column * self.tileSize, row * self.tileSize, self.tileSize, self.tileSize))

    def DrawTilemap(self):
        screen.blit(self.tilemapSurface, (0, 0))

player = Player()

tilemap = Tilemap()
tilemap.CreateTilemap()

running = True
clock = pygame.time.Clock()

while running:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.Jump()

    player.Movement(collisions)

    screen.fill((255, 255, 255))

    tilemap.DrawTilemap()
    
    player.DrawCollider()
    player.Draw() 

    pygame.display.update() #atualiza a tela