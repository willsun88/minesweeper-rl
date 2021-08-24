from tkinter import *
import random
from PIL import ImageTk, Image, ImageOps
from time import time

class MinesweepGame(object):
    def __init__(self, size, numMines, scale, b, pad):
        self.colors = {-1: "black", 0: "black", 1: "blue", 2: "green", 3: "red", 4: "purple", 5: "black", 6: "maroon", 7: "gray", 8: "turquoise"}
        self.timeOn = False
        self.size = size
        self.numMines = numMines
        self.scale = scale
        self.b = b
        self.pad = pad

        self.root = Tk()
        self.root.title("Minesweeper")
        self.root.geometry(str(self.size[1]*self.scale+2)+"x"+str(self.size[0]*self.scale+2+self.pad))
        self.root.resizable(False, False)
    
    def timer(self):
        #print(str(round(time()-init, 2)).zfill(6))
        self.timeLabel['text']="Time: "+str("{:.2f}".format(time()-self.init))
        if not self.timeOn:
            return
        self.timeLabel.after(10, self.timer)

    def callback(self, x, y, board):
        if not self.timeOn:
            self.timeOn = True
            self.init = time()
            self.timer()
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if (x>=1+self.scale*j and x<1+self.scale*(j+1)) and (y>=1+self.scale*i and y<1+self.scale*(i+1)) and board.revealed[i][j]==-2:
                    if not board.start:
                        board.createBoard((i*self.size[1])+j)
                    self.canvas.create_image(1 + self.scale * j, 1 + self.scale * i, anchor=NW, image=self.unc)
                    board.revealed[i][j] = board.board[i][j]
                    #print(board.board[i][j])
                    if board.board[i][j]!=0:
                        self.canvas.create_text(1+self.scale*j+(self.scale/2), 1+self.scale*i+(self.scale/2), font="MINE-SWEEPER 25",
                                        fill=self.colors[board.board[i][j]], text=board.board[i][j])
                    if board.board[i][j]==0:
                        try:
                            self.callback(x - self.scale, y - self.scale, board)
                        except:
                            pass
                        try:
                            self.callback(x - self.scale, y, board)
                        except:
                            pass
                        try:
                            self.callback(x - self.scale, y + self.scale, board)
                        except:
                            pass
                        try:
                            self.callback(x, y - self.scale, board)
                        except:
                            pass
                        try:
                            self.callback(x, y + self.scale, board)
                        except:
                            pass
                        try:
                            self.callback(x + self.scale, y - self.scale, board)
                        except:
                            pass
                        try:
                            self.callback(x + self.scale, y, board)
                        except:
                            pass
                        try:
                            self.callback(x + self.scale, y + self.scale, board)
                        except:
                            pass
                    elif board.board[i][j]==-1:
                        self.timeOn = False
                        for s in range(self.size[0]):
                            for t in range(self.size[1]):
                                if board.revealed[s][t]==-3 and board.board[s][t]!=-1:
                                    self.canvas.create_image(1 + self.scale * t, 1 + self.scale * s, anchor=NW, image=self.c_flag_wrong)
                                if board.board[s][t] == -1:
                                    if board.revealed[s][t]!=-3:
                                        self.canvas.create_image(1 + self.scale * t, 1 + self.scale * s, anchor=NW, image=self.mine)
                        self.canvas.create_image(1 + self.scale * j, 1 + self.scale * i, anchor=NW, image=self.mine_red)
                        self.btn.configure(image=self.dead)
                        self.btn.pack()
                        self.canvas.unbind("<Button-1>")
                        self.canvas.unbind("<Button-3>")

                    if board.finished():
                        for s in range(self.size[0]):
                            for t in range(self.size[1]):
                                if board.board[s][t] == -1:
                                    r = self.canvas.create_image(1 + self.scale * t, 1 + self.scale * s, anchor=NW, image=self.c_flag)
                        self.mineCount = 0
                        self.mineLabel['text'] = "Mines: "+str(self.mineCount).zfill(3)
                        self.btn.configure(image=self.win)
                        self.btn.pack()
                        self.timeOn = False
                        self.canvas.unbind("<Button-1>")
                        self.canvas.unbind("<Button-3>")

                    self.canvas.pack()

    def flag(self, x, y, board):
        if not self.timeOn:
            self.timeOn = True
            self.init = time()
            self.timer()
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if (x>=1+self.scale*j and x<1+self.scale*(j+1)) and (y>=1+self.scale*i and y<1+self.scale*(i+1)):
                    if board.revealed[i][j]==-2:
                        self.mineCount-=1
                        self.mineLabel['text'] = "Mines: "+str(self.mineCount).zfill(3)
                        self.canvas.create_image(1+self.scale*j, 1+self.scale*i, anchor=NW, image=self.c_flag)
                        board.revealed[i][j] = -3
                        self.canvas.pack()
                    elif board.revealed[i][j]==-3:
                        self.mineCount += 1
                        self.mineLabel['text'] = "Mines: "+str(self.mineCount).zfill(3)
                        self.canvas.create_image(1+self.scale*j, 1+self.scale*i, anchor=NW, image=self.c)
                        board.revealed[i][j] = -2
                        self.canvas.pack()

    def reset(self):
        self.canvas.destroy()
        self.mineLabel.destroy()
        self.timeLabel.destroy()
        self.btn.destroy()
        self.timeOn = False
        self.minesweep()

    def minesweep(self):
        self.game = Minesweep(*self.size, self.numMines)

        rsz = (self.scale-2*self.b, self.scale-2*self.b)
        brdr = (self.b, self.b)
        self.canvas= Canvas(self.root, width=self.game.n*self.scale, height=self.game.m*self.scale)
        self.c_flag = ImageTk.PhotoImage(ImageOps.expand(Image.open("images/covered_flag.jpg").resize(rsz, Image.ANTIALIAS), border=brdr, fill=(127, 127, 127)))
        self.c_flag_wrong = ImageTk.PhotoImage(ImageOps.expand(Image.open("images/covered_flag_wrong.jpg").resize(rsz, Image.ANTIALIAS), border=brdr, fill=(127, 127, 127)))
        self.unc = ImageTk.PhotoImage(ImageOps.expand(Image.open("images/uncovered1.jpg").resize(rsz, Image.ANTIALIAS), border=brdr, fill=(127, 127, 127)))
        self.c = ImageTk.PhotoImage(ImageOps.expand(Image.open("images/covered.jpg").resize(rsz, Image.ANTIALIAS), border=brdr, fill=(127, 127, 127)))

        self.mine = ImageTk.PhotoImage(ImageOps.expand(Image.open("images/mine.png").resize(rsz, Image.ANTIALIAS), border=brdr, fill=(127, 127, 127)))
        self.mine_red = ImageTk.PhotoImage(ImageOps.expand(Image.open("images/mine_red.png").resize(rsz, Image.ANTIALIAS), border=brdr, fill=(127, 127, 127)))

        self.good = ImageTk.PhotoImage(ImageOps.expand(Image.open("images/good.png").resize((self.scale, self.scale)), fill=(127, 127, 127)))
        self.win = ImageTk.PhotoImage(ImageOps.expand(Image.open("images/win.png").resize((self.scale, self.scale)), fill=(127, 127, 127)))
        self.dead = ImageTk.PhotoImage(ImageOps.expand(Image.open("images/dead.png").resize((self.scale, self.scale)), fill=(127, 127, 127)))

        for i in range(self.size[0]):
            for j in range(self.size[1]):
                self.canvas.create_image(1+self.scale*j,1+self.scale*i,anchor=NW, image=self.c)

        self.canvas.bind("<Button-1>", lambda e: self.callback(e.x, e.y, self.game))
        self.canvas.bind("<Button-3>", lambda e: self.flag(e.x, e.y, self.game))
        self.canvas.pack()

        self.mineLabel = Label(self.root, text="Mines: "+str(self.numMines).zfill(3), fg="red", bg="black", font="MINE-SWEEPER 15", anchor=CENTER)
        self.mineCount = self.numMines
        self.mineLabel.pack()

        self.timeLabel = Label(self.root, text="Time: 000.00", fg="red", bg="black", font="MINE-SWEEPER 15", anchor=CENTER)
        self.timeLabel.pack()
        self.init = time()
        self.timer()

        self.btn = Button(self.root, image=self.good, command=self.reset)
        self.btn.pack()

        self.root.mainloop()

class Minesweep(object):
    def __init__(self, m, n, num_mines):
        # Defining the board size as m x n, m being the height and n being the width, with num_mines number of mines
        self.m = m
        self.n = n
        self.num_mines = num_mines
        self.board = [[0 for x in range(self.n)] for y in range(self.m)]
        self.start = False
        #self.createBoard(no=1)

        # Revealed board; -2 is not revealed, -3 is flagged, everything else is the actual number
        self.revealed = [[-2 for x in range(self.n)] for y in range(self.m)]

    def createBoard(self, no=0):
        self.start = True

        # Note that the board is formatted so that the numbers correspond to the numbers displayed, with -1 being a mine
        # Select random positions for mines (using sampling w/o replacement)

        for x in random.sample(list(range(self.m*self.n))[:no]+list(range(self.m*self.n))[no+1:], self.num_mines):
            #print(x, int((x-x%self.n)/self.n), int(x%self.n))
            self.board[int((x-x%self.n)/self.n)][int(x%self.n)] = -1

        # Go through the whole board and define the position numbers
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j]!=-1:
                    if i - 1 >= 0 and j - 1 >= 0:
                        if self.board[i - 1][j - 1] == -1:
                            self.board[i][j] += 1
                    if i - 1 >= 0:
                        if self.board[i - 1][j] == -1:
                            self.board[i][j] += 1
                    if i - 1 >= 0 and j + 1 <= self.n - 1:
                        if self.board[i - 1][j + 1] == -1:
                            self.board[i][j] += 1
                    if j - 1 >= 0:
                        if self.board[i][j - 1] == -1:
                            self.board[i][j] += 1
                    if j + 1 <= self.n - 1:
                        if self.board[i][j + 1] == -1:
                            self.board[i][j] += 1
                    if i + 1 <= self.m - 1 and j - 1 >= 0:
                        if self.board[i + 1][j - 1] == -1:
                            self.board[i][j] += 1
                    if i + 1 <= self.m - 1:
                        if self.board[i + 1][j] == -1:
                            self.board[i][j] += 1
                    if i + 1 <= self.m - 1 and j + 1 <= self.n - 1:
                        if self.board[i + 1][j + 1] == -1:
                            self.board[i][j] += 1
        self.dispBoard()

    def dispBoard(self):
        print("\n")
        # Test print the board into the console
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                print(self.board[i][j], end="\t")
            print("")

    def finished(self):
        fin = True
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j]!=-1 and (self.revealed[i][j]==-2 or self.revealed[i][j]==-3):
                    fin = False
        return fin