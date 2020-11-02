from matplotlib import pyplot
from mazegen import MazeGen

print("mazegen start")
maze: MazeGen = MazeGen(32, 32, "maze.png")
img = maze.generate()
