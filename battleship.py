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
        
    def create_piece(self, piece):
        # Overloading the default
        self.pieces.append(piece)
        
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
        # range is a list containing tuples
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
        
def putpiece(chosen, board):
    print("Where to put?")
    inp = input("> ")
    startpos = inputtopos(inp)
    
    if startpos == False:
        return False
    
    print("Extending to? (up/down/left/right)")
    inp = input("> ")
    
    if inp in ("up", "down", "left", "right"):
        chosen.range = [startpos]
        toofar = {
            'up': startpos[0] - (chosen.hp - 1) < 0,
            'down': startpos[0] + (chosen.hp - 1) < 0,
            'left': startpos[1] - (chosen.hp - 1) < 0,
            'right': startpos[1] + (chosen.hp - 1) < 0
            }
        
        if toofar[inp]
            print("Dood, ye can't go that way")
            
        else:
            conflict = False
            for x in range(1,chosen.hp):
                if inp == "up":
                    pos = (startpos[0]-x, startpos[1])
                elif inp == "down":
                    pos = (startpos[0]+x, startpos[1])
                elif inp == "left":
                    pos = (startpos[1]-x, startpos[1])
                elif inp == "right":
                    pos = (startpos[1]+x, startpos[1])
                
                if board.findpiece(pos):
                    print("There's already another ship that way.")
                    break
                    
                else:
                    chosen.range.append( (startpos[0]-x, startpos[1]) )
                    
            if not conflict:
                board.create_piece(chosen)
                
    else:
        return False
        
    return True
        
comp = Player(0)        
one = Player(1)
players = [comp, one]
comp.num_o_pieces = 1
one.num_o_pieces = 3

board = BattleshipBoard()

destroyer1 = BattleshipPiece( 
    [(0,0), (0,1)], 
    "Destroyer", 
    one )
destroyer2 = BattleshipPiece(
    [(0,0), (0,1)], 
    "Destroyer", 
    one )
carrier = BattleshipPiece( 
    [(0,0), (0,1), (0,2), (0,3), (0,4)],
    "Aircraft Carrier",
    one )
    
ships = { 'Destroyer': [destroyer1, destroyer2], 'Carrier': [carrier] } 

inp = None
print(board)
    
while inp != "x":
    for ship in ships:
        print("{}x {} (size {})".format(len(ships[ship]), ship, ships[ship][0].hp))
        
    inp = input("> ")
    if inp in ships:
        try:
            chosen = ships[inp].pop()
        except IndexError:
            print("There's no more ship of that type!")
        else:
            if putpiece(chosen, board):
                if len(ships[inp]) == 0:
                    del ships[inp]
            else:
                ships[inp].append(chosen)
    else:
        print("?")
            

    
    
""" Attacking test
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
"""



