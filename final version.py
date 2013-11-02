"""
NeuTRON
Jan 20, 2012

Implemented by Jaguar Kristeller, Michaela Ennis, and Neerja Aggerwal 
Player Class written by Jaguar Kristeller (jaguark@mit.edu)
Menu Class and Main Loop written by Michaela Ennis (mennis@mit.edu)
Grid Class(es) written by Neerja Aggarwal (neerja@mit.edu)

"""

import os, pygame, sys, random
from pygame.locals import *




### Global Variables
WIDTH = 20  # sets the width of an individual square
HEIGHT = 20 # sets the height of an individual square
SIZEX = 70
SIZEY = 38
COLOR = grey = (100, 100, 100)





# Direction definitions with number of degrees starting upwards and rotating clockwise
UP = 0  
RIGHT = 90
DOWN = 180
LEFT = 270

# RGB Color definitions
black = (0, 0, 0)
grey = (100, 100, 100)
white = (255, 255, 255)
green = (0, 255, 0)
red   = (255, 0, 0)
blue  = (0, 0, 255)
orange = (255, 140, 0)
yellow = (250, 250, 210)

# Location methods
def getRowTopLoc(rowNum, location = 0, height = HEIGHT):
    """
    Returns the location of the top pixel in a square in
    row rowNum, given the row height.
    """
    return rowNum*height + 10 + location

def getColLeftLoc(colNum, location = 0, width = WIDTH):
    """
    Returns the location of the leftmost pixel in a square in
    column colNum, given the column width. 
    """
    return colNum*width + 10 + location


def newGame(numPlayer, gridType, Player1wins, Player2wins, Player3wins, Player4wins):
        pygame.quit()
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)
        pygame.init()
        pygame.display.set_caption('NeuTRON')
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode(((WIDTH*SIZEX + 20), (HEIGHT*SIZEY + 20))) #create screen about the size of the grid
        screen.fill((0,0,0)) #fill screen with black
        grid = portalGrid(SIZEX,SIZEY, numPlayer)
      
        if gridType == "normal":
            grid = Grid(SIZEX, SIZEY, numPlayer) #create an instance of grid (which will also create squares and players)
        elif gridType == "erase":
            grid = eraseGrid(SIZEX, SIZEY, numPlayer)
            grid.wall()
        elif gridType == "obstacle":
            grid = obstacleGrid(SIZEX, SIZEY, numPlayer)
        elif gridType == "portal":
            grid = portalGrid(SIZEX, SIZEY, numPlayer)
        
        grid.initializePlayers(numPlayer) #initializes players in Grid instance
        grid.refreshGrid(screen, clock)
        mainLoop(numPlayer, gridType, grid, screen, clock, Player1wins, Player2wins, Player3wins, Player4wins) #call main loop

def menuLoop(Player1wins, Player2wins, Player3wins, Player4wins):
    pygame.init() #initialize pygame
    background = pygame.image.load("Neutron-Artwork.jpeg") 
    size = background.get_size() #load background image and set size of screen equal to size of background image
    
    screen = pygame.display.set_mode(size) 
    pygame.display.set_caption('NeuTRON') #sets window caption to NeuTRON
    backgroundRect = background.get_rect()
    screen.blit(background, backgroundRect) #fill screen with background
    pygame.mixer.init() #initialize music function for pygame
    pygame.mixer.music.load("tron main menu music.mp3") #upload song
    pygame.display.flip()
    menu = Menu() #create new instance of menu
    menu.items.draw(screen) #draw buttons on screen
    pygame.display.flip() #update screen
    pygame.mixer.music.play(-1) #loop music indefinitely until stop command (at end of menu)
    
    while 1: #infinite loop
        
        for event in pygame.event.get(): #loop through pygame "events" to look for user input
                if event.type == QUIT: #exit pygame if user quits
                        pygame.quit()
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                        pygame.quit()
                elif event.type == MOUSEBUTTONDOWN: #check to see if mouse button is clicked
                        for item in menu.menu_items: #if it is, see if it is touching any of the buttons
                            if item.touch():
                                if item == menu.menu_items[1]:
                                        continue #if it's touching title button do nothing
                                elif item == menu.menu_items[2]:
                                    screen.blit(background, backgroundRect) #clear screen
                                   
                                    font = pygame.font.Font(None, 20) #set up font
            
                                    text = font.render("Player 1 moves with the arrow keys, Player 2 with WASD, Player 3 with TFGH, and Player 4 with IJKL. With the xbox controllers the YXAB buttons will control turning for all players.", True, (255,255,255), (0,0,0)) #type instructions
                                    text2 = font.render("The start button pauses. Left trigger is yes to play again at the end game screen, right trigger is no to quit. Left stick moves the mouse and left stick click clicks the mouse.", True, (255,255,255), (0,0,0))
                                    text3 = font.render("Avoid your own and the other players' paths for the longest to win. There are 4 types of game boards- regular (normal tron game, screen wraps),", True, (255,255,255), (0,0,0))
                                    text4 = font.render("erasing (paths disappear after a given amount of time; players also move faster. There is a wall), obstacle (the board includes traps),", True, (255,255,255), (0,0,0))
                                    text5 = font.render("and portal (players are able to teleport across the board by going through portals that pop up in new locations every so often)", True, (255,255,255), (0,0,0))
                                    text6 = font.render("To go back to the main screen, press backspace (back button on xbox controller).", True, (255,255,255), (0,0,0))
                                    textRect = text.get_rect()
                                
                                    
                                    screen.blit(text, textRect)
                                    screen.blit(text2, (0,20))
                                    screen.blit(text3, (0,40))
                                    screen.blit(text4, (0,60))
                                    screen.blit(text5, (0,80))
                                    screen.blit(text6, (0,100))
                                    pygame.display.flip() #update screen
                                    while 1: #loop to stay on instructions screen until backspace is pressed
                                        for event in pygame.event.get():
                                            if event.type == KEYDOWN and event.key == K_BACKSPACE:
                                                screen.blit(background, backgroundRect)
                                                menu.items.draw(screen)
                                                pygame.display.flip()
                                                break
                                            else:
                                                continue
                                        else:
                                            continue
                                        break
                                    continue
                                    
                                elif item == menu.menu_items[0]:
                                        screen.blit(background, backgroundRect)
                                        menu.playerScreenCreate() #run method to set up player selection screen
                                break
                        else: 
                                continue
                        break
        else: 
            continue #break out of full loop if for loop was broken, if for loop ended naturally continue
        break
    
    
    menu.items.draw(screen) #draw new buttons
    pygame.display.flip() #update screen
    while 1: #infinite loop
        for event in pygame.event.get():  #loop through pygame "events" to look for user input
             if event.type == QUIT: #exit pygame if user quits
                    pygame.quit()
             elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    pygame.quit()
             elif event.type == MOUSEBUTTONDOWN: #check to see if mouse button is clicked
                    for item in menu.menu_items: #if it is, see if it is touching any of the buttons
                        if item.touch():
                            if item == menu.menu_items[0]: #if clicking how many players button do nothing
                                    continue
                            elif item == menu.menu_items[1]: #if clicking 2 button set game to 2 players
                                    numPlayer = 2
                                    screen.blit(background, backgroundRect)
                                    menu.levelScreenCreate()
                            elif item == menu.menu_items[2]: #if clicking 3 button set game to 3 players
                                    numPlayer = 3
                                    screen.blit(background, backgroundRect)
                                    menu.levelScreenCreate()
                            elif item == menu.menu_items[3]: #if clicking 4 button set game to 4 players
                                    numPlayer = 4
                                    screen.blit(background, backgroundRect)
                                    menu.levelScreenCreate()
                            elif item == menu.menu_items[4]:
                                    numPlayer = 1
                                    screen.blit(background, backgroundRect)
                                    menu.levelScreenCreate()
                            break
                    else: 
                       continue
                    break
        else: 
            continue #break out of full loop if for loop was broken, if for loop ended naturally continue
        break

    menu.items.draw(screen)
    pygame.display.flip()
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
            elif event.type == MOUSEBUTTONDOWN:
                for item in menu.menu_items:
                    if item.touch():
                        if item == menu.menu_items[0]:
                            gridType = "normal"
                        elif item == menu.menu_items[1]:
                            gridType = "obstacle"
                        elif item == menu.menu_items[2]:
                            gridType = "erase"
                        elif item == menu.menu_items[3]:
                            gridType = "portal"
                        break
                else:
                    continue
                break
        else:
            continue
        break
    pygame.mixer.music.stop() #stop music now that done with menu
    newGame(numPlayer, gridType, Player1wins, Player2wins, Player3wins, Player4wins) #start the game with specified number of players

def mainLoop(numPlayer, gridType, grid, screen, clock, Player1wins, Player2wins, Player3wins, Player4wins):
    pygame.mixer.music.load("in game music.mp3") #load new music
    pygame.mixer.music.play(-1) #loop music until stop called
    

    while 1: #infinite loop
            index = len(grid.livePlayers) 
            for i in xrange(index): #for each live player, leave a trail on their current square
                x = grid.getPlayerSquare(grid.livePlayers[i]) 
                x.changeColor((grid.livePlayers[i].color))
            grid.refreshGrid(screen, clock) #update the screen
            for event in pygame.event.get():  #loop through pygame "events" to look for user input  
                 if event.type == QUIT: #exit pygame if user quits
                        pygame.quit()
                 elif event.type == KEYDOWN and event.key == K_ESCAPE: #exit pygame if user quits
                        pygame.quit()
                 elif event.type == KEYDOWN and event.key == K_p: #pause function
                        while 1:
                            for event in pygame.event.get(): #infinitely loops and does not move forward until pause pressed again
                                if event.type == KEYDOWN and event.key == K_p:
                                    break
                            else:
                                continue
                            break
                 elif event.type == KEYDOWN and event.key == K_LEFT: #check for user input that will move player based on current rotation
                        if grid.returnPlayer(green) != False and grid.returnPlayer(green).rotation == 0: #player 1 uses arrow keys (green is player 1 color)
                                    grid.returnPlayer(green).rotateLeft()
                        elif grid.returnPlayer(green) != False and grid.returnPlayer(green).rotation == 180:
                                    grid.returnPlayer(green).rotateRight() 
                 elif event.type == KEYDOWN and event.key == K_RIGHT:
                        if grid.returnPlayer(green) != False and grid.returnPlayer(green).rotation == 0:
                                    grid.returnPlayer(green).rotateRight()
                        elif grid.returnPlayer(green) != False and grid.returnPlayer(green).rotation == 180:
                                    grid.returnPlayer(green).rotateLeft() 
                 elif event.type == KEYDOWN and event.key == K_UP:
                        if grid.returnPlayer(green) != False and grid.returnPlayer(green).rotation == 90:
                                    grid.returnPlayer(green).rotateLeft()
                        elif grid.returnPlayer(green) != False and grid.returnPlayer(green).rotation == 270:
                                    grid.returnPlayer(green).rotateRight() 
                 elif event.type == KEYDOWN and event.key == K_DOWN:
                        if grid.returnPlayer(green) != False and grid.returnPlayer(green).rotation == 90:
                                    grid.returnPlayer(green).rotateRight()
                        elif grid.returnPlayer(green) != False and grid.returnPlayer(green).rotation == 270:
                                    grid.returnPlayer(green).rotateLeft() 
                 elif event.type == KEYDOWN and event.key == K_a: #player 2 uses WASD (orange is player 2 color)
                        if grid.returnPlayer(orange) != False and grid.returnPlayer(orange).rotation == 0:
                                    grid.returnPlayer(orange).rotateLeft()
                        elif grid.returnPlayer(orange) != False and grid.returnPlayer(orange).rotation == 180:
                                    grid.returnPlayer(orange).rotateRight() 
                 elif event.type == KEYDOWN and event.key == K_d:
                        if grid.returnPlayer(orange) != False and grid.returnPlayer(orange).rotation == 0:
                                    grid.returnPlayer(orange).rotateRight()
                        elif grid.returnPlayer(orange) != False and grid.returnPlayer(orange).rotation == 180:
                                    grid.returnPlayer(orange).rotateLeft() 
                 elif event.type == KEYDOWN and event.key == K_w:
                        if grid.returnPlayer(orange) != False and grid.returnPlayer(orange).rotation == 90:
                                    grid.returnPlayer(orange).rotateLeft()
                        elif grid.returnPlayer(orange) != False and grid.returnPlayer(orange).rotation == 270:
                                    grid.returnPlayer(orange).rotateRight() 
                 elif event.type == KEYDOWN and event.key == K_s:
                        if grid.returnPlayer(orange) != False and grid.returnPlayer(orange).rotation == 90:
                                    grid.returnPlayer(orange).rotateRight()
                        elif grid.returnPlayer(orange) != False and grid.returnPlayer(orange).rotation == 270:
                                    grid.returnPlayer(orange).rotateLeft() 
                 elif event.type == KEYDOWN and event.key == K_f: #player 3 uses TFGH (red is player 3 color)
                        if grid.returnPlayer(red) != False and grid.returnPlayer(red).rotation == 0:
                                    grid.returnPlayer(red).rotateLeft()
                        elif grid.returnPlayer(red) != False and grid.returnPlayer(red).rotation == 180:
                                    grid.returnPlayer(red).rotateRight() 
                 elif event.type == KEYDOWN and event.key == K_h:
                        if grid.returnPlayer(red) != False and grid.returnPlayer(red).rotation == 0:
                                    grid.returnPlayer(red).rotateRight()
                        elif grid.returnPlayer(red) != False and grid.returnPlayer(red).rotation == 180:
                                    grid.returnPlayer(red).rotateLeft() 
                 elif event.type == KEYDOWN and event.key == K_t:
                        if grid.returnPlayer(red) != False and grid.returnPlayer(red).rotation == 90:
                                    grid.returnPlayer(red).rotateLeft()
                        elif grid.returnPlayer(red) != False and grid.returnPlayer(red).rotation == 270:
                                    grid.returnPlayer(red).rotateRight() 
                 elif event.type == KEYDOWN and event.key == K_g:
                        if grid.returnPlayer(red) != False and grid.returnPlayer(red).rotation == 90:
                                    grid.returnPlayer(red).rotateRight()
                        elif grid.returnPlayer(red) != False and grid.returnPlayer(red).rotation == 270:
                                    grid.returnPlayer(red).rotateLeft() 
                 elif event.type == KEYDOWN and event.key == K_j: #player 4 uses IJKL (blue is player 4 color)
                        if grid.returnPlayer(blue) != False and grid.returnPlayer(blue).rotation == 0:
                                    grid.returnPlayer(blue).rotateLeft()
                        elif grid.returnPlayer(blue) != False and grid.returnPlayer(blue).rotation == 180:
                                    grid.returnPlayer(blue).rotateRight() 
                 elif event.type == KEYDOWN and event.key == K_l:
                        if grid.returnPlayer(blue) != False and grid.returnPlayer(blue).rotation == 0:
                                    grid.returnPlayer(blue).rotateRight()
                        elif grid.returnPlayer(blue) != False and grid.returnPlayer(blue).rotation == 180:
                                    grid.returnPlayer(blue).rotateLeft()
                 elif event.type == KEYDOWN and event.key == K_i:
                        if grid.returnPlayer(blue) != False and grid.returnPlayer(blue).rotation == 90:
                                    grid.returnPlayer(blue).rotateLeft()
                        elif grid.returnPlayer(blue) != False and grid.returnPlayer(blue).rotation == 270:
                                    grid.returnPlayer(blue).rotateRight()
                 elif event.type == KEYDOWN and event.key == K_k:
                        if grid.returnPlayer(blue) != False and grid.returnPlayer(blue).rotation == 90:
                                    grid.returnPlayer(blue).rotateRight()
                        elif grid.returnPlayer(blue) != False and grid.returnPlayer(blue).rotation == 270:
                                    grid.returnPlayer(blue).rotateLeft() 
                 grid.refreshGrid(screen, clock) #update screen
          
            for p in grid.livePlayers: #after each current square has changed color and player has rotated according to user input, loop through players to move each forward one space
                p.stepForward()
            grid.refreshGrid(screen, clock) #refresh screen
            for p in grid.livePlayers: #loop through players and check to see if any of them moved into another player's trail
                if grid.isDead(p): 
                    grid.removeDeadPlayer(p) #if player has crashed, delete it from list and remove from screen
                
            grid.refreshGrid(screen, clock) #update the screen
            if numPlayer > 1:
               if len(grid.livePlayers) == 1: #check to see if only one player is left, if so break the loop, if not go back through
                   break
            else:
                if len(grid.livePlayers) == 0:
                    break
    if len(grid.livePlayers) == 1:
        if grid.livePlayers[0].color == green: #once loop is broken update player number of wins
            Player1wins = Player1wins + 1
        
        if grid.livePlayers[0].color == orange:
            Player2wins = Player2wins + 1
        
        if grid.livePlayers[0].color == red:
            Player3wins = Player3wins + 1
        
        if grid.livePlayers[0].color == blue:
            Player4wins = Player4wins + 1
        
    #go to game over screen, display each player's win count and ask if player would like to restart
    screen.fill((0,0,0))
    font = pygame.font.Font(None, 20) #set up font   
    text = font.render("Game Over! Would you like to play again? press y to restart, m to return to the menu, or n to quit. win count below in order of player number: " + str(Player1wins) + ", " + str(Player2wins) + ", " +  str(Player3wins) + ", " +  str(Player4wins), True, (255,255,255), (0,0,0)) 
    textRect = text.get_rect()
    screen.blit(text, textRect)
    pygame.display.flip()
    while 1: #infinite loop
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_y: #if player says yes return to newGame method
                newGame(numPlayer, gridType, Player1wins, Player2wins, Player3wins, Player4wins)
                pygame.mixer.music.stop()
            elif event.type == KEYDOWN and event.key == K_m: #to return to menu
                menuLoop(Player1wins, Player2wins, Player3wins, Player4wins)
                pygame.mixer.music.stop()
            elif event.type == KEYDOWN and event.key == K_n: #if player says no break the loop and stop the music/exit game
                break
        else:
            continue
        break

    pygame.mixer.music.stop()
    pygame.quit()
    sys.exit()

class Menu:
     def __init__(self): #initialize instance of menu
        self.menu_items = [] #create a list to store buttons
        self.items = pygame.sprite.RenderPlain() #set up sprite data set to store buttons
        self.mainScreenCreate() #run mainScreenCreate method since menu will always start with this screen

     def createItems(self, item_image):
            #create the buttons within menu (buttons are instances of item class)
            width, height = item_image.get_size() #width and height of buttons determined by size of image
            item_rect = pygame.Rect(0,0, width, height) #create rect for image (will initially place in top left corner)
            item = Item(item_rect, item_image, width, height) #create item
            self.menu_items.append(item) #add item to list for accesibility  
            self.items.add(item) #add item to sprite data set for drawing
            
     def mainScreenCreate(self):

            self.createItems(pygame.image.load("play_button.gif").convert_alpha()) #create play button
            
            self.createItems(pygame.image.load("Tron Title Screen.png").convert_alpha()) #create title text
        
            self.createItems(pygame.image.load("Instructions.png").convert_alpha()) #create instructions button
            #reposition buttons so that they are aligned correctly
            self.reposition(0, (600, 400)) #play
            self.reposition(1, (300, 20)) #title text
            self.reposition(2, (850, 700)) #instructions
           


     def playerScreenCreate(self):
            for i in xrange(2, -1, -1):
                self.items.remove(self.menu_items[i]) #remove previously created items from list (the main menu items)
                self.menu_items.pop(i) #remove previously created items from sprite data set
            
            self.createItems(pygame.image.load("how many players.png").convert_alpha()) #create how many players text
        
            self.createItems(pygame.image.load("2.png").convert_alpha()) #create 2 button
        
            self.createItems(pygame.image.load("3.png").convert_alpha()) #create 3 button
        
            self.createItems(pygame.image.load("4.png").convert_alpha()) #create 4 button
            self.createItems(pygame.image.load("1.png").convert_alpha())
            #reposition buttons so that they are aligned correctly
            self.reposition(0, (200, 50)) #question text
            self.reposition(1, (500, 600)) #2
            self.reposition(2, (700, 600)) #3
            self.reposition(3, (900, 600)) #4
            self.reposition(4, (300, 600)) #1

            #then reposition here
     def levelScreenCreate(self):
        for i in xrange(4, -1, -1):
                self.items.remove(self.menu_items[i]) #remove previously created items from list (the main menu items)
                self.menu_items.pop(i) #remove previously created items from sprite data set
        self.createItems(pygame.image.load("normal.png").convert_alpha())
        self.createItems(pygame.image.load("obstacle.png").convert_alpha())
        self.createItems(pygame.image.load("erase.png").convert_alpha())
        self.createItems(pygame.image.load("portal.png").convert_alpha())
        self.reposition(0, (100, 100)) 
        self.reposition(1, (100, 500)) 
        self.reposition(2, (800, 100)) 
        self.reposition(3, (800, 500)) 

     def reposition(self, index, new_pos):
        #reposition items method, takes in a new position and creates a new rect with correct item and height/width at that position
        
        self.menu_items[index].rect = pygame.Rect(new_pos, (self.menu_items[index].width, self.menu_items[index].height))

     

class Item(pygame.sprite.Sprite):
    #items are the buttons on screen
     def __init__(self, rect, image, width, height):
        self.rect = rect #instantiate items with a rect, image, width, and height from params
        self.image = image
        self.width = width
        self.height = height
        pygame.sprite.Sprite.__init__(self) #set up items for sprites
     
     def touch(self):
        #returns whether or not mouse is touching a menu item

        return self.rect.collidepoint((pygame.mouse.get_pos()))

class Grid:
    # make it so width of grid doesn't have to match height
    def __init__(self, sizex, sizey, num_players):
        self.sizex = sizex
        self.sizey = sizey
        self.squares = pygame.sprite.RenderPlain()
        self.gridSquares = {}

        self.num_players = num_players
        self.players = pygame.sprite.RenderPlain()
        self.livePlayers = []
        self.location = 0
        self.currFrame = 0
        self.initializeSquares()

        # initialize starting positions of all players
    def initializePlayers(self, num_players):    
        player0 = Player(self.sizey/4, self.sizex/2, DOWN, green, 0, self)    # in place of self, we may want an integer for mini_grid(s)
        self.livePlayers.append(player0)
        if num_players > 1:
           player1 = Player(self.sizey/2, 3*self.sizex/4, LEFT, orange, 1, self)
           self.livePlayers.append(player1)
        if num_players == 3 or num_players == 4:
           player2 = Player(3*self.sizey/4, self.sizex/2, UP, red, 2, self)
           self.livePlayers.append(player2)
        if num_players == 4:
           player3 = Player(self.sizey/2, self.sizex/4, RIGHT, blue, 3, self)
           self.livePlayers.append(player3)

        for i in self.livePlayers:
            self.players.add(i)

        
    def initializeSquares(self):
        for i in xrange(self.sizey):
            for j in xrange(self.sizex):
                s = Square(i,j,COLOR)
                s.rect = s.getRect(self.location)
                self.gridSquares[(i,j)] = s
                self.squares.add(s) 

    def drawGrid(self, screen): 
        ''' draws grid '''
    
        for r in xrange(self.sizey + 1):
            pygame.draw.line(screen, white, (getColLeftLoc(0), getRowTopLoc(r)), (getColLeftLoc(self.sizex), getRowTopLoc(r))) #drawing horizontal lines        
        for c in xrange(self.sizex + 1):
            pygame.draw.line(screen, white, (getColLeftLoc(c), getRowTopLoc(0)), (getColLeftLoc(c), getRowTopLoc(self.sizey))) #drawing vertical lines
        
    def refreshGrid(self, screen, clock):
        """
        Draw square sprites, draw the grid, and draw the player sprites 

        MAKE SURE THE THINGS YOUR REFRESHING ARE IN ORDER, otherwise they will refresh over each other
        """ 
        self.squares.draw(screen) #draw Sprites (Squares)
        self.drawGrid(screen)
        self.players.draw(screen) #draw player Sprite    

        pygame.display.flip() #update screen
        clock.tick(30)

    def getSquare(self, x, y): 

        return self.gridSquares[(y,x)]

    def resetColor(self,color):
        '''
        deletes trails for dead players
        '''

        for g in self.gridSquares:
            if self.gridSquares[g].color == color:
                self.gridSquares[g].changeColor(black)


    ### Player related methods
    def getPlayerSquare(self, player):
        """
        Returns the a Square object of the specified Player's position
        """
        y = player.row # changing x and y (may cause problems) !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! 
        x = player.col

        return self.getSquare(x, y)

    def isDead(self, player):
        """
        Checks if player has collided with a wall or Player object and returns a boolean 
        """

        return self.getPlayerSquare(player).color != COLOR

    def removeDeadPlayer(self, player):
        """
        Checks method isDead() and removes player for entire game (grid)
        """        
        self.livePlayers.remove(player)
        self.players.remove(player)

    def returnPlayer(self, color): #returns a given instance of player based on color. check for green for P1, orange for P2, etc
        for p in self.livePlayers:
            if p.color == color:
                return p
        return False

class eraseGrid(Grid):
    """

    """

    def __init___(self, sizex,sizey,num_players):
        Grid.__init__(self,sizex,sizey,num_players)
        

    
    def deleteTrails(self):
        for g in self.gridSquares:
            self.gridSquares[g].changeColor(grey);

    def wall(self):
        for i in xrange(self.sizex):      #draws wall along border with white squares
            self.gridSquares[(0,i)].color = white
            self.gridSquares[(self.sizey-1, i)].color = white
            Square.changeColor(self.gridSquares[(0,i)], white)
            Square.changeColor(self.gridSquares[(self.sizey-1, i)], white)
        for j in xrange(self.sizey):
            self.gridSquares[(j,0)].color = white
            self.gridSquares[(j,self.sizex-1)].color = white
            Square.changeColor(self.gridSquares[(j,0)], white)
            Square.changeColor(self.gridSquares[(j,self.sizex-1)], white)

    def refreshGrid(self, screen, clock):
        """
        Draw square sprites, draw the grid, and draw the player sprites 

        MAKE SURE THE THINGS YOUR REFRESHING ARE IN ORDER, otherwise they will refresh over each other
        """ 
        #if time == something
        self.currFrame = self.currFrame + 1
        if self.currFrame >= 600:
            self.deleteTrails()
            self.currFrame = 0
            self.wall()

        self.squares.draw(screen) #draw Sprites (Squares)
        self.drawGrid(screen)
        self.players.draw(screen) #draw player Sprite    

        pygame.display.flip() #update screen
        clock.tick(60) #players are moving faster than normal grid

class obstacleGrid(Grid): 
    """
    sublclass of Grid, inherits all of its methods, 
    but will actually use the ones relating only to Square (first five)
    same as regular grid but as 1/40 obstacle white squares in random locations
    needs to be instantiated in mainloop and incorporated
    """

    def __init__(self, sizex, sizey, num_players):
        
        Grid.__init__(self, sizex, sizey, num_players)
        self.randomMaze()
        #offsets this grid from the original one, directly to right 
            

    def randomMaze(self):
        for i in xrange(self.sizey):
            for j in xrange(self.sizex):
                r = random.randint(0,40)     #populates board with random colored squares
                if r == 0:
                    self.gridSquares[(i,j)].color = (255,255,255)
                    Square.changeColor(self.gridSquares[(i,j)], (255,255,255))
    

class portalGrid(Grid):
    def __init__(self, sizex,sizey, num_players):
        Grid.__init__(self, sizex, sizey, num_players)

        self.pi1 = 0 #initially maps the initial portal to (0,0) and (1,1)
        self.pj1 = 0
        self.pi2 = 1
        self.pj2 = 1
        #self.link = (self.gridSquares[(self.pi1,self.pj1)], self.gridSquares[(self.pi2,self.pj2)]) #tuple that holds two squares
        #self.portal = (0,0)

    def createPortal(self):
        '''
        potential idea:
        after a given amount of time, randomly generate portals on 2 new squares so only on 2 squares at once and moving around (don't change color, but add an image on top)
        can use random number generator to generate an i and j value for 2 squares that can be used for portals
        '''

        while 1:
            self.pi1 = random.randint(0,self.sizex-1) # creates random index values for potential portal squares
            self.pj1 = random.randint(0,self.sizey-1)
            self.pi2 = random.randint(0,self.sizex-1)
            self.pj2 = random.randint(0,self.sizey-1)
            if self.getSquare(self.pi1,self.pj1).color == COLOR and self.getSquare(self.pi2,self.pj2).color == COLOR and self.pi1 != self.pi2 and self.pj1 != self.pj2:

                self.gridSquares[(self.pj1,self.pi1)].changeColor(yellow)
                self.gridSquares[(self.pj2,self.pi2)].changeColor(yellow)
                self.gridSquares[(self.pj1,self.pi1)].image = pygame.image.load('portal2.jpeg').convert_alpha() 
                self.gridSquares[(self.pj1,self.pi1)].image = pygame.transform.scale(self.gridSquares[(self.pj1,self.pi1)].image, (WIDTH, HEIGHT))
                self.gridSquares[(self.pj2,self.pi2)].image = pygame.image.load('portal2.jpeg').convert_alpha() 
                self.gridSquares[(self.pj2,self.pi2)].image = pygame.transform.scale(self.gridSquares[(self.pj2,self.pi2)].image, (WIDTH, HEIGHT))
                break

    def teleportPlayer(self,player):
        """
        Changes player's row and col value and teleports player
        """
        print 'teleport'
        if player.col == self.pi1:
            player.col = self.pi2
        elif player.col == self.pi2:
            player.col = self.pi1
        if player.row == self.pj1:
            player.row = self.pj2
        elif player.row == self.pj2:
            player.row = self.pj1
        self.deletePortal()

    def deletePortal(self):
        self.gridSquares[(self.pj1,self.pi1)].changeColor(grey)
        self.gridSquares[(self.pj2,self.pi2)].changeColor(grey)

    def isDead(self, player):
        """
        Checks if player is on a teleport square first, if so, calls teleport function
        and then checks has collided with a wall or Player object and returns a boolean 
        """
        if self.getPlayerSquare(player).color == yellow:
            self.teleportPlayer(player)
        else:
            return self.getPlayerSquare(player).color != COLOR

    def refreshGrid(self, screen, clock):
        """
        Draw square sprites, draw the grid, and draw the player sprites 

        MAKE SURE THE THINGS YOUR REFRESHING ARE IN ORDER, otherwise they will refresh over each other
        """ 
        #if time == something
        self.currFrame = self.currFrame + 1
        if self.currFrame >= 100:
            self.deletePortal()
            self.createPortal()
            self.currFrame = 0

        self.squares.draw(screen) #draw Sprites (Squares)
        self.drawGrid(screen)
        self.players.draw(screen) #draw player Sprite    

        pygame.display.flip() #update screen
        clock.tick(30) #players are moving faster than normal grid

class Square(pygame.sprite.Sprite):
    def __init__(self, row, col, color):
        pygame.sprite.Sprite.__init__(self)
        self.row = row
        self.col = col
        self.image = pygame.Surface([WIDTH, HEIGHT])
        self.rect = self.image.get_rect() 
        self.color = color
        self.image.fill(color)

    def getRect(self, location):
        return pygame.Rect(getColLeftLoc(self.col, location), getRowTopLoc(self.row, location), WIDTH, HEIGHT)
    
    def getColor(self):
        return self.color

    def changeColor(self, color):
        '''
        Changes the color of the square.  
        Assumes that mainloop will assign correct color in argument based on which player is on the square 
        '''

        self.color = color
        self.image.fill(self.color) 
   

class Player(pygame.sprite.Sprite):
    def __init__(self, row, col, rotation, color, player_num, grid):
        pygame.sprite.Sprite.__init__(self)

        self.row = row
        self.col = col
        self.player_num = player_num
        self.color = color
        self.grid = grid        
        
        self.losses = 0       # we need to figure out how to keep track of these
        self.game_num = 0   # this too

        self.rect = pygame.Rect(getColLeftLoc(col) + 1, getRowTopLoc(row) + 1, WIDTH, HEIGHT)
        self.setPic()
        self.rotation = rotation  # we may want to randomize this later !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.image = pygame.transform.rotate(self.image, -self.rotation) # rotates player to initial specifications


    # def 

    def rotateLeft(self):
        """
        Rotates the player 90 degrees counterclockwise
        """
        self.image = pygame.transform.rotate(self.image, 90)
    
        if ((self.rotation - 90) < 0):
            self.rotation = 270
        else:
            self.rotation -= 90

    def rotateRight(self):
        """
        Rotates the plater 90 degrees clockwise
        """
        self.image = pygame.transform.rotate(self.image, -90)

        if ((self.rotation + 90) > 270):
            self.rotation = 0
        else:
            self.rotation += 90     

    def stepForward(self):
        """
        Make the player take a step forward in whatever direction it's currently pointing.
        """
        # assigns new coordinates
        if(self.rotation == UP):
            self.row -= (1)
        elif(self.rotation == RIGHT):
            self.col += (1)
        elif(self.rotation == DOWN):
            self.row += (1)
        else:
            self.col -= (1)

        # incorporates wrapping
        if(self.col == self.grid.sizex):
            self.col = 0
        if(self.col == -1):
            self.col = self.grid.sizex - 1

        if(self.row == self.grid.sizey):
            self.row = 0
        if(self.row == -1):
            self.row = self.grid.sizey - 1 

        self.rect = pygame.Rect(getColLeftLoc(self.col) + 1, getRowTopLoc(self.row) + 1, WIDTH, HEIGHT) # I added one to these coordinates to account for the grid lines (This makes the player centered in the square)
 
    def teleport(self, new_grid):
        """
        Checks which Square the player is on, and transfers them to the same Square on another grid
        """

        pass    

    def setPic(self):
        """
        Sets the image of the player
        """
        self.image = pygame.image.load('player_%d.png' % (self.player_num)).convert_alpha() # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! I'm not sure if it will like this line, we need to figure out what to name the images for each player
        self.image = pygame.transform.scale(self.image, (WIDTH - 1, HEIGHT - 1))


menuLoop(0,0,0,0)

