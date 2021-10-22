import pygame
import random
import math

# All images are original
class Character(pygame.sprite.Sprite):
    
    def __init__(self, x, y, density):
        image = "DOOD.png"
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (165, 165))
        self.mask =  pygame.mask.from_surface(self.image)

        self.x = x
        self.y = y
        self.mass = 1
        self.density = density
        self.volume = self.mass / 1

        self.width = 80
        self.height = 120
        self.baseImage = self.image 

        self.rect = self.mask.get_bounding_rects()[0]
        self.rect = pygame.Rect(self.x + 58, self.y + 33, 40, 78)  

        self.clickedOn = False
        self.collidedH = False
        self.collidedW = False

        self.velocity = Vector(0,0)
        self.gravityForce = 0.00000981 + 0.001
        self.bouyantForce = -1 * self.volume * .000981
        self.dragForcex = (0.005) * (0.047) * (density) * (1) * self.velocity.xComponent**2
        self.dragForcey = (0.005) * (0.047) * (density) * (1) * self.velocity.yComponent**2
        self.momentum = 0 

        self.netForceY = self.gravityForce + self.bouyantForce + self.dragForcey
        self.netForceX = self.dragForcex
    
    def updateRect(self):
        self.rect = pygame.Rect(self.x + 58, self.y + 33, 40, 78)  
    
    def updateDensity(self):
        self.dragForcex = (0.005) * (0.047) * (self.density) * (1) * self.velocity.xComponent**2
        self.dragForcey = (0.005) * (0.047) * (self.density) * (1) * self.velocity.yComponent**2
        self.netForceY = self.gravityForce + self.bouyantForce + self.dragForcey
        self.netForceX = self.dragForcex

class Instructions(object):
    def __init__(self):
        self.on = False
        self.bg = pygame.image.load("tmp 04-28-2020 04-08-14.png")
        self.bg = pygame.transform.scale(self.bg, (Game.width, Game.height))
        self.message = pygame.image.load("Instrutions.PNG")
        self.message = pygame.transform.scale(self.message, (800, 700))
        self.exitRect = pygame.Rect(1105, 35, 60, 55)
        
class OpeningScreen(object):
    def __init__(self):
        self.on = True
        self.bg = pygame.image.load("BGborder.PNG")
        self.bg = pygame.transform.scale(self.bg, (Game.width, Game.height))
        self.Font = pygame.font.SysFont('Bahnschrift', 90)
        self.textColor = (255,255,255)
        self.levelButton = Button("levelSelect.PNG", Game.width//2 - 250, Game.height//2, 192, 186,100)
        self.levelMakerButton = Button("Level create button.png", Game.width//2 + 10, Game.height//2, 192, 186,100)
        self.instructionsButton = Button("Inst.png", Game.width//2 - 250, Game.height//2 + 100, 200, 90,0)
        self.highScoresButton =  Button("HighScores.png", Game.width//2 + 7, Game.height//2 + 111, 200, 70,0)

class HighScoresList(object):
    def __init__(self):
        self.on = False
        self.bg = pygame.image.load("tmp 04-28-2020 04-08-14.png")
        self.bg = pygame.transform.scale(self.bg, (Game.width, Game.height))
        self.exitRect = pygame.Rect(1105, 35, 60, 55)
        self.textColor = (255, 255, 255)
        self.Font = pygame.font.SysFont('Impact MS', 50)
        
        self.level1File = "Level1Scores.txt"
        self.level2File = "Level2Scores.txt"
        self.level3File = "Level3Scores.txt"
        self.level1Scores = self.readFile("Level1Scores.txt")
        self.level2Scores = self.readFile("Level2Scores.txt")
        self.level3Scores = self.readFile("Level2Scores.txt")

        self.level1Surfaces = [None for i in range(10)] + [pygame.Surface((10,10))]
        self.level2Surfaces = [None for i in range(10)] + [pygame.Surface((10,10))]
        self.level3Surfaces = [None for i in range(10)] + [pygame.Surface((10,10))]
        self.updateScores()

    # FIle functions take from https://www.cs.cmu.edu/~112/notes/notes-strings.html#basicFileIO
    @staticmethod
    def readFile(path):
        with open(path, "rt") as f:
            return f.read()

    @staticmethod
    def writeFile(path, contents):
        with open(path, "wt") as f:
            f.write(contents)
    
    def saveScore(self, level, timer):
        if isinstance(level, Level1): 
            level = self.level1Scores
            f = self.level1File
        elif isinstance(level, Level2): 
            level = self.level2Scores
            f = self.level2File
        elif isinstance(level, Level3): 
            level = self.level3Scores
            f = self.level3File
        score = str(timer)
        results = ""
        addedScore = False
        r = 9
        i = -1
        while i < r:
            i += 1
            num = level.splitlines()[i]
            if (int(score) < int(num)) and (not addedScore):
                results += score
                results += "\n"
                r = 8
                addedScore = True
            results += num
            results += "\n"
        self.writeFile(f,results)

    def updateScores(self):
        self.level1Scores = self.readFile("Level1Scores.txt")
        self.level2Scores = self.readFile("Level2Scores.txt")
        self.level3Scores = self.readFile("Level3Scores.txt")
        index = -1
        for num in self.level1Scores.split("\n"):
            index += 1
            surface = self.Font.render(str(num), False, self.textColor)
            self.level1Surfaces[index] = surface
        heading1 = self.Font.render("Level 1", False, self.textColor)
        self.level1Surfaces.insert(0, heading1) 
        index = -1
        for num in self.level2Scores.split("\n"):
            index += 1
            surface = self.Font.render(str(num), False, self.textColor)
            self.level2Surfaces[index] = surface
        heading1 = self.Font.render("Level 2", False, self.textColor)
        self.level2Surfaces.insert(0, heading1) 
        index = -1
        for num in self.level3Scores.split("\n"):
            index += 1
            surface = self.Font.render(str(num), False, self.textColor)
            self.level3Surfaces[index] = surface
        heading1 = self.Font.render("Level 3", False, self.textColor)
        self.level3Surfaces.insert(0, heading1) 

class CYOLScreen(object):
    def __init__(self):
        self.on = False
        self.objectSelectSize = 100
        self.objectSelectRect = (0, 0, Game.width, self.objectSelectSize)
        self.CYOlevelborders = (0, self.objectSelectSize, Game.width, Game.height - self.objectSelectSize)

        self.Font = pygame.font.SysFont('Impact MS', 50)
        self.winText = "You win!"
        self.textColor = (255, 255, 255)
        self.winSurface = self.Font.render(self.winText, False, self.textColor)

        self.error = -1

        self.x = 0
        self.endCount = 0
        self.keyCount = 0

        self.keyImage = pygame.image.load("Key.PNG")
        self.keyImage = pygame.transform.scale(self.keyImage, (50, 50)) 
        self.keyClickedOn = False
        self.keyImageX = -100
        self.keyImageY = -100
        self.actualKeyRect = pygame.Rect(self.keyImageX, self.keyImageY, 50, 50)
        self.hasKey = False
        self.lockedIndex = -1
        
        self.endPlatformRect = pygame.Rect(20, 30, 80, 70)
        self.upRect = pygame.Rect(125, 30, 70, 60)
        self.downRect = pygame.Rect(210, 30, 70, 60)
        self.leftRect = pygame.Rect(300, 30, 60, 69)
        self.rightRect = pygame.Rect(380, 30, 60, 70)
        self.barrierRect = pygame.Rect(525, 60, 90, 15)
        self.keyRect = pygame.Rect(450, 30, 60, 70)
        self.vertBarrierRect = pygame.Rect(647, 20, 15, 90)
        self.densitySliderRec = pygame.Rect(450, 450, 15, 90)
        self.startGameRect = pygame.Rect(900, 30, 100, 60)

        self.CYOLDensitySliderCircX = 780
        self.CYOLDensitySliderCircY = 52
        self.CYOLDensitySliderCircClickedOn = False
        self.CYOLDensitySliderCirc = pygame.Rect(self.CYOLDensitySliderCircX, self.CYOLDensitySliderCircY, 25, 25)

        self.CYOLrestartRect = pygame.Rect(1027, 35, 60, 55)
        self.CYOLExitRect = pygame.Rect(1105, 35, 60, 55)

        self.startPlat = None
        self.endPlat = None
        self.liquidDensity = 2
    
    def update(self):
        self.CYOLDensitySliderCirc = pygame.Rect(self.CYOLDensitySliderCircX, 52, 25, 25)
        self.actualKeyRect = pygame.Rect(self.keyImageX, self.keyImageY, 50, 50)

class LevelScreen(object):
    def __init__(self):
        self.on = False
        self.bg = pygame.image.load("levelSelectBG.png")
        self.bg = pygame.transform.scale(self.bg, (Game.width, Game.height))
        self.Font = pygame.font.SysFont('Bahnschrift', 90)
        self.textColor = (255,255,255)

        self.levelList = []
        self.level1 = Level1()
        self.level2 = Level2()
        self.level3 = Level3()
        self.levelList = [self.level1, self.level2, self.level3]

        self.winImage = pygame.image.load("Win.png")
        self.winImage = pygame.transform.scale(self.winImage, (600, 350))
        self.winArrow = pygame.Rect(348,420,180,30)

class Level1(object):
    def __init__(self):
        self.name = "1"

        self.on = False
        self.bg = pygame.image.load("Level bg.png")
        self.bg = pygame.transform.scale(self.bg, (Game.width, Game.height)) 
        self.rect = pygame.Rect(295, 215, 160, 150)
        self.textColor = (255, 255, 255)
        self.Font = pygame.font.SysFont('Impact MS', 50)
        self.barrierList = [Barrier(50,407,"vertical"), Barrier(50,322,"vertical", 130), Barrier(135,220,"horizontal"), Barrier(-7,7,"horizontal"), 
                            Barrier(178,7,"horizontal"), Barrier(365,7,"horizontal"), Barrier(457,116,"vertical"), 
                            Barrier(539,202,"horizontal"), Barrier(248,322,"vertical",130), Barrier(248,407,"vertical"), Barrier(333,350,"horizontal"), 
                            Barrier(520,350,"horizontal"), Barrier(726,202,"horizontal"), Barrier(911,202,"horizontal"), 
                            Barrier(706,350,"horizontal"), Barrier(1024,303,"vertical"), Barrier(818,451,"vertical"), Barrier(1025,412,"vertical") ]
        
        self.upRect = pygame.Rect(30, 30, 85, 70)
        self.downRect = pygame.Rect(120, 30, 100, 60)
        self.leftRect = pygame.Rect(240, 30, 120, 40)
        self.rightRect = pygame.Rect(340, 30, 80, 60)
        self.startGameRect = pygame.Rect(900, 30, 100, 60)
        self.restartRect = pygame.Rect(1027, 35, 60, 55)
        self.exitRect = pygame.Rect(1105, 35, 60, 55)

        self.timer = 0
        self.scoreSurface = self.Font.render(str(self.timer), False, self.textColor)
        
        self.bubbleColList = []
        self.bubbleRowList = []
        self.start = Start(0, 450)
        self.end = End(950, 450) 

class Level2(object):
    def __init__(self):
        self.name = "2"

        self.on = False
        self.bg = pygame.image.load("Level bg.png")
        self.bg = pygame.transform.scale(self.bg, (Game.width, Game.height)) 
        
        self.keyImage = pygame.image.load("Key.PNG")
        self.keyImage = pygame.transform.scale(self.keyImage, (50, 50)) 
        self.keyRect = pygame.Rect(380, 200, 50, 50)
        self.hasKey = False

        self.rect = pygame.Rect(515, 215, 160, 150)

        self.textColor = (255, 255, 255)
        self.Font = pygame.font.SysFont('Impact MS', 50)
        
        self.barrierList = [Barrier(444, 193, 'horizontal', 50), Barrier(314, 193, 'horizontal', 50),
                            Barrier(-8, 367, "horizontal"), Barrier(93, 290 ,"vertical"), Barrier(93, 226, 'vertical'), Barrier(168 ,126, 'horizontal', 150), 
                            Barrier(270, 118, 'vertical'), Barrier(365, 118 ,'vertical'),  Barrier(489, 126, 'horizontal'), Barrier(405, 118, 'vertical'),
                            Barrier(885, 450, 'vertical', 50), Barrier(261, 450, 'vertical', 50), Barrier(224, 118, 'vertical'),
                            Barrier(625, 126, 'horizontal'), Barrier(804, 126, 'horizontal'),  Barrier(335, 340, 'horizontal'), 
                            Barrier(515, 340, 'horizontal'), Barrier(783 ,340, 'horizontal'),  Barrier(683 ,340, 'horizontal'),
                            Barrier(515, 380, 'horizontal'), Barrier(783 ,380, 'horizontal'),  Barrier(683 ,380, 'horizontal'), Barrier(335, 380, 'horizontal'),
                            Barrier(909 ,113, 'vertical'), LockedBarrier(994, 270 ,'horizontal') ] # pop the last element when u get key 
        
        self.start = Start(0, 455)
        self.end = End(1020, 140) 

        self.timer = 0
        self.scoreSurface = self.Font.render(str(self.timer), False, self.textColor)

        self.upRect = pygame.Rect(30, 30, 85, 70)
        self.downRect = pygame.Rect(120, 30, 100, 60)
        self.leftRect = pygame.Rect(240, 30, 120, 40)
        self.rightRect = pygame.Rect(340, 30, 80, 60)
        self.startGameRect = pygame.Rect(900, 30, 100, 60)
        self.restartRect = pygame.Rect(1027, 35, 60, 55)
        self.exitRect = pygame.Rect(1105, 35, 60, 55)

class Level3(object):
    def __init__(self):
        self.name = "3"

        self.on = False
        self.bg = pygame.image.load("Level 2 bg.png")
        self.bg = pygame.transform.scale(self.bg, (Game.width, Game.height)) 
        
        self.rect = pygame.Rect(740, 215, 160, 150)
        self.textColor = (255, 255, 255)
        self.Font = pygame.font.SysFont('Impact MS', 50)
        
        self.barrierList = [Barrier(-5, 360, 'horizontal'), Barrier(96, 281, 'vertical'),
                            Barrier(96, 115, 'vertical'), Barrier(178, 320, 'vertical', 154), Barrier(252, 360, 'horizontal'), Barrier(172, 115, 'vertical', 100), 
                            Barrier(246, 100, 'horizontal'), Barrier(252, 217, 'horizontal'), Barrier(426, 217, 'horizontal'),
                            Barrier(426, 100, 'horizontal'), Barrier(432, 360, 'horizontal'), Barrier(608, 217, 'horizontal'),
                            Barrier(601, 100, 'horizontal'), Barrier(782, 100, 'horizontal'),  Barrier(885, 115, 'vertical', 100), 
                            Barrier(662, 217, 'horizontal'), Barrier(885, 323, 'vertical', 110),  Barrier(964, 220, 'horizontal'), Barrier(562, 360, 'horizontal'), 
                            Barrier(1000, 220, 'horizontal'), Barrier(763, 323, 'vertical', 154),  Barrier(662, 360, 'horizontal'), Barrier(660, 360, 'horizontal'),
                            Barrier(1000, 311, 'horizontal'), Barrier(964, 311, 'horizontal'), Barrier(964, 415, 'vertical', 180) ]  
        
        self.start = Start(0, 455)
        self.end = End(1010, 150) 

        self.timer = 0
        self.scoreSurface = self.Font.render(str(self.timer), False, self.textColor)

        self.upRect = pygame.Rect(30, 30, 85, 70)
        self.downRect = pygame.Rect(120, 30, 100, 60)
        self.leftRect = pygame.Rect(240, 30, 120, 40)
        self.rightRect = pygame.Rect(340, 30, 80, 60)
        self.startGameRect = pygame.Rect(900, 30, 100, 60)
        self.restartRect = pygame.Rect(1027, 35, 60, 55)
        self.exitRect = pygame.Rect(1105, 35, 60, 55)

class Button(object):
    def __init__(self, image, x, y, width, height,minus):
        self.x = x
        self.y = y
        self.Font = pygame.font.SysFont('Bahnschrift', 50)
        self.textColor = (255, 255, 255)
        self.bgColor = (0, 0, 100)
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.surface = self.image
        self.rect = pygame.Rect(self.x, self.y, width, height-minus)

# Simple vector for physics computations            
class Vector(object):

    def __init__(self, xComponent, yComponent):
        self.xComponent = xComponent
        self.yComponent = yComponent
    
    def __str__(self):
        return f"<{self.xComponent},{self.yComponent}>"

    def arrow(self):
        end = (100 * (self.xComponent), 100 * (self.yComponent ))
        return {"end":end }

# Vectors for vector field and graphics
class FieldVector(object):

    def __init__(self, startCoord, components, show):
            self.xLocation = startCoord[0]
            self.yLocation = startCoord[1]
            self.xComponent = components[0]
            self.yComponent = components[1]
            self.show = show
    
    def __repr__(self):
        return f"<{self.xComponent},{self.yComponent}>"
    
    def add(self,other, show):
        x = self.xComponent + other.xComponent
        y = self.yComponent + other.yComponent
        return FieldVector( (self.xLocation, self.yLocation), (x,y), show )
    
    # Deals with arrow graphics 
    def arrow(self):
        if self.xComponent > 0 and self.yComponent == 0:
            start = (self.xLocation, self.yLocation)
            end = (self.xLocation + self.xComponent, self.yLocation - self.yComponent)
            tip1 = (self.xLocation + self.xComponent - 2, self.yLocation - self.yComponent + 5)
            tip2 = (self.xLocation + self.xComponent - 2, self.yLocation - self.yComponent - 2)
        elif self.xComponent < 0 and self.yComponent == 0: 
            start = (self.xLocation, self.yLocation)
            end = (self.xLocation + self.xComponent, self.yLocation - self.yComponent)
            tip1 = (self.xLocation + self.xComponent + 2, self.yLocation + self.yComponent + 5)
            tip2 = (self.xLocation + self.xComponent + 2, self.yLocation + self.yComponent - 2)
        elif self.xComponent == 0 and self.yComponent > 0: 
            start = (self.xLocation, self.yLocation)
            end = (self.xLocation + self.xComponent, self.yLocation - self.yComponent)
            tip1 = (self.xLocation + self.xComponent + 3, self.yLocation - self.yComponent + 5)
            tip2 = (self.xLocation + self.xComponent - 3, self.yLocation - self.yComponent + 5)
        elif self.xComponent == 0 and self.yComponent < 0: 
            start = (self.xLocation, self.yLocation)
            end = (self.xLocation + self.xComponent, self.yLocation - self.yComponent)
            tip1 = (self.xLocation + self.xComponent - 3, self.yLocation - self.yComponent - 5)
            tip2 = (self.xLocation + self.xComponent + 3, self.yLocation - self.yComponent - 5)
        elif self.xComponent < 0 and self.yComponent > 0:
            start = (self.xLocation, self.yLocation)
            end = (self.xLocation + self.xComponent, self.yLocation - self.yComponent)
            tip1 = (self.xLocation + self.xComponent + 2, self.yLocation - self.yComponent - 2)
            tip2 = (self.xLocation + self.xComponent + 2, self.yLocation - self.yComponent + 5)
        elif self.xComponent > 0 and self.yComponent < 0:
            start = (self.xLocation, self.yLocation)
            end = (self.xLocation + self.xComponent, self.yLocation - self.yComponent)
            tip1 = (self.xLocation + self.xComponent - 2, self.yLocation - self.yComponent + 2)
            tip2 = (self.xLocation + self.xComponent - 2, self.yLocation - self.yComponent - 5)
        elif self.xComponent > 0 and self.yComponent > 0:
            start = (self.xLocation, self.yLocation)
            end = (self.xLocation + self.xComponent, self.yLocation - self.yComponent)
            tip1 = (self.xLocation + self.xComponent - 2, self.yLocation - self.yComponent - 2)
            tip2 = (self.xLocation + self.xComponent - 2, self.yLocation - self.yComponent + 5)
        elif self.xComponent < 0 and self.yComponent < 0:
            start = (self.xLocation, self.yLocation)
            end = (self.xLocation + self.xComponent, self.yLocation - self.yComponent)
            tip1 = (self.xLocation + self.xComponent + 2, self.yLocation - self.yComponent + 2)
            tip2 = (self.xLocation + self.xComponent + 2, self.yLocation - self.yComponent - 5)
        else:
            start = (self.xLocation, self.yLocation + 1)
            end = (self.xLocation , self.yLocation)
            tip1 = (self.xLocation -1, self.yLocation)
            tip2 = (self.xLocation + 1, self.yLocation)
        return {"start":start, "end":end, "tip1":tip1, "tip2":tip2 }
    
    def updateRect(self):
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size) 

class GameObject(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(GameObject, self).__init__()
        self.clickedOn = False
        self.x = x
        self.y = y 

class BubbleMaker(GameObject):
    def __init__(self, x, y, strength):
        super().__init__(x,y)
        self.bubbles = pygame.sprite.Group()
        self.vectorGridHeight = Game.vectorGridHeight
        self.vectorGridWidth = Game.vectorGridWidth
        self.strength = strength

    def updateRect(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

class Bubble(pygame.sprite.Sprite):
    bubbleList = []
    def __init__(self,x,y, vectorComponents, mass, density):

        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.color = (0, 200, 255)
        self.mass = mass
        self.size = math.sqrt(self.mass / 1) * 1000

        
        self.dragForcex = (0.0001) * (0.047) * (density) * (1) * vectorComponents[0]
        self.dragForcey = (0.0001) * (0.047) * (density) * (1) * vectorComponents[1]
        self.dvx = self.dragForcex / self.mass
        self.dvy = self.dragForcey / self.mass
        self.velocity = Vector(vectorComponents[0] - self.dvx, vectorComponents[1] - self.dvy)

        self.rect = pygame.Rect(self.x, self.y, self.size, self.size) 
    
    def updateRect(self):
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size) 

class BubbleDown(BubbleMaker):
    def __init__(self, x, y, strength, density):
        super().__init__(x,y,strength)
        image = "left.PNG"
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.image = pygame.transform.rotate(self.image, -90)
        self.baseImage = self.image

        self.width, self.height = self.image.get_size()

        self.columnRect = pygame.Rect(self.x,0,self.width,self.y + self.height)
        self.rect = self.image.get_rect()

        # Sepcifies range for vector graphics and bubble creation
        self.colStart = self.y // Game.vectorGridHeight
        self.colEnd = self.colStart + 20
        if self.colEnd > Game.vectorGridRows:
            self.colEnd = (Game.height) // Game.vectorGridHeight
        self.rowStart = (self.x) // Game.vectorGridWidth 
        self.rowEnd = (self.x + self.width) // Game.vectorGridWidth

        self.yStrength = strength
        self.density = density

    def makeBubbles(self):
        xLoc = random.randint(self.x, self.x + self.height)
        self.bubbles.add(Bubble(xLoc, self.y + self.height, (0, 0.05), 0.00002, self.density))

    def updateRect(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height) 
        self.columnRect = pygame.Rect(self.x, self.y, self.width,self.y + self.height)
        self.colStart = (self.y + self.height) // Game.vectorGridHeight
        self.colEnd = self.colStart + 20
        if self.colEnd > Game.vectorGridRows:
            self.colEnd = (Game.height) // Game.vectorGridHeight
        self.rowStart = (self.x) // Game.vectorGridWidth + 1
        self.rowEnd = (self.x + self.width) // Game.vectorGridWidth + 1

    def updateVectorField(self, vectorField, clear):
        for i in range(self.rowStart, self.rowEnd):
            for j in range(self.colStart, self.colEnd):
                if clear:
                    vectorField[i][j] = vectorField[i][j].add(FieldVector((0,0), (0, self.yStrength), False), False)
                elif self.colStart > 8:
                    vectorField[i][j] = vectorField[i][j].add(FieldVector((0,0), (0, -self.yStrength), True), True)
    
    def update(self):
        self.updateRect()

class BubbleUp(BubbleMaker):
    def __init__(self, x, y, strength, density):
        super().__init__(x,y, strength)
        image = "up.PNG"
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.baseImage = self.image

        self.width, self.height = self.image.get_size()

        self.columnRect = pygame.Rect(self.x,0,self.width,self.y + self.height)
        self.rect = self.image.get_rect()

        # Sepcifies range for vector graphics and bubble creation
        self.colStart = self.y // Game.vectorGridHeight
        self.colEnd = (self.y + self.height) // Game.vectorGridHeight
        self.rowStart = (self.x) // Game.vectorGridWidth 
        self.rowEnd = (self.x + self.width) // Game.vectorGridWidth

        self.yStrength = strength
        self.density = density

    
    def makeBubbles(self):
        xLoc = random.randint(self.x, self.x + self.height)
        self.bubbles.add(Bubble(xLoc, self.y, (0, -0.05), 0.00002, self.density))
    
    def updateRect(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height) 
        self.columnRect = pygame.Rect(self.x, self.y, self.width,self.y + self.height)
        self.colEnd = (self.y + self.height) // Game.vectorGridHeight
        self.colStart = self.colEnd - 20
        if self.colStart < (100 // Game.vectorGridHeight):
            self.colStart = 100 // Game.vectorGridHeight
        self.rowStart = (self.x) // Game.vectorGridWidth + 1
        self.rowEnd = (self.x + self.width) // Game.vectorGridWidth + 1
    
    def updateVectorField(self, vectorField, clear):
        for i in range(self.rowStart, self.rowEnd):
            for j in range(self.colStart, self.colEnd):
                if clear:
                    vectorField[i][j] = vectorField[i][j].add(FieldVector((0,0), (0, -self.yStrength), False), False)
                elif self.colStart > 7:
                    vectorField[i][j] = vectorField[i][j].add(FieldVector((0,0), (0, self.yStrength), True), True) 
    
    def update(self):
        self.updateRect()

class BubbleLeft(BubbleMaker):
    def __init__(self, x, y, strength, density):
        super().__init__(x,y, strength)
        image = "up.PNG"
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.image = pygame.transform.rotate(self.image, 90)
        self.baseImage = self.image

        self.width, self.height = self.image.get_size()

        self.rowRect = pygame.Rect(0, self.y, self.x + self.width, self.height)
        self.rect = self.image.get_rect()

        self.colStart = self.y // Game.vectorGridHeight + 1
        self.colEnd = (self.y + self.height) // Game.vectorGridHeight - 1
        self.rowEnd = (self.x + self.width) // Game.vectorGridWidth 
        self.rowStart = self.rowEnd - 15
        if self.rowStart < 0:
            self.rowStart = 0 // Game.vectorGridWidth 
        self.xStrength = strength
        self.density = density
    
    def makeBubbles(self):
        yLoc = random.randint(self.y, self.y + self.width)
        self.bubbles.add(Bubble(self.x, yLoc, (-0.05, 0), 0.00002, self.density))

    def updateRect(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height) 
        self.columnRect = pygame.Rect(self.x, self.y, self.width,self.y + self.height)
        self.colStart = self.y // Game.vectorGridHeight + 1
        self.colEnd = (self.y + self.height) // Game.vectorGridHeight - 1
        self.rowEnd = (self.x + self.width) // Game.vectorGridWidth 
        self.rowStart = self.rowEnd - 15
        if self.rowStart < 0:
            self.rowStart = 0 // Game.vectorGridWidth 
        
    def updateVectorField(self, vectorField, clear):
        for i in range(self.rowStart, self.rowEnd):
            for j in range(self.colStart, self.colEnd):
                if clear:
                    vectorField[i][j] = vectorField[i][j].add(FieldVector((0,0), (self.xStrength, 0), False), False)
                elif self.colStart > 7:
                    vectorField[i][j] = vectorField[i][j].add(FieldVector((0,0), (-self.xStrength, 0), True), True)
    
    def update(self):
        self.updateRect()

class BubbleRight(BubbleMaker):
    def __init__(self, x, y, strength, density):
        #print(density)
        super().__init__(x,y,strength)
        image = "Left.PNG"
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.baseImage = self.image

        self.width, self.height = self.image.get_size()

        self.rowRect = pygame.Rect(0, self.y, self.x + self.width, self.height)
        self.rect = self.image.get_rect()

        self.colStart = self.y // self.vectorGridHeight + 1
        self.colEnd = (self.y + self.height) // self.vectorGridHeight - 1
        self.rowStart = (self.x + self.width) // self.vectorGridWidth 
        self.rowEnd = self.rowStart + 15
        if self.rowEnd > (Game.width // self.vectorGridWidth ):
            self.rowEnd = Game.width // self.vectorGridWidth 

        self.xStrength = strength
        self.density = density

    
    def makeBubbles(self):
        yLoc = random.randint(self.y, self.y + self.width)
        self.bubbles.add(Bubble(self.x + self.width, yLoc, (0.05, 0), 0.00002, self.density))

    def updateRect(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height) 
        self.columnRect = pygame.Rect(self.x, self.y, self.width,self.y + self.height)
        self.colStart = self.y // self.vectorGridHeight + 1
        self.colEnd = (self.y + self.height) // self.vectorGridHeight - 1
        self.rowStart = (self.x + self.width) // self.vectorGridWidth 
        self.rowEnd = self.rowStart + 15
        if self.rowEnd > (Game.width // self.vectorGridWidth ):
            self.rowEnd = Game.width // self.vectorGridWidth 
        
    def updateVectorField(self, vectorField, clear):
        for i in range(self.rowStart, self.rowEnd):
            for j in range(self.colStart, self.colEnd):
                if clear:
                    vectorField[i][j] = vectorField[i][j].add(FieldVector((0,0), (-self.xStrength, 0), False), False)
                elif self.colStart > 8:
                    vectorField[i][j] = vectorField[i][j].add(FieldVector((0,0), (self.xStrength, 0), True), True)
    
    def update(self):
        self.updateRect()

class Barrier(GameObject):

    def __init__(self, x, y, orientation, size=None):
        super().__init__(x,y) 
        image = "Border.PNG"
        self.image = pygame.image.load(image).convert_alpha()

        self.orientation = orientation

        self.size = size

        # Rects hardcoded to fix discrepancies with image size and actual barrier size 
        if self.size == None:
            self.image = pygame.transform.scale(self.image, (200, 200))
            if self.orientation == "vertical":
                self.image = pygame.transform.rotate(self.image, -90)
                self.width, self.height = self.image.get_size()
                self.rect = pygame.Rect(self.x + self.width//2 - 30, self.y + 10, 35, self.height - 20)
            else:
                self.width, self.height = self.image.get_size()
                self.rect = pygame.Rect(self.x + 10, self.y + self.height//2 + 6, self.width - 27, 13)
        else:
            if self.orientation == "vertical":
                self.image = pygame.transform.scale(self.image, (size, 200))
                self.image = pygame.transform.rotate(self.image, -90)
                self.width, self.height = self.image.get_size()
                self.rect = pygame.Rect(self.x + self.width//2 - 20, self.y + 5, 12, self.height-7)
            else:
                self.image = pygame.transform.scale(self.image, (size, 200))
                self.width, self.height = self.image.get_size()
                self.rect = pygame.Rect(self.x + 10, self.y + self.height//2 + 5, self.width, 13)
        
        self.group = pygame.sprite.Group()
    
    def updateRect(self):
        # Barriers also hardcoded to make collisions more smooth 
        if self.size == None:
            self.image = pygame.transform.scale(self.image, (200, 200))
            if self.orientation == "vertical":
                self.width, self.height = self.image.get_size()
                self.rect = pygame.Rect(self.x + self.width//2 - 38, self.y + 10, 35, self.height - 20)
            else:
                self.width, self.height = self.image.get_size()
                self.rect = pygame.Rect(self.x + 12, self.y + self.height//2 + 8, self.width - 27, 13)
        else:
            if self.orientation == "vertical":
                self.image = pygame.transform.scale(self.image, (size, 200))
                self.width, self.height = self.image.get_size()
                self.rect = pygame.Rect(self.x + self.width//2 - 13, self.y + 5, 9, self.height-7)
            else:
                self.width, self.height = self.image.get_size()
                self.rect = pygame.Rect(self.x + self.width//2 + 5, self.y, size, 15)

class LockedBarrier(Barrier):

    def __init__(self, x, y, orientation, size=None):
        super().__init__(x,y, orientation, size=None) 
        image = "Locked border.png"
        self.image = pygame.image.load(image).convert_alpha()

        self.orientation = orientation

        self.size = size

        if self.size == None:
            self.image = pygame.transform.scale(self.image, (200, 50))
            if self.orientation == "vertical":
                self.image = pygame.transform.rotate(self.image, -90)
                self.width, self.height = self.image.get_size()
                self.rect = pygame.Rect(self.x + 10, self.y, 25, self.height)
            else:
                self.width, self.height = self.image.get_size()
                self.rect = pygame.Rect(self.x, self.y + 10, self.width, 25)

    def updateRect(self):
        if self.size == None:
            if self.orientation == "vertical":
                self.width, self.height = self.image.get_size()
                self.rect = pygame.Rect(self.x + 10, self.y, 25, self.height)
            else:
                self.width, self.height = self.image.get_size()
                self.rect = pygame.Rect(self.x, self.y + 10, self.width, 25)

# Object to specify where the character starts for each respective level
class Start(GameObject):

    def __init__(self,x,y):
        super().__init__(x,y)
        image = "DOOD.png"
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (165, 165))
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 150, 150)
        self.color = (201, 0, 232) 
    
    def updateRect(self):
        self.rect = pygame.Rect(self.x, self.y, 50, 50) 

# Object to specify where the end chest is located for each respective level
class End(GameObject):
    
    def __init__(self,x,y):
        super().__init__(x,y)
        image = "Chest.PNG"
        self.image = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.x = x
        self.y = y

        self.width = 150
        self.height = 150
        self.rect = pygame.Rect(self.x + 25, self.y + 20, self.width-70, self.height-50)
    
    def updateRect(self):
        self.rect = pygame.Rect(self.x + 25, self.y + 20, self.width-70, self.height-50)

# Framework adapted from http://blog.lukasperaza.com/getting-started-with-pygame/ 
class Game(object):
    width = 1200
    height = 600
    screen = pygame.display.set_mode((width, height))

    # Dimensions for the vector field
    vectorGridRows = 50
    vectorGridCols = 50
    vectorGridWidth = width // vectorGridCols
    vectorGridHeight = height // vectorGridRows 

    def __init__(self):
        self.fps = 200
        self.title = "Scuba Adventure"
        self.bgColor = (250,250,250)
        self.bg = pygame.image.load("CYOLBG.png")
        self.bg = pygame.transform.scale(self.bg, (Game.width, Game.height))
        self.xBorder = Game.width - 50
        self.yBorder = Game.height - 50
        pygame.init()
        pygame.font.init()

        self.vectorGrid = []
        self.initializeVectorGrid()
    
        self.openingScreen = OpeningScreen()
        self.CYOLScreen = CYOLScreen()
        self.levelScreen = LevelScreen()
        self.instructions = Instructions()
        self.highScoreList = HighScoresList()

        self.runGame = False
        self.win = False

        self.go = False
        self.hold = False

        self.gameObjectList = []
        self.barrierList = []
        self.bubbleColList = []
        self.bubbleRowList = []
        self.barrierGroup = pygame.sprite.Group()

        self.character = Character(0,450,0)

    # Initlize a blank vector field
    def initializeVectorGrid(self):
        for i in range(0, Game.vectorGridRows):
            vectorRow = []
            for j in range(0, Game.vectorGridCols):
                vectorRow.append(FieldVector( (i * Game.vectorGridWidth, j * Game.vectorGridHeight), (0, 0), False ))
            self.vectorGrid.append(vectorRow)
   
   # Calculates collision velocites of 2 objects
   # Assumes a perfectly elastic collision, equations derived from conservation of momentum and kinetic energy
    def calcVelocity(self, object1, object2):
        originalXvelocity = object1.velocity.xComponent
        object1.velocity.xComponent = ( (object1.mass - object2.mass) / (object1.mass + object2.mass) ) * object1.velocity.xComponent + ( (2 * object2.mass) / (object1.mass + object2.mass) ) * object2.velocity.xComponent
        object2.velocity.xComponent = ( (2 * object1.mass) / (object1.mass + object2.mass) ) * originalXvelocity - ( ((object1.mass - object2.mass) / (object1.mass + object2.mass)) * object2.velocity.xComponent )
        originalYvelocity = object1.velocity.yComponent
        object1.velocity.yComponent = ( (object1.mass - object2.mass) / (object1.mass + object2.mass) ) * object1.velocity.yComponent + ( (2 * object2.mass) / (object1.mass + object2.mass) ) * object2.velocity.yComponent
        object2.velocity.yComponent = ( (2 * object1.mass) / (object1.mass + object2.mass) ) * originalYvelocity - ( ((object1.mass - object2.mass) / (object1.mass + object2.mass)) * object2.velocity.yComponent )

    def timerFired(self, dt):
        if self.runGame:
            if self.CYOLScreen.endPlat != None:
                self.CYOLScreen.endPlat.update()
                if self.character.rect.colliderect(self.CYOLScreen.endPlat.rect):
                    self.runGame = False
                    self.win = True
            
            if self.CYOLScreen.on:
                # Deals with placing keys and locked barriers 
                if self.CYOLScreen.keyCount == 2:
                    if self.character.rect.colliderect(self.CYOLScreen.actualKeyRect):
                        self.CYOLScreen.hasKey = True
                        self.barrierList.pop(self.CYOLScreen.lockedIndex)
                        self.barrierGroup = pygame.sprite.Group()
                        for barrier in self.barrierList:
                            self.barrierGroup.add(barrier)
                        self.CYOLScreen.keyImageY = -100
                        self.CYOLScreen.keyCount += 1

            if self.levelScreen.level1.on:
                self.levelScreen.level1.timer += 1

            if self.levelScreen.level2.on:
                self.levelScreen.level2.timer += 1
                # Deals with the key and the locked barrier
                if self.levelScreen.level2.hasKey == False:
                    if self.character.rect.colliderect(self.levelScreen.level2.keyRect):
                        self.levelScreen.level2.hasKey = True
                        self.levelScreen.level2.keyRect = (1000,1000,50,50)
                if self.levelScreen.level2.hasKey == True:
                    self.levelScreen.level2.barrierList.pop()
                    self.barrierGroup = self.levelScreen.level2.barrierList
                    self.levelScreen.level2.hasKey = False

            if self.levelScreen.level3.on:
                self.levelScreen.level3.timer += 1

            # Borders 
            if self.character.x + self.character.width + 30 > Game.width-10:
                self.character.x =  Game.width - 10 - self.character.width - 30
                self.character.velocity.x = 0
            if self.character.x < -50:
                self.character.x = -50
                self.character.velocity.x = 0
            if self.character.y + self.character.height >= 595:
                self.character.y = 595 - self.character.height
                self.character.velocity.y = 0
            elif self.character.y < 90:
                self.character.y = 90
                self.character.velocity.y = 0
            
            # Deals with bubble collisions with character 
            for bubbleCol in self.bubbleColList:
                bubbleCol.makeBubbles()
                for bubble in bubbleCol.bubbles:
                    if self.character.rect.colliderect(bubble.rect):
                        self.calcVelocity(self.character, bubble)
                        bubbleCol.bubbles.remove(bubble)
                    if bubble.y < 130:
                        bubbleCol.bubbles.remove(bubble)
                    if pygame.sprite.spritecollideany(bubble, self.barrierGroup):
                        bubbleCol.bubbles.remove(bubble)
                    
                    oldX = self.character.x
                    oldY = self.character.y

                    self.character.x += self.character.velocity.xComponent * dt
                    self.character.y += self.character.velocity.yComponent * dt

                    # Caracter collisions with barriers
                    if pygame.sprite.spritecollideany(self.character, self.barrierGroup):
                        collisions = pygame.sprite.spritecollide(self.character, self.barrierGroup, False, False)
                        for barrier in collisions:
                            if barrier.orientation == "horizontal":
                                self.character.collidedH = True
                                self.character.y = oldY
                                self.character.velocity.yComponent = 0
                            if barrier.orientation == "vertical":
                                self.character.collidedW = True
                                self.character.x = oldX
                                self.character.velocity.xComponent = 0

                    
                    bubble.x += bubble.velocity.xComponent * dt
                    bubble.y += bubble.velocity.yComponent * dt
                    self.character.updateRect()
                    bubble.updateRect()
            
            for bubbleRow in self.bubbleRowList:
                bubbleRow.makeBubbles()
                for bubble in bubbleRow.bubbles:
                    if self.character.rect.colliderect(bubble.rect):
                        self.calcVelocity(self.character, bubble)
                        bubbleRow.bubbles.remove(bubble)
                    if bubble.y < 130:
                        bubbleRow.bubbles.remove(bubble)
                    if pygame.sprite.spritecollideany(bubble, self.barrierGroup):
                        bubbleRow.bubbles.remove(bubble)
                    
                    oldX = self.character.x
                    oldY = self.character.y

                    self.character.x += self.character.velocity.xComponent * dt
                    self.character.y += self.character.velocity.yComponent * dt

                    if pygame.sprite.spritecollideany(self.character, self.barrierGroup):
                        collisions = pygame.sprite.spritecollide(self.character, self.barrierGroup, False, False)
                        for barrier in collisions:
                            if barrier.orientation == "horizontal":
                                self.character.collidedH = True
                                self.character.y = oldY
                                self.character.velocity.yComponent = 0
                            if barrier.orientation == "vertical":
                                self.character.collidedW = True
                                self.character.x = oldX
                                self.character.velocity.xComponent = 0

                    
                    bubble.x += bubble.velocity.xComponent * dt
                    bubble.y += bubble.velocity.yComponent * dt
                    self.character.updateRect()
                    bubble.updateRect()
            
            #Only move when not collided with a barrier
            if not self.character.collidedW and not self.character.collidedH:
                self.character.momentum += self.character.netForceY
                self.character.y += (self.character.momentum / self.character.mass) * dt
            
            # Deals with bubble collisions with eachother
            for bubbleCol in self.bubbleColList:
                for bubbleRow in self.bubbleRowList:
                    collisions = pygame.sprite.groupcollide(bubbleCol.bubbles, bubbleRow.bubbles, False, False)
                    for bubble1 in collisions:
                        for bubble2 in collisions[bubble1]:
                            # Almost perfectly elastic collisions (add x and y components)
                            bubble1.velocity.xComponent = bubble2.velocity.xComponent 
                            bubble1.velocity.yComponent -= 0.0001 # Subtract a small amount to make sure bubbles arent moving too fast
                            bubble2.velocity.yComponent = bubble1.velocity.yComponent 
                            bubble2.velocity.xComponent += 0.0001
                            bubble2.updateRect()
                            bubble1.updateRect()
            
            self.character.collidedH = False
            self.character.collidedW = False

            # Collisions with treasure chest
            for level in self.levelScreen.levelList:
                if level.on:
                    if self.character.rect.colliderect(level.end.rect):
                        self.highScoreList.saveScore(level, level.timer)
                        self.highScoreList.updateScores()
                        self.runGame = False
                        self.win = True
            
    # Deals with all mouse presses 
    def mousePressed(self, pos):
        x, y = pos[0], pos[1]
        self.CYOLScreen.error = -1 
        if x > 0 and x < Game.width and y > 0 and y < Game.height:
            if self.openingScreen.on:
                if self.openingScreen.levelMakerButton.rect.collidepoint((x,y)):
                    self.openingScreen.on = False 
                    self.CYOLScreen.on = True
                if self.openingScreen.levelButton.rect.collidepoint((x,y)):
                    self.openingScreen.on = False 
                    self.levelScreen.on = True
                if self.openingScreen.instructionsButton.rect.collidepoint((x,y)):
                    self.openingScreen.on = False 
                    self.instructions.on = True
                if self.openingScreen.highScoresButton.rect.collidepoint((x,y)):
                    self.openingScreen.on = False 
                    self.highScoreList.on = True
            
            elif self.instructions.on:
                if self.instructions.exitRect.collidepoint((x,y)):
                    self.instructions.on = False
                    self.openingScreen.on = True 
            
            elif self.highScoreList.on:
                if self.highScoreList.exitRect.collidepoint((x,y)):
                    self.highScoreList.on = False
                    self.openingScreen.on = True 
            
            elif self.CYOLScreen.on:
                # Deals with key placing and barrier clicking
                if self.CYOLScreen.keyCount == 1:
                    for barrier in self.barrierList:
                        if barrier.rect.collidepoint((x,y)):
                            self.CYOLScreen.lockedIndex = self.barrierList.index(barrier)
                            self.barrierList[self.CYOLScreen.lockedIndex] = LockedBarrier(barrier.x + 70, barrier.y + 70, barrier.orientation)
                            self.CYOLScreen.keyCount += 1
                            self.CYOLScreen.error = -1 

                self.CYOLScreen.CYOLDensitySliderCircClickedOn = False

                # Deals with placing chests 
                if self.CYOLScreen.endPlatformRect.collidepoint((x,y)):
                    if self.CYOLScreen.endCount == 0:
                        self.CYOLScreen.endPlat = End(x,y)
                        self.gameObjectList.append(self.CYOLScreen.endPlat)
                        self.CYOLScreen.endCount += 1
                        self.CYOLScreen.endPlat.clickedOn = True 
                    else:
                        self.CYOLScreen.error = 1
                # Deals with creating game objects when clicking on their respective rects
                elif self.CYOLScreen.upRect.collidepoint((x,y)):
                    obj = BubbleUp(x,y,10,self.CYOLScreen.liquidDensity)
                    self.bubbleColList.append(obj)
                    obj.clickedOn = True
                elif self.CYOLScreen.downRect.collidepoint((x,y)):
                    obj = BubbleDown(x,y,10,self.CYOLScreen.liquidDensity)
                    self.bubbleColList.append(obj)
                    obj.clickedOn = True
                elif self.CYOLScreen.leftRect.collidepoint((x,y)):
                    obj = BubbleLeft(x,y,10,self.CYOLScreen.liquidDensity)
                    self.bubbleRowList.append(obj)
                    obj.clickedOn = True
                elif self.CYOLScreen.rightRect.collidepoint((x,y)):
                    obj = BubbleRight(x,y,10,self.CYOLScreen.liquidDensity)
                    self.bubbleRowList.append(obj)
                    obj.clickedOn = True
                elif self.CYOLScreen.barrierRect.collidepoint((x,y)):
                    obj = Barrier(x,y, "horizontal")
                    self.barrierList.append(obj)
                    obj.add(self.barrierGroup)
                    obj.clickedOn = True
                elif self.CYOLScreen.vertBarrierRect.collidepoint((x,y)):
                    obj = Barrier(x,y, "vertical")
                    self.barrierList.append(obj)
                    obj.add(self.barrierGroup)
                    obj.clickedOn = True
                elif self.CYOLScreen.CYOLDensitySliderCirc.collidepoint((x,y)):
                    self.CYOLScreen.CYOLDensitySliderCircClickedOn = True
                elif self.CYOLScreen.startGameRect.collidepoint((x,y)):
                    self.runGame = True
                elif self.CYOLScreen.CYOLrestartRect.collidepoint((x,y)):
                    self.CYOLScreen = CYOLScreen()
                    self.character = Character(0,450,0)
                    self.CYOLScreen.on = True
                    self.gameObjectList = []
                    self.barrierGroup = pygame.sprite.Group()
                    self.barrierList = []
                    self.bubbleColList = []
                    self.bubbleRowList = []
                    self.win = False
                    self.runGame = False 
                elif self.CYOLScreen.CYOLExitRect.collidepoint((x,y)):
                    self.CYOLScreen.on = False
                    self.CYOLScreen.keyCount = 0
                    self.CYOLScreen.hasKey = False
                    self.CYOLScreen.keyImageX = -100
                    self.CYOLScreen.keyImageY = -100
                    self.CYOLScreen.lockedIndex = -1
                    self.CYOLScreen = CYOLScreen()
                    self.gameObjectList = []
                    self.barrierList = []
                    self.bubbleColList = []
                    self.bubbleRowList = []
                    self.win = False
                    self.runGame = False 
                    self.openingScreen.on = True
                
                # If you click on an already placed piece
                for obj in self.gameObjectList:
                    if obj.rect.collidepoint((x,y)):
                        obj.clickedOn = True
                for row in self.bubbleRowList:
                    if row.rect.collidepoint((x,y)):
                        row.clickedOn = True
                for col in self.bubbleColList:
                    if col.rect.collidepoint((x,y)):
                        col.clickedOn = True
                for barrier in self.barrierList:
                    if barrier.rect.collidepoint((x,y)):
                        barrier.clickedOn = True
                if self.character.rect.collidepoint((x,y)):
                    self.character.clickedOn = True
                if self.CYOLScreen.keyRect.collidepoint((x,y)):
                    if self.CYOLScreen.keyCount >= 1:
                        self.CYOLScreen.error = 2
                    elif len(self.barrierList) == 0:
                        self.CYOLScreen.error = 3
                    else:
                        self.CYOLScreen.keyClickedOn = True
                        self.CYOLScreen.keyCount += 1
                        self.CYOLScreen.error = 0
                if self.CYOLScreen.actualKeyRect.collidepoint((x,y)):
                    self.CYOLScreen.keyClickedOn = True
            
            elif self.levelScreen.on:
                # Initializes levels when pressed
                if self.levelScreen.level1.rect.collidepoint((x,y)):
                    self.levelScreen.level1.on = True
                    self.levelScreen.on = False
                    self.barrierList = self.levelScreen.level1.barrierList
                    for barrier in self.barrierList:
                        barrier.add(self.barrierGroup) 
                    self.gameObjectList.extend([self.levelScreen.level1.end])
                    self.character = Character(self.levelScreen.level1.start.x, self.levelScreen.level1.start.y, self.CYOLScreen.liquidDensity)
                elif self.levelScreen.level2.rect.collidepoint((x,y)):
                    self.levelScreen.level2.on = True
                    self.levelScreen.on = False
                    self.levelScreen.level2.hasKey = False
                    self.levelScreen.level2.keyRect = pygame.Rect(380, 200, 50, 50)
                    self.barrierList = self.levelScreen.level2.barrierList
                    for barrier in self.barrierList:
                        barrier.add(self.barrierGroup) 
                    self.gameObjectList.extend([self.levelScreen.level2.end])
                    self.character = Character(self.levelScreen.level2.start.x, self.levelScreen.level2.start.y, self.CYOLScreen.liquidDensity)
                elif self.levelScreen.level3.rect.collidepoint((x,y)):
                    self.levelScreen.level3.on = True
                    self.levelScreen.on = False
                    self.barrierList = self.levelScreen.level3.barrierList
                    for barrier in self.barrierList:
                        barrier.add(self.barrierGroup) 
                    self.gameObjectList.extend([self.levelScreen.level3.end])
                    self.character = Character(self.levelScreen.level3.start.x, self.levelScreen.level3.start.y, self.CYOLScreen.liquidDensity)
                elif self.CYOLScreen.CYOLExitRect.collidepoint((x,y)):
                    self.gameObjectList = []
                    self.barrierList = []
                    self.bubbleColList = []
                    self.bubbleRowList = []
                    self.barrierGroup = pygame.sprite.Group()
                    self.runGame = False 
                    self.levelScreen.level1.on = False
                    self.levelScreen.on = False
                    self.openingScreen.on = True
            
            elif self.levelScreen.level1.on:
                # Deals with going to the next level from a previous level
                if self.win:
                    if self.levelScreen.winArrow.collidepoint((x,y)):
                        self.levelScreen.level1.on = False
                        self.gameObjectList = []
                        self.barrierList = []
                        self.bubbleColList = []
                        self.bubbleRowList = []
                        self.barrierGroup = pygame.sprite.Group()
                        self.levelScreen.level2.on = True
                        self.barrierList = self.levelScreen.level2.barrierList
                        for barrier in self.barrierList:
                            barrier.add(self.barrierGroup) 
                        self.gameObjectList.extend([self.levelScreen.level2.end])
                        self.character = Character(self.levelScreen.level2.start.x, self.levelScreen.level2.start.y, self.CYOLScreen.liquidDensity)
                        self.levelScreen.level2.on = True
                        self.win= False

                if self.levelScreen.level1.upRect.collidepoint((x,y)):
                    obj = BubbleUp(x,y,10,self.CYOLScreen.liquidDensity)
                    obj.updateVectorField(self.vectorGrid, True)
                    obj.updateVectorField(self.vectorGrid, False)   
                    self.bubbleColList.append(obj)
                    obj.clickedOn = True
                elif self.levelScreen.level1.downRect.collidepoint((x,y)):
                    obj = BubbleDown(x,y,10,self.CYOLScreen.liquidDensity)
                    obj.updateVectorField(self.vectorGrid, True)
                    obj.updateVectorField(self.vectorGrid, False)
                    self.bubbleColList.append(obj)
                    obj.clickedOn = True
                elif self.levelScreen.level1.leftRect.collidepoint((x,y)):
                    obj = BubbleLeft(x,y,10,self.CYOLScreen.liquidDensity)
                    obj.updateVectorField(self.vectorGrid, True)
                    obj.updateVectorField(self.vectorGrid, False)
                    self.bubbleRowList.append(obj)
                    obj.clickedOn = True
                elif self.levelScreen.level1.rightRect.collidepoint((x,y)):
                    obj = BubbleRight(x,y,10,self.CYOLScreen.liquidDensity)
                    obj.updateVectorField(self.vectorGrid, True)
                    obj.updateVectorField(self.vectorGrid, False)
                    self.bubbleRowList.append(obj)
                    obj.clickedOn = True
                elif self.levelScreen.level1.startGameRect.collidepoint((x,y)):
                    self.runGame = True 
                elif self.levelScreen.level1.restartRect.collidepoint((x,y)):
                    self.gameObjectList = []
                    self.barrierList = []
                    self.bubbleColList = []
                    self.bubbleRowList = []
                    self.barrierGroup = pygame.sprite.Group()
                    self.barrierList = self.levelScreen.level1.barrierList
                    self.levelScreen.level1.timer = 0
                    for barrier in self.barrierList:
                        barrier.add(self.barrierGroup) 
                    self.gameObjectList.extend([self.levelScreen.level1.end])
                    self.character = Character(self.levelScreen.level1.start.x, self.levelScreen.level1.start.y, self.CYOLScreen.liquidDensity)
                    self.runGame = False 
                    self.win = False
                elif self.levelScreen.level1.exitRect.collidepoint((x,y)):
                    self.levelScreen.level1.timer = 0
                    self.gameObjectList = []
                    self.barrierList = []
                    self.bubbleColList = []
                    self.bubbleRowList = []
                    self.barrierGroup = pygame.sprite.Group()
                    self.runGame = False 
                    self.win = False
                    self.levelScreen.level1.on = False
                    self.levelScreen.on = True

                # If you click on an already placed piece
                for obj in self.gameObjectList:
                    if obj.rect.collidepoint((x,y)):
                        obj.clickedOn = True
                for row in self.bubbleRowList:
                    if row.rect.collidepoint((x,y)):
                        row.clickedOn = True
                for col in self.bubbleColList:
                    if col.rect.collidepoint((x,y)):
                        col.clickedOn = True

            elif self.levelScreen.level2.on:
                if self.win:
                    if self.levelScreen.winArrow.collidepoint((x,y)):
                        self.levelScreen.level2.on = False
                        self.levelScreen.level2.barrierList.append(LockedBarrier(994, 270 ,'horizontal'))
                        self.levelScreen.level2.hasKey = False
                        self.levelScreen.level3.on = True
                        self.bubbleColList = []
                        self.bubbleRowList = []
                        self.gameObjectList = []
                        self.barrierList = self.levelScreen.level3.barrierList
                        self.barrierGroup = pygame.sprite.Group()
                        for barrier in self.barrierList:
                            barrier.add(self.barrierGroup) 
                        self.gameObjectList.extend([self.levelScreen.level3.end])
                        self.character = Character(self.levelScreen.level3.start.x, self.levelScreen.level3.start.y, self.CYOLScreen.liquidDensity)
                        self.levelScreen.level3.on = True
                        self.win= False

                if self.levelScreen.level2.upRect.collidepoint((x,y)):
                    obj = BubbleUp(x,y,10,self.CYOLScreen.liquidDensity)
                    obj.updateVectorField(self.vectorGrid, True)
                    obj.updateVectorField(self.vectorGrid, False)   
                    self.bubbleColList.append(obj)
                    obj.clickedOn = True
                elif self.levelScreen.level2.downRect.collidepoint((x,y)):
                    obj = BubbleDown(x,y,10,self.CYOLScreen.liquidDensity)
                    obj.updateVectorField(self.vectorGrid, True)
                    obj.updateVectorField(self.vectorGrid, False)
                    self.bubbleColList.append(obj)
                    obj.clickedOn = True
                elif self.levelScreen.level2.leftRect.collidepoint((x,y)):
                    obj = BubbleLeft(x,y,10,self.CYOLScreen.liquidDensity)
                    obj.updateVectorField(self.vectorGrid, True)
                    obj.updateVectorField(self.vectorGrid, False)
                    self.bubbleRowList.append(obj)
                    obj.clickedOn = True
                elif self.levelScreen.level2.rightRect.collidepoint((x,y)):
                    obj = BubbleRight(x,y,10,self.CYOLScreen.liquidDensity)
                    obj.updateVectorField(self.vectorGrid, True)
                    obj.updateVectorField(self.vectorGrid, False)
                    self.bubbleRowList.append(obj)
                    obj.clickedOn = True
                elif self.levelScreen.level2.startGameRect.collidepoint((x,y)):
                    self.runGame = True 
                elif self.levelScreen.level2.restartRect.collidepoint((x,y)):
                    self.gameObjectList = []
                    self.barrierList = []
                    self.bubbleColList = []
                    self.bubbleRowList = []
                    self.levelScreen.level2.barrierList.append(LockedBarrier(994, 270 ,'horizontal') )
                    self.barrierList = self.levelScreen.level2.barrierList
                    self.barrierGroup = pygame.sprite.Group()
                    for barrier in self.barrierList:
                        barrier.add(self.barrierGroup) 
                    self.gameObjectList.extend([self.levelScreen.level2.end])
                    self.character = Character(self.levelScreen.level2.start.x, self.levelScreen.level2.start.y, self.CYOLScreen.liquidDensity)
                    self.levelScreen.level2.hasKey = False
                    self.levelScreen.level2.keyRect = pygame.Rect(380, 200, 50, 50)
                    self.levelScreen.level2.timer = 0
                    self.runGame = False 
                    self.win = False
                elif self.levelScreen.level2.exitRect.collidepoint((x,y)):
                    self.gameObjectList = []
                    self.barrierList = []
                    self.bubbleColList = []
                    self.bubbleRowList = []
                    self.levelScreen.level2.timer = 0
                    self.barrierGroup = pygame.sprite.Group()
                    self.runGame = False 
                    self.levelScreen.level2.hasKey = False
                    self.levelScreen.level2.on = False
                    self.levelScreen.on = True
                    self.win = False

                # If you click on an already placed piece
                for obj in self.gameObjectList:
                    if obj.rect.collidepoint((x,y)):
                        obj.clickedOn = True
                for row in self.bubbleRowList:
                    if row.rect.collidepoint((x,y)):
                        row.clickedOn = True
                for col in self.bubbleColList:
                    if col.rect.collidepoint((x,y)):
                        col.clickedOn = True

            elif self.levelScreen.level3.on:
                # Winning 3rd level takes you back to level select
                if self.win:
                    if self.levelScreen.winArrow.collidepoint((x,y)):
                        self.levelScreen.level3.on = False
                        self.levelScreen.on = True
                        self.bubbleColList = []
                        self.bubbleRowList = []
                        self.barrierList = []
                        self.gameObjectList = []
                        self.win = False

                if self.levelScreen.level3.upRect.collidepoint((x,y)):
                    obj = BubbleUp(x,y,10,self.CYOLScreen.liquidDensity)
                    obj.updateVectorField(self.vectorGrid, True)
                    obj.updateVectorField(self.vectorGrid, False)   
                    self.bubbleColList.append(obj)
                    obj.clickedOn = True
                elif self.levelScreen.level3.downRect.collidepoint((x,y)):
                    obj = BubbleDown(x,y,10,self.CYOLScreen.liquidDensity)
                    obj.updateVectorField(self.vectorGrid, True)
                    obj.updateVectorField(self.vectorGrid, False)
                    self.bubbleColList.append(obj)
                    obj.clickedOn = True
                elif self.levelScreen.level3.leftRect.collidepoint((x,y)):
                    obj = BubbleLeft(x,y,10,self.CYOLScreen.liquidDensity)
                    obj.updateVectorField(self.vectorGrid, True)
                    obj.updateVectorField(self.vectorGrid, False)
                    self.bubbleRowList.append(obj)
                    obj.clickedOn = True
                elif self.levelScreen.level3.rightRect.collidepoint((x,y)):
                    obj = BubbleRight(x,y,10,self.CYOLScreen.liquidDensity)
                    obj.updateVectorField(self.vectorGrid, True)
                    obj.updateVectorField(self.vectorGrid, False)
                    self.bubbleRowList.append(obj)
                    obj.clickedOn = True
                elif self.levelScreen.level3.startGameRect.collidepoint((x,y)):
                    self.runGame = True 
                elif self.levelScreen.level3.restartRect.collidepoint((x,y)):
                    self.gameObjectList = []
                    self.barrierList = []
                    self.bubbleColList = []
                    self.bubbleRowList = []
                    self.barrierList = self.levelScreen.level3.barrierList
                    for barrier in self.barrierList:
                        barrier.add(self.barrierGroup) 
                    self.gameObjectList.extend([self.levelScreen.level3.end])
                    self.character = Character(self.levelScreen.level3.start.x, self.levelScreen.level3.start.y, self.CYOLScreen.liquidDensity)
                    self.levelScreen.level3.timer = 0
                    self.runGame = False 
                    self.win = False
                elif self.levelScreen.level3.exitRect.collidepoint((x,y)):
                    self.gameObjectList = []
                    self.barrierList = []
                    self.bubbleColList = []
                    self.bubbleRowList = []
                    self.barrierGroup = pygame.sprite.Group()
                    self.runGame = False 
                    self.levelScreen.level3.timer = 0
                    self.levelScreen.level3.on = False
                    self.levelScreen.on = True
                    self.win = False

                # If you click on an already placed piece
                for obj in self.gameObjectList:
                    if obj.rect.collidepoint((x,y)):
                        obj.clickedOn = True
                for row in self.bubbleRowList:
                    if row.rect.collidepoint((x,y)):
                        row.clickedOn = True
                for col in self.bubbleColList:
                    if col.rect.collidepoint((x,y)):
                        col.clickedOn = True

    def mouseMoved(self, pos):
        x, y = pos[0], pos[1]
        for obj in self.gameObjectList:
            if obj.clickedOn:
                obj.x = x - obj.width//2
                if obj.x + obj.width - 20 > Game.width:
                    obj.x = Game.width - obj.width + 20
                elif obj.x < -5:
                    obj.x = -5
                obj.y = y - obj.height //2
                if obj.y + obj.height - 10 > Game.height:
                    obj.y = Game.height - obj.height + 10
                elif obj.y < 110:
                    obj.y = 110
                obj.updateRect() 
        for row in self.bubbleRowList:
            if row.clickedOn:
                row.x = x - row.width//2
                if row.x + row.width  > Game.width:
                    row.x = Game.width - row.width 
                elif row.x < -5:
                    row.x = -5
                row.y = y - row.height//2
                if row.y + row.height - 5 > Game.height:
                    row.y = Game.height - row.height - 5
                elif row.y < 130:
                    row.y = 130
                row.updateRect()
        for col in self.bubbleColList:
            if col.clickedOn:
                col.x = x - col.width//2
                if col.x + col.width + 10 > Game.width:
                    col.x = Game.width - col.width - 10
                elif col.x < -5:
                    col.x = -5
                col.y = y - col.height//2
                if col.y + col.height - 5 > Game.height:
                    col.y = Game.height - col.height - 5
                elif col.y < 125:
                    col.y = 125
                col.updateRect()
        for barrier in self.barrierList:
            if barrier.clickedOn:
                barrier.x = x - barrier.width//2
                barrier.y = y - barrier.height//2
                if barrier.orientation == "horizontal":
                    if barrier.x + barrier.width  > Game.width:
                        barrier.x = Game.width - barrier.width 
                    elif barrier.x < -5:
                        barrier.x = -5
                    if barrier.y + barrier.height - 60 > Game.height:
                        barrier.y = Game.height - barrier.height + 60
                    elif barrier.y + barrier.height < 225:
                        barrier.y = 225 - barrier.height
                else:
                    if barrier.x + barrier.width - 90> Game.width:
                        barrier.x = Game.width - barrier.width + 90
                    elif barrier.x < -60:
                        barrier.x = -60 
                    if barrier.y + barrier.height - 5 > Game.height:
                        barrier.y = Game.height - barrier.height - 5
                    elif barrier.y < 125:
                        barrier.y = 125
                barrier.updateRect()
        if self.character.clickedOn:
            self.character.x = x - self.character.width
            self.character.y = y - self.character.height//2
            if self.character.x + self.character.width  > Game.width:
                    self.character.x = Game.width - row.width 
            elif self.character.x < -50:
                self.character.x = -50
            if self.character.y + self.character.height - 5 > Game.height:
                self.character.y = Game.height - self.character.height - 5
            elif self.character.y < 100:
                self.character.y = 100
            self.character.updateRect()
        if self.CYOLScreen.on:
            # Deals with create your own level speed slider
            # (In terms of density so increasing the slider means the liquid is more dense so it slows down bubbles)
            if self.CYOLScreen.CYOLDensitySliderCircClickedOn:
                self.CYOLScreen.CYOLDensitySliderCircX = x
                if self.CYOLScreen.CYOLDensitySliderCircX < 690:
                    self.CYOLScreen.CYOLDensitySliderCircX = 690
                elif self.CYOLScreen.CYOLDensitySliderCircX > 840:
                    self.CYOLScreen.CYOLDensitySliderCircX = 840
                self.CYOLScreen.liquidDensity = self.CYOLScreen.CYOLDensitySliderCircX // 100 - 5
            if self.CYOLScreen.keyClickedOn:
                self.CYOLScreen.keyImageX = x - 25
                self.CYOLScreen.keyImageY = y - 25
            self.CYOLScreen.update() 

    # Deals with text for create your own level error messages
    def drawErroMessages(self, errorIndex):
        if errorIndex != -1:
            errors = [ "Click on a barrier to lock it!",
                        "Only one chest per level",
                        "Can only place 1 key",
                        "Must place barrier first"
                        ]
            message = errors[errorIndex]
            textColor = (255,255,255)
            font = pygame.font.SysFont('Impact MS', 40)
            messageSurface = font.render(message, False, textColor)
            self.screen.blit(messageSurface, (15, 130))

    # Draws all game objects
    def drawObject(self,screen):
        for obj in self.gameObjectList:
            screen.blit(obj.image, (obj.x, obj.y))

        for bubbleCol in self.bubbleColList:
            screen.blit(bubbleCol.image, (bubbleCol.x,bubbleCol.y))
        for bubbleRow in self.bubbleRowList:
            screen.blit(bubbleRow.image, (bubbleRow.x,bubbleRow.y))
        for bubbleCol in self.bubbleColList:
            for bubble in bubbleCol.bubbles:
                pygame.draw.ellipse(Game.screen, bubble.color, bubble.rect)
        for bubbleRow in self.bubbleRowList:
            for bubble in bubbleRow.bubbles:
                pygame.draw.ellipse(Game.screen, bubble.color, bubble.rect)
        
        for barrier in self.barrierList:
            screen.blit(barrier.image, (barrier.x, barrier.y))
        
        for row in self.vectorGrid:
            for vector in row:
                if vector.show:
                    pygame.draw.line(Game.screen, (0,0,0), vector.arrow()["start"], vector.arrow()["end"])
                    pygame.draw.line(Game.screen, (0,0,0), vector.arrow()["end"], vector.arrow()["tip1"])
                    pygame.draw.line(Game.screen, (0,0,0), vector.arrow()["end"], vector.arrow()["tip2"])

    def redrawAll(self, screen):
        if self.openingScreen.on:
            screen.blit(self.openingScreen.bg, (0,0))
            screen.blit(self.openingScreen.levelButton.surface, self.openingScreen.levelButton.rect)
            screen.blit(self.openingScreen.levelMakerButton.surface, self.openingScreen.levelMakerButton.rect)
            screen.blit(self.openingScreen.instructionsButton.surface, self.openingScreen.instructionsButton.rect)
            screen.blit(self.openingScreen.highScoresButton.surface, self.openingScreen.highScoresButton.rect)
        elif self.instructions.on:
            screen.blit(self.instructions.bg, (0,0))
            screen.blit(self.instructions.message, (200,-50))
        elif self.highScoreList.on:
            screen.blit(self.highScoreList.bg, (0,0))
            i1 = i2 = i3 = 0
            for surface in self.highScoreList.level1Surfaces:
                i1 += 10
                screen.blit(surface, (50,i1*5) )
            for surface in self.highScoreList.level2Surfaces:
                i2 += 10
                screen.blit(surface, (450,i2*5) )
            for surface in self.highScoreList.level3Surfaces:
                i3 += 10
                screen.blit(surface, (850,i3*5) )
        
        elif self.CYOLScreen.on:
            screen.blit(self.bg, (0,0))

            pygame.draw.ellipse(Game.screen, (250,250,250), self.CYOLScreen.CYOLDensitySliderCirc)

            screen.blit(self.CYOLScreen.keyImage, (self.CYOLScreen.keyImageX, self.CYOLScreen.keyImageY))
            screen.blit(self.character.image, (self.character.x, self.character.y))

            self.drawErroMessages(self.CYOLScreen.error)
            if self.win:
                screen.blit(self.CYOLScreen.winSurface, (550, 300))
                return

        elif self.levelScreen.on:
            screen.blit(self.levelScreen.bg, (0,0))
            
        elif self.levelScreen.level1.on:
            screen.blit(self.levelScreen.level1.bg, (0,0) )
            screen.blit(self.character.image, (self.character.x, self.character.y))
            
            self.levelScreen.level1.scoreSurface = self.levelScreen.level1.Font.render(str(self.levelScreen.level1.timer), False, self.levelScreen.level1.textColor)
            screen.blit(self.levelScreen.level1.scoreSurface, (560, 130))
        
        elif self.levelScreen.level2.on:
            screen.blit(self.levelScreen.level2.bg, (0,0) )
            screen.blit(self.character.image, (self.character.x, self.character.y))
            screen.blit(self.levelScreen.level2.keyImage, self.levelScreen.level2.keyRect)

            self.levelScreen.level2.scoreSurface = self.levelScreen.level2.Font.render(str(self.levelScreen.level2.timer), False, self.levelScreen.level2.textColor)
            screen.blit(self.levelScreen.level2.scoreSurface, (560, 130))
        
        elif self.levelScreen.level3.on:
            screen.blit(self.levelScreen.level2.bg, (0,0) )
            screen.blit(self.character.image, (self.character.x, self.character.y))

            self.levelScreen.level3.scoreSurface = self.levelScreen.level3.Font.render(str(self.levelScreen.level3.timer), False, self.levelScreen.level3.textColor)
            screen.blit(self.levelScreen.level3.scoreSurface, (560, 130))
            
        self.drawObject(screen)

        if self.win:
            screen.blit(self.levelScreen.winImage, (280, 150) )
        
    def run(self):
        clock = pygame.time.Clock()
        pygame.display.set_caption(self.title)
        running = True
        while running:
            time = clock.tick(self.fps)
            self.timerFired(time)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        running = False
                # Update vector field every time you click, so whenever a game object is moved
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.hold = True
                    for row in self.bubbleRowList:
                        row.updateVectorField(self.vectorGrid, True)
                    for col in self.bubbleColList:
                        col.updateVectorField(self.vectorGrid, True)
                    self.mousePressed(event.pos)
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.hold = False
                    for obj in self.gameObjectList:
                        obj.clickedOn = False
                    for row in self.bubbleRowList:
                        row.clickedOn = False
                        row.updateVectorField(self.vectorGrid, False)
                    for col in self.bubbleColList:
                        col.clickedOn = False
                        col.updateVectorField(self.vectorGrid, False)
                    for barrier in self.barrierList:
                        barrier.clickedOn = False
                    self.character.clickedOn = False
                    self.CYOLScreen.keyClickedOn = False
                elif event.type == pygame.MOUSEMOTION:
                    if self.hold:
                        self.mouseMoved(event.pos)
            self.screen.fill(self.bgColor)
            self.redrawAll(self.screen)
            pygame.display.flip()
        pygame.quit()
        
Game().run()
