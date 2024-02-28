import pygame
import random

#Colores
negro = (0,0,0)
blanco = (255,255,255)

#----------Clases------------
class Nave(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = nave
        self.rect = self.image.get_rect()
        self.rect.x = 334
        self.rect.y = 475
        self.velocidad = 0
            
    def update(self):
        self.rect.x += self.velocidad

    def izquierda(self):
        self.velocidad = -8
    
    def derecha(self):
        self.velocidad = 8
        
class Marciano(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = marciano
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0,753)
        self.rect.y = random.randint(-400, -40)

    def update(self):
        if marcador<50:
            self.rect.y += 2 
        else:
            self.rect.y += 4

class Laser(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = laser
        self.rect = self.image.get_rect()
        self.rect.x = nave_prota.rect.centerx
        self.rect.y = nave_prota.rect.centery
        self.velocidad = 0

    def update(self):
        self.rect.y -= 7

#Inicio pygame
pygame.init()

#Pantalla
size = (800,600)
pantalla = pygame.display.set_mode(size)
pygame.display.set_caption("Invasores")

#Listas para los sprites
lista_todos_sprites = pygame.sprite.Group()
lista_marcianos = pygame.sprite.Group()
lista_laser = pygame.sprite.Group()

#Carga de todas las imagenes
fondo = pygame.image.load("fondo_morado.png").convert()
fondo_escalado = pygame.transform.scale(fondo, (800, 600))
nave = pygame.image.load("nave.png").convert()
nave.set_colorkey(negro)
marciano = pygame.image.load("marciano.png").convert()
marciano.set_colorkey(negro)
laser = pygame.image.load("laser.png").convert()
laser.set_colorkey(negro)

#Musica y sonido laser
sonido_laser = pygame.mixer.Sound("audio_laser.ogg")
cancion = pygame.mixer.Sound("cancion_juego.wav")
cancion.play(-1) 

#Creacion de marcianos
for m in range(15):
    marcianos = Marciano()
    lista_todos_sprites.add(marcianos)
    lista_marcianos.add(marcianos)
    coincide_marciano=pygame.sprite.spritecollide(marcianos, lista_marcianos, False)
    while len(coincide_marciano)>1:
        marcianos.rect.x = random.randint(0,753)
        marcianos.rect.y = random.randint(-400, -40)
        coincide_marciano=pygame.sprite.spritecollide(marcianos, lista_marcianos, False)

#Creado el objeto de la clase nave y anadido a la lista de sprites
nave_prota = Nave()
lista_todos_sprites.add(nave_prota)
    
#Score
marcador = 0  

#Reloj
clock = pygame.time.Clock()

#------------Bucle principal del programa---------------
funcionando = True
while funcionando: 
    #-------------Eventos-------------------------------
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            funcionando = False
            print ("Has salido del juego.")
            print ("Marcador:"), marcador
        
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                nave_prota.izquierda()
            if evento.key == pygame.K_RIGHT:
                nave_prota.derecha()
            if evento.key == pygame.K_SPACE:
                sonido_laser.play()
                disparo = Laser()
                lista_laser.add(disparo)
                lista_todos_sprites.add(disparo)

        if evento.type == pygame.KEYUP:  
            if evento.key == pygame.K_LEFT:
                nave_prota.velocidad = 0
            if evento.key == pygame.K_RIGHT:
                nave_prota.velocidad = 0

    #----------------Logica del juego-----------------------               
    if nave_prota.rect.right >= 800:
        nave_prota.rect.right = 800
    if nave_prota.rect.left <= 0:
        nave_prota.rect.left = 0
    
    #Disparo
    for disparo in lista_laser:
        lista_marcianos_alcanzados = pygame.sprite.spritecollide(disparo, lista_marcianos, True)
        #Si alcanza a un marciano
        for marcianos in lista_marcianos_alcanzados:
            lista_laser.remove(disparo)
            lista_todos_sprites.remove(disparo)
            marcador += 1
            #Los marcianos se regeneran
            marcianos.rect.x = random.randint(0,753)
            marcianos.rect.y = random.randint(-300, -20)
            lista_todos_sprites.add(marcianos)
            lista_marcianos.add(marcianos)
            coincide_marciano=pygame.sprite.spritecollide(marcianos, lista_marcianos, False)
            while len(coincide_marciano)>1:
                marcianos.rect.x = random.randint(0,753)
                marcianos.rect.y = random.randint(-300, -20)
                coincide_marciano=pygame.sprite.spritecollide(marcianos, lista_marcianos, False)
        #Si el disparo sale de la pantalla
        if disparo.rect.y<0:
            lista_laser.remove(disparo)
            lista_todos_sprites.remove(disparo)
    
    #Si los marcianos salen de la pantalla
    for marcianos in lista_marcianos: 
        if marcianos.rect.y>600:
            marcianos.rect.x = random.randint(0,753)
            marcianos.rect.y = random.randint(-300, -20)
            coincide_marciano=pygame.sprite.spritecollide(marcianos, lista_marcianos, False)
            while len(coincide_marciano)>1:
                marcianos.rect.x = random.randint(0,753)
                marcianos.rect.y = random.randint(-300, -20)
                coincide_marciano=pygame.sprite.spritecollide(marcianos, lista_marcianos, False)
    
    #Cuando un marciano choca con la nave
    game_over = pygame.sprite.spritecollide(nave_prota, lista_marcianos, False)
    for colision in game_over:
        funcionando=False
        print ("Has perdido, te ha alcanzado un marciano.")
        print ("Marcador:"), marcador 


    lista_todos_sprites.update()

    #--------------Codigo de dibujo--------------------------
    #Imprime el fondo en la pantalla
    pantalla.blit(fondo_escalado,[0, 0])

    #Texto     
    fuente = pygame.font.Font(None,25)
    texto = fuente.render("Score: " + str(marcador), True, blanco)
    pantalla.blit(texto, [2, 575])
    
    #Carga en la pantalla y velocidad del juego
    lista_todos_sprites.draw(pantalla)
    pygame.display.flip()
    clock.tick(30)

pygame.quit()