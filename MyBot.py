from hlt import *
from networking import *

Raphael, gameMap = getInit()
sendInit("CaramelBot3")

counter = 0

while True:
    moves = []
    gameMap = getFrame()
    for y in range(gameMap.height):
        for x in range(gameMap.width):
            if gameMap.getSite(Location(x, y)).owner == Raphael:
                
                counter += 1
                ready = False
                attack = False
                regroup = False
                move = False
                expand = False
                reinforce = False
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
                for i in range(1,4):
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

                if not ready and surrounded != 1 and surrounded != 4 and gameMap.getSite(Location(x, y)).strength < 3*gameMap.getSite(Location(x, y)).production:
                    reinforce = True
                    ready = True    
                if not ready and gameMap.getSite(Location(x, y)).strength > 255-gameMap.getSite(Location(x, y)).production:
                    move = True
                    ready = True
                
                if not ready:
                    if surrounded == 0:
                        move = True
                        ready = True
                    if surrounded == 1 or surrounded == 2:
                        attack = True
                        ready = True
                    if surrounded == 3:
                        flip = int(random.random() * 7)
                        if flip:
                            attack = True
                        if not flip:
                            regroup = True
                        ready = True
                    if surrounded == 4:
                        expand = True
                        ready = True
                        
                if ready and attack:
                    if gameMap.getSite(Location(x, y), prodD).owner != Raphael and gameMap.getSite(Location(x, y), prodD).strength < gameMap.getSite(Location(x, y)).strength:
                                moves.append(Move(Location(x, y), prodD))
                                ready = False
                                break
                    for d in CARDINALS:
                        if gameMap.getSite(Location(x, y), d).owner != Raphael and gameMap.getSite(Location(x, y), d).strength < gameMap.getSite(Location(x, y)).strength:
                            moves.append(Move(Location(x, y), d))
                            ready = False
                            break
                    if ready:
                        reinforce = True
                        ready = False
                if ready and regroup:
                    if gameMap.getSite(Location(x, y), prodD).owner != Raphael and gameMap.getSite(Location(x, y), prodD).strength < gameMap.getSite(Location(x, y)).strength:
                                moves.append(Move(Location(x, y), prodD))
                                ready = False
                                break
                    for d in CARDINALS:
                        if gameMap.getSite(Location(x, y), d).owner != Raphael and gameMap.getSite(Location(x, y), d).strength < gameMap.getSite(Location(x, y)).strength:
                            moves.append(Move(Location(x, y), d))
                            ready = False
                            break
                    if ready:
                        for d in CARDINALS:
                            if gameMap.getSite(Location(x, y), d).owner == Raphael:
                                moves.append(Move(Location(x, y), d))
                                ready = False
                if ready and move:
                    for i in range(1,10):
                        if y < i:
                            if gameMap.getSite(Location(x, y-i+gameMap.height)).owner != Raphael:
                                moves.append(Move(Location(x, y), NORTH))
                                ready = False
                                break
                        if y > i:
                            if gameMap.getSite(Location(x, y-i)).owner != Raphael:
                                moves.append(Move(Location(x, y), NORTH))
                                ready = False
                                break
                        if x > gameMap.width-i:
                            if gameMap.getSite(Location(x+i-gameMap.width, y)).owner != Raphael:
                                moves.append(Move(Location(x, y), EAST))
                                ready = False
                                break 
                        if x < gameMap.width-i:
                            if gameMap.getSite(Location(x+i, y)).owner != Raphael:
                                moves.append(Move(Location(x, y), EAST))
                                ready = False
                                break
                        if y > gameMap.height-i:
                            if gameMap.getSite(Location(x, y+i-gameMap.height)).owner != Raphael:
                                moves.append(Move(Location(x, y), SOUTH))
                                ready = False
                                break
                        if y < gameMap.height-i:
                            if gameMap.getSite(Location(x, y+i)).owner != Raphael:
                                moves.append(Move(Location(x, y), SOUTH))
                                ready = False
                                break
                        if x < i:
                            if gameMap.getSite(Location(x-i+gameMap.width, y)).owner != Raphael:
                                moves.append(Move(Location(x, y), WEST))
                                ready = False
                                break    
                        if x > i:
                            if gameMap.getSite(Location(x-i, y)).owner != Raphael:
                                moves.append(Move(Location(x, y), WEST))
                                ready = False
                                break
                    if ready:
                        moves.append(Move(Location(x, y), int(random.random() * 2)))
                        ready = False
                if ready and expand:
                    if gameMap.getSite(Location(x, y), prodD).owner != Raphael and gameMap.getSite(Location(x, y), prodD).strength < gameMap.getSite(Location(x, y)).strength:
                                moves.append(Move(Location(x, y), prodD))
                                ready = False
                                break
                    if ready:
                        flip = int(random.random() * 5)
                        if flip:
                            for d in CARDINALS:
                                if gameMap.getSite(Location(x, y), d).owner != Raphael and gameMap.getSite(Location(x, y), d).strength < gameMap.getSite(Location(x, y)).strength:
                                    moves.append(Move(Location(x, y), d))
                                    ready = False
                                    break
                        if not flip:
                            moves.append(Move(Location(x, y), prodD))
                            ready = False
                if ready and reinforce:
                    moves.append(Move(Location(x, y), STILL))
                    ready = False
    sendFrame(moves)
