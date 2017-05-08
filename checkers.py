"""
A Game of Checkers
Text-based, played on the terminal
Made with Python 3
by PseudoMon

Board format:
  0 1 2 3 4 5
0 . . . . . . 
1 . . . . . .
2 . . . . . .
3 . . . . . .
4 . . . . . .
5 . . . . . .

All coordinates are in (row, column) or (y, x)

Player 1 = 'o' -> flipped: ó
Player 2 = 'i' -> flipped: í
I really don't like that Python has no multi-line comment
"""    
    
class Piece:
    def __init__(self, startpos=(0,0), player=0):
        #player should be a Player object
        self.player = player
        self.symbol = player.symbol
        self.row = startpos[0]
        self.col = startpos[1]
        
        #Checkers-specific flip (flipped piece can move backwards)
        self.flipped = False
        
    def __str__(self):
        return self.symbol
        
    def move_to_pos(self, topos):
        self.row = topos[0]
        self.col = topos[1]
        return
        
    # Checkers-specific function
    def checkflip(self, max=(5,5)):
        if self.player.ord == 1:
            if self.row >= 5:
                print("Flipped!")
                self.flipped = True
                self.symbol = self.player.flipsymbol
                
                return True
                
        elif self.player.ord == 2:
            if self.row <= 0:
                print("Flipped 2!")
                self.flipped = True
                self.flipped = True
                self.symbol = self.player.flipsymbol
                
                return True
                
        return False
                
    # NOW OBSOLETE
    def is_valid_checkersmove(self, pos):
        valid = True
        
        # Player 0 moves from the top
        if self.player == 0:
            if pos[0] != self.row + 1:
                valid = False
              
        # Player 1 moves from the bottom
        else:
            if pos[0] != self.row - 1:
                valid = False
            
        # Sideways movement
        if pos[1] == self.col - 1 or pos[1] == self.col + 1:
            pass
        else:
            valid = False
            
        return valid
        
class Board:
    def __init__(self, size, pieces=[]):
        self.board = [["." for x in range(size[0])] for y in range(size[1])]
        self.pieces = pieces
   
    def __str__(self):
        boardstr = " \n  012345\n"
        rownum = 0
        
        for row in self.board:
            boardstr += str(rownum) + " "
            rownum += 1
            
            for col in row:
                boardstr += col
                
            boardstr += "\n"
        return boardstr
        
    def create_piece(self, piece):
        self.pieces.append(piece)
        return
    
    def set_piece(self, piece):
        self.board[piece.row][piece.col] = piece.symbol
        return
        
    def set_many_pieces(self, pieces):
        for piece in pieces:
            self.set_piece(piece)
        return
        
    def move_piece_to_pos(self, piece, topos):
        if self.board[topos[0]][topos[1]] != ".":
            print("That position is already filled!")
            return False
        else:
            pass
            
        self.board[piece.row][piece.col] = "."
        piece.move_to_pos(topos)
        self.board[piece.row][piece.col] = piece.symbol
        return True
    
    def findpiece(self, pos, player=None):
        nopiece = True
        
        for piece in self.pieces:
            
            if piece.row == pos[0] and piece.col == pos[1]:
                nopiece = False
                
                if player == None:
                    return piece
                    
                else:
                    if piece.player.ord == player:
                        return piece
                        
                    else:
                        print("The piece is not yours!")
                        return 0
        
        if nopiece:
            print("No piece in that position!")
            return 0
    
    def destroy_piece_at(self, pos):        
    
        piece_to_remove = self.findpiece(pos)
        
        piece_to_remove.player.num_o_pieces -= 1
        
        self.pieces.remove(piece_to_remove)
        self.board[pos[0]][pos[1]] = "."
        
        return
        
    def is_valid_checkersmove(self, piece, pos):
        valid = True
        
        if piece.flipped:
            if pos[0] != piece.row + 1 and pos[0] != piece.row - 1:
                valid = False
        
        # Player 1 moves from the top
        elif piece.player.ord == 1:
            if pos[0] != piece.row + 1:
                valid = False
              
        # Player 2 moves from the bottom
        else:
            if pos[0] != piece.row - 1:
                valid = False
            
        # Sideways movement
        if pos[1] == piece.col - 1 or pos[1] == piece.col + 1:
            pass
        else:
            valid = False
            
        # Check eatery
        
        #For Player 1 and flipped pieces, going down:
        if (piece.player.ord == 1 or piece.flipped) and (pos[0] == piece.row + 2):
        
            # Going right
            if pos[1] == piece.col + 2:
                if self.board[pos[0] - 1][pos[1] - 1] != ".":
                    todestroy = ((pos[0] - 1), (pos[1] - 1))
                    valid = True
                    self.destroy_piece_at(todestroy)
                    
                else:
                    print("Nothing to eat!")
                    valid = False
                    
            # Going left
            elif pos[1] == piece.col - 2:
                if self.board[pos[0] - 1][pos[1] + 1] != ".":
                    todestroy = ((pos[0] - 1), (pos[1] + 1))
                    valid = True
                    self.destroy_piece_at(todestroy)
                else:
                    print("Nothing to eat!")
                    valid = False
            else: 
                valid = False
                
        # For Player 2 and flipped pieces(moving up)
        elif (piece.player.ord == 2 or piece.flipped) and (pos[0] == piece.row - 2):
        
            # Going right
            if pos[1] == piece.col + 2:
                if self.board[pos[0] + 1][pos[1] - 1] != ".":
                    todestroy = ((pos[0] + 1), (pos[1] - 1))
                    valid = True
                    self.destroy_piece_at(todestroy)
                else:
                    print("Nothing to eat!")
                    valid = False
                    
            # Going left
            elif pos[1] == piece.col - 2:
                if self.board[pos[0] + 1][pos[1] + 1] != ".":
                    todestroy = ((pos[0] + 1), (pos[1] + 1))
                    valid = True
                    self.destroy_piece_at(todestroy)
                else:
                    print("Nothing to eat!")
                    valid = False
            else: 
                valid = False
                
                
        return valid
        
class Player:
    def __init__(self, ord, symbol='o', flipsymbol='x'):
        self.ord = ord
        self.num_o_pieces = 0
        self.symbol = symbol
        
        #Checkers-specific
        self.flipsymbol = flipsymbol
       
    def __str__(self):
        return str(self.ord)

        
def inputtopos(inp):
        
    if "." in inp:
        inp = inp.split('.')
        
    elif "," in inp:
        inp = inp.split(',')
        
    try:
        pos = ( int(inp[0]), int(inp[1]) )
    except (IndexError, ValueError):
        print("Input error!")
        
    return pos
    
    
def checkwin(players):
    for player in players:
        if player.num_o_pieces <= 0:
            print("Player {} has ran out of unit!".format(player.ord))
            
            players.remove(player)
            return players[0]
    return None

    
def swapplayer(player):
    if player == 1:
        player = 2
    elif player == 2:
        player = 1
    return player
    
    
def testmove():
    print("Move piece at position (1,1)")
    for piece in pieces:
        if piece.row == 1 and piece.col == 1:
            board.move_piece_to_pos(piece, (2,0))
            
    print(board)


## Setup
size = (6, 6)
board = Board(size)
pieces = []

## Create the two players
player_one = Player(1, 'o', 'ó')
player_two = Player(2, 'a', 'á')
players = [player_one, player_two]


## Create two rows of Player 1's units
for i in range(0, 6, 2):
    pieces.append(Piece((0, i), player_one))
    pieces.append(Piece((1, i+1), player_one))
    player_one.num_o_pieces += 2
    
## Create two rows of Player 2
bottomrow = 5
for i in range(0, 6, 2):
    pieces.append(Piece((bottomrow, i + 1), player_two))
    pieces.append(Piece((bottomrow - 1, i), player_two))    
    player_two.num_o_pieces += 2
del bottomrow


board.set_many_pieces(pieces)
board.pieces = pieces
    
print(board)
inp = None
playerord = player_one.ord


## Looper
while inp != "x" and inp != "exit":
    print("Player {}'s turn".format(playerord))
    print("Position of piece to move?")
    inp = input("> ")
    if inp == "x" or inp == "exit":
        break
        
    pos = inputtopos(inp)

    piecetomove = board.findpiece(pos, playerord)

    if piecetomove != 0:
        print("Where to?")
        inp = input("> ")
        if inp == "x" or inp == "exit":
            break
            
        pos = inputtopos(inp)
        
        if board.is_valid_checkersmove(piecetomove, pos):
            moved = board.move_piece_to_pos(piecetomove, pos)
            
            if moved:
                if piecetomove.checkflip():
                    board.set_piece(piecetomove)
                    
                winner = checkwin(players)
                if winner:
                    break
                    
                playerord = swapplayer(playerord)
        else:
            print("You can't do that!")
            

    print(board)
    
try:
    print(board)
    print("Player {} has won the game!".format(winner.ord))
except (NameError, AttributeError):
    pass
