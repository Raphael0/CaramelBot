from hlt import *
from networking import *

Raphael, gameMap = getInit()
sendInit("CaramelBot3")


movements = 0
prodN = 0
prodE = 0
prodS = 0
prodW = 0
prodD = 0
flip = 0
earlyGame = True
midGame = False
midLateGame = False
lateGame = False
prodScanRange = 3
moveScanRange = 12

def runInitProdScan():
    "Initial scan for production rates around first square"
    for i in range(1,12):
        prod = 0
        direction = 0
        if y < i:
            if gameMap.getSite(Location(x, y-i+gameMap.height)).production >= prod:
                prod = gameMap.getSite(Location(x, y-i+gameMap.height)).production
                direction = 1
        if y > i:
            if gameMap.getSite(Location(x, y-i)).production >= prod:
                prod = gameMap.getSite(Location(x, y-i)).production
                direction = 1
        if x > gameMap.width-i:
            if gameMap.getSite(Location(x+i-gameMap.width, y)).production >= prod:
                prod = gameMap.getSite(Location(x+i-gameMap.width, y)).production
                direction = 2
        if x < gameMap.width-i:
            if gameMap.getSite(Location(x+i, y)).production >= prod:
                prod = gameMap.getSite(Location(x+i, y)).production
                direction = 2
        if y > gameMap.height-i:
            if gameMap.getSite(Location(x, y+i-gameMap.height)).production >= prod:
                prod = gameMap.getSite(Location(x, y+i-gameMap.height)).production
                direction = 3
        if y < gameMap.height-i:
            if gameMap.getSite(Location(x, y+i)).production >= prod:
                prod = gameMap.getSite(Location(x, y+i)).production
                direction = 3
        if x < i:
            if gameMap.getSite(Location(x-i+gameMap.width, y)).production >= prod:
                prod = gameMap.getSite(Location(x-i+gameMap.width, y)).production
                direction = 4   
        if x > i:
            if gameMap.getSite(Location(x-i, y)).production >= prod:
                prod = gameMap.getSite(Location(x-i, y)).production
                direction = 4
    return direction

def runAttackProdD():
    "Attack prodD if weak enough"
    "Stay undecided if prodD enemy too strong"
    global decided
    if gameMap.getSite(Location(x, y), prodD).owner != Raphael and gameMap.getSite(Location(x, y), prodD).strength < gameMap.getSite(Location(x, y)).strength:
        moves.append(Move(Location(x, y), prodD))
        decided = True
def runAttack():
    "Attack nearby(1) enemies if stronger, first check proD then CARDINALS"
    "Stay undecided if no weak enemy found"
    global decided
    if gameMap.getSite(Location(x, y), prodD).owner != Raphael and gameMap.getSite(Location(x, y), prodD).strength < gameMap.getSite(Location(x, y)).strength:
        moves.append(Move(Location(x, y), prodD))
        decided = True
    else:
        for d in CARDINALS:
            if gameMap.getSite(Location(x, y), d).owner != Raphael and gameMap.getSite(Location(x, y), d).strength < gameMap.getSite(Location(x, y)).strength:
                moves.append(Move(Location(x, y), d))
                decided = True
                break
    return

def runMove():
    "Move away from allied territory. If border too far away, move randomly"
    "Always decided"
    global decided
    global movements
    for i in range(1,moveScanRange):
        if y < i:
            if gameMap.getSite(Location(x, y-i+gameMap.height)).owner != Raphael:
                moves.append(Move(Location(x, y), NORTH))
                decided = True
                break
        if y > i:
            if gameMap.getSite(Location(x, y-i)).owner != Raphael:
                moves.append(Move(Location(x, y), NORTH))
                decided = True
                break
        if x > gameMap.width-i:
            if gameMap.getSite(Location(x+i-gameMap.width, y)).owner != Raphael:
                moves.append(Move(Location(x, y), EAST))
                decided = True
                break
        if x < gameMap.width-i:
            if gameMap.getSite(Location(x+i, y)).owner != Raphael:
                moves.append(Move(Location(x, y), EAST))
                decided = True
                break
        if y > gameMap.height-i:
            if gameMap.getSite(Location(x, y+i-gameMap.height)).owner != Raphael:
                moves.append(Move(Location(x, y), SOUTH))
                decided = True
                break
        if y < gameMap.height-i:
            if gameMap.getSite(Location(x, y+i)).owner != Raphael:
                moves.append(Move(Location(x, y), SOUTH))
                decided = True
                break
        if x < i:
            if gameMap.getSite(Location(x-i+gameMap.width, y)).owner != Raphael:
                moves.append(Move(Location(x, y), WEST))
                decided = True
                break    
        if x > i:
            if gameMap.getSite(Location(x-i, y)).owner != Raphael:
                moves.append(Move(Location(x, y), WEST))
                decided = True
                break
    if not decided:
        moves.append(Move(Location(x, y), int(random.random() * 3)))
        decided = True
    movements += 1
        
def runRegroup():
    "Join nearby(1) ally, check CARDINALS"
    "Stay undecided if nearby allies too weak"
    global decided
    for d in CARDINALS:
        if gameMap.getSite(Location(x, y), d).owner == Raphael and 2*gameMap.getSite(Location(x, y), d).strength > gameMap.getSite(Location(x, y)).strength:
            moves.append(Move(Location(x, y), d))
            decided = True
            break

def runReinforce():
    "Stay still"
    "Always decided"
    global decided
    moves.append(Move(Location(x, y), STILL))
    decided = True
    return
    
def runExpand():
    "Normal attack avoiding fields with zero production"
    "Stay undecided if nearby enemies too strong"
    global decided
    for d in CARDINALS:
        if gameMap.getSite(Location(x, y), d).owner != Raphael and gameMap.getSite(Location(x, y), d).strength < gameMap.getSite(Location(x, y)).strength and gameMap.getSite(Location(x, y), d).production != 0:
            moves.append(Move(Location(x, y), d))
            decided = True
            break
        
def runCheckProdD():
    global prodN
    global prodE
    global prodS
    global prodW
    global prodD
    global prodDCheck
    for i in range(1,prodScanRange):
        if y < i:
            prodN += gameMap.getSite(Location(x, y-i+gameMap.height)).production
        if y > i:
            prodN += gameMap.getSite(Location(x, y-i)).production
        if x > gameMap.width-i:
            prodE += gameMap.getSite(Location(x+i-gameMap.width, y)).production 
        if x < gameMap.width-i:
            prodE += gameMap.getSite(Location(x+i, y)).production
        if y > gameMap.height-i:
            prodS += gameMap.getSite(Location(x, y+i-gameMap.height)).production
        if y < gameMap.height-i:
            prodS += gameMap.getSite(Location(x, y+i)).production
        if x < i:
            prodW += gameMap.getSite(Location(x-i+gameMap.width, y)).production    
        if x > i:
            prodW += gameMap.getSite(Location(x-i, y)).production
    if prodN == max(prodN,prodE,prodS,prodW):
        prodD = 1
    if prodE == max(prodN,prodE,prodS,prodW):
        prodD = 2
    if prodS == max(prodN,prodE,prodS,prodW):
        prodD = 3
    if prodW == max(prodN,prodE,prodS,prodW):
        prodD = 4
    prodDCheck = True

while True:
    moves = []
    gameMap = getFrame()
    for y in range(gameMap.height):
        for x in range(gameMap.width):
            if gameMap.getSite(Location(x, y)).owner == Raphael:

                surrounded = 0
                prodDCheck = False
                decided = False
                
                if 16000 <= movements < 20000:
                    midGame = True
                    earlyGame = False
                    prodScanRange = 2
                    moveScanRange = 8
                    
                if 20000 <= movements < 25000:
                    midLateGame = True
                    midGame = False
                    prodScanRange = 1
                    moveScanRange = 5
                       
                if 25000 <= movements <= 29000:
                    lateGame = True
                    midLateGame = False
                    prodScanRange = 1
                    moveScanRange = 2
                    
                if movements >= 29000:
                    endGame = True
                    lateGame = False
                    for d in CARDINALS:
                        if gameMap.getSite(Location(x, y), d).owner != Raphael:
                            surrounded += 1
                    if surrounded == 0:
                        moves.append(Move(Location(x, y), int(random.random() * 3)))
                        decided = True
                    if undecided:
                        runAttack()
                    if undecided:
                        runReinforce()
                        
                    
                if not decided:
                    for d in CARDINALS:
                        if gameMap.getSite(Location(x, y), d).owner != Raphael:
                            surrounded += 1
                 
                if not decided and gameMap.getSite(Location(x, y)).strength > 255-gameMap.getSite(Location(x, y)).production:
                    if not prodDCheck and lateGame == False:
                        runCheckProdD()
                    if not lateGame:
                        runAttackProdD()
                    if not decided:
                        runMove()
                
                if not decided:
                    if surrounded == 0:
                        if maxProduction <= 5:
                            if gameMap.getSite(Location(x, y)).production <= 1:
                                if gameMap.getSite(Location(x, y)).strength < 2*gameMap.getSite(Location(x, y)).production:
                                    runReinforce()
                            elif 3 <= gameMap.getSite(Location(x, y)).production <= 2:
                                if gameMap.getSite(Location(x, y)).strength < 3*gameMap.getSite(Location(x, y)).production:
                                    runReinforce()
                            elif 5 <= gameMap.getSite(Location(x, y)).production <= 3:
                                if gameMap.getSite(Location(x, y)).strength < 4*gameMap.getSite(Location(x, y)).production:
                                    runReinforce()
                            elif 7 <= gameMap.getSite(Location(x, y)).production <= 4:
                                if gameMap.getSite(Location(x, y)).strength < 6*gameMap.getSite(Location(x, y)).production:
                                    runReinforce()
                            elif gameMap.getSite(Location(x, y)).production >=5:
                                if gameMap.getSite(Location(x, y)).strength < 7*gameMap.getSite(Location(x, y)).production:
                                    runReinforce()
                            if not decided:
                                runMove()
                        if maxProduction <= 10:
                            if gameMap.getSite(Location(x, y)).production <= 2:
                                if gameMap.getSite(Location(x, y)).strength < 3*gameMap.getSite(Location(x, y)).production:
                                    runReinforce()
                            elif 3 <= gameMap.getSite(Location(x, y)).production <= 4:
                                if gameMap.getSite(Location(x, y)).strength < 4*gameMap.getSite(Location(x, y)).production:
                                    runReinforce()
                            elif 5 <= gameMap.getSite(Location(x, y)).production <= 6:
                                if gameMap.getSite(Location(x, y)).strength < 5*gameMap.getSite(Location(x, y)).production:
                                    runReinforce()
                            elif 7 <= gameMap.getSite(Location(x, y)).production <= 8:
                                if gameMap.getSite(Location(x, y)).strength < 6*gameMap.getSite(Location(x, y)).production:
                                    runReinforce()
                            elif gameMap.getSite(Location(x, y)).production >=10:
                                if gameMap.getSite(Location(x, y)).strength < 7*gameMap.getSite(Location(x, y)).production:
                                    runReinforce()
                            if not decided:
                                runMove()
                        if maxProduction >= 10:
                            if gameMap.getSite(Location(x, y)).production <= 2:
                                if gameMap.getSite(Location(x, y)).strength < 2*gameMap.getSite(Location(x, y)).production:
                                    runReinforce()
                            elif 3 <= gameMap.getSite(Location(x, y)).production <= 5:
                                if gameMap.getSite(Location(x, y)).strength < 4*gameMap.getSite(Location(x, y)).production:
                                    runReinforce()
                            elif 5 <= gameMap.getSite(Location(x, y)).production <= 8:
                                if gameMap.getSite(Location(x, y)).strength < 5*gameMap.getSite(Location(x, y)).production:
                                    runReinforce()
                            elif 7 <= gameMap.getSite(Location(x, y)).production <= 11:
                                if gameMap.getSite(Location(x, y)).strength < 6*gameMap.getSite(Location(x, y)).production:
                                    runReinforce()
                            if not decided:
                                runMove()
                        
                    if surrounded == 1 or surrounded == 2:
                        flip = int(random.random() * 3)
                        if flip:
                            if not prodDCheck and lateGame == False:
                                runCheckProdD()
                            if not lateGame:
                                runAttackProdD
                            if not decided:
                                runAttack()
                        if not flip:
                            for d in CARDINALS:
                                if gameMap.getSite(Location(x, y), d).owner == Raphael and 0.9*gameMap.getSite(Location(x, y), d).strength < gameMap.getSite(Location(x, y)).strength < gameMap.getSite(Location(x, y), d).strength*1.1:
                                    moves.append(Move(Location(x, y), d))
                                    decided = True
                                    break
                            if not decided and lateGame == False:
                                runAttackProdD
                            if not decided:
                                runAttack()
                        
                    if surrounded == 3:
                        if not prodDCheck and lateGame == False:
                            runCheckProdD()
                        if not lateGame:
                            runAttackProdD
                        if not decided:
                            runAttack()
                        if not decided:
                            flip = int(random.random() * 6)
                            if flip:
                                runReinforce()
                            if not flip:
                                for d in CARDINALS:
                                    if gameMap.getSite(Location(x, y), d).owner != Raphael and gameMap.getSite(Location(x, y), d).strength < gameMap.getSite(Location(x, y)).strength+gameMap.getSite(Location(x, y)).production:
                                        runReinforce()
                                    else:
                                        runRegroup()
                                        if not decided:
                                            runReinforce()
                                            
                    if surrounded == 4:
                        maxProduction = runInitProdScan()
                        if not prodDCheck:
                            runCheckProdD()
                        runAttackProdD()
                        if not decided:
                            runExpand()
                        if not decided:
                            runReinforce()
    sendFrame(moves)
    
    
"add late-game mode, reducing number of checks and focusing on Moving (range 5) and semi random movement"
"add regroup for similar strength levels"