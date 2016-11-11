from hlt import *
from networking import *

Raphael, gameMap = getInit()
sendInit("CaramelBot3")

while True:
    moves = []
    gameMap = getFrame()
    for y in range(gameMap.height):
        for x in range(gameMap.width):
            if gameMap.getSite(Location(x, y)).owner == Raphael:
                
                ready = False
                attack = False
                regroup = False
                move = False
                reinforce = False
                flip = 0
                surrounded = 0
                for d in CARDINALS:
                    if gameMap.getSite(Location(x, y), d).owner != Raphael:
                        surrounded +=1
                        
                if not ready and surrounded != 1 and gameMap.getSite(Location(x, y)).strength < 3*gameMap.getSite(Location(x, y)).production:
                    reinforce = True
                    ready = True
                
                if not ready:
                    if surrounded == 0:
                        move = True
                        ready = True
                    if surrounded == 1 or surrounded == 2 or surrounded == 4:
                        attack = True
                        ready = True
                    if surrounded == 3:
                        flip = int(random.random() * 8)
                        if flip:
                            attack = True
                        if not flip:
                            regroup = True
                        ready = True
                        
                if ready and attack:
                    for d in CARDINALS:
                        if gameMap.getSite(Location(x, y), d).owner != Raphael and gameMap.getSite(Location(x, y), d).strength < gameMap.getSite(Location(x, y)).strength:
                            moves.append(Move(Location(x, y), d))
                            ready = False
                        if ready:
                            reinforce = True
                if ready and regroup:
                    for d in CARDINALS:
                        if gameMap.getSite(Location(x, y), d).owner == Raphael:
                            moves.append(Move(Location(x, y), d))
                            ready = False
                if ready and move:
                    moves.append(Move(Location(x, y), 1+int(random.random() * 2)))
                    ready = False
                if ready and reinforce:
                    moves.append(Move(Location(x, y), STILL))
                    ready = False
    sendFrame(moves)
