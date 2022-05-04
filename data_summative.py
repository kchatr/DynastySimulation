import random as rand
from random import randint
import numpy as np
from numpy import roll
import matplotlib
import matplotlib.pyplot as plt

import time


wins = [0, 0, 0, 0] # WINS FROM EACH PLAYER
total_duels = dict() # DUELS FROM ALL GAMES
total_rolls = dict() # DICE ROLLS ACROSS ALL GAMES
dice_prob = dict() # NUMBER OF WINS AND TOTAL NUMBER OF ROLLS IN DUELS FOR NUMBERS ON DICE (2-12)
total_duel_rolls = [] # APPEND DUEL ROLLS TO LIST; USED FOR HISTOGRAM (O(n))
player_stats = dict()

for i in range(2, 13):
    dice_prob[i] = [0, 0] 

for i in range(0, 4):
    player_stats[i] = [0, 0, 0, 0] # WINS; NO. OF DUELS WON IN WINNING GAMES; NO. OF TOTAL DUELS IN WINNING GAMES; TOTAL DUELS ACROSS ALL GAMES

def ongoing(duels, pawns):
    global player_stats
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
        player_stats[winner][0] += 1
        player_stats[winner][1] += duels[winner][0]
        player_stats[winner][2] += duels[winner][1]
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

def plot_dice_prob(sims):
    x1 = [i for i in range(2, 13)]
    y1 = [dice_prob[i][1] for i in dice_prob.keys()]
    y2 = [dice_prob[i][0] for i in dice_prob.keys()]
    y3 = [(dice_prob[i][0]/dice_prob[i][1]) for i in dice_prob.keys()]
    # scatter_plot(x1, y1, "Roll Result", "Number of Rolls")
    # plot(x1, y2, "Roll Result", "Number of Duels Won", linestyle=":")
    # plt.show()

    fig, ax = plt.subplots()
    plt.title(f"Duel Statistics for {sims} Simulations")
    ax.scatter(x1, y1, c="coral")
    ax.plot(np.unique(x1), np.poly1d(np.polyfit(x1, y1, 8))(np.unique(x1)), color="coral")
    # ax.plot(x1, y1, color="coral")
    ax.set_xlabel("Roll")
    ax.set_ylabel("Number of Rolls", color="coral")

    ax2 = ax.twinx()
    ax2.plot(x1, y3, linestyle = "--", color="cadetblue")
    ax2.set_ylabel("Probability of Winning Duel", color="cadetblue")

    plt.show()

    plt.title(f"Duel Roll Distribution for {sims} Simulations")
    plt.xlabel("Roll")
    sns.histplot(total_duel_rolls, bins=11, kde=True, discrete=True, color="rebeccapurple", kde_kws={"bw_adjust":2})
    plt.show()

def main():
    global num_pawns, positions, home_positions, pawns, wins, total_duels, total_rolls, total_duel_rolls

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
        rand.shuffle(positions)
        home_positions = [7, 11, 3, 15]
        duels = [[0, 0], [0, 0], [0, 0], [0, 0]]
        num_rolls = 0

        print(positions)

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

                        total_duel_rolls.append(roll_1)
                        total_duel_rolls.append(roll_2)

                        duels[i][1] += 1
                        duels[j][1] += 1

                        player_stats[i][3] += 1
                        player_stats[j][3] += 1

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
                        total_duel_rolls.append(roll_1)
                        total_duel_rolls.append(roll_2)

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
                
                # print(positions)
                # print(pawns)

    
        total_duels[r] = duels
        total_rolls[r] = num_rolls
    
    end = time.time()

    # print(f"Total wins: {wins}")
    # print(f"Total duels: {total_duels}")
    # print(f"Duels by winners: {player_stats}")
    # print(f"Total rolls: {total_rolls}")
    print(player_stats)
    duel_plot(num)
    duel_ratio_plot(num)
    print("\n\n")
    print(dice_prob)
    print("\n\n EXECUTION TIME:", end-start)
    plot_dice_prob(num)

def duels_stats(duels):
    tot_duels = 0
    for key, value in duels.items():
        tot_duels += sum([value[i][1] for i in range(0, 3)])
    
    return tot_duels

def roll_stats(rolls):
    tot_rolls = 0

    for key, value in rolls.items():
        tot_rolls += value
    
    return tot_rolls
def duel_ratio_plot(n):
    labels = ["Red", "Blue", "Green", "Black"]
    wins = [player_stats[i][0] for i in range(4)]
    duels_wins = [round(player_stats[i][2]/wins[i], 3) for i in range(4)]
    duels_losses = [round((player_stats[i][3]-player_stats[i][2])/(sum(wins) - wins[i]), 3) for i in range(4)]

    x = np.arange(len(labels))
    width = 0.20

    fig, ax = plt.subplots()

    rects1 = ax.bar(x - width/2, duels_wins, width, label = "Average Duels Engaged in During Win", color="m")
    rects2 = ax.bar(x + width/2, duels_losses, width, label = "Average Duels Engaged in During Loss", color="c")

    ax.set_xlabel('Player')
    ax.set_ylabel("Duels Engaged In")
    ax.set_title(f'Player Duel Statistics After {n} Trials ')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend(loc=2)

    
    ax.bar_label(rects1, padding=1, label_type='center', rotation=45, fontsize=10) 
    ax.bar_label(rects2, padding=1, label_type='center', rotation=45, fontsize=8)

    fig.tight_layout()

    plt.show()

def duel_plot(n):
    global player_stats

    labels = ["Red", "Blue", "Green", "Black"]
    wins = [player_stats[i][0] for i in range(4)]
    avg_duels_won = [round(player_stats[i][1]/wins[i], 3) for i in range(4)]
    avg_duels_played = [player_stats[i][2]/wins[i] for i in range(4)]
    avg_win_percentage = [100 * round(avg_duels_won[i]/avg_duels_played[i], 3) for i in range(4)]

    avg_req_duels = sum(avg_duels_won)/4
    avg_req_win_perc = sum(avg_win_percentage)/4

    x = np.arange(len(labels))
    width = 0.20

    fig, ax = plt.subplots()

    ax2 = ax.twinx() 

    rects1 = ax.bar(x - width, wins, width, label = "Total Wins", color="m")
    rects2 = ax.bar(x, avg_duels_won, width, label = "Average Duels Won", color="c")
    rects3 = ax2.bar(x + width, avg_win_percentage, width, label = "Average Duel Win %", color="#6ca0f5")

    ax.set_xlabel('Player')
    ax.set_ylabel("Game Wins & Average Duel Wins in Games Won")
    ax2.set_ylabel("Duel Win %")
    ax.set_title(f'Player Win Statistics After {n} Trials ')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend(loc=2)
    ax2.legend(loc=1)

    all_axes = fig.get_axes()
    for axis in all_axes:
        legend = axis.get_legend()
        if legend is not None:
            legend.remove()
            all_axes[-1].add_artist(legend)

    ax.bar_label(rects1, padding=1, label_type='center', rotation=45, fontsize=10) 
    ax.bar_label(rects2, padding=1, label_type='center', rotation=45, fontsize=8)
    ax2.bar_label(rects3, padding=1, label_type='center', rotation=45, fontsize=10)


    fig.tight_layout()

    plt.show()

    print(avg_req_duels)
    print(avg_req_win_perc)    
    

if __name__ == '__main__':
    main()
