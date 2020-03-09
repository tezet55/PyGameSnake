import pygame as pg
import random


class GameManager:

    boardSize = (22, 20)
    blockSize = 20
    margin = 50
    width = boardSize[0] * blockSize
    height = boardSize[1] * blockSize + margin
    size = (width, height)
    done = False
    buttonWidth = 200
    buttonHeight = 100
    buttonPos = (width // 2 - 100, height // 2)
    exit = False

    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    black = (0, 0, 0)
    white = (255, 255, 255)
    purple = (128, 0, 128)

    snakeSpeed = 5
    fpsClock = pg.time.Clock()

    def initValues(self):
        bugPos = []
        bugAmount = 0
        tick = 0
        bugTime = []

        red = (255, 0, 0)
        green = (0, 255, 0)
        blue = (0, 0, 255)
        black = (0, 0, 0)
        white = (255, 255, 255)
        purple = (128, 0, 128)

    headLeft = pg.transform.scale(pg.image.load('data//snakeHeadLeft.png'), (blockSize, blockSize))
    headRight = pg.transform.scale(pg.image.load('data//snakeHeadRight.png'), (blockSize, blockSize))
    headUp = pg.transform.scale(pg.image.load('data//snakeHeadUp.png'), (blockSize, blockSize))
    headDown = pg.transform.scale(pg.image.load('data//snakeHeadDown.png'), (blockSize, blockSize))

    tailLeft = pg.transform.scale(pg.image.load('data//snakeTailLeft.png'), (blockSize, blockSize))
    tailRight = pg.transform.scale(pg.image.load('data//snakeTailRight.png'), (blockSize, blockSize))
    tailUp = pg.transform.scale(pg.image.load('data//snakeTailUp.png'), (blockSize, blockSize))
    tailDown = pg.transform.scale(pg.image.load('data//snakeTailDown.png'), (blockSize, blockSize))

    bodyVertical = pg.transform.scale(pg.image.load('data//snakeVertical.png'), (blockSize, blockSize))
    bodyHorizontal = pg.transform.scale(pg.image.load('data//snakeHorizontal.png'), (blockSize, blockSize))
    bodyDownLeft = pg.transform.scale(pg.image.load('data//snakeTurnDownLeft.png'), (blockSize, blockSize))
    bodyDownRight = pg.transform.scale(pg.image.load('data//snakeTurnDownRight.png'), (blockSize, blockSize))
    bodyUpRight = pg.transform.scale(pg.image.load('data//snakeTurnUpRight.png'), (blockSize, blockSize))
    bodyUpLeft = pg.transform.scale(pg.image.load('data//snakeTurnUpLeft.png'), (blockSize, blockSize))
    appleImg = pg.transform.scale(pg.image.load('data//apple.png'), (blockSize, blockSize))

    icon = pg.transform.scale(appleImg, (32, 32))

    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(self.size)
        pg.display.set_icon(self.icon)
        pg.display.set_caption("SnakeX")
        self.menu()

    def gameInit(self):
        self.snakePos = [(0, 0), (1, 0)]
        self.snakeCurve = ["right"]
        self.newPos = False
        self.key = 0
        self.previousDirection = "right"
        self.direction = "right"
        self.applePos = []
        self.appleAmount = 1
        self.board = []
        self.blockPos = []
        self.blockAmount = 2
        self.bugPos = []
        self.bugAmount = 0
        self.tick = 0
        self.bugTime = []
        self.tunelPos = []

    def printSquare(self, pos, color):
        pg.draw.rect(self.screen, color, pg.Rect(pos[0]*self.blockSize, pos[1]*self.blockSize + self.margin, self.blockSize, self.blockSize))

    def printSnakeTail(self):
        self.printSquare(self.snakePos[0], self.green)
        pos = (self.snakePos[0][0] * self.blockSize, self.snakePos[0][1] * self.blockSize + self.margin)
        if self.snakeCurve[0] == "right":
            self.screen.blit(self.tailRight, pos)
        elif self.snakeCurve[0] == "left":
            self.screen.blit(self.tailLeft, pos)
        elif self.snakeCurve[0] == "up":
            self.screen.blit(self.tailUp, pos)
        else:
            self.screen.blit(self.tailDown, pos)

    def printSnakeBlock(self):
        self.printSquare(self.snakePos[-2], self.green)
        pos = (self.snakePos[-2][0] * self.blockSize, self.snakePos[-2][1] * self.blockSize + self.margin)
        if self.snakeCurve[-1] == "right" and self.snakeCurve[-2] == "right" or self.snakeCurve[-1] == "left" and self.snakeCurve[-2] == "left":
            self.screen.blit(self.bodyHorizontal, pos)
        elif self.snakeCurve[-1] == "up" and self.snakeCurve[-2] == "up" or self.snakeCurve[-1] == "down" and self.snakeCurve[-2] == "down":
            self.screen.blit(self.bodyVertical, pos)
        elif self.snakeCurve[-1] == "down" and self.snakeCurve[-2] == "right" or self.snakeCurve[-1] == "left" and self.snakeCurve[-2] == "up":
            self.screen.blit(self.bodyDownLeft, pos)
        elif self.snakeCurve[-1] == "down" and self.snakeCurve[-2] == "left" or self.snakeCurve[-1] == "right" and self.snakeCurve[-2] == "up":
            self.screen.blit(self.bodyDownRight, pos)
        elif self.snakeCurve[-1] == "left" and self.snakeCurve[-2] == "down" or self.snakeCurve[-1] == "up" and self.snakeCurve[-2] == "right":
            self.screen.blit(self.bodyUpLeft, pos)
        elif self.snakeCurve[-1] == "right" and self.snakeCurve[-2] == "down" or self.snakeCurve[-1] == "up" and self.snakeCurve[-2] == "left":
            self.screen.blit(self.bodyUpRight, pos)

    def printSnakeHead(self):
        self.printSquare(self.snakePos[-1], self.green)
        pos = (self.snakePos[-1][0]*self.blockSize, self.snakePos[-1][1]*self.blockSize + self.margin)
        if self.snakeCurve[-1] == "right":
            self.screen.blit(self.headRight, pos)
        elif self.snakeCurve[-1] == "left":
            self.screen.blit(self.headLeft, pos)
        elif self.snakeCurve[-1] == "up":
            self.screen.blit(self.headUp, pos)
        else:
            self.screen.blit(self.headDown, pos)

    def printSnake(self):
        self.printSnakeTail()
        for pos in self.snakePos[1:-1]:
            self.printSnakeBlock()
        self.printSnakeHead()

    def makeApple(self):
        freeSpace = list(set(self.board) - set(self.snakePos) - set(self.applePos) - set(self.blockPos) - set(self.bugPos) - set(self.tunelPos))
        self.applePos.append(freeSpace[random.randint(0, len(freeSpace) - 1)])
        for apple in self.applePos:
            pos = (apple[0] * self.blockSize, apple[1] * self.blockSize + self.margin)
            self.screen.blit(self.appleImg, pos)

    def makeBug(self):
        if not self.tick / self.snakeSpeed % 15:
            freeSpace = list(set(self.board) - set(self.snakePos) - set(self.applePos) - set(self.blockPos) - set(self.tunelPos))
            self.bugPos.append(freeSpace[random.randint(0, len(freeSpace) - 1)])
            self.bugTime.append(self.tick)
            for bug in self.bugPos:
                self.printSquare(bug, self.purple)

    def deleteBug(self):
        for time in self.bugTime:
            if (self.tick - time)/5 == 5:
                self.printSquare(self.bugPos[self.bugTime.index(time)], self.green)
                self.bugPos.pop(self.bugTime.index(time))
                self.bugTime.remove(time)

    def makeBlock(self):
        freeSpace = list(set(self.board) - set(self.snakePos) - set(self.blockPos))
        self.blockPos.append(freeSpace[random.randint(0, len(freeSpace) - 1)])
        for block in self.blockPos:
            self.printSquare(block, self.black)

    def printMargin(self):
        pg.draw.rect(self.screen, self.black, pg.Rect(0, 0, self.width, self.margin))

    def pause(self):
        key = self.key
        done = False
        while not done:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.exit = True
                    return
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        done = True
                        self.key = key
                        break

    def control(self, key):
        if key == pg.K_UP and self.previousDirection != "down":
            self.direction = "up"
        elif key == pg.K_DOWN and self.previousDirection != "up":
            self.direction = "down"
        elif key == pg.K_LEFT and self.previousDirection != "right":
            self.direction = "left"
        elif key == pg.K_RIGHT and self.previousDirection != "left":
            self.direction = "right"

        if self.direction == "up":
            self.newPos = self.snakePos[-1][0], (self.snakePos[-1][1] - 1) % self.boardSize[1]
        elif self.direction == "down":
            self.newPos = self.snakePos[-1][0], (self.snakePos[-1][1] + 1) % self.boardSize[1]
        elif self.direction == "left":
            self.newPos = (self.snakePos[-1][0] - 1) % self.boardSize[0], self.snakePos[-1][1]
        elif self.direction == "right":
            self.newPos = (self.snakePos[-1][0] + 1) % self.boardSize[0], self.snakePos[-1][1]

    def moveSnake(self):
        if self.newPos:
            if self.newPos in self.snakePos[1:] or self.newPos in self.blockPos:
                self.done = True
            else:
                self.snakePos.append(self.newPos)
                self.previousDirection = self.direction
                self.snakeCurve.append(self.direction)
                if self.newPos in self.applePos:
                    self.applePos.remove(self.newPos)
                    self.makeApple()
                elif self.newPos in self.bugPos:
                    self.bugTime.pop(self.bugPos.index(self.newPos))
                    self.bugPos.remove(self.newPos)
                else:
                    self.printSquare(self.snakePos.pop(0), self.green)
                    self.snakeCurve.pop(0)
                self.printSnake()

    def gameOver(self):
        font = pg.font.Font('freesansbold.ttf', 52)
        text = font.render('GAME OVER', True, self.white)
        textRect = text.get_rect()
        textRect.center = (self.width // 2, self.height // 2)
        self.screen.blit(text, textRect)
        pg.display.update()
        self.done = False
        while not self.done:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.exit = True
                    return
                if event.type == pg.KEYDOWN:
                    self.done = True
                    break

    def run(self):
        self.gameInit()
        for i in range(self.boardSize[0]):
            for j in range(self.boardSize[1]):
                self.board.append((i, j))
        self.screen.fill(self.green)
        self.printMargin()
        self.printSnake()
        for i in range(self.blockAmount):
            self.makeBlock()
        for i in range(self.appleAmount):
            self.makeApple()
        pg.display.update()
        self.done = False
        while not self.done:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.exit = True
                    return
                if event.type == pg.KEYDOWN:
                    self.done = True
        self.done = False
        while not self.done:
            self.fpsClock.tick(self.snakeSpeed)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.exit = True
                    return
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        self.pause()
                        self.fpsClock.tick(self.snakeSpeed)
                    else:
                        self.key = event.key
                    break
            if self.done:
                break
            self.control(self.key)
            self.moveSnake()
            self.printSnakeTail()
            self.tick += 1
            self.makeBug()
            self.deleteBug()
            pg.display.update()
        self.gameOver()


    def printMenu(self):
        self.screen.fill(self.black)
        font = pg.font.Font('freesansbold.ttf', 52)
        text = font.render('SnakeX', True, self.white, self.black)
        textRect = text.get_rect()
        textRect.center = (self.width // 2, self.height // 2 - 100)
        self.screen.blit(text, textRect)

    def menu(self):
        self.printMenu()
        fontPlay = pg.font.Font('freesansbold.ttf', 30)
        textPlay = fontPlay.render('Play', True, self.black)
        playRect = textPlay.get_rect()
        playRect.center = (self.width // 2, self.height // 2 + 50)
        pg.display.update()

        pick = 0
        done = False
        while not done:
            pick = 0
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
                    break
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        pick = "run"
                        break
                mouse = pg.mouse.get_pos()
                if self.buttonPos[0] < mouse[0] < self.buttonPos[0] + self.buttonWidth and self.buttonPos[1] < mouse[1] < self.buttonPos[1] + self.buttonHeight:
                    pg.draw.rect(self.screen, (0, 200, 0), pg.Rect(self.buttonPos[0], self.buttonPos[1], self.buttonWidth, self.buttonHeight))
                    self.screen.blit(textPlay, playRect)
                    if pg.mouse.get_pressed()[0]:
                        pick = "run"
                        break
                else:
                    pg.draw.rect(self.screen, self.green, pg.Rect(self.buttonPos[0], self.buttonPos[1], self.buttonWidth, self.buttonHeight))
                    self.screen.blit(textPlay, playRect)
            pg.display.update()

            if pick == "run":
                self.run()
                self.printMenu()
                if self.exit:
                    done = True
