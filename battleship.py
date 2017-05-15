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
from random import randint 

class BattleshipBoard(Board):
    def __init__(self, pieces=[]):
        Board.__init__(self, (10, 10), pieces)
        
    def create_piece(self, piece):
        # Overloading the default, simply because Battleship doesn't use the typical row-col positioning
        self.pieces.append(piece)
        
    def findpiece(self, pos):
        nopiece = True
        
        for piece in self.pieces:
            
            if pos in piece.range:
                nopiece = False
                return piece
                
        if nopiece:
            return False
            
    def make_visible(self):
        for piece in self.pieces:
            for mass in piece.range:
                self.board[mass[0]][mass[1]] = "x"
                
    def make_invisible(self):
        for row in range(0,self.size[0]):
            for col in range(0,self.size[1]):
                self.board[row][col] = "."
                
    def set_piece(self, chosen, auto = False, startpos=None, going=None):
        # Overloading the default, Battleship piece-setting
        # is a bit more complicated
        if not auto:
            print("Where to put?")
            inp = input("> ")
            startpos = inputtopos(inp)
        
            if startpos == False:
                return False
            
        if self.findpiece(startpos):
            if not auto:
                print("There's already another ship there.")
            return False
        
        if not auto:
            print("Extending to? (up/down/left/right)")
            inp = input("> ")
        else:
            inp = going
        
        if inp in ("up", "down", "left", "right"):
            chosen.range = [startpos]
            toofar = {
                'up': startpos[0] - (chosen.hp - 1) < 0,
                'down': startpos[0] + (chosen.hp - 1) > self.size[0]-1,
                'left': startpos[1] - (chosen.hp - 1) < 0,
                'right': startpos[1] + (chosen.hp - 1) > self.size[1]-1
                }
            
            if toofar[inp]:
                if not auto:
                    print("Dood, ye can't go that way")
                return False
                
            else:
                for x in range(1,chosen.hp):
                    if inp == "up":
                        pos = (startpos[0]-x, startpos[1])
                    elif inp == "down":
                        pos = (startpos[0]+x, startpos[1])
                    elif inp == "left":
                        pos = (startpos[0], startpos[1]-x)
                    elif inp == "right":
                        pos = (startpos[0], startpos[1]+x)
                    
                    if self.findpiece(pos):
                        if not auto:
                            print("There's already another ship that way.")
                        return False
                        
                    else:
                        chosen.range.append(pos)
                        
                self.create_piece(chosen)
                    
        else:
            return False
            
        return True
                
        
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
        
class Destroyer(BattleshipPiece):
    def __init__(self, owner):
        BattleshipPiece.__init__(self,
            [(0,0), (0,1)], 
            "Destroyer", 
            owner ) 
            
class Submarine(BattleshipPiece):
    def __init__(self, owner):
        BattleshipPiece.__init__(self,
            [(0,0)],
            "Submarine",
            owner )
            
class Carrier(BattleshipPiece):
    def __init__(self, owner):
        BattleshipPiece.__init__(self,
            [(0,0), (0,1), (0,2), (0,3), (0,4)],
            "Carrier",
            owner ) 
            
class Battleshipship(BattleshipPiece):
    def __init__(self, owner):
        BattleshipPiece.__init__(self,
            [(0,0), (0,1), (0,2), (0,3)],
            "Battleship",
            owner ) 
            
class Cruiser(BattleshipPiece):
    def __init__(self, owner):
        BattleshipPiece.__init__(self,
            [(0,0), (0,1), (0,2)],
            "Cruiser",
            owner )         
        
class BattleshipPlayer(Player):
    def __init__(self, ord):
        Player.__init__(self, ord)
        

def position_ships(ships, board):
    inp = None
    while inp != "x":
        for ship in ships:
            print("{}x {} (size {})".format(len(ships[ship]), ships[ship][0].name, ships[ship][0].hp))
            
        inp = input("> ")
        inp = inp.lower()
        if inp in ships:
            try:
                chosen = ships[inp].pop()
            except IndexError:
                print("There's no more ship of that type!")
            else:
                if board.set_piece(chosen):
                    if len(ships[inp]) == 0:
                        del ships[inp]
                else:
                    # put piece back if unsuccesful
                    ships[inp].append(chosen)
                    
        else:
            print("?")
            
        board.make_visible()
        print(board)
        
        if len(ships) == 0:
            break
            
def position_ships_random(ships, board):
    for ship in ships:
        for chosen in ships[ship]:
            placed = False
            while placed == False:
                directions = {0: 'up', 1: 'down', 2: 'left', 3: 'right'}
                startpos = (randint(0, 9), randint(0,9))
                going = directions[randint(0,3)]
       
                placed = board.set_piece(chosen, True, startpos, going)
                
    #board.make_visible()
    #print(board)
    
def attack_prompt(oppboard, cur_player):
    print("It's now {}'s turn".format(cur_player))
    done = False
    while not done:
        print("Check which tile?")
        inp = input("> ")
        
        if inp == "x" or inp == "exit":
            exit()
            
        pos = inputtopos(inp)
        
        if pos:
            if oppboard.board[pos[0]][pos[1]] != ".":
                print("You've already checked that tile!")
                
            else:
                hit = oppboard.findpiece(pos)
                
                if not hit:
                    oppboard.board[pos[0]][pos[1]] = "o"
                    
                else:
                    print("You hit something!")
                    hit.attacked()
                    oppboard.board[pos[0]][pos[1]] = "x"
                    
                done = True
    
        
comp = Player(0)        
one = Player(1)
players = [comp, one]
comp.num_o_pieces = 7
one.num_o_pieces = 99

compboard = BattleshipBoard()

destroyer1 = Destroyer(comp)
destroyer2 = Destroyer(comp)
submarine1 = Submarine(comp)
submarine2 = Submarine(comp)
carrier = Carrier(comp)
battleship = Battleshipship(comp)
cruiser = Cruiser(comp)

ships = { 'destroyer': [destroyer1, destroyer2], 'carrier': [carrier], 'submarine': [submarine1, submarine2], 'battleship': [battleship], 'cruiser': [cruiser] } 

print(compboard)
position_ships_random(ships, compboard)


""" Attacking test """
cur_player = 1
while True:
    attack_prompt(compboard, cur_player)
    print(compboard)
    winner = checkwin(players)
    if winner:
        break
    
print(compboard)
print("Player wins!")




