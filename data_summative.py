from cProfile import label
from random import randint
import numpy as np
from numpy import roll
import matplotlib.pyplot as plt

import time


wins = [0, 0, 0, 0] # WINS FROM EACH PLAYER
total_duels = dict() # DUELS FROM ALL GAMES
total_rolls = dict() # DICE ROLLS ACROSS ALL GAMES
dice_prob = dict() # NUMBER OF WINS AND TOTAL NUMBER OF ROLLS IN DUELS FOR NUMBERS ON DICE (2-12)

for i in range(2, 13):
    dice_prob[i] = [0, 0] 

def ongoing(duels, pawns):
    count = 0
    
    max = 0
    winner = 0

    for i in pawns.keys():
        if pawns[i] <= 0: 
            count += 1
        if(duels[i][0] > max): # WINNER IS THE PLAYER WHO WON THE MOST DUELS (EACH DUEL WON = +1 CAPTURED PAWNS)
            max = duels[i][0]
            winner = i
    
    if count == 3: 
        wins[winner] += 1
        return False
    return True
        
def roll():
    x = randint(1, 6)
    if randint(0, 1): x *= -1 
    return x

def duel():
    return randint(1,6) + randint(1,6)

def scatter_plot(x, y, xlabel, ylabel, label=None, linestyle="-"):
    plt.scatter(x, y, label=label, linestyle=linestyle)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    # plt.show()

def plot(x, y, xlabel, ylabel, label=None, linestyle="-"):
    plt.plot(x, y, label=label, linestyle=linestyle)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    # plt.show()

def plot_dice_prob():
    x1 = [i for i in range(2, 13)]
    y1 = [dice_prob[i][1] for i in dice_prob.keys()]
    y2 = [dice_prob[i][0] for i in dice_prob.keys()]
    y3 = [(dice_prob[i][0]/dice_prob[i][1]) for i in dice_prob.keys()]
    # scatter_plot(x1, y1, "Roll Result", "Number of Rolls")
    # plot(x1, y2, "Roll Result", "Number of Duels Won", linestyle=":")
    # plt.show()

    fig, ax = plt.subplots()
    plt.title("Duel Statistics")
    ax.scatter(x1, y1, c="coral")
    ax.plot(np.unique(x1), np.poly1d(np.polyfit(x1, y1, 8))(np.unique(x1)), color="coral")
    # ax.plot(x1, y1, color="coral")
    ax.set_xlabel("Roll Result")
    ax.set_ylabel("Number of Rolls", color="coral")

    ax2 = ax.twinx()
    ax2.plot(x1, y3, linestyle = "--", color="cadetblue")
    ax2.set_ylabel("Probability of Winning Duel", color="cadetblue")

    plt.show()

def main():
    global num_pawns, positions, home_positions, pawns, wins, total_duels, total_rolls

    start = time.time()

    num_pawns = 3
    num = int(input("How many games?\n"))
    for r in range(num):
        print(f"-- GAME NUMBER: {r} -- \n")
        pawns = {
            0 : num_pawns,
            1: num_pawns,
            2: num_pawns,
            3: num_pawns,
        }   
        positions = [7, 11, 3, 15]
        home_positions = [7, 11, 3, 15]
        duels = [[0, 0], [0, 0], [0, 0], [0, 0]]
        num_rolls = 0

        while ongoing(duels, pawns):
            for i, x in enumerate(positions): # GO THROUGH CURRENT POSITIONS
                if pawns[i] <= 0: continue # IF PLAYER IS ELIMINATED, SKIP
                num_rolls += 1 
                dice_roll = roll() 
                # print(f"PLAYER {i} ROLLS {dice_roll}, from position {positions[i]} to position {[positions[i] + dice_roll , positions[i] + dice_roll - 16][positions[i] + dice_roll > 16]}")
                positions[i] = (positions[i] + dice_roll + 16) % 16 # MOVE PLAYER I 
                
                for j, v in enumerate(positions): # GO THROUGH POSITIONS OF ALL OTHER PLAYERS
                    if j == i or pawns[j] == 0: continue # IGNORE CURRENT PLAYER
                    
                    if positions[i] == v: # IF PLAYER I LANDS ON THE SAME SPOT AS ANOTHER PLAYER:
                        roll_1 = duel()
                        roll_2 = duel()
                        while roll_1 == roll_2:
                            roll_1 = duel() # ROLL FOR PLAYER I
                            roll_2 = duel() # ROLL FOR PLAYER J
                        # print(f"Player {i} and {j} fighting.\n Player {i}: {roll_1} \n Player {j}: {roll_2}")
                        
                        duels[i][1] += 1
                        duels[j][1] += 1

                        dice_prob[roll_1][1] += 1
                        dice_prob[roll_2][1] += 1
                        
                        if roll_1 > roll_2:
                            pawns[j] -= 1
                            duels[i][0] += 1
                            dice_prob[roll_1][0] += 1
                        else:
                            pawns[i] -= 1
                            duels[j][0] += 1
                            dice_prob[roll_2][0] += 1
                    
                for j, v in enumerate(home_positions): # CHECK IF PLAYER I IS ON ANOTHER PLAYERS HOMEBASE
                    if j == i or pawns[j] == 0 or pawns[i] == 0 or positions[j] == home_positions[j]: continue 
                    
                    if positions[i] == v:
                        roll_1 = duel()
                        roll_2 = duel()
                        while roll_1 == roll_2:
                            roll_1 = duel() # ROLL FOR PLAYER I
                            roll_2 = duel() # ROLL FOR PLAYER J
                        # print(f"Player {i} and {j} fighting.\n Player {i}: {roll_1} \n Player {j}: {roll_2}")
                        
                        duels[i][1] += 1
                        duels[j][1] += 1

                        dice_prob[roll_1][1] += 1
                        dice_prob[roll_2][1] += 1


                        if roll_1 > roll_2:
                            pawns[j] -= 1
                            duels[i][0] += 1
                            dice_prob[roll_1][0] += 1
                        else:
                            pawns[i] -= 1
                            duels[j][0] += 1
                            dice_prob[roll_2][0] += 1
                
                print(positions)
                print(pawns)

    
        total_duels[r] = duels
        total_rolls[r] = num_rolls
    
    end = time.time()

    print(wins)
    print(total_duels)
    print(total_rolls)
    print("\n\n")
    print(dice_prob)
    print("\n\n EXECUTION TIME:", end-start)
    plot_dice_prob()

if __name__ == '__main__':
    main()