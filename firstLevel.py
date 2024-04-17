from mainScript import getValues , pygame , screen , color , Text , clock , width , height , fps , key_left , key_right , my_font , lvl_start , storeValues , lvl_end , antialiasing , getScore , saveScore , saveLevel

obj_height = height - 88
last_obj_colision = None 
move_right = True 
move_left = True
allowJump = True

#clasa Player pentru toate functiile legate de player , de la move , pos , jump , vel etc
class Player:
    global obj_height , color , lvl_start , allowJump
     
    #initializare playerului 
    def __init__(self, x , y):

        #imaginea playerului si date caracteristice lui 
        self.image_source_player = pygame.image.load("image_caracters\\caracter.png").convert_alpha()
        self.playerRect = pygame.Rect(x , y , 32 , 64)
        self.velX = 0
        self.left_key = False
        self.right_key = False 
        self.isJump = False 
        self.isFall = False
        self.fallSpeed = -1
        self.speed = 6
        self.jumpSpeed = 8
        self.player_score = 0
        
    def draw(self , screen):
        #prindem playerul de ecran
        screen.blit(self.image_source_player , self.playerRect)
    
    #actualizam valorile de jump , fall , x , y ale playerului 
    def update(self):
        global allowJump , obj_height , in_colision

        self.velX = 0
        
        #miscare la stanga
        if self.left_key and not self.right_key:
            self.velX = -self.speed 

        #miscare la dreapta
        if self.right_key and not self.left_key:
            self.velX = self.speed
        
        #atunci cand playerul sare
        if self.isJump:

            if self.jumpSpeed >= 0:
                self.playerRect.y -= (self.jumpSpeed * abs(self.jumpSpeed)) * 0.35 #controlam cat de sus sarim
                self.jumpSpeed -= 0.20 #este viteza de scadere
            else:
                self.jumpSpeed = 8
                self.isJump = False
                self.isFall = True

            if self.playerRect.top <= 0:
                self.jumpSpeed = 8
                self.isJump = False
                self.isFall = True

        #atunci cand playerul cade
        if self.isFall:
            allowJump = False

            if self.fallSpeed >= -20:
                self.playerRect.y -= (self.fallSpeed * abs(self.fallSpeed)) * 0.15
                self.fallSpeed -= 0.15
            else:
                self.fallSpeed = -1
                self.isFall = False
                allowJump = True
            
            if self.playerRect.bottom >= obj_height:
                self.playerRect.bottom = obj_height
                self.fallSpeed = -1
                self.isFall = False
                allowJump = True
            
        self.playerRect.x += self.velX
    
    #coliziunea playerului cu alte obiect(teren)
    def playerColision(self , vector):
        global move_right , move_left , obj_height , last_obj_colision

        i = None #aici cautam daca suntem in coliziune cu vre un obiect din vector
        for k in range(0 , len(vector)):
            if self.playerRect.colliderect(vector[k]):
                i = k; break

        if i is not None:
            
            #coliziune la stanga obiectui
            if self.playerRect.right >= vector[i].left and self.playerRect.left < vector[i].left and self.playerRect.bottom <= vector[i].bottom and self.playerRect.top > vector[i].top:
                self.playerRect.right = vector[i].left - 2
                move_right = False; self.right_key = False
            
            #coliziune la dreapta obictului 
            if self.playerRect.left <= vector[i].right and self.playerRect.right > vector[i].right and self.playerRect.bottom <= vector[i].bottom and self.playerRect.top > vector[i].top:
                self.playerRect.left = vector[i].right + 2
                move_left = False; self.left_key = False
            
            #coliziune deasupra obiectului
            if (self.playerRect.bottom >= vector[i].top) and self.playerRect.right > vector[i].left  and self.playerRect.left < vector[i].right:
                obj_height = vector[i].top
                last_obj_colision = vector[i]

            #coliziune sub obiect
            if (self.playerRect.top <= vector[i].bottom and self.playerRect.top > vector[i].top) and self.playerRect.right > vector[i].left and self.playerRect.left < vector[i].right: 
                self.playerRect.top = vector[i].bottom; obj_height = height - 25; self.isJump = False; self.jumpSpeed = 8
                self.isFall = True

        else: #daca nu mai suntem in coliziune cu nici un obiect

            move_right = True
            move_left = True
            obj_height = height - 25

            if last_obj_colision is not None:

                if not(self.isJump) and (self.playerRect.right < last_obj_colision.left or self.playerRect.left > last_obj_colision.right):
        
                    self.isFall = True
                    last_obj_colision = None

#functia Game() pentru fiecare nivel 
def Game():

    global screen , width , height , fps, color , obj_height , move_left ,move_right , allowJump , key_left , key_right , antialiasing, lvl_start , lvl_end , getScore , saveScore , saveLevel

    default_values = getValues()
    try:

        width = int(default_values[0][0])
        height = int(default_values[0][1])
        fps = int(default_values[0][2])
        key_left = default_values[0][3]
        key_right = default_values[0][4]
        lvl_start = default_values[0][5]
        lvl_end = default_values[0][6]
        antialiasing = default_values[0][7]
    except:

        width = int(1920)
        height = int(1080)
        fps = int(60)
        key_left = "A"
        key_right = "D"
        lvl_start = "1"
        lvl_end = "3"
        antialiasing = "YES"
    
    #unde se gaseste playerul la inceput
    player = Player(25 , height - 88)
    allowJump = True 

    #fontul pentru obiectele text
    my_font = pygame.font.SysFont('Arial', 30)

    #imaginea punctelor de pe harta
    points_image = pygame.image.load("image_objects\\money1.png").convert_alpha()

    #imaginile scenelor de pe harta
    scenes = [pygame.image.load("level[1]\\scene1.png").convert_alpha() , pygame.image.load("level[1]\\scene2.png").convert_alpha() , pygame.image.load("level[1]\\scene3.png").convert_alpha() , pygame.image.load("level[1]\\scene4.png").convert_alpha() , pygame.image.load("level[1]\\scene5.png").convert_alpha() , pygame.image.load("level[1]\\scene6.png").convert_alpha() , pygame.image.load("level[1]\\scene7.png").convert_alpha() , pygame.image.load("level[1]\\scene8.png").convert_alpha() , pygame.image.load("level[1]\\scene9.png").convert_alpha() , pygame.image.load("level[1]\\scene10.png").convert_alpha()]
    scenes_counter = 0; max_scene = 9

    #fiecare obiect de pe harta(teren)
    scene1_objects = [pygame.Rect(960,960,96,96),pygame.Rect(1152,768,96*4,96),pygame.Rect(1728,672,96*2,96*4)]
    scene2_objects = [pygame.Rect(0,672,96*8,96),pygame.Rect(0,768,96*11,96),pygame.Rect(0,864,96*5,96*2),pygame.Rect(1152,960,96,96),pygame.Rect(1056,480,96*3,96),pygame.Rect(1440,288,96*3,96),pygame.Rect(1824,288,96,96*8)]
    scene3_objects = [pygame.Rect(0,288,96,96*8),pygame.Rect(96,480,96,96*6),pygame.Rect(288,288,96,96),pygame.Rect(480,288,96,96),pygame.Rect(288,576,96,96),pygame.Rect(288,960,96*3,96),pygame.Rect(384,864,96,96),pygame.Rect(576,672,96,96*4),pygame.Rect(672,288,96,96*8),pygame.Rect(960,0,96,96*6),pygame.Rect(864,576,96*3,96),pygame.Rect(768,288,96,96),pygame.Rect(1248,960,96*2,96),pygame.Rect(1440,864,96*5,96*2),pygame.Rect(1632,384,96*3,96),pygame.Rect(1824,0,96,96*4),pygame.Rect(1248,768,96,96*2),pygame.Rect(1344,480,96*2,96),pygame.Rect(1824,672,96,96*2)]
    scene4_objects = [pygame.Rect(0,672,96*3,96),pygame.Rect(0,768,96,96*3),pygame.Rect(288,864,96,96*2),pygame.Rect(384,576,96,96),pygame.Rect(576,480,96,96),pygame.Rect(864,480,96,96),pygame.Rect(1152,672,96*8,96),pygame.Rect(1248,768,96*7,96),pygame.Rect(1248,0,96,96*6),pygame.Rect(1344,480,96*3,96),pygame.Rect(1824,0,96,96*7),pygame.Rect(1440,288,96,96),pygame.Rect(1536,192,96,96),pygame.Rect(1824,1056,96,96)]
    scene5_objects = [pygame.Rect(25,1080,60,24),pygame.Rect(0,672,96*3,96),pygame.Rect(0,0,96,96*7),pygame.Rect(384,864,96,96*2),pygame.Rect(288,384,96,96),pygame.Rect(576,288,96*2,96),pygame.Rect(864,768,96,96*3),pygame.Rect(768,960,96,96),pygame.Rect(1152,672,96*2,96),pygame.Rect(1152,576,96,96),pygame.Rect(1344,768,96*3,96),pygame.Rect(1632,672,96,96),pygame.Rect(1824,768,96,96*3),pygame.Rect(1728,576,96*2,96*2)]
    scene6_objects = [pygame.Rect(0,576,96*2,96*5),pygame.Rect(192,480,96,96*6),pygame.Rect(384,768,96*4,96),pygame.Rect(480,384,96,96*4),pygame.Rect(576,576,96,96*2),pygame.Rect(960,768,96*2,96),pygame.Rect(1152,960,96,96),pygame.Rect(768,288,96*3,96),pygame.Rect(1152,288,96,96),pygame.Rect(1344,288,96,96),pygame.Rect(1536,288,96,96),pygame.Rect(1824,288,96,96*8)]
    scene7_objects = [pygame.Rect(0,288,96*3,96*8),pygame.Rect(288,768,96,96),pygame.Rect(576,576,96,96),pygame.Rect(672,384,96*2,96*7),pygame.Rect(864,768,96,96),pygame.Rect(1152,576,96,96),pygame.Rect(1248,480,96*2,96*6),pygame.Rect(1440,768,96,96),pygame.Rect(1728,672,96,96),pygame.Rect(1824,576,96,96*5)]
    scene8_objects = [pygame.Rect(0,576,96,96*5),pygame.Rect(384,0,96,96*9),pygame.Rect(672,864,96,96*2),pygame.Rect(768,672,96*2,96),pygame.Rect(1152,672,96,96),pygame.Rect(1536,672,96*2,96),pygame.Rect(1728,480,96,96),pygame.Rect(1440,288,96*2,96),pygame.Rect(1152,288,96,96),pygame.Rect(960,288,96,96),pygame.Rect(480,288,96*2,96),pygame.Rect(1824,192,96,96*9)]
    scene9_objects = [pygame.Rect(0,192,96,96*9),pygame.Rect(288,960,96*4,96),pygame.Rect(480,864,96,96),pygame.Rect(672,672,96*2,96),pygame.Rect(1152,576,96*2,96),pygame.Rect(1824,480,96,96*6),pygame.Rect(1536,384,96*4,96)]
    scene10_objects= [pygame.Rect(0,384,96,96*7),pygame.Rect(96,672,96*2,96),pygame.Rect(288,960,96,96),pygame.Rect(384,576,96,96*2),pygame.Rect(768,672,96,96),pygame.Rect(1152,672,96*4,96*4),pygame.Rect(1440,384,96*4,96),pygame.Rect(1728,672,96*2,96*4),pygame.Rect(1728,480,96,96*2),pygame.Rect(1536,960,96*2,96)]

    #fiecare obiect de pe harta(puncte)
    scene1_points = []
    scene2_points = [pygame.Rect(576,960,96,96)]
    scene3_points = [pygame.Rect(192,960,96,96),pygame.Rect(1728,288,96,96)]
    scene4_points = [pygame.Rect(1536,96,96,96)]
    scene5_points = [pygame.Rect(1632,960,96,96),pygame.Rect(672,192,96,96)]
    scene6_points = [pygame.Rect(1344,192,96,96)]
    scene7_points = [pygame.Rect(864,672,96,96)]
    scene8_points = [pygame.Rect(480,192,96,96)]
    scene9_points = []
    scene10_points= [pygame.Rect(576,384,96,96)]

    scenes_vector = [scene1_objects, scene2_objects, scene3_objects , scene4_objects , scene5_objects , scene6_objects , scene7_objects , scene8_objects , scene9_objects , scene10_objects]
    scenes_points = [scene1_points,scene2_points,scene3_points,scene4_points,scene5_points,scene6_points,scene7_points,scene8_points,scene9_points,scene10_points] # vor fi toate stelutele pentru toate scenele
    while True:
        
        screen.blit(scenes[scenes_counter], (0, 0))
 
        for event in pygame.event.get():
            
            if event.type == pygame.KEYDOWN:

                if event.key == ord(str(key_left)) and move_left:
                    player.left_key = True

                if event.key == ord(str(key_right)) and move_right:
                    player.right_key = True
                    
                if event.key == ord(' ') and allowJump:
                    player.isJump = True

                if event.key == pygame.K_ESCAPE:
                    return 0

            if event.type == pygame.KEYUP:

                if event.key == ord(str(key_left)):
                    player.left_key = False

                if event.key == ord(str(key_right)):
                    player.right_key = False
        
        #coliziunea cu punctele pe harta si actualizarea scorului
        for k in range(0 , len(scenes_points[scenes_counter])):
            if scenes_points[scenes_counter][k] is not None:
                if player.playerRect.colliderect(scenes_points[scenes_counter][k]):
                    player.player_score += 1; scenes_points[scenes_counter][k] = None; break

        #prindem imaginile punctelor pe ecran
        for k in range(0 , len(scenes_points[scenes_counter])):
            if scenes_points[scenes_counter][k] is not None:
                screen.blit(points_image , scenes_points[scenes_counter][k])

        #verificam trecerea de la o scena la alta si actualizarea corespunzatoare a variabilei scene_counter
        if player.playerRect.x < 0 and scenes_counter >= 1:
            
            scenes_counter = scenes_counter - 1
            size = len(scenes_vector[scenes_counter]) - 1
            player.playerRect.right = scenes_vector[scenes_counter][size].right - 10
            player.playerRect.bottom = scenes_vector[scenes_counter][size].top

        if player.playerRect.right >= width and scenes_counter != 9:

            scenes_counter = scenes_counter + 1
            player.playerRect.x = scenes_vector[scenes_counter][0].x
            player.playerRect.bottom = scenes_vector[scenes_counter][0].top
        elif player.playerRect.colliderect(scene10_objects[9]) and scenes_counter == max_scene:
            
            #de odata ce playerul ajunge la finalul primului nivel se salveaza scorul in db si ca novelul este terminat
            saveScore(str(player.player_score))
            saveLevel(str(int(lvl_start) + 1))

            #trecem la nivelul 2
            import secondLevel; secondLevel.Game(); return 0
        
        #apel la functia update din Player class
        player.update()
        #apel la functia draw din Player class
        player.draw(screen)
        #apel la functia playerColision din Player class
        player.playerColision(scenes_vector[scenes_counter])
        
        #scorul afisat pe ecran
        Text.displayText("SCORE: " + str(player.player_score) , width - 250, 50 , color[0] , screen , my_font)
        
        #actualizarea ecranului
        pygame.display.flip()

        #ceasul jocului, FPS
        clock.tick(int(fps))
