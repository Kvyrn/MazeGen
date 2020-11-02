from PIL import Image
from random import randint

white = (255, 255, 255, 255)
red = (255, 0, 0, 255)
green = (0, 255, 0, 255)


class MazeGenUnfixed:
    output_filename = ""
    
    img = None
    x_size = 0
    y_size = 0
    
    # current position on image
    pointer = [1, 1]
    # heading direction
    direction = 0
    last_directions = []
    
    def __init__(self, x_size: int, y_size: int, output_filename: str):
        # self.img = numpy.array(Image.new("RGBA", (x_size, y_size), color="black"))
        self.img_raw = Image.new("RGBA", (x_size, y_size), color="black")
        self.img = self.img_raw.load()
        dir(self.img)
        self.output_filename = output_filename
        self.x_size, self.y_size = self.img_raw.size
    
    def generate(self):
        self.img[1, 1] = white
        complete = False
        # backtracking loop
        while True:
            self.direction = randint(0, 3)
            print(self.direction)
            while not self.is_usable_direction():
                print("inusable direction")
                self.direction = randint(0, 3)
            self.last_directions.append(self.direction)
            
            if self.should_stop():
                if self.direction == 0:
                    self.pointer = [self.pointer[0] + 1, self.pointer[1]]
                elif self.direction == 1:
                    self.pointer = [self.pointer[0], self.pointer[1] - 1]
                elif self.direction == 2:
                    self.pointer = [self.pointer[0] - 1, self.pointer[1]]
                elif self.direction == 3:
                    self.pointer = [self.pointer[0], self.pointer[1] + 1]
                self.img[self.pointer[0], self.pointer[1]] = white
            else:
                complete = True
                print("line finished")
            print(self.pointer)
            
            if complete:
                break
        # red starting point
        self.img[1, 1] = red
        
        self.img_raw.save(self.output_filename)
        return self.img_raw
    
    def is_usable_direction(self):
        if len(self.last_directions) < 1:
            return True
        
        using_directions = self.last_directions[len(self.last_directions) - 2:]
        if self.direction == 0:
            opposite = 2
        elif self.direction == 1:
            opposite = 3
        elif self.direction == 2:
            opposite = 0
        elif self.direction == 3:
            opposite = 1
        else:
            opposite = 4
        return opposite not in using_directions
    
    def should_stop(self):
        # directions: 0 = right, 1 = down, 2 = left, 3 = up
        if self.direction == 0:
            print("direction 0")
            front1 = [self.pointer[0] + 1, self.pointer[1]]
            front2 = [self.pointer[0] + 2, self.pointer[1]]
            front3 = [self.pointer[0] + 3, self.pointer[1]]
            
            left = [front1[0], front1[1] + 1]
            right = [front1[0], front1[1] - 1]
        elif self.direction == 1:
            print("direction 1")
            front1 = [self.pointer[0], self.pointer[1] - 1]
            front2 = [self.pointer[0], self.pointer[1] - 2]
            front3 = [self.pointer[0], self.pointer[1] - 3]
            
            left = [front1[0] + 1, front1[1]]
            right = [front1[0] - 1, front1[1]]
        elif self.direction == 2:
            print("direction 2")
            front1 = [self.pointer[0] - 1, self.pointer[1]]
            front2 = [self.pointer[0] - 2, self.pointer[1]]
            front3 = [self.pointer[0] - 3, self.pointer[1]]
            
            left = [front1[0], front1[1] + 1]
            right = [front1[0], front1[1] - 1]
        elif self.direction == 3:
            print("direction 3")
            front1 = [self.pointer[0], self.pointer[1] + 1]
            front2 = [self.pointer[0], self.pointer[1] + 2]
            front3 = [self.pointer[0], self.pointer[1] + 3]
            
            left = [front1[0] + 1, front1[1]]
            right = [front1[0] - 1, front1[1]]
        else:
            return True
        
        b1 = self.is_pointer_in_range(front1) and self.img[front1[0], front1[1]] != white
        b2 = self.is_pointer_in_range(front2) and self.img[front2[0], front2[1]] != white
        b3 = self.is_pointer_in_range(front3) and self.img[front3[0], front3[1]] != white
        b4 = self.is_pointer_in_range(left) and self.img[left[0], left[1]] != white
        b5 = self.is_pointer_in_range(right) and self.img[right[0], right[1]] != white
        return b1 and b2 and b3 and b4 and b5
    
    # check if a pixel is inside the image
    def is_pointer_in_range(self, point):
        if point[0] > self.x_size or point[0] < 0:
            print("pointer out of range, axis=x")
            return False
        elif point[1] > self.y_size or point[1] < 0:
            print("pointer out of range, axis=y")
            return False
        else:
            return True
    
    # testing method
    def info(self):
        print(f"x_size: {self.x_size}")
        print(f"y_size: {self.y_size}")
        print(f"output_filename: {self.output_filename}")
