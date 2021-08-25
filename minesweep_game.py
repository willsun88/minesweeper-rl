from tkinter import *
import random
from PIL import ImageTk, Image, ImageOps
from time import time
from minesweep import Minesweep, Game

# Game parameters
size = (10, 10)
numMines = 17
scale = 50
b = 2
pad = 120

# Run the game
game = Game(size, numMines, scale, b, pad)
game.minesweep()