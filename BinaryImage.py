import numpy as np
import random
import pygame as pg
import sys
import os

class BinaryImage:
    def __init__(self, width, height, label, traindata = "traindata.txt", testdata = "testdata.txt"):
        self.width = width
        self.height = height
        self.traindata = traindata
        self.testdata = testdata
        self.pixels = np.zeros((width, height))
        self.label = label
    
    def draw(self, x, y):
        self.pixels[x, y] = 1

    def clear(self):
        self.pixels = np.zeros((self.width, self.height))

    def data(self):
        res = ""
        for i in self.pixels:
            for j in i:
                res += str(int(j))
        return res + str(self.label)

    def save(self, datatype):
        if datatype:
            file = open(self.testdata, "a")
        else:
            file = open(self.traindata, "a")
        file.write(self.data())
        file.write(os.linesep)
        file.close()

class Inputs:
    def __init__(self, imagewidth, imageheight, datacount = 20, coef = 10, traindata = "traindata.txt", testdata = "testdata.txt", font = "arial.ttf", fontsize = 50):
        self.width = imagewidth * coef
        self.height = imageheight * coef + 50
        self.coef = coef
        self.font = pg.font.SysFont(font, fontsize)
        self.screen = pg.display.set_mode((self.width, self.height))
        self.datacount = datacount
        self.addeddata = 0
        self.datalist = []
        self.traindata = traindata
        self.testdata = testdata
    
    def create_datalist(self):
        for i in range(self.datacount):
            if i < 10:
                self.datalist.append(i)
            else:
                self.datalist.append(random.randint(0, 9))

    def pos2index(self, pos):
        return ((pos[1] - 50)//self.coef, pos[0]//self.coef)

    def draw(self, image, label):
        self.screen.fill((255, 255, 255))
        for i in range(self.width//self.coef):
            for j in range((self.height - 50)//self.coef):
                if image.pixels[j, i]:
                    pg.draw.rect(self.screen, (0, 0, 0), (i*self.coef, j*self.coef + 50, self.coef, self.coef))
        self.screen.blit(self.font.render(str(label) + "   " + str(self.addeddata) + "/" + str(self.datacount), True, (0, 0, 0)), pg.Rect(0, 0, self.width, 50))
        pg.display.update()

    def validpos(self, event):
        try:
            return event.pos[0] < self.width and event.pos[1] < self.height and event.pos[1] > 50
        except:
            return False

    def input(self, label, datatype):
        self.screen.fill((255, 255, 255))
        image = BinaryImage(self.width//self.coef, (self.height - 50)//self.coef, label, self.traindata, self.testdata)
        cont = True
        while cont:
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    pg.quit()
                    sys.exit()
                elif event.type == pg.MOUSEBUTTONDOWN or (pg.mouse.get_pressed()[0] and self.validpos(event)):
                    image.draw(self.pos2index(event.pos)[0], self.pos2index(event.pos)[1])
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN or event.key == pg.K_SPACE:
                        image.save(datatype)
                        image.clear()
                        cont = False
                    elif event.key == pg.K_BACKSPACE or event.key == pg.K_DELETE or event.key == pg.K_z or event.key == pg.K_LCTRL:
                        image.clear()
                self.draw(image, label)

    def run(self):
        self.create_datalist()
        for i in self.datalist:
            self.input(i, 0)
            self.addeddata += 1
        self.addeddata = 0
        for i in self.datalist:
            self.input(i, 1)
            self.addeddata += 1

def main():
    datacount = input("How many images of data do you want to create? (for both training and testing, so you will draw twice this amount, default is 20): ")
    try:
        datacount = int(datacount)
    except:
        datacount = 20
    pg.init()
    pg.font.init()
    inputs = Inputs(16, 16, datacount, 30)
    inputs.run()

if __name__ == "__main__":
    main()

