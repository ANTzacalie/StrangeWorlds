from mainScript import pygame , screen , color , clock , width , height , fps , key_left , key_right , my_font , lvl_start , storeValues , lvl_end , antialiasing , getScore , saveScore , saveLevel


def ending():

    global screen , fps, color

    global_score = getScore()

    background = pygame.image.load("image_objects\\endScreen.png").convert_alpha()
    image_background_settings_blur = pygame.image.load("image_objects\\settingsBackgroundBlur.png").convert_alpha()
    
    my_font = pygame.font.SysFont('Arial', 60)
    my_font2 = pygame.font.SysFont('Arial', 30)

    text = "GAME FINISHED WITH SCORE: " + global_score[0][0]
    text_finish = my_font.render(str(text) , True , color[0])     
    textRectangle = pygame.Rect(250 , 350 , 100 , 150)

    text2 = "PRESS ESC TO GO TO MAIN SCREEN"
    text_finish2 = my_font2.render(str(text2) , True , color[0])
    textRectangle2 = pygame.Rect(50 , 50 , 100 , 150)

    saveScore("0")
    saveLevel("1")
    while True:
        
        screen.blit(background, (0,0))
        screen.blit(image_background_settings_blur , (0,0))
        
        screen.blit(text_finish , textRectangle)
        screen.blit(text_finish2 , textRectangle2)

        for event in pygame.event.get():
            
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    return 0

        pygame.display.flip()
        clock.tick(int(fps))

#DEV: M.C.A
#VER 2.2