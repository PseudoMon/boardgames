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
from copy import deepcopy

class BattleshipBoard(Board):
    def __init__(self, pieces=[]):
        super(BattleshipBoard, self).__init__((10, 10), pieces)
        self.atk_board = deepcopy(self.board)
        
    def stratkboard(self):
        boardstr = " \n"
        
        # Header nums
        boardstr += "  "
        for col in range(self.size[1]):
            boardstr += str(col)
        boardstr += "\n"
            
        rownum = 0
        
        for row in self.atk_board:
            boardstr += str(rownum) + " "
            rownum += 1
            
            for col in row:
                boardstr += col
                
            boardstr += "\n"
        return boardstr
        
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
            
    def make_visible(self, atk_board=False):
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
        board = None
        
    def setup_board(self, randompos=True):
        self.num_o_pieces = 7
        self.board = BattleshipBoard([])
        # I've no idea why, but not setting empty list here will fuck up everything
        
        destroyer1 = Destroyer(self)
        destroyer2 = Destroyer(self)
        submarine1 = Submarine(self)
        submarine2 = Submarine(self)
        carrier = Carrier(self)
        battleship = Battleshipship(self)
        cruiser = Cruiser(self)
        
        ships = { 'destroyer': [destroyer1, destroyer2], 'carrier': [carrier], 'submarine': [submarine1, submarine2], 'battleship': [battleship], 'cruiser': [cruiser] } 
        
        if randompos:
            position_ships_random(ships, self.board)
        else:
            position_ships(ships, self.board)
        
        self.board.make_visible()
        

def position_ships(ships, board):
    inp = None
    print(board)
    while True:
        print("These are the ships you can position:")
        for ship in ships:
            print("{}x {} (size {})".format(len(ships[ship]), ships[ship][0].name, ships[ship][0].hp))
            
        inp = input("> ")
        inp = inp.lower()
        
        if inp == "x" or inp == "exit":
            exit()
        
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

    
def attack_prompt(oppboard, cur_player):
    print("It's now Player {}'s turn".format(cur_player))
    done = False
    while not done:
        pos = None
        print("Address of position to attack?")
        inp = input("> ")
        
        if inp == "x" or inp == "exit":
            exit()
            
        elif inp == "check my ships":
            print(cur_player.board)
            
        elif inp == "check attack grid":
            print(oppboard.stratkboard())
            
        elif inp == "help":
            printhelp()
            
        else:
            pos = inputtopos(inp)
        
        if pos:
            if oppboard.atk_board[pos[0]][pos[1]] != ".":
                print("You've already checked that tile!")
                
            else:
                hit = oppboard.findpiece(pos)
                
                if not hit:
                    oppboard.atk_board[pos[0]][pos[1]] = "o"
                    oppboard.board[pos[0]][pos[1]] = "o"
                    
                else:
                    print("You hit something!")
                    hit.attacked()
                    oppboard.atk_board[pos[0]][pos[1]] = "x"
                    oppboard.board[pos[0]][pos[1]] = "A"
                    
                done = True

def random_attack(oppboard):
    done = False

    while not done:
        pos = (randint(0, 9), randint(0,9))
        if oppboard.atk_board[pos[0]][pos[1]] != ".":
                pass
        else:
            hit = oppboard.findpiece(pos)
            if not hit:
                print("The computer hits nothing!")
                oppboard.atk_board[pos[0]][pos[1]] = "o"
                oppboard.board[pos[0]][pos[1]] = "o"
                
            else:
                print("The computer hits something!")
                hit.attacked()
                oppboard.atk_board[pos[0]][pos[1]] = "x"
                oppboard.board[pos[0]][pos[1]] = "A"
               
            done = True
                
def printhelp():
    print("\nHelp\nDo not look at another player's turn!")
    print("\nType in the address of the location you'd like to attack.")
    print("Ex: [09] will attack the topmost-rightmost tile.")
    print("\nType [check my ships] to see the position of your ships. (Do not let the other player see this)")
    print("\nType [check attack grid] to see your attack grid again.")
    print("\nIn your ship's grid, [x] is your ship, [o] is where your opponent has ataccked and missed. [A] is the part of your ship that's damaged.")
    print("In your attack grid, [o] is where you missed, [x] is where you got a hit.")
    print("\nType [x] or [exit] to exit the game.")
    print("")
    return
    

        
one = BattleshipPlayer(1)        
two = BattleshipPlayer(2)
players = [one, two]
twoiscomp = False

print("Welcome to Battleship")
print("This game should be played alternatively by two players.")
print("Type [help] for instructions.")

print("Versus [player] or [comp]uter?")
while True:
    inp = input("player/comp > ")
    if inp == "comp":
        twoiscomp = True
        break
    elif inp == "player":
        break
        
if not twoiscomp:
    print("\nPlayer 2, don't look!\n")
print("Player 1! \nWould you like to position your ships yourself? (Random otherwisse)")
inp = input("y/n > ")

if inp.lower() == "y":
    one.setup_board(False)
else:
    one.setup_board(True)
    
if not twoiscomp:
    print("\nPlayer 1, don't look!\n")
    print("Player 2! \nWould you like to position your ships yourself? (Random otherwise)")
    inp = input("y/n >")

    if inp.lower() == "y":
        two.setup_board(False)
    else:
        two.setup_board(True)
else:
    two.setup_board()

print("\nBeginning game!")

while True:
    # One's turn
    print(two.board.stratkboard())
    attack_prompt(two.board, one)
    #print(two.board.stratkboard())
    
    winner = checkwin(players)
    if winner:
        break
    
    # Two's turn
    if twoiscomp:
        print("\nComputer is attacking...")
        random_attack(one.board)
    else:
        print(one.board.stratkboard())
        attack_prompt(one.board, two)
        print(one.board.stratkboard())
    
    winner = checkwin(players)
    if winner:
        break
    
print("Player one's board:")
print(one.board)
print("Player two's board:")
print(two.board)
print("Player {} wins!".format(winner))
