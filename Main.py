from PIL import Image
import cv2
import numpy as np
from random import randint

pixels = []
colors = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 0, 255), (0, 0, 0)]
for y in range(20):
    pixels.append([0 for x in range(10)])


class Block:
    def __init__(self):
        self.x = 5
        self.y = 1
        self.blockType = randint(0, 4)
        pixels[self.y][self.x] = 3

    def __str__(self):
        return f"{self.x} {self.y}"

    def update(self):
        if pixels[self.y-1][self.x] != 0:
            pixels[self.y - 1][self.x] = 3
            return "new"
        try:
            pixels[self.y][self.x] = 0
            self.y += 1
            pixels[self.y][self.x] = 3
            return "keep"
        except:
            pixels[self.y - 1][self.x] = 3
            return "new"


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
            a = Block()
            Blocks.remove(block)
            Blocks.append(a)

    cv2.imshow("", img)
    cv2.waitKey(500)
