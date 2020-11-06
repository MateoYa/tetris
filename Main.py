from PIL import Image
import cv2
import numpy as np
from random import randint
pixels = []
colors = [(0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 0, 255)]
for y in range(10):
    pixels.append([randint(0, len(colors)) for x in range(10)])
for pixel in pixels:
    print(pixel)

pixels[0][0] = 5
SIZE = 10

while True:
    env = np.zeros((SIZE, SIZE, 3), dtype=np.uint8)
    row = 0
    column = 0
    for pixel_row in pixels:
        column += 1
        row = 0
        for pixel in pixel_row:
            row += 1
            env[column-1][row-1] = colors[pixel-1]
    img = Image.fromarray(env, "RGB")
    img = img.resize((300, 300), resample=Image.NEAREST)
    img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
    cv2.imshow("", img)
    cv2.waitKey(0)
