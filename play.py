#!/usr/bin/python3

'''
 13   12   11   10     9    8    7        ========> Pit numbers
    --------------------------------
 00 | 04 | 04 | 04 || 04 | 04 | 04 | P2
----------------------------------------
 P1 | 04 | 04 | 04 || 04 | 04 | 04 | 00
    --------------------------------
       0    1    2     3    4    5    6   ========> Pit numbers
'''
from config import *
from player import *
from state import *

def print_usage():
    print('Usage: ./play player1 player2\n\n' + \
          'player1 and player2 can be random, minimax, alphabeta, or human')

def print_winner(current_state):
    utility = current_state.get_utility()

    print('Game over. ', end='')
    if utility == 0:
        print('It\'s a draw!')
    else:
        print('Player ' + ('1' if utility > 0 else '2') + ' won!')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print_usage()
        exit(0)
    
    p1 = player(sys.argv[1], IS_P1)
    p2 = player(sys.argv[2], IS_P2)

    init_board = ([NUM_STONES for i in range((NUM_PITS - 2) // 2)] + [0]) * 2
    current_state = state(init_board)

    print(current_state)

    while True:
        current_state = current_state.result(p1.move(current_state))
        print(current_state)

        if current_state.is_terminal_state():
            print_winner(current_state)
            exit(0)

        current_state = current_state.result(p2.move(current_state))
        print(current_state)

        if current_state.is_terminal_state():
            print_winner(current_state)
            exit(0)
