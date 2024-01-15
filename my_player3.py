from copy import deepcopy
   
def neighbours(row, col, currBoard):
    
    out=[]
    if row > 0:
        out.append((row-1, col))
    if col > 0:
        out.append((row, col-1))
    if row < len(currBoard) - 1:
        out.append((row+1, col))
    if col <len(currBoard) - 1:
        out.append((row, col+1))
    return out
        

def friendGroup(row, col, currBoard, player):
    
    to_visit=[(row, col)]
    friends=[]
    while (to_visit):
        val = to_visit.pop()
        if val not in friends:
            friends.append(val)
                                 
        ns = neighbours(val[0], val[1], currBoard)    
        for n in ns:            
            if currBoard[n[0]][n[1]] == player and n not in friends:
                to_visit.append((n[0], n[1]))
    return friends


def libertyOfGroup(row, col, currBoard, player):
    
    emptySpots=[]
    friends=friendGroup(row, col, currBoard, player)
    
    for f in friends:
        neighbour = neighbours(f[0], f[1], currBoard)
        for n in neighbour:
            if currBoard[n[0]][n[1]] == 0 and n not in emptySpots:
                emptySpots.append(n)
    return emptySpots


def removeCaptured(currBoard, player):
    
    remove=[]    
    for i in range(len(currBoard)):
        for j in range(len(currBoard)):
            if currBoard[i][j] == player:
                emptySpots = libertyOfGroup(i, j, currBoard, player)
                if not emptySpots and (i,j) not in remove:
                    remove.append((i,j))       
    for r in remove:
        currBoard[r[0]][r[1]] = 0
        
    return currBoard



def validMoves(prevBoard, currBoard, player):
    
    allMoves=[]
    opponent = 3 - player
       
    iterBoard = [(2,2),(2,1),(1,2),(2,3),(3,2),(1,1),(1,3),(3,1),(3,3),(2,0),(0,2),(2,4),(4,2),(1,0),(0,3),(3,4),(4,1),\
                  (3,0),(0,1),(1,4),(4,3),(0,0),(0,4),(4,4),(4,0)]   
    for b in iterBoard:
        if currBoard[b[0]][b[1]] == 0:
            allMoves.append((b[0],b[1]))
                           
    validMoves =[]
    for m in allMoves:
        copyCurrBoard = deepcopy(currBoard)
        
        copyCurrBoard[m[0]][m[1]] = player
        copyCurrBoard = removeCaptured(copyCurrBoard, opponent)
        
        suicideCurrBoard = deepcopy(currBoard)
        suicideCurrBoard[m[0]][m[1]] = player
        suicideCurrBoard = removeCaptured(suicideCurrBoard, opponent)
        
        suicideLiberty = removeCaptured(suicideCurrBoard, opponent)
        
        if not suicideLiberty:
            continue
        
        if copyCurrBoard != prevBoard:
            validMoves.append(m)
            
    return validMoves
  
    
def allLiberties(currBoard, player):
    
    allMoves=[]
    for i in range(len(currBoard)):
        for j in range(len(currBoard)):
            if currBoard[i][j] == player: 
                temp = libertyOfGroup(i, j, currBoard, player)
                for t in temp:
                    if t not in allMoves:
                        allMoves.append(t)
                        
    return len(allMoves)    

    
def evalFunction(currBoard, player):
    
    me = 0
    opp = 0
    for i in range(len(currBoard)):
        for j in range(len(currBoard)):
            if currBoard[i][j] != 0:
                
                if currBoard[i][j] == player:
                    me += 1
                else:
                    opp += 1
                    
    myLib = allLiberties(currBoard, player)
    oppLib = allLiberties(currBoard, 3-player)
                 
    if myPlayer == player:   
        return (me-opp)
    else:
        return -((me-opp))


def ABSearch(prevBoard, currBoard, depth, A, B, player):
        
    return Max(prevBoard, currBoard, depth, A, B, player)  
    
    
def Max(prevBoard, currBoard, depth, A, B, player):
        
    if depth == 0:
        return evalFunction(currBoard, player), None  
    
    Moves = validMoves(prevBoard, currBoard, player)    
    if not Moves:
        return 0, "PASS"
    
    bestMove = None
    v = -100000
    for m in Moves:
        nextState = deepcopy(currBoard)
        nextState[m[0]][m[1]] = player
        nextState = removeCaptured(nextState, 3-player)
        val = Min(currBoard, nextState, depth-1, A, B, 3-player)
        
        if val[0] > v:
            v = val[0]
            A = max(A, v)
            bestMove = m
            
        if A >= B:
            break
    return v, bestMove


    
def Min(prevBoard, currBoard, depth, A, B, player):
        
    if depth == 0:
        return evalFunction(currBoard, player), None  
    
    Moves = validMoves(prevBoard, currBoard, player)    
    if not Moves:
        return 0, "PASS"
    
    bestMove = None   
    v = 100000
    for m in Moves:
        nextState = deepcopy(currBoard)
        nextState[m[0]][m[1]] = player
        nextState = removeCaptured(nextState, 3-player)
        val = Max(currBoard, nextState, depth-1, A, B, 3-player)
        
        if val[0] < v:
            v = val[0]
            B = min(B, v)
            bestMove = m           
        if A >= B:
            break            
    return v, bestMove 


def readInput(n, path="input.txt"):

    with open(path, 'r') as f:
        lines = f.readlines()
        piece_type = int(lines[0])
        previous_board = [[int(x) for x in line.rstrip('\n')] for line in lines[1:n+1]]
        board = [[int(x) for x in line.rstrip('\n')] for line in lines[n+1: 2*n+1]]
        return piece_type, previous_board, board


def writeOutput(result, path="output.txt"):
    res = ""
    if result == "PASS":
        res = "PASS"
    else:
        res += str(result[0]) + ',' + str(result[1])
    with open(path, 'w') as f:
        f.write(res)
            

AllInput = readInput(5)
myPlayer,prevBoard,currBoard = AllInput[0], AllInput[1], AllInput[2]
move = ABSearch(prevBoard, currBoard, 2, -100000, 100000, myPlayer)
writeOutput(move[1])

        
        
        
        
        
        
        
