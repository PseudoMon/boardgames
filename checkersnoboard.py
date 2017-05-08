from baseboard import Piece, Board, Player
from baseboard import inputtopos, checkwin, swapplayer 

class CheckersPiece(Piece):
    def __init__(self, startpos=(0,0), player=0):
        Piece.__init__(self, startpos, player)
        self.flipped = False
        
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
        
class CheckersBoard(Board):
    def __init__(self, size, pieces=[]):
        Board.__init__(self, size, pieces)
        
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
        
class CheckersPlayer(Player):
    def __init__(self, ord, symbol='o', flipsymbol='x'):
        Player.__init__(self, ord, symbol)
   
        self.flipsymbol = flipsymbol
        
## Setup
size = (8, 8)
board = CheckersBoard(size)
pieces = []

## Create the two players
player_one = CheckersPlayer(1, 'o', '?')
player_two = CheckersPlayer(2, 'a', '?')
players = [player_one, player_two]


## Create two rows of Player 1's units
for i in range(0, size[1], 2):
    pieces.append(CheckersPiece((0, i), player_one))
    pieces.append(CheckersPiece((1, i+1), player_one))
    player_one.num_o_pieces += 2
    
## Create two rows of Player 2
bottomrow = size[0] - 1
for i in range(0, size[1], 2):
    pieces.append(CheckersPiece((bottomrow, i + 1), player_two))
    pieces.append(CheckersPiece((bottomrow - 1, i), player_two))    
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