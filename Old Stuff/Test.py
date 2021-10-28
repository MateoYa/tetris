pixels = []

for y in range(20):
    pixels.append([0 for x in range(10)])
pixels[19][0] = 1
pixels[19][1] = 1
pixels[19][2] = 1
pixels[19][3] = 1
pixels[19][4] = 1
pixels[19][5] = 1
pixels[19][6] = 1
pixels[19][7] = 1
pixels[19][8] = 1
pixels[19][9] = 1
for pixel in pixels:
    print(pixel)
row = -1
for pixelRow in pixels:
    rowClear = 0
    row += 1
    for pixel in pixelRow:
        if pixel != 0:
            rowClear += 1
        if rowClear == 10:
            del pixels[row]
            print(row)
            print("ok")
for pixel in pixels:
    print(pixel)