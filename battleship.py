"""
TODO: Change input to letters-numbers

search in pieces
if piece has that location
Board.board with that location -> x
if not -> o

1x Aircraft Carrier 5
1x Battleship 4
1x Cruiser 3
2x Destroyer 2
2x Submarine 1
"""

from baseboard import Piece, Board, Player
from baseboard import inputtopos, checkwin, swapplayer 

class BattleshipBoard(Board):
    def __init__(self, pieces=[]):
        Board.__init__(self, (10, 10), pieces)
        
    def findpiece(self, pos):
        nopiece = True
        
        for piece in self.pieces:
            
            if pos in piece.range:
                nopiece = False
                return piece
                
        if nopiece:
            return False
        
class BattleshipPiece(Piece):
    def __init__(self, range, name, player):
        # range is a tuple containing tuples
        Piece.__init__(self, range[0], player)
        
        self.hp = len(range)
        self.range = range
        self.name = name
        
    def attacked(self):
        self.hp -= 1
        
        if self.hp == 0:
            print("A {} is destroyed!".format(self.name))
            self.player.num_o_pieces -= 1
            
        return
        
class BattleshipPlayer(Player):
    def __init__(self, ord):
        Player.__init__(self, ord)
        
comp = Player(0)        
one = Player(1)
players = [comp, one]
comp.num_o_pieces = 1
one.num_o_pieces = 99

board = BattleshipBoard()

destroyer1 = BattleshipPiece( ((5,5), (6,5)), "Destroyer", comp)
destroyer2 = BattleshipPiece( ((0,0), (0,1)), "Destroyer", comp)

board.create_piece(destroyer1)

print(board)
inp = None

while inp != "x":
    inp = input("> ")
    if inp == "x" or inp == "exit":
        break
        
    pos = inputtopos(inp)
    hit = board.findpiece(pos)
    
    if not hit:
        board.board[pos[0]][pos[1]] = "o"
        
    else:
        print("You hit something!")
        hit.attacked()
        board.board[pos[0]][pos[1]] = "x"
        
        winner = checkwin(players)
        
        if winner:
            break
            
    print(board)
    
print(board)
print("Player wins!")




