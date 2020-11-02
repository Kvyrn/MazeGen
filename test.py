from matplotlib import image, pyplot
from PIL.PngImagePlugin import PngImageFile

img: PngImageFile = image.imread('test.png')
# pyplot.imshow(img)
# pyplot.show()

# print(img[0, 0])

for x in range(len(img)):
    for y in range(len(img[0])):
        print(round(img[x, y, 3]), "", end="")
    print()
