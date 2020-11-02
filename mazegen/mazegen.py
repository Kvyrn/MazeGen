from random import choice
from PIL import Image
from PIL.PngImagePlugin import PngImageFile
from matplotlib import pyplot
from time import sleep

white = (255, 255, 255, 255)
blue = (0, 0, 255, 255)
red = (255, 0, 0, 255)
green = (0, 255, 0, 255)
black = (0, 0, 0, 255)


class MazeGen:
    x_size = 0
    y_size = 0
    filename = "maze.png"
    img = None
    img_raw: PngImageFile = None
    
    # current position on image
    pointer = (0, 0)
    # heading direction
    direction = 0
    # is currently backtracking
    backtracking = False
    finished = False
    
    def __init__(self, x_size: int, y_size: int, filename: str):
        self.img_raw = Image.new("RGBA", (x_size, y_size), color="black")
        self.img = self.img_raw.load()
        self.filename = filename
        self.x_size, self.y_size = self.img_raw.size
    
    def generate(self):
        f = open("out.txt", "w+")
        a = 0
        self.img[0, 0] = red
        
        # pyplot.ion()
        # pyplot.show()
        while not self.finished:
            # pyplot.imshow(self.img_raw)
            # pyplot.pause(0.001)
            self.img_raw.save(f"animation/frame{a}.png")
            print(f"round {a}")
            self.step()
            a += 1
            # sleep(.1)
        
        f.close()
        self.img_raw.save(self.filename)
        input()
        return self.img_raw
    
    def is_pointer_in_range(self, point):
        if point[0] > self.x_size - 1 or point[0] < 0:
            print("pointer out of range, axis=x")
            return False
        elif point[1] > self.y_size - 1 or point[1] < 0:
            print("pointer out of range, axis=y")
            return False
        else:
            return True
    
    def set_direction(self):
        # directions: 0 = right, 1 = down, 2 = left, 3 = up
        choices = []
        if self.is_walkable_direction(0):
            choices.append(0)
        
        if self.is_walkable_direction(1):
            choices.append(1)
        
        if self.is_walkable_direction(2):
            choices.append(2)
        
        if self.is_walkable_direction(3):
            choices.append(3)
        
        if len(choices) > 0:
            self.direction = choice(choices)
            return True
        else:
            self.backtracking = True
            return False
    
    def is_walkable_direction(self, direction):
        print(self.get_pixel_woffset(direction, 1), self.get_pixel_woffset(direction, 2))
        return (self.is_pointer_in_range(self.get_pixel_woffset(direction, 1))) and \
               (self.is_pointer_in_range(self.get_pixel_woffset(direction, 2))) and \
               (self.img[self.get_pixel_woffset(direction, 1)] == black) and \
               (self.img[self.get_pixel_woffset(direction, 2)] == black)
    
    def get_pixel_woffset(self, direction: int, amount: int):
        # directions: 0 = right, 1 = down, 2 = left, 3 = up
        if direction == 0:
            return self.pointer[0] + amount, self.pointer[1]
        elif direction == 1:
            return self.pointer[0], self.pointer[1] - amount
        elif direction == 2:
            return self.pointer[0] - amount, self.pointer[1]
        elif direction == 3:
            return self.pointer[0], self.pointer[1] + amount
        else:
            return self.pointer[0], self.pointer[1]
    
    def step(self):
        if self.backtracking:
            print("backtracking...")
            self.backtrack_move()
        else:
            print("generating...")
            if self.set_direction():
                self.img[self.get_pixel_woffset(self.direction, 1)] = red
                self.img[self.get_pixel_woffset(self.direction, 2)] = red
                self.pointer = self.get_pixel_woffset(self.direction, 2)
    
    def backtrack_move(self):
        for n in range(2):
            self.img[self.pointer] = white
            found = False
            for r in range(4):
                pixel = self.get_pixel_woffset(r, 1)
                if self.is_pointer_in_range(pixel) and self.img[pixel] == red:
                    self.pointer = pixel
                    found = True
                    break
        self.backtracking = False
        if not found:
            self.finished = True
