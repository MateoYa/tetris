# Mateo's Tetris Test with open cv in python
from PIL import Image
import cv2
import numpy as np
from random import randint
from pynput import keyboard
import threading
from time import sleep

pixels = []
colors = [(0, 255, 255), (125, 0, 125), (0, 0, 255), (255, 127, 0), (255, 0, 0), (0, 255, 0), (255, 255, 0), (0, 0, 0)]
for y in range(20):
    pixels.append([0 for x in range(10)])


class Block():
    def __init__(self, x):
        self.blockType = x
        if self.blockType == 1:
            self.positions = [[1, 3], [1, 4], [1, 5], [1, 6]]
        if self.blockType == 2:
            self.positions = [[1, 4], [1, 3], [1, 5], [0, 4]]
        if self.blockType == 3:
            self.positions = [[1, 4], [1, 3], [0, 3], [1, 5]]
        if self.blockType == 4:
            self.positions = [[1, 4], [1, 5], [1, 3], [0, 5]]
        if self.blockType == 5:
            self.positions = [[1, 4], [0, 4], [0, 3], [1, 5]]
        if self.blockType == 6:
            self.positions = [[1, 4], [0, 4], [1, 3], [0, 5]]
        if self.blockType == 7:
            self.positions = [[1, 4], [0, 4], [1, 5], [0, 5]]
        for pos in self.positions:
            pixels[pos[0]][pos[1]] = self.blockType
        self.move()
        self.rotateState = 1

    def on_press(self, key):
        farX = 0
        closeX = 10
        for pos in self.positions:
            if pos[1] > farX:
                farX = pos[1]
            if pos[1] < closeX:
                closeX = pos[1]

        if key == keyboard.Key.up:
            self.rotate()
        if key == keyboard.Key.left:
            canMove = True
            # checks if it will run into anything
            for pos in self.positions:
                if pos[1] + 1 > 1:
                    if pixels[pos[0]][pos[1] - 1] != 0 and [pos[0], pos[1] - 1] not in self.positions:
                        canMove = False
                else:
                    canMove = False
            if canMove:
                for pos in self.positions:
                    pixels[pos[0]][pos[1]] = 0
                for i in range(4):
                    self.positions[i][1] -= 1
        if key == keyboard.Key.right:
            canMove = True
            # checks if it will run into anything
            for pos in self.positions:
                if pos[1] + 1 < 10:
                    if pixels[pos[0]][pos[1] + 1] != 0 and [pos[0], pos[1] + 1] not in self.positions:
                        canMove = False
                else:
                    canMove = False
            if canMove:
                for pos in self.positions:
                    pixels[pos[0]][pos[1]] = 0
                for i in range(4):
                    self.positions[i][1] += 1
        #Updates Board
        for pos in self.positions:
            pixels[pos[0]][pos[1]] = self.blockType

    def rotate(self):
        for postion in self.positions:
            pixels[postion[0]][postion[1]] = 0
        self.rotateState += 1
        # this Code Handles the turning states of the 4 tall block
        if self.blockType == 1:
            if self.rotateState == 1:
                allY = self.positions[1][0]
                self.positions = [[allY, self.positions[0][1] - 1], [allY, self.positions[1][1]],
                                  [allY, self.positions[2][1] + 1], [allY, self.positions[3][1] + 2]]
            if self.rotateState == 2:
                allX = self.positions[2][1]
                self.positions = [[self.positions[0][0], allX], [self.positions[1][0] + 1, allX],
                                  [self.positions[2][0] + 2, allX], [self.positions[3][0] + 3, allX]]
            if self.rotateState == 3:
                allY = self.positions[2][0]
                self.positions = [[allY, self.positions[0][1] + 1], [allY, self.positions[1][1]],
                                  [allY, self.positions[2][1] - 1], [allY, self.positions[3][1] - 2]]
            if self.rotateState == 4:
                allX = self.positions[2][1]
                self.positions = [[self.positions[0][0] + 1, allX], [self.positions[1][0] - 1, allX],
                                  [self.positions[2][0], allX], [self.positions[3][0] - 2, allX]]
                self.rotateState = 0
        # Tee Piece
        if self.blockType == 2:
            if self.rotateState == 1:
                allX = self.positions[0][1]
                allY = self.positions[0][0]
                self.positions = [[allY, allX], [allY, allX - 1], [allY, allX + 1], [allY - 1, allX]]
            if self.rotateState == 2:
                allX = self.positions[0][1]
                allY = self.positions[0][0]
                self.positions = [[allY, allX], [allY + 1, allX], [allY - 1, allX], [allY, allX + 1]]
            if self.rotateState == 3:
                allX = self.positions[0][1]
                allY = self.positions[0][0]
                self.positions = [[allY, allX], [allY, allX - 1], [allY, allX + 1], [allY + 1, allX]]
            if self.rotateState == 4:
                allX = self.positions[0][1]
                allY = self.positions[0][0]
                self.positions = [[allY, allX], [allY - 1, allX], [allY + 1, allX], [allY, allX - 1]]
                self.rotateState = 0
        # Backwards L
        if self.blockType == 3:
            if self.rotateState == 1:
                print("tf")
                allX = self.positions[0][1]
                allY = self.positions[0][0]
                self.positions = [[allY, allX], [allY, allX - 1], [allY - 1, allX - 1], [allY, allX + 1]]
            if self.rotateState == 2:
                allX = self.positions[0][1]
                allY = self.positions[0][0]
                self.positions = [[allY, allX], [allY - 1, allX], [allY - 1, allX + 1], [allY + 1, allX]]
            if self.rotateState == 3:
                allX = self.positions[0][1]
                allY = self.positions[0][0]
                self.positions = [[allY, allX], [allY, allX + 1], [allY + 1, allX + 1], [allY, allX - 1]]
            if self.rotateState == 4:
                allX = self.positions[0][1]
                allY = self.positions[0][0]
                self.positions = [[allY, allX], [allY + 1, allX], [allY + 1, allX - 1], [allY - 1, allX]]
                self.rotateState = 0
        # normal L
        if self.blockType == 4:
            if self.rotateState == 1:
                allX = self.positions[0][1]
                allY = self.positions[0][0]
                self.positions = [[allY, allX], [allY, allX + 1], [allY - 1, allX + 1], [allY, allX - 1]]
            if self.rotateState == 2:
                allX = self.positions[0][1]
                allY = self.positions[0][0]
                self.positions = [[allY, allX], [allY + 1, allX], [allY + 1, allX + 1], [allY - 1, allX]]
            if self.rotateState == 3:
                allX = self.positions[0][1]
                allY = self.positions[0][0]
                self.positions = [[allY, allX], [allY + 1, allX - 1], [allY, allX - 1], [allY, allX + 1]]
            if self.rotateState == 4:
                allX = self.positions[0][1]
                allY = self.positions[0][0]
                self.positions = [[allY, allX], [allY - 1, allX], [allY - 1, allX - 1], [allY + 1, allX]]
                self.rotateState = 0
        # Z peice
        if self.blockType == 5:
            if self.rotateState == 1:
                allX = self.positions[0][1]
                allY = self.positions[0][0]
                self.positions = [[allY, allX], [allY - 1, allX], [allY - 1, allX - 1], [allY, allX + 1]]
            if self.rotateState == 2:
                allX = self.positions[0][1]
                allY = self.positions[0][0]
                self.positions = [[allY, allX], [allY, allX + 1], [allY - 1, allX + 1], [allY + 1, allX]]
            if self.rotateState == 3:
                allX = self.positions[0][1]
                allY = self.positions[0][0]
                self.positions = [[allY, allX], [allY, allX - 1], [allY + 1, allX], [allY + 1, allX + 1]]
            if self.rotateState == 4:
                allX = self.positions[0][1]
                allY = self.positions[0][0]
                self.positions = [[allY, allX], [allY - 1, allX], [allY, allX - 1], [allY + 1, allX - 1]]
                self.rotateState = 0
        # S piece
        if self.blockType == 6:
            if self.rotateState == 1:
                allX = self.positions[0][1]
                allY = self.positions[0][0]
                self.positions = [[allY, allX], [allY - 1, allX], [allY - 1, allX + 1], [allY, allX - 1]]
            if self.rotateState == 2:
                allX = self.positions[0][1]
                allY = self.positions[0][0]
                self.positions = [[allY, allX], [allY - 1, allX], [allY, allX + 1], [allY + 1, allX + 1]]
            if self.rotateState == 3:
                allX = self.positions[0][1]
                allY = self.positions[0][0]
                self.positions = [[allY, allX], [allY + 1, allX], [allY, allX + 1], [allY + 1, allX - 1]]
            if self.rotateState == 4:
                allX = self.positions[0][1]
                allY = self.positions[0][0]
                self.positions = [[allY, allX], [allY, allX - 1], [allY - 1, allX - 1], [allY + 1, allX]]
                self.rotateState = 0
        for postion in self.positions:
            pixels[postion[0]][postion[1]] = self.blockType
    def Update(self):
        canMove = True
        # checks if it will run into anything
        for pos in self.positions:
            if pos[0] + 1 < 20:
                if pixels[pos[0] + 1][pos[1]] != 0 and [pos[0] + 1, pos[1]] not in self.positions:
                    canMove = False
            else:
                canMove = False
        if canMove:
            for pos in self.positions:
                pixels[pos[0]][pos[1]] = 0
            for i in range(4):
                self.positions[i][0] += 1
        #Updates Board
        for pos in self.positions:
            pixels[pos[0]][pos[1]] = self.blockType
        if canMove == False:
            self.listener.stop()
            self.ClearRows()
            return "new"
        if canMove:
            return "keep"

    def ClearRows(self):
        self.row = -1
        for pixelRow in pixels:
            rowClear = 0
            self.row += 1
            for pixel in pixelRow:
                if pixel != 0:
                    rowClear += 1
                if rowClear == 10:
                    del pixels[self.row]
                    pixels.insert(0, [0 for x in range(10)])

    def move(self):
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()


SIZE = (20, 10, 3)
newBlock = Block(randint(1, 7))
for pixel in pixels:
    print(pixel)
while True:
    env = np.zeros(SIZE, dtype=np.uint8)
    row = 0
    column = 0
    for pixel_row in pixels:
        column += 1
        row = 0
        for pixel in pixel_row:
            row += 1
            env[column - 1][row - 1] = colors[pixel - 1]
    img = Image.fromarray(env, "RGB")
    img = img.resize((300, 600), resample=Image.NEAREST)
    img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
    a = newBlock.Update()
    if a == "new":
        newBlock = Block(randint(1, 7))
    cv2.imshow("", img)
    cv2.waitKey(1000)
