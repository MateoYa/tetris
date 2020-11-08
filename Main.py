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
        self.x = 5
        self.y = 1
        #self.positions = [[1, 5], [2, 5], [3, 5], [4, 5]]
        self.blockType = randint(0, 4)
        #for pos in self.positions:
        pixels[self.y][self.x] = 3
        self.canMove = True

    def __str__(self):
        return f"{self.x} {self.y}"

    def update(self):
        y, x, z = SIZE
        if self.y == y - 1:
            pixels[self.y][self.x] = 3
            self.canMove = False
            return "new"
        elif pixels[self.y + 1][self.x] == 0:
            pixels[self.y][self.x] = 0
            self.y += 1
            pixels[self.y][self.x] = 3
            self.canMove = True
            self.move()
            return "keep"
        else:
            self.canMove = False
            pixels[self.y][self.x] = 3
            return "new"

    def on_press(self, key):
        if key == keyboard.Key.left and self.canMove == True:
            pixels[self.y][self.x] = 0
            self.x -= 1
            pixels[self.y][self.x] = 3
            self.canMove = False

        if key == keyboard.Key.right and self.canMove == True:
            pixels[self.y][self.x] = 0
            self.x += 1
            pixels[self.y][self.x] = 3
            self.canMove = False

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
            for block_ in Blocks:
                print(block_)

    cv2.imshow("", img)
    cv2.waitKey(100)
