import numpy as np
import pygame as pg
import os
import sys


class BinaryImage:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pixels = np.zeros((width, height))
    
    def draw(self, x, y):
        self.pixels[x, y] = 1

    def clear(self):
        self.pixels = np.zeros((self.width, self.height))

    def data(self):
        res = []
        for i in self.pixels:
            for j in i:
                res.append(int(j))
        return np.array(res)

class Inputs:
    def __init__(self, imagewidth, imageheight, coef = 10, font = "arial.ttf", fontsize = 50):
        self.width = imagewidth * coef
        self.height = imageheight * coef
        self.coef = coef
        self.font = pg.font.SysFont(font, fontsize)
        self.screen = pg.display.set_mode((self.width, self.height))

    def pos2index(self, pos):
        return (pos[1]//self.coef, pos[0]//self.coef)

    def draw(self, image):
        self.screen.fill((255, 255, 255))
        for i in range(self.width//self.coef):
            for j in range(self.height//self.coef):
                if image.pixels[j, i]:
                    pg.draw.rect(self.screen, (0, 0, 0), (i*self.coef, j*self.coef, self.coef, self.coef))
        pg.display.update()

    def validpos(self, event):
        try:
            return event.pos[0] < self.width and event.pos[1] < self.height
        except:
            return False

    def input(self):
        self.screen.fill((255, 255, 255))
        image = BinaryImage(self.width//self.coef, self.height//self.coef)
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
                        return image.data()
                    elif event.key == pg.K_BACKSPACE or event.key == pg.K_DELETE or event.key == pg.K_z or event.key == pg.K_LCTRL:
                        image.clear()
                self.draw(image)
    
    def output(self, prediction):
        self.screen.fill((255, 255, 255))
        text = self.font.render(str(prediction), True, (0, 0, 0))
        self.screen.blit(text, (self.width//2 - text.get_width()//2, self.height//2 - text.get_height()//2))
        pg.display.update()
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    pg.quit()
                    sys.exit()
                if (event.type == pg.KEYDOWN and (event.key == pg.K_RETURN or event.key == pg.K_SPACE)) or event.type == pg.MOUSEBUTTONDOWN:
                    return None


def predict(pixels, weights, bias):
    return np.dot(weights, pixels) + bias

def main():

    cont = True
    while cont:
        try:
            weights = np.loadtxt(input("Weights file name: "))
            with open(input("Bias file name: "), "r") as f:
                bias = float(f.read())
                f.close()
            cont = False
        except FileNotFoundError:
            print("File not found, try again")

    pg.init()
    pg.display.set_caption("Number Reader")
    inputs = Inputs(16, 16, 40)

    while True:
        pixels = inputs.input()
        inputs.output(int(round(predict(pixels, weights, bias))))

if __name__ == "__main__":
    main()



