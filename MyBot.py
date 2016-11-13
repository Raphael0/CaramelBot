from hlt import *
from networking import *

myID, gameMap = getInit()
sendInit("MyPythonBot")
from hlt import *
from networking import *

Raphael, gameMap = getInit()
sendInit("CaramelBot3")

counter = 0
def runAttackProdD():
    "Attack prodD if weak enough"
    "Stay undecided if prodD too strong"
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
    for i in range(1,10):
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
        
def runRegroup():
    "Join nearby(1) ally, check CARDINALS"
    "Always decided"
    global decided
    for d in CARDINALS:
        if gameMap.getSite(Location(x, y), d).owner == Raphael:
            moves.append(Move(Location(x, y), d))
            decided = True

def runReinforce():
    "Stay still"
    "Always decided"
    global decided
    moves.append(Move(Location(x, y), STILL))
    decided = True
    return

while True:
    moves = []
    gameMap = getFrame()
    for y in range(gameMap.height):
        for x in range(gameMap.width):
            if gameMap.getSite(Location(x, y)).owner == Raphael:
                
                counter += 1
                decided = False
                flip = 0
                surrounded = 0
                prodN = 0
                prodE = 0
                prodS = 0
                prodW = 0
                prodD = 0
                for d in CARDINALS:
                    if gameMap.getSite(Location(x, y), d).owner != Raphael:
                        surrounded += 1
                for i in range(1,3):
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
 
                if not decided and gameMap.getSite(Location(x, y)).strength > 255-gameMap.getSite(Location(x, y)).production:
                    runAttackProdD()
                    if not decided:
                        runMove()
                
                if not decided:
                    if surrounded == 0:
                        if gameMap.getSite(Location(x, y)).production <= 2:
                            if gameMap.getSite(Location(x, y)).strength < 2*gameMap.getSite(Location(x, y)).production:
                                runReinforce()
                        if 3 <= gameMap.getSite(Location(x, y)).production <= 4:
                            if gameMap.getSite(Location(x, y)).strength < 3*gameMap.getSite(Location(x, y)).production:
                                runReinforce()
                        if 5 <= gameMap.getSite(Location(x, y)).production <= 6:
                            if gameMap.getSite(Location(x, y)).strength < 4*gameMap.getSite(Location(x, y)).production:
                                runReinforce()
                        if gameMap.getSite(Location(x, y)).production >=7:
                            if gameMap.getSite(Location(x, y)).strength < 5*gameMap.getSite(Location(x, y)).production:
                                runReinforce()
                        else:
                            runMove()
                    if surrounded == 1 or surrounded == 2:
                        runAttack()
                    if surrounded == 3:
                        runAttack()
                        if not decided:
                            flip = int(random.random() * 7)
                            if flip:
                                runReinforce()
                            if not flip:
                                for d in CARDINALS:
                                    if gameMap.getSite(Location(x, y), d).owner != Raphael and gameMap.getSite(Location(x, y), d).strength < gameMap.getSite(Location(x, y)).strength+gameMap.getSite(Location(x, y)).production:
                                        runReinforce()
                                    else:
                                        runRegroup()
                    if surrounded == 4:
                        runAttackProdD()
                        if not decided:
                            flip = int(random.random() * 5)
                            if flip:
                                runAttack()
                                if not decided:
                                    runReinforce()
                            if not flip:
                                moves.append(Move(Location(x, y), prodD))
                                decided = True
    sendFrame(moves)
while True:
    moves = []
    gameMap = getFrame()
    for y in range(gameMap.height):
        for x in range(gameMap.width):
            if gameMap.getSite(Location(x, y)).owner == myID:
                moves.append(Move(Location(x, y), int(random.random() * 5)))
    sendFrame(moves)
