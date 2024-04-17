from mainScript import getValues , pygame , screen , color , Text , clock , width , height , fps , key_left , key_right , my_font , lvl_start , storeValues , lvl_end , antialiasing , getScore , saveScore , saveLevel

obj_height = height - 88
last_obj_colision = None
move_right = True 
move_left = True
allowJump = True

class Player:
    global obj_height , color , lvl_start
     
    def __init__(self, x , y):

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
        screen.blit(self.image_source_player , self.playerRect)
        
    def update(self):
        global allowJump , OnObjectHight , onObject , obj_height , in_colision

        self.velX = 0

        if self.left_key and not self.right_key:
            self.velX = -self.speed 

        if self.right_key and not self.left_key:
            self.velX = self.speed
            
        if self.isJump:

            if self.jumpSpeed >= 0: 
                self.playerRect.y -= (self.jumpSpeed * abs(self.jumpSpeed)) * 0.35 
                self.jumpSpeed -= 0.20 
            else:
                self.jumpSpeed = 8
                self.isJump = False
                self.isFall = True

            if self.playerRect.top <= 0:
                self.jumpSpeed = 8
                self.isJump = False
                self.isFall = True

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
    
    def playerColision(self , vector):
        global move_right , move_left , obj_height , last_obj_colision

        i = None
        for k in range(0 , len(vector)):
            if self.playerRect.colliderect(vector[k]):
                i = k; break

        if i is not None:

            if self.playerRect.right >= vector[i].left and self.playerRect.left < vector[i].left and self.playerRect.top > vector[i].top - 20 and self.playerRect.bottom <= vector[i].bottom: 
                self.playerRect.right = vector[i].left - 2
                move_right = False; self.right_key = False
            
            if self.playerRect.left <= vector[i].right and self.playerRect.right > vector[i].right and self.playerRect.top > vector[i].top - 20 and self.playerRect.bottom <= vector[i].bottom: 
                self.playerRect.left = vector[i].right + 2
                move_left = False; self.left_key = False
            
            if (self.playerRect.bottom >= vector[i].top) and self.playerRect.right > vector[i].left  and self.playerRect.left < vector[i].right: 
                obj_height = vector[i].top
                last_obj_colision = vector[i]

            if (self.playerRect.top <= vector[i].bottom and self.playerRect.top > vector[i].top) and self.playerRect.right > vector[i].left and self.playerRect.left < vector[i].right: 
                self.playerRect.top = vector[i].bottom; obj_height = height - 25; self.isJump = False; self.jumpSpeed = 8
                self.isFall = True

        else:

            move_right = True
            move_left = True
            obj_height = height - 25

            if last_obj_colision is not None:

                if not(self.isJump) and (self.playerRect.right < last_obj_colision.left or self.playerRect.left > last_obj_colision.right):
        
                    self.isFall = True
                    last_obj_colision = None

def Game():

    global screen , width , height , fps, color , obj_height , move_left ,move_right , allowJump , key_left , key_right , antialiasing, lvl_start , lvl_end , getScore , saveScore , saveLevel , obj_height

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
        lvl_start = "3"
        lvl_end = "3"
        antialiasing = "YES"

    player = Player(25 , height - 88)
    allowJump = True
    my_font = pygame.font.SysFont('Arial', 30)

    points_image = pygame.image.load("image_objects\\money3.png").convert_alpha()
    scenes = [pygame.image.load("level[3]\\scene1.png").convert_alpha(),pygame.image.load("level[3]\\scene2.png").convert_alpha(),pygame.image.load("level[3]\\scene3.png").convert_alpha(),pygame.image.load("level[3]\\scene4.png").convert_alpha(),pygame.image.load("level[3]\\scene5.png").convert_alpha(),pygame.image.load("level[3]\\scene6.png").convert_alpha(),pygame.image.load("level[3]\\scene7.png").convert_alpha(),pygame.image.load("level[3]\\scene8.png").convert_alpha(),pygame.image.load("level[3]\\scene9.png").convert_alpha(),pygame.image.load("level[3]\\scene10.png").convert_alpha(), ]
    scenes_counter = 0; max_scene = 9

    scene1_objects = [pygame.Rect(25,1056,40,24),pygame.Rect(576,960,96*2,96),pygame.Rect(672,864,96,96),pygame.Rect(960,960,96,96),pygame.Rect(1344,864,96*6,96)]
    scene2_objects = [pygame.Rect(0,864,96,96*2),pygame.Rect(192,672,96*3,96),pygame.Rect(480,384,96*2,96),pygame.Rect(0,288,96*3,96),pygame.Rect(576,768,96*3,96),pygame.Rect(960,768,96,96),pygame.Rect(1152,768,96,96),pygame.Rect(1248,576,96,96),pygame.Rect(1152,288,96,96),pygame.Rect(1440,192,96,96*2),pygame.Rect(1536,576,96*2,96),pygame.Rect(1824,576,96,96*5)]
    scene3_objects = [pygame.Rect(0,576,96,96*5),pygame.Rect(288,0,96,96*9),pygame.Rect(384,768,96,96),pygame.Rect(672,672,96*2,96),pygame.Rect(480,480,96*2,96),pygame.Rect(384,192,96*2,96),pygame.Rect(768,192,96*3,96*2),pygame.Rect(864,384,96,96*7),pygame.Rect(960,768,96,96),pygame.Rect(1344,384,96,96*4),pygame.Rect(1440,0,96,96*9),pygame.Rect(1536,480,96,96),pygame.Rect(1728,768,96,96),pygame.Rect(1824,288,96,96*8),pygame.Rect(1728,192,96*2,96)]
    scene4_objects = [pygame.Rect(0,192,96,96*9),pygame.Rect(96,576,96*4,96*2),pygame.Rect(576,960,96,96),pygame.Rect(672,769,96*2,96*3),pygame.Rect(864,672,96*4,96*4),pygame.Rect(1248,864,96*4,96*2),pygame.Rect(1632,960,96,96),pygame.Rect(288,0,96*17,96*3),pygame.Rect(576,288,96*3,96),pygame.Rect(1248,288,96*7,96),pygame.Rect(1440,384,96*5,96),pygame.Rect(1632,480,96*3,96),pygame.Rect(1728,576,96*2,96),pygame.Rect(1824,1056,96,96)]
    scene5_objects = [pygame.Rect(25,1056,40,24),pygame.Rect(0,0,96,96*7),pygame.Rect(384,960,96*3,96),pygame.Rect(768,768,96*2,96),pygame.Rect(480,480,96*2,96),pygame.Rect(288,384,96,96),pygame.Rect(96,192,96*2,96),pygame.Rect(1056,576,96*3,96),pygame.Rect(1536,672,96*2,96*4),pygame.Rect(1344,288,96*2,96),pygame.Rect(1728,288,96*2,96*8)]
    scene6_objects = [pygame.Rect(0,288,96,96*8),pygame.Rect(192,288,96*2,96),pygame.Rect(384,576,96,96),pygame.Rect(288,864,96*2,96),pygame.Rect(576,0,96,96*7),pygame.Rect(576,960,96*4,96),pygame.Rect(768,864,96,96),pygame.Rect(864,672,96,96*3),pygame.Rect(960,384,96*2,96),pygame.Rect(1248,672,96*2,96),pygame.Rect(1632,864,96*3,96*2)]
    scene7_objects = [pygame.Rect(0,864,96,96*2),pygame.Rect(0,0,96,96*5),pygame.Rect(192,0,96,96*4),pygame.Rect(192,768,96,96*3),pygame.Rect(384,0,96,96*5),pygame.Rect(384,864,96,96*2),pygame.Rect(576,0,96,96*3),pygame.Rect(576,672,96,96*4),pygame.Rect(768,0,96,96),pygame.Rect(768,480,96,96*6),pygame.Rect(960,0,96,96*2),pygame.Rect(960,576,96,96*5),pygame.Rect(1152,0,96,96*4),pygame.Rect(1152,768,96,96*3),pygame.Rect(1344,0,96,96*3),pygame.Rect(1344,672,96,96*4),pygame.Rect(1536,0,96,96*5),pygame.Rect(1536,864,96,96*2),pygame.Rect(1728,0,96*2,96*4),pygame.Rect(1728,768,96*2,96*3)]
    scene8_objects = [pygame.Rect(0,768,96,96*3),pygame.Rect(0,0,96,96*4),pygame.Rect(288,864,96*2,96*2),pygame.Rect(672,864,96*2,96*2),pygame.Rect(864,576,96*2,96),pygame.Rect(672,384,96,96),pygame.Rect(384,192,96*2,96*2),pygame.Rect(1248,576,96*2,96*2),pygame.Rect(1824,864,96,96*2),pygame.Rect(1632,672,96*3,96*2)]
    scene9_objects = [pygame.Rect(0,672,96,96*4),pygame.Rect(288,0,96,96*8),pygame.Rect(384,672,96*13,96),pygame.Rect(768,960,96,96),pygame.Rect(1728,864,96,96*2),pygame.Rect(1824,384,96,96*7),pygame.Rect(1344,576,96,96),pygame.Rect(384,480,96,96*2),pygame.Rect(576,288,96*14,96)]
    scene10_objects= [pygame.Rect(0,288,96*3,96*8),pygame.Rect(288,384,96*2,96*7),pygame.Rect(480,480,96*2,96*6),pygame.Rect(672,576,96*4,96*5),pygame.Rect(1824,384,96,96*7),pygame.Rect(1440,288,96*5,96),pygame.Rect(1056,672,96*5,96*4) , pygame.Rect(1536 , 1020 , 96 * 3 , 30)]
    
    scene1_points = []
    scene2_points = [pygame.Rect(96,192,96,96),pygame.Rect(1440,96,96,96)]
    scene3_points = [pygame.Rect(1344,288,96,96)]
    scene4_points = [pygame.Rect(96,960,96,96)]
    scene5_points = [pygame.Rect(96,96,96,96)]
    scene6_points = [pygame.Rect(192,384,96,96)]
    scene7_points = [pygame.Rect(864,192,96,96)]
    scene8_points = [pygame.Rect(384,96,96,96),pygame.Rect(1056,672,96,96)]
    scene9_points = [pygame.Rect(960,480,96,96)]
    scene10_points= []

    scene1_trap = [pygame.Rect(768,960,96,96),pygame.Rect(1248,960,96,96),pygame.Rect(1536,768,96,96)]
    scene2_trap = [pygame.Rect(96,960,96*18,96),pygame.Rect(960,672,96,96),pygame.Rect(1440,384,96,96)]
    scene3_trap = [pygame.Rect(960,384,96,96*4),pygame.Rect(1248,384,96,96*4),pygame.Rect(1728,864,96,96),pygame.Rect(1536,576,96,96)]
    scene4_trap = [pygame.Rect(96,480,96,96),pygame.Rect(384,288,96,96),pygame.Rect(576,384,96,96),pygame.Rect(96,768,96*4,96),pygame.Rect(768,672,96,96),pygame.Rect(960,576,96,96),pygame.Rect(1152,288,96,96),pygame.Rect(1248,768,96,96),pygame.Rect(1248,384,96,96),pygame.Rect(1536,480,96,96),pygame.Rect(1632,864,96,96)]
    scene5_trap = []
    scene6_trap = [pygame.Rect(96,960,96*5,96),pygame.Rect(960,960,96*7,96),pygame.Rect(1056,480,96,96)]
    scene7_trap = [pygame.Rect(672,960,96*3,96)]
    scene8_trap = [pygame.Rect(192,864,96,96*2),pygame.Rect(480,864,96,96*2),pygame.Rect(576,864,96,96*2),pygame.Rect(864,864,96,96*2),pygame.Rect(864,672,96*2,96),pygame.Rect(384,384,96*2,96),pygame.Rect(288,192,96,96*2),pygame.Rect(1152,576,96,96*2),pygame.Rect(1248,768,96*2,96),pygame.Rect(1440,576,96,96*2),pygame.Rect(1536,672,96,96*2),pygame.Rect(1632,864,96*2,96)]
    scene9_trap = [pygame.Rect(288,960,96,96),pygame.Rect(576,768,96,96),pygame.Rect(960,768,96*2,96),pygame.Rect(1536,384,96,96),pygame.Rect(1152,384,96,96),pygame.Rect(768,576,96*2,96)]
    scene10_trap= [pygame.Rect(480,384,96,96),pygame.Rect(864,480,96,96),pygame.Rect(1440,192,96*5,96)]
    
    scenes_vector = [scene1_objects, scene2_objects, scene3_objects , scene4_objects , scene5_objects , scene6_objects , scene7_objects , scene8_objects , scene9_objects , scene10_objects]
    scenes_points = [scene1_points,scene2_points,scene3_points,scene4_points,scene5_points,scene6_points,scene7_points,scene8_points,scene9_points,scene10_points]
    scenes_traps  = [scene1_trap , scene2_trap , scene3_trap , scene4_trap , scene5_trap , scene6_trap , scene7_trap , scene8_trap , scene9_trap , scene10_trap]
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
        
        for k in range(0 , len(scenes_points[scenes_counter])):
            if scenes_points[scenes_counter][k] is not None:
                if player.playerRect.colliderect(scenes_points[scenes_counter][k]):
                    player.player_score += 1; scenes_points[scenes_counter][k] = None; break

        for k in range(0 , len(scenes_points[scenes_counter])):
            if scenes_points[scenes_counter][k] is not None:
                screen.blit(points_image , scenes_points[scenes_counter][k])

        if player.playerRect.x < 0 and scenes_counter >= 1:

            scenes_counter = scenes_counter - 1
            size = len(scenes_vector[scenes_counter]) - 1
            player.playerRect.right = scenes_vector[scenes_counter][size].right - 10
            player.playerRect.bottom = scenes_vector[scenes_counter][size].top

        if player.playerRect.right >= width and scenes_counter != 9:

            scenes_counter = scenes_counter + 1
            player.playerRect.x = scenes_vector[scenes_counter][0].x
            player.playerRect.bottom = scenes_vector[scenes_counter][0].top
        elif player.playerRect.colliderect(scene10_objects[7]) and scenes_counter == max_scene:
            
            dbScore = getScore()
            saveScore(str(player.player_score + int(dbScore[0][0])))
            import gameFinished; gameFinished.ending()
            
            return 0

        #coliziunea cu obiectele inamice(cactusi)
        for k in range(0 , len(scenes_traps[scenes_counter])):
            if player.playerRect.colliderect(scenes_traps[scenes_counter][k]):
                player.playerRect.x = scenes_vector[scenes_counter][0].x + 5; player.playerRect.bottom = scenes_vector[scenes_counter][0].top + 2
                last_obj_colision = scenes_vector[scenes_counter][0]; playerDeath = True; break

        player.update()
        player.draw(screen)
        player.playerColision(scenes_vector[scenes_counter])
        
        Text.displayText("SCORE: " + str(player.player_score) , width - 250, 50 , color[0] , screen , my_font)
        
        pygame.display.flip()
        clock.tick(int(fps))
