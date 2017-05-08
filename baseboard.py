class Piece:
    def __init__(self, startpos=(0,0), player=0):
        #player should be a Player object
        self.player = player
        self.row = startpos[0]
        self.col = startpos[1]
        
        try:
            self.symbol = player.symbol
        except AttributeError:
            print("Player for a piece is not a player object!")
            self.symbol = "x"
        
    def __str__(self):
        return self.symbol
        
    def move_to_pos(self, topos):
        self.row = topos[0]
        self.col = topos[1]
        return
        
        
class Board:
    def __init__(self, size, pieces=[]):
        self.board = [["." for x in range(size[0])] for y in range(size[1])]
        self.size = size
        self.pieces = pieces
   
    def __str__(self):
        boardstr = " \n"
        
        # Header nums
        boardstr += "  "
        for col in range(self.size[1]):
            boardstr += str(col)
        boardstr += "\n"
            
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
        self.set_piece(piece)
        
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
        
        
class Player:
    def __init__(self, ord, symbol='o'):
        self.ord = ord
        self.num_o_pieces = 0
        self.symbol = symbol
       
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
            
            if len(players) == 1:
                return players[0]
    return None

    
def swapplayer(current_player, players=[1,2]):

    # players should be a list containing 
    # the order of all players
    if isinstance(players[0], Player):
        players = [x.ord for x in players]
        
    # Change current_player to the next in the list
    # or restart from the beginning 
    # if all the players have moved
    i = 0
    while i < len(players):
        if players[i] == current_player:
        
            try:
                current_player = players[i+1]
            except IndexError:
                current_player = players[0]
                
            break
        i += 1
        
    return current_player
