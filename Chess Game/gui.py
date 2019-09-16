from tkinter import *

import board


class BoardGUI:
    # initialize variable
    mousePressedX = 0
    mousePressedY = 0
    mouseReleasedX = 0
    mouseReleasedY = 0

    move2compare = []

    # constructor (will be called automatically when the class is called)
    def __init__(self):
        clear = open("notation.txt", "w+")
        clear.write("")

        self.turn = 0

        # initialize the GUI frame
        self.root = Tk()

        # this line prints out the board in the terminal
        # for i in range(8):
        #     print(board.Board().chessBoard[i][:])
        #     print ("")

        # set the cavas height and width
        self.canvas_width = 1245
        self.canvas_height = 830

        # set the square size
        self.square_size = 80

        # create a container for the whole display
        self.myContainer1 = Frame(self.root)
        # add the container to the frame
        self.myContainer1.pack()

        # create a canvas
        self.w = Canvas(self.myContainer1, width=self.canvas_width, height=self.canvas_height)
        # add the canvas to the frame
        self.w.pack()

        # Fill in background as white
        self.w.create_rectangle(0, 0, 2000, 2000, fill='white', outline="")

        # this creates the chess board
        # this goes from left to right, top to bottom
        for i in range(8):
            for j in range(8):
                if (j + i) % 2 == 0:
                    self.w.create_rectangle(i * self.square_size, j * self.square_size, self.square_size * (i + 1),
                                            self.square_size * (j + 1), fill="gold")
                else:
                    self.w.create_rectangle(i * self.square_size, j * self.square_size, self.square_size * (i + 1),
                                            self.square_size * (j + 1), fill="dark red")

        self.w.yAxis = PhotoImage(file='yAxis.png')
        self.w.create_image(642, 2, anchor='nw', image=self.w.yAxis)
        self.w.xAxis = PhotoImage(file='xAxis.png')
        self.w.create_image(2, 642, anchor='nw', image=self.w.xAxis)

        self.w.logo = PhotoImage(file='ChessComrades.png')
        self.w.create_image(1, 682, anchor='nw', image=self.w.logo)

        self.w.meme = PhotoImage(file='lmaoo.png')
        self.w.create_image(640, 635, anchor='nw', image=self.w.meme)

        self.w.whiteTurn = PhotoImage(file='WhiteTurn.png').subsample(3, 3)
        self.w.create_image(675, 590, anchor='nw', image=self.w.whiteTurn)
        self.w.blackTurn = PhotoImage(file='BlackTurn.png').subsample(3, 3)
        self.w.create_image(675, 0, anchor='nw', image=self.w.blackTurn)
        self.w.create_rectangle(675, 0, 842, 250, fill='white', outline="")

        self.w.notationBox = PhotoImage(file="Notation.png")
        self.w.create_image(840, 0, anchor='nw', image=self.w.notationBox)

        # this command updates the GUI every 10 miliseconds
        # calls the drawPieces() function every 10 miliseconds
        self.root.after(10, self.drawPieces)
        self.root.mainloop()

    # this function fires during a mousepress event
    def Mousepress(self, event):
        # get the position of the mouse press and divide with the square size to the get the square of which the mouse pointer is pointed
        self.mousePressedX = int(event.y / self.square_size)
        self.mousePressedY = int(event.x / self.square_size)
        # this function returns nothing, it just updates the mousePressedX and mousePressedY variables
        return

    # this function fires when the mouse is released
    def Mousereleased(self, event):
        # get the location of the mouse released event
        self.mouseReleasedX = event.y
        self.mouseReleasedY = event.x
        # initialize a list to verify the move
        self.move2compare = []
        # append the position of the mouse clicked and the mouse released location
        self.move2compare.append((self.mousePressedX, self.mousePressedY, int(self.mouseReleasedX / self.square_size),
                                  int(self.mouseReleasedY / self.square_size)))
        # calls the function determinePiece() from the board.py
        worked = board.Board().determinePiece(self.move2compare, self.turn)
        # this calls back the function drawPieces() after 100 miliseconds
        self.root.after(100, self.drawPieces())

        if worked=="Checkmate":
            self.w.checkmate = PhotoImage(file='Checkmate.png')
            self.w.create_image(2, 682, anchor='nw', image=self.w.checkmate)
        if worked:
            if not self.turn%2==0:  # if white
                self.w.create_rectangle(675, 0, 842, 200, fill='white', outline="")  # cover up black
                self.w.whiteTurn = PhotoImage(file='WhiteTurn.png').subsample(3, 3)  # create white
                self.w.create_image(675, 590, anchor='nw', image=self.w.whiteTurn)
            else:  # if black
                self.w.create_rectangle(675, 590, 842, 635, fill='white', outline="")  # cover up white
                self.w.blackTurn = PhotoImage(file='BlackTurn.png').subsample(3, 3)  # create black
                self.w.create_image(675, 0, anchor='nw', image=self.w.blackTurn)
            self.turn = self.turn+1

        return

    # this function is used to draw the pieces on the board
    def drawPieces(self):

        if (self.turn % 2 != 0):
            xStartPx = 925
            # draw notation onto screen
            self.w.create_rectangle(840, 0, 2000, 2000, fill='white', outline="")  # cover up old text
            self.w.notationBox = PhotoImage(file="Notation.png")
            self.w.create_image(840, 0, anchor='nw', image=self.w.notationBox)
            F = open("notation.txt", "r+")
            input = F.readlines()
            yStartPx = 45
            count = 0;
            for line in input:
                self.w.create_text(xStartPx, yStartPx, fill="black", font="Times 7", text=line)
                count = count + 1
                yStartPx = yStartPx + 16
                if count > 45:
                    xStartPx = xStartPx + 75
                    count = 0
                    yStartPx = 45

        # all these lines set the variables to the right image path
        # subsample function reduces the size of the image
        self.w.whiteRook = PhotoImage(file='rookWhite.gif').subsample(4, 4)
        self.w.whiteKnight = PhotoImage(file='knightWhite.gif').subsample(4, 4)
        self.w.whiteBishop = PhotoImage(file='bishopWhite.gif').subsample(4, 4)
        self.w.whiteQueen = PhotoImage(file='queenWhite.gif').subsample(4, 4)
        self.w.whiteKing = PhotoImage(file='kingWhite.png').subsample(4, 4)
        self.w.whitePawn = PhotoImage(file='pawnWhite.gif').subsample(4, 4)

        self.w.blackPawn = PhotoImage(file='pawnBlack.gif').subsample(4, 4)
        self.w.blackRook = PhotoImage(file='rookBlack.gif').subsample(4, 4)
        self.w.blackKnight = PhotoImage(file='knightBlack.gif').subsample(4, 4)
        self.w.blackBishop = PhotoImage(file='bishopBlack.gif').subsample(4, 4)
        self.w.blackQueen = PhotoImage(file='queenBlack.gif').subsample(4, 4)
        self.w.blackKing = PhotoImage(file='kingBlack.gif').subsample(4, 4)

        # iterates through all the tiles
        for i in range(64):
            # if the particular tile on the board has the letter "R", then a white Rook will be placed
            if board.Board().chessBoard[int(i / 8)][i % 8] == "R":
                WRook = self.w.create_image((i % 8) * self.square_size + 2, int(i / 8) * self.square_size + 2,
                                            anchor='nw', image=self.w.whiteRook)
                self.w.tag_bind(WRook, '<ButtonPress-1>',
                                self.Mousepress)  # binding the rook image with the function Mousepress()
                self.w.tag_bind(WRook, '<ButtonRelease-1>',
                                self.Mousereleased)  # binding the rook image with the function Mousereleased()

            # if the particular tile on the board has the letter "N", then a white Knight will be placed
            elif board.Board().chessBoard[int(i / 8)][i % 8] == "N":
                WKnight = self.w.create_image((i % 8) * self.square_size + 2, int(i / 8) * self.square_size + 2,
                                              anchor='nw', image=self.w.whiteKnight)
                self.w.tag_bind(WKnight, '<ButtonPress-1>',
                                self.Mousepress)  # binding the knight image with the function Mousepress()
                self.w.tag_bind(WKnight, '<ButtonRelease-1>',
                                self.Mousereleased)  # binding the knight image with the function Mousereleased()

            # if the particular tile on the board has the letter "B", then a white Bishop will be placed
            elif board.Board().chessBoard[int(i / 8)][i % 8] == "B":
                WBishop = self.w.create_image((i % 8) * self.square_size + 2, int(i / 8) * self.square_size + 2,
                                              anchor='nw', image=self.w.whiteBishop)
                self.w.tag_bind(WBishop, '<ButtonPress-1>',
                                self.Mousepress)  # binding the bishop image with the function Mousepress()
                self.w.tag_bind(WBishop, '<ButtonRelease-1>',
                                self.Mousereleased)  # binding the bishop image with the function Mousereleased()

            # if the particular tile on the board has the letter "Q", then a white Queen will be placed
            elif board.Board().chessBoard[int(i / 8)][i % 8] == "Q":
                WQueen = self.w.create_image((i % 8) * self.square_size + 2, int(i / 8) * self.square_size + 2,
                                             anchor='nw', image=self.w.whiteQueen)
                self.w.tag_bind(WQueen, '<ButtonPress-1>',
                                self.Mousepress)  # binding the queen image with the function Mousepress()
                self.w.tag_bind(WQueen, '<ButtonRelease-1>',
                                self.Mousereleased)  # binding the queen image with the function Mousereleased()

            elif board.Board().chessBoard[int(i / 8)][i % 8] == "K":
                WKing = self.w.create_image((i % 8) * self.square_size + 2, int(i / 8) * self.square_size + 2,
                                            anchor='nw', image=self.w.whiteKing)
                self.w.tag_bind(WKing, '<ButtonPress-1>', self.Mousepress)
                self.w.tag_bind(WKing, '<ButtonRelease-1>', self.Mousereleased)

            elif board.Board().chessBoard[int(i / 8)][i % 8] == "P":
                WPawn = self.w.create_image((i % 8) * self.square_size + 2, int(i / 8) * self.square_size + 2,
                                            anchor='nw', image=self.w.whitePawn)
                self.w.tag_bind(WPawn, '<ButtonPress-1>', self.Mousepress)
                self.w.tag_bind(WPawn, '<ButtonRelease-1>', self.Mousereleased)

            elif board.Board().chessBoard[int(i / 8)][i % 8] == "p":
                BPawn = self.w.create_image((i % 8) * self.square_size + 2, int(i / 8) * self.square_size + 2,
                                            anchor='nw', image=self.w.blackPawn)
                self.w.tag_bind(BPawn, '<ButtonPress-1>', self.Mousepress)
                self.w.tag_bind(BPawn, '<ButtonRelease-1>', self.Mousereleased)

            elif board.Board().chessBoard[int(i / 8)][i % 8] == "r":
                BRook = self.w.create_image((i % 8) * self.square_size + 2, int(i / 8) * self.square_size + 2,
                                            anchor='nw', image=self.w.blackRook)
                self.w.tag_bind(BRook, '<ButtonPress-1>', self.Mousepress)
                self.w.tag_bind(BRook, '<ButtonRelease-1>', self.Mousereleased)

            elif board.Board().chessBoard[int(i / 8)][i % 8] == "n":
                BKnight = self.w.create_image((i % 8) * self.square_size + 2, int(i / 8) * self.square_size + 2,
                                              anchor='nw', image=self.w.blackKnight)
                self.w.tag_bind(BKnight, '<ButtonPress-1>', self.Mousepress)
                self.w.tag_bind(BKnight, '<ButtonRelease-1>', self.Mousereleased)

            elif board.Board().chessBoard[int(i / 8)][i % 8] == "b":
                BBishop = self.w.create_image((i % 8) * self.square_size + 2, int(i / 8) * self.square_size + 2,
                                              anchor='nw', image=self.w.blackBishop)
                self.w.tag_bind(BBishop, '<ButtonPress-1>', self.Mousepress)
                self.w.tag_bind(BBishop, '<ButtonRelease-1>', self.Mousereleased)

            elif board.Board().chessBoard[int(i / 8)][i % 8] == "q":
                BQueen = self.w.create_image((i % 8) * self.square_size + 2, int(i / 8) * self.square_size + 2,
                                             anchor='nw', image=self.w.blackQueen)
                self.w.tag_bind(BQueen, '<ButtonPress-1>', self.Mousepress)
                self.w.tag_bind(BQueen, '<ButtonRelease-1>', self.Mousereleased)

            elif board.Board().chessBoard[int(i / 8)][i % 8] == "k":
                BKing = self.w.create_image((i % 8) * self.square_size + 2, int(i / 8) * self.square_size + 2,
                                            anchor='nw', image=self.w.blackKing)
                self.w.tag_bind(BKing, '<ButtonPress-1>', self.Mousepress)
                self.w.tag_bind(BKing, '<ButtonRelease-1>', self.Mousereleased)


# calls the class
BoardGUI()
