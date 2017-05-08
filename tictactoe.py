def setboard(pieces):
    board = "  a b c \nx " + pieces['ax'] + " " + pieces['bx'] + " "+ pieces['cx'] + "\ny " + pieces['ay'] + " " + pieces['by'] + " " + pieces['cy'] + "\nz " + pieces['az'] + " " + pieces['bz'] + " " + pieces['cz']
    
    return board

def resetpieces():
    pieces = {'ax': ".",
        'bx': ".",
        'cx': ".",
        'ay': ".",
        'by': ".",
        'cy': ".",
        'az': ".", 
        'bz': ".",
        'cz': "." }
        
    return pieces

def resetwins():
    wins = { 'a' : [0,0],
            'b' : [0,0],
            'c' : [0,0],
            'x' : [0,0],
            'y' : [0,0],
            'z' : [0,0],
            'd1' : [0,0],
            'd2' : [0,0] }
    return wins
    
def checkwin(wins):
    for win in wins:
        if wins[win][0] == 3:
            print(win, "=", wins[win][0], ":", wins[win][1])
            print("Player 1 wins!")
            return True
            
        elif wins[win][1] == 3:
            print(win, "=", wins[win][0], ":", wins[win][1])
            print("Player 2 wins!")
            return True
            
    return False
    
def checkfull(board):
    full = True
    for pos in board:
        if board[pos] == ".":
            full = False
    
    return full
    
def debug(wins, pieces, board):
    print("Here's the wins:")
    for win in wins:
        print(win, "=", wins[win])

wins = resetwins()
pieces = resetpieces()
board = setboard(pieces)
print(board)
l = None
player = 0

while l != "x" and l != "exit":
    if player == 0:
        print("Player 1's turn")
        l = input("x >")
        
    elif player == 1:
        print("Player 2's turn")
        l = input("o >")
    
    ## If move is valid
    if l in pieces:
    
        if pieces[l] != ".":
            print("Position already filled!")
            
        else:
            
            if player == 0:
                pieces[l] = "x"
            elif player == 1:
                pieces[l] = "o"
            
            wins[l[0]][player] += 1
            wins[l[1]][player] += 1 
            
            if l in ('ax', 'by', 'cz'):
                wins['d1'][player] += 1
            
            if l in ('cx', 'by', 'az'):
                wins['d2'][player] += 1
            
            board = setboard(pieces)
            
            # change player if move is valid
            if player == 0:
                player = 1
            else:
                player = 0
        
    ## Debug command
    elif l == "DEBUG":
        debug(wins, pieces, board)
        
    ## If move is invalid
    else:
        print("No such position!")
        
    ## Check if any win formation is made
    done = checkwin(wins)
    
    if done:
        board = setboard(pieces)
        print(board)
        print("\nStarting a new game...")
        
        wins = resetwins()
        pieces = resetpieces()
        board = setboard(pieces)
        
    elif checkfull(pieces):
        print("Tie!")
        board = setboard(pieces)
        print(board)
        print("\nStarting a new game...")
        
        wins = resetwins()
        pieces = resetpieces()
        board = setboard(pieces)
    
    print("")
    print(board)
    
    