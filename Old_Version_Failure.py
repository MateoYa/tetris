from PIL import Image
import cv2
import numpy as np
from random import randint
from pynput import keyboard
import threading
from time import sleep

pixels = []
colors = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 0, 255), (0, 0, 0)]
for y in range(20):
    pixels.append([0 for x in range(10)])


def wait(seconds):
    sleep(seconds)
    return True


class Block:
    def __init__(self):
        self.x = []
        self.y = 1
        self.row = 0
        self.positions = [[1, 5], [2, 5], [3, 5], [4, 5]]
        self.blockType = randint(0, 4)
        self.maxY = 0
        self.isBlockDown = False
        for pos in self.positions:
            pixels[pos[0]][pos[1]] = 3
        self.canMove = True
        self.move()
        self.rotationPos = 0

    def __str__(self):
        return f"{self.x} {self.y}"

    def update(self):
        print("hi")
        y, x, z = SIZE
        for pos in self.positions:
            if pos[0] >= self.maxY:
                self.maxY = pos[0]
        if self.maxY == y - 1:
            for pos in self.positions:
                pixels[pos[0]][pos[1]] = 3
            self.canMove = False
            return self.placed()
        for pos in self.positions:
            if pixels[self.maxY + 1][pos[1]] != 0:
                self.isBlockDown = True
        if self.isBlockDown:
            self.canMove = False
            for pos in self.positions:
                pixels[pos[0]][pos[1]] = 3
            return self.placed()
        else:
            if self.canMove:
                self.canMove = True
                for pos in self.positions:
                    pixels[pos[0]][pos[1]] = 0
                for pos in self.positions:
                    pos[0] += 1
                for pos in self.positions:
                    pixels[pos[0]][pos[1]] = 3
                return "keep"
            if not self.canMove:
                self.canMove = True
                return "keep"

    def placed(self):
        # Row Clear
        y, x, z = SIZE
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
        return "new"

    def on_press(self, key):
        for pos in self.positions:
            if pos[0] >= self.maxY:
                self.maxY = pos[0]
        if key == keyboard.Key.up:
            self.rotate()

        if key == keyboard.Key.left and self.canMove == True:
            self.canMove = True
            for pos in self.positions:
                if pixels[pos[0]][pos[1] - 1] != 0:
                    self.canMove = False
            if self.canMove:
                for pos in self.positions:
                    pixels[pos[0]][pos[1]] = 0
                for pos in self.positions:
                    pos[1] -= 1
                    if pos[0] >= self.maxY:
                        for pos_ in self.positions:
                            pos_[0] -= 1
                for pos in self.positions:
                    pixels[pos[0]][pos[1]] = 3
                self.canMove = False

        if key == keyboard.Key.right and self.canMove == True:
            self.canMove = True
            for pos in self.positions:
                if pixels[pos[0]][pos[1] + 1] != 0:
                    self.canMove = False
            if self.canMove:
                for pos in self.positions:
                    pixels[pos[0]][pos[1]] = 0
                for pos in self.positions:
                    pos[1] += 1
                    if pos[0] >= self.maxY:
                        for pos_ in self.positions:
                            pos_[0] -= 1
                for pos in self.positions:
                    pixels[pos[0]][pos[1]] = 3
                self.canMove = False

    def rotate(self):
        if self.rotationPos == 2:
            self.rotationPos += 1
            increaseAmount = 1
            for pos in self.positions:
                pixels[pos[0]][pos[1]] = 0
            for pos in self.positions:
                pos[0] = self.positions[2][0]
                pos[1] -= increaseAmount
                increaseAmount += 1
            for pos in self.positions:
                pos[1] += 2
            for pos in self.positions:
                pixels[pos[0]][pos[1]] = 3

        if self.rotationPos == 1:
            self.rotationPos += 1
            increaseAmount = 1
            for pos in self.positions:
                pixels[pos[0]][pos[1]] = 0
            for pos in self.positions:
                pos[1] = self.positions[2][1]
                pos[0] -= increaseAmount
                increaseAmount -= 1
            for pos in self.positions:
                pixels[pos[0]][pos[1]] = 3

        if self.rotationPos == 0:
            self.rotationPos += 1
            increaseAmount = 1
            for pos in self.positions:
                pixels[pos[0]][pos[1]] = 0
            for pos in self.positions:
                pos[0] = self.positions[2][0]
                pos[1] += increaseAmount
                increaseAmount += 1
            for pos in self.positions:
                pos[1] -= 2
            for pos in self.positions:
                pixels[pos[0]][pos[1]] = 3
        if self.rotationPos == 3:
            self.rotationPos = 0
            increaseAmount = 1
            for pos in self.positions:
                pixels[pos[0]][pos[1]] = 0
            for pos in self.positions:
                pos[1] = self.positions[2][1]
                pos[0] -= increaseAmount+2
                increaseAmount -= 1
            for pos in self.positions:
                pixels[pos[0]][pos[1]] = 3

    def move(self):
        listener = keyboard.Listener(on_press=self.on_press)
        listener.start()


SIZE = (20, 10, 3)
Blocks = []
a = Block()
Blocks.append(a)
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
    for block in Blocks:
        a = block.update()
        if a == "new":
            Blocks.remove(block)
            a = Block()
            Blocks.append(a)
    cv2.imshow("", img)
    cv2.waitKey(1000)
