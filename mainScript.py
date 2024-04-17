import pygame
import sqlite3

#functie prin care luam din baza de date scorul
def getScore():
    
    conn = sqlite3.connect("gameInternalDataBase[A].db")
    cursor = conn.cursor()
      
    try:
        query = (f'SELECT SCORE FROM GAME')
        cursor.execute(query)
        result = cursor.fetchall()
        conn.close()
    except sqlite3.Error as e:
        print("SOMETHING WENT WRONG, COULD NOT WITHDRAW THE VALUES FROM THE DB: " + str(e)); return 0
    return result

#functie prin care luam nivelul actual salvat ultima oara de joc 
def getLevel():
    
    conn = sqlite3.connect("gameInternalDataBase[A].db")
    cursor = conn.cursor()
      
    try:
        query = (f'SELECT LVL_START FROM GAME')
        cursor.execute(query)
        result = cursor.fetchone()
        conn.close()
    except sqlite3.Error as e:
        print("SOMETHING WENT WRONG, COULD NOT WITHDRAW THE VALUES FROM THE DB: " + str(e)); return 0
    return result

#functie prin care salvam scorul in baza de date
def saveScore(value):

    conn = sqlite3.connect("gameInternalDataBase[A].db")
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE GAME SET SCORE = ?', (value,))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print("SOMTHING WENT WRONG VALUES NOT STROED IN DB: " + str(e))
    else:
        print("VALUES STORED IN DB!")

#functie prin care salvam nivelul actual in baza de date
def saveLevel(value):

    conn = sqlite3.connect("gameInternalDataBase[A].db")
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE GAME SET LVL_START = ?', (value , ))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print("SOMTHING WENT WRONG VALUES NOT STROED IN DB: " + str(e))
    else:
        print("VALUES STORED IN DB!")

#functie prin care luam toate valorile de baza functionari jocului de la width , height ... antialiasing
def getValues():
    
    conn = sqlite3.connect("gameInternalDataBase[A].db")
    cursor = conn.cursor()
      
    try:
        query = (f'SELECT WIDTH , HEIGHT , FPS , KEY_LEFT , KEY_RIGHT , LVL_START , LVL_END , ANTI FROM GAME')
        cursor.execute(query)
        result = cursor.fetchall()
        conn.close()
    except sqlite3.Error as e:
        print("SOMETHING WENT WRONG, COULD NOT WITHDRAW THE VALUES FROM THE DB: " + str(e)); return 0
    return result

#functuie prin care salvam valorile de baza de date
def storeValues(list_of_values):

    conn = sqlite3.connect("gameInternalDataBase[A].db")
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE GAME SET WIDTH = ? , HEIGHT = ? , FPS = ? , KEY_LEFT = ? , KEY_RIGHT = ? , LVL_START = ? , LVL_END = ? , ANTI = ?', (
        list_of_values[0] , list_of_values[1] , list_of_values[2] , 
        list_of_values[3] , list_of_values[4] , list_of_values[5] , 
        list_of_values[6] , list_of_values[7]
        ))
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print("SOMTHING WENT WRONG VALUES NOT STROED IN DB: " + str(e))
    else:
        print("VALUES STORED IN DB!")

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
    width = int(1980)
    height =  int(1080)
    fps = int(60)
    key_left = "A"
    key_right = "D"
    lvl_start = "1"
    lvl_end = "3"
    antialiasing = "YES"

pygame.init() #initializam libraria pygame

#initializam ecranul
if antialiasing == "NO":
    screen = pygame.display.set_mode((width , height) , pygame.HWSURFACE , 32) #fara antialiasing
else:
    screen = pygame.display.set_mode((width , height) , pygame.HWSURFACE | pygame.SRCALPHA , 32) #cu antialiasing

#vector care stocheaza culori in RGB
color = [(255,250,250), (0 , 0 , 0), (0 , 0 , 255)]

#initializam pygame font
pygame.font.init() 
#fontul pentru obiectele text
my_font = pygame.font.SysFont('Arial', 45) 
my_font2 = pygame.font.SysFont('Arial', 25) 

#initializam pygame clock(ceasul jocului sau cel care stabileste FPS(cadre pe secunda / rulaje ale codului pe secunda))
clock = pygame.time.Clock()

#clasa care detine functia displayText , pentru eficienta de memorie , displayText fiind solicitat des
class Text:
    def displayText(text , x , y , color , screen , font):
        text = font.render(str(text) , True , color)
        textRectangle = pygame.Rect(x , y , 50 , 20)
        screen.blit(text , textRectangle)

#scriptul de initierere / functia main
def mainScript():
    global screen

    #aici incarcam iconul jocului 
    icon = pygame.image.load("icon.png")

    #setam iconul , ca sa apara in coltul ecranului
    pygame.display.set_icon(icon)

    #titlul din coltul ecranului
    pygame.display.set_caption('Strange World')

    #imaginea de background a meniului principal
    image_background = pygame.image.load("image_objects\\mainMenu.png")

    #effectul de blur
    image_background_settings_blur = pygame.image.load("image_objects\\settingsBackgroundBlur.png").convert_alpha()

    #ciclul continu principal
    while True:
        #variabile globale , functia nu poate folosi variabile globale daca nu sunt precizate cu global var1 , var2 ... etc
        global screen , width , height , fps , key_left , key_right , antialiasing , lvl_end , lvl_start , color , getLevel , saveLevel

        #prindem imaginea de fundal pe ecran
        screen.blit(image_background , (0 , 0))
        screen.blit(image_background_settings_blur , (0 , 0))
        
        #luam evenimentele(scanam pentru input de la periferice)
        events = pygame.event.get()
        for event in events:
            
            #aseste ca mausul a fost folosit si click
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                #luam pozitia mousului in x , y
                mousePos = pygame.mouse.get_pos()
                
                #pozitie pe ecran in care daca mousul se gaseste pe ea , o actiune se va executa
                if mousePos[0] <  width / 2 + 70 and mousePos[0] >  width / 2 - 125 and mousePos[1] > height / 2 -115 and mousePos[1] < height / 2 - 70: # o sa facem text rect si scapam de condiitiile astea lungi
                    lvl_start = "1"; saveLevel(lvl_start)
                    import firstLevel
                    firstLevel.Game()
                
                #pozitie pe ecran in care daca mousul se gaseste pe ea , o actiune se va executa
                if mousePos[0] <  width / 2 + 70 and mousePos[0] >  width / 2 - 125 and mousePos[1] > height / 2 -50 and mousePos[1] < height / 2 - 5:

                    #luam nivelul actual prin intermediul functiei getLevel()
                    lvl = getLevel()
                    lvl_start = lvl[0][0]

                    #selectorul novelului actual
                    if lvl_start =="1":
                        import firstLevel
                        firstLevel.Game()
                    elif lvl_start == "2":
                        import secondLevel
                        secondLevel.Game()
                    elif lvl_start == "3":
                        import thirdLevel
                        thirdLevel.Game()
                
                #pozitie pe ecran in care daca mousul se gaseste pe ea , o actiune se va executa
                if mousePos[0] <  width / 2 + 70 and mousePos[0] >  width / 2 - 125 and mousePos[1] > height / 2 + 15 and mousePos[1] < height / 2 + 60:
                    import settings
                    settings.settings()
                
                #pozitie pe ecran in care daca mousul se gaseste pe ea , o actiune se va executa
                if mousePos[0] <  100 and mousePos[0] >  50 and mousePos[1] > 50 and mousePos[1] < 70:
                    #parasim jocul , pygame.quit()
                    pygame.quit()
                    
            #daca se detecteaza input de la tastatura
            if event.type == pygame.KEYDOWN:
                
                #se identifica ca butonul K este apasat
                if event.key == pygame.K_ESCAPE:
                    #parasim jocul , pygame.quit()
                    pygame.quit()
        
        #afisam textul(butoane in cazul asta) pe ecran
        Text.displayText("New Game" , width / 2 - 125 , height / 2 - 115, color[0], screen , my_font)
        Text.displayText("Resume Game", width / 2 - 125 , height / 2 - 50 , color[0], screen , my_font)
        Text.displayText("Settings", width / 2 - 125 , height / 2 + 15, color[0], screen , my_font)
        Text.displayText("Esc" , 50 , 50 , color[0], screen , my_font2)

        #acutalizeaza tot ce se afisaza pe ecran
        pygame.display.flip()
        
        #ceasul jocului , FPS
        clock.tick(fps)

#se foloseste doar aici , daca scriptul este rulat primul se apeleaza functia mainScript()
if __name__ == "__main__":
    mainScript()

#ver: 3.0 #dev: M.C.A




