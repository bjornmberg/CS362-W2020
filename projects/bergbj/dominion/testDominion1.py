# -*- coding: utf-8 -*-
# Edited by: Bjorn Berg
# Last Edited: 1/14/20

import Dominion
import random
from collections import defaultdict
import testUtility

#Define player names
player_names = testUtility.PlayerNames()

#number of curses and victory cards
if len(player_names)>2:
    nV = 12
else:
    nV = 8
nC = -10 + 10 * len(player_names)

#Define box
box = testUtility.GetBoxes(nV)

# Define the supply order
supply_order = testUtility.SupplyOrder()

#Pick 10 cards from box to be in the supply.
# Bug: introduce 11 cards
boxlist = [k for k in box]
random.shuffle(boxlist)
random10 = boxlist[:11]
supply = defaultdict(list,[(k,box[k]) for k in random10])


# Define the cards that supply always has
supply = testUtility.SupplyAlwaysHas(supply, player_names, nV, nC)

#initialize the trash
trash = []

#Costruct the Player objects
players = testUtility.PlayerConstruction(player_names)

#Play the game
turn  = 0
while not Dominion.gameover(supply):
    turn += 1    
    print("\r")    
    for value in supply_order:
        print (value)
        for stack in supply_order[value]:
            if stack in supply:
                print (stack, len(supply[stack]))
    print("\r")
    for player in players:
        print (player.name,player.calcpoints())
    print ("\rStart of turn " + str(turn))    
    for player in players:
        if not Dominion.gameover(supply):
            print("\r")
            player.turn(players,supply,trash)
            

#Final score
dcs=Dominion.cardsummaries(players)
vp=dcs.loc['VICTORY POINTS']
vpmax=vp.max()
winners=[]
for i in vp.index:
    if vp.loc[i]==vpmax:
        winners.append(i)
if len(winners)>1:
    winstring= ' and '.join(winners) + ' win!'
else:
    winstring = ' '.join([winners[0],'wins!'])

print("\nGAME OVER!!!\n"+winstring+"\n")
print(dcs)
