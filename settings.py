import pygame
from mainScript import screen , width , height , fps , key_left , key_right , antialiasing , lvl_end , lvl_start , color , storeValues , getValues

class Text:
    
    def displayText(text , x , y , color , screen , font):
        text = font.render(str(text) , True , color)     
        textRectangle = pygame.Rect(x , y , 50 , 20)
    
        screen.blit(text , textRectangle)  
   
def settings():
    
    global screen , width , height , fps , key_left , key_right , antialiasing , lvl_end , lvl_start , color , storeValues

    #luam valorile din db prin getValues()
    default_values = getValues()
    #extragem valorile din default_values folosindune de matricea intorsa de functia getValues()
    try:

        width = int(default_values[0][0])
        height = int(default_values[0][1])
        fps = int(default_values[0][2])
        key_left = default_values[0][3]
        key_right = default_values[0][4]
        lvl_start = default_values[0][5]
        lvl_end = default_values[0][6]
        antialiasing = default_values[0][7]
    except: #in cazul in care getValues() are probleme , initializam variabilele de baza cu valori predefinite
        width = int(1920)
        height =  int(1080)
        fps = int(60)
        key_left = "A"
        key_right = "D"
        lvl_start = "1"
        lvl_end = "3"
        antialiasing = "YES"

    #constante , mai bine spus variabile care vor fi modificate doar intr-un anumit if al functiei 
    const_config_WIDTH = width
    const_config_HEIGHT = height
    const_config_fps = fps

    #variabile dinamice care nu trebuies sa fie constante
    config_WIDTH = str(width)
    config_HEIGHT = str(height)
    config_FPS = str(fps)

    #booleane pentru selector_y din loop , ca sa stim pe ce pozitie suntem in y
    bool_config_WIDTH = False
    bool_config_HEIGHT = False
    bool_config_FPS = False
    bool_config_KEY_A = False
    bool_config_KEY_D = False
    bool_config_lvl_SI = False
    bool_config_lvl_EI = False
    bool_config_anti_aly = False

    #fonturile pentru scrisul afisat pe ecran , marimea si tipul 
    master_font  = pygame.font.SysFont('Arial' , 20)
    master_fontA = pygame.font.SysFont('Arial' , 18)
    master_fontB = pygame.font.SysFont('Arial' , 25)

    image_background_settings = pygame.image.load("image_objects\\settingsBackground.png").convert_alpha()

    #effectul de blur
    image_background_settings_blur = pygame.image.load("image_objects\\settingsBackgroundBlur.png").convert_alpha()
    
    clock = pygame.time.Clock()
    
    #coordonatele de inceput ale selectorului si startBool
    selector_y = 30
    selector_x = 240
    startBool = True

    while True:

        screen.blit(image_background_settings , (0 , 0))
        screen.blit(image_background_settings_blur , (0 , 0))

        if selector_y > 310: 
            selector_y = 30
            selector_x = 240
            
        if selector_y < 30:  
            selector_y = 310
            selector_x = 310

        events = pygame.event.get()

        for event in events:
        
            if event.type == pygame.MOUSEBUTTONDOWN and startBool:
                mousePos = pygame.mouse.get_pos()
                
                if mousePos[0] > int(const_config_WIDTH)  / 2 and mousePos[0] < (int(const_config_WIDTH) / 2) + 50 and mousePos[1] > (int(const_config_HEIGHT) - 200) and mousePos[1] < (int(const_config_HEIGHT) - 175):
                    storeValues([config_WIDTH , config_HEIGHT , config_FPS , key_left , key_right , lvl_start , lvl_end , antialiasing])
                    
                    const_config_WIDTH = int(config_WIDTH)
                    const_config_HEIGHT = int(config_HEIGHT)
                    const_config_fps = int(config_FPS)

                    if antialiasing == "NO":
                        screen = pygame.display.set_mode((const_config_WIDTH , const_config_HEIGHT) , pygame.HWSURFACE , 32) #fara antialiasing
                    else:
                        screen = pygame.display.set_mode((const_config_WIDTH , const_config_HEIGHT) , pygame.HWSURFACE | pygame.SRCALPHA , 32) #cu antialiasing

            if event.type == pygame.MOUSEBUTTONDOWN and startBool:
                mousePos = pygame.mouse.get_pos()

                if mousePos[0] > (int(const_config_WIDTH)  / 2) - 120 and mousePos[0] < (int(const_config_WIDTH) / 2) - 70 and mousePos[1] > (int(const_config_HEIGHT) - 200) and mousePos[1] < (int(const_config_HEIGHT) - 175):
                    return 0 

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_w and startBool:
                    selector_y -= 40

                if event.key == pygame.K_s and startBool: 
                    selector_y += 40

                if event.key == pygame.K_ESCAPE:

                    startBool = True

                    match selector_y:

                        case 30:
                            bool_config_WIDTH  = False
                        case 70:
                            bool_config_HEIGHT = False
                        case 110:
                            bool_config_FPS = False
                        case 150:
                            bool_config_KEY_A = False
                        case 190:
                            bool_config_KEY_D = False
                        case 230:
                            bool_config_lvl_SI = False
                        case 270:
                            bool_config_lvl_EI = False
                        case 310:
                            bool_config_anti_aly = False

                if (event.key == pygame.K_w or event.key == pygame.K_s) and startBool:

                    match selector_y:

                        case 30:
                            selector_x = 240
                        case 70:
                            selector_x = 245
                        case 110:
                            selector_x = 200
                        case 150:
                            selector_x = 250
                        case 190:
                            selector_x = 260
                        case 230:
                            selector_x = 205
                        case 270:
                            selector_x = 205
                        case 310:
                            selector_x = 315

                if event.key == pygame.K_RETURN:
                    
                    startBool = False

                    match selector_y:

                        case 30:
                            bool_config_WIDTH = True
                        case 70:
                            bool_config_HEIGHT = True
                        case 110:
                            bool_config_FPS = True
                        case 150:
                            bool_config_KEY_A = True
                        case 190:
                            bool_config_KEY_D = True
                        case 230:
                            bool_config_lvl_SI = True
                        case 270:
                            bool_config_lvl_EI = True
                        case 310:
                            bool_config_anti_aly = True

                if bool_config_anti_aly and event.key != pygame.K_ESCAPE:
                    
                    if event.key == pygame.K_d:
                        antialiasing = "NO"
                    elif event.key == pygame.K_a:
                        antialiasing = "YES"

                if bool_config_WIDTH and event.key != pygame.K_ESCAPE:
                    
                    if event.key == pygame.K_BACKSPACE:
                        config_WIDTH = config_WIDTH[:-1]
                    elif not event.unicode.isalpha():
                        config_WIDTH += event.unicode

                if bool_config_HEIGHT and event.key != pygame.K_ESCAPE:
                   
                    if event.key == pygame.K_BACKSPACE:
                        config_HEIGHT = config_HEIGHT[:-1]
                    elif not event.unicode.isalpha():
                        config_HEIGHT += event.unicode

                if bool_config_FPS and event.key != pygame.K_ESCAPE:
                    
                    if event.key == pygame.K_BACKSPACE:
                        config_FPS = config_FPS[:-1]
                    elif not event.unicode.isalpha():
                        config_FPS += event.unicode

                if bool_config_KEY_A and event.key != pygame.K_ESCAPE:
                    
                    if event.key == pygame.K_BACKSPACE:
                        key_left = key_left[:-1]
                    elif event.unicode.isalpha():
                        key_left += event.unicode

                if bool_config_KEY_D and event.key != pygame.K_ESCAPE:
                    
                    if event.key == pygame.K_BACKSPACE:
                        key_right = key_right[:-1]
                    elif event.unicode.isalpha():
                        key_right += event.unicode

                if bool_config_lvl_EI and event.key != pygame.K_ESCAPE and event.key != pygame.K_RETURN:
                    
                    if event.key == pygame.K_BACKSPACE:
                        lvl_end = lvl_end[:-1]
                    elif not event.unicode.isalpha():
                        lvl_end += event.unicode

                if bool_config_lvl_SI and event.key != pygame.K_ESCAPE and event.key != pygame.K_RETURN:
                    
                    if event.key == pygame.K_BACKSPACE:
                        lvl_start = lvl_start[:-1]
                    elif not event.unicode.isalpha():
                        lvl_start += event.unicode 

        #AFISAM INSTRUCTIUNILE SETARILOR PENTRU UTILIZATOR
        Text.displayText("PRESS W/S TO MOVE UP/DOWN" , 350 , 30 , color[0], screen , master_fontA)
        Text.displayText("PRESS ENTER TO CHANGE VALUES" , 350 , 60 , color[0], screen , master_fontA)
        Text.displayText("AFTER A VALUE IS CHANGED PRESS ESC" , 350 , 90 , color[0], screen , master_fontA)
        Text.displayText("TO SAVE CHANGES CLICK ON SAVE" , 350 , 120 , color[0], screen , master_fontA)
        #AICI AFISAM VALORILE DEFAULT/MODIFICATE IN TIMP REAL ALE JOCULUI
        Text.displayText("WIDTH: ", 100 , 30 , color[0] , screen , master_font)
        Text.displayText(config_WIDTH , 175 , 30 , color[0] , screen , master_font)
        Text.displayText("HEIGHT: " , 100 , 70 , color[0] , screen , master_font)
        Text.displayText(config_HEIGHT , 185 , 70 , color[0] , screen , master_font)
        Text.displayText("FPS: " , 100 , 110 , color[0] , screen , master_font)
        Text.displayText(config_FPS , 150 , 110 , color[0] , screen ,master_font)
        Text.displayText("KEY_LEFT: " , 100 , 150 , color[0] , screen , master_font)
        Text.displayText(key_left , 205 , 150 , color[0] , screen , master_font )
        Text.displayText("KEY_RIGHT: " , 100 , 190 , color[0] , screen, master_font)
        Text.displayText(key_right , 220 , 190 , color[0] , screen , master_font)
        ##################### DEV ONLY ################################################################################
        Text.displayText("LVL SI: ", 100 , 230 , color[0] , screen, master_font)
        Text.displayText(lvl_start , 170 , 230 , color[0] , screen , master_font)
        Text.displayText("LVL EI: " ,100 , 270 , color[0] , screen , master_font)
        Text.displayText(lvl_end , 170 , 270 , color[0], screen , master_font)
        #AICI AFISAM VALORILE DEFAULT/MODIFICATE IN TIMP REAL ALE JOCULUI
        Text.displayText("ANTI-ALIASING: ", 100 , 310 , color[0] , screen , master_font)
        Text.displayText(antialiasing , 255 , 310 , color[0] , screen , master_font)
        #AICI SE FACE PLASAREA BUTOANELOR SAVE SI BACK PE ECRAN
        Text.displayText("SAVE" , (int(const_config_WIDTH) / 2) , int(const_config_HEIGHT) - 200 , color[0] , screen , master_fontB)
        Text.displayText("BACK" , (int(const_config_WIDTH) / 2) - 120 , int(const_config_HEIGHT) - 200 , color[0] , screen , master_fontB)
        
        #GENERAM UN PUNCT ALBASTRU CARE ESTE SELECTORUL VALORILOR WIDTH, HEIGHT , FPS etc.....
        pygame.draw.circle(screen , color[2] , (selector_x , selector_y + 10) , 10)
        pygame.display.flip()
        clock.tick(int(const_config_fps))
