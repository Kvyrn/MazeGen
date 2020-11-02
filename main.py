from matplotlib import pyplot
from mazegen import MazeGen

print("mazegen start")
maze: MazeGen = MazeGen(129, 129, "maze.png")
img = maze.generate()
