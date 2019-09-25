#!/usr/bin/python3
import sys
import time

'''
 13   12   11   10     9    8    7        ========> Pit numbers
    --------------------------------
 00 | 04 | 04 | 04 || 04 | 04 | 04 | P2
----------------------------------------
 P1 | 04 | 04 | 04 || 04 | 04 | 04 | 00
    --------------------------------
       0    1    2     3    4    5    6   ========> Pit numbers
'''

NUM_STONES = 1
NUM_PITS = 14

P1_STORE = (NUM_PITS - 2) // 2
P2_STORE = NUM_PITS - 1

P1_ACTIONS = [i for i in range(P1_STORE)]
P2_ACTIONS = [i for i in range(P1_STORE + 1, P2_STORE)]

IS_P1 = 1
IS_P2 = 0

INT_MIN = -sys.maxsize - 1
INT_MAX = sys.maxsize

class state():
    def __init__(self, board):
        self.board = board
        self.is_terminal = False
        self.utility = 0

        # compute utility if the board represents a terminal state
        p1_pit_sum = sum(self.board[0:P1_STORE])
        p2_pit_sum = sum(self.board[P1_STORE + 1:P2_STORE])
        if (p1_pit_sum == 0) or (p2_pit_sum == 0):
            self.is_terminal = True
            self.utility = self.board[P1_STORE] + p1_pit_sum - self.board[P2_STORE] - p2_pit_sum

        self.min_value = None
        self.max_value = None
        self.result_of = {i:None for i in range(NUM_PITS)}
    
    def __str__(self):
        result = ''

        # result += '       6    5    4     3    2    1\n'
        result += ' 13   12   11    10    9    8    7\n'
        result += '    --------------------------------\n'

        for i in range(13, 9, -1): result += ' ' + '{:02d}'.format(self.board[i]) + ' |'
        result += '|'
        for i in range(9, 6, -1): result += ' ' + '{:02d}'.format(self.board[i]) + ' |'
        result += ' P2\n'

        result += '----------------------------------------\n'
        
        result += ' P1 |'
        for i in range(0, 3): result += ' ' + '{:02d}'.format(self.board[i]) + ' |'
        for i in range(3, 7): result += '| ' + '{:02d}'.format(self.board[i]) + ' '
        result += '\n'

        result += '    --------------------------------\n'
        # result += '       1    2    3     4    5    6\n'
        result += '       0    1    2     3    4    5    6\n'

        return result
    
    def result(self, chosen_pit):
        # return the precomputed next state if we have it
        #================================================
        if self.result_of[chosen_pit]:
            return self.result_of[chosen_pit]

        # we don't have the next state precomputed => compute and store it
        #=================================================================
        next_board = self.board[:]

        # DEBUG
        # print('Chosen pit = ' + str(chosen_pit))

        pit_to_fill = chosen_pit
        is_p1 = chosen_pit < P1_STORE
        is_p2 = not is_p1
        while next_board[chosen_pit] > 0:
            pit_to_fill = (pit_to_fill + 1) % NUM_PITS
            
            if (is_p1 and pit_to_fill == P2_STORE) or \
               (is_p2 and pit_to_fill == P1_STORE):
                continue
            
            next_board[pit_to_fill] += 1
            next_board[chosen_pit] -= 1
        
        # update the dictionary of resultant states
        next_state = state(next_board)
        self.result_of[chosen_pit] = next_state

        return next_state
    
    def is_terminal_state(self):
        return self.is_terminal
    
    def is_valid_action(self, chosen_pit):
        return ((chosen_pit >= 0 and chosen_pit < P2_STORE) and
                (chosen_pit != P1_STORE) and
                (self.board[chosen_pit] != 0))
    
    def get_utility(self):
        return self.utility
    
    def set_min_value(self, value):
        self.min_value = value
    
    def set_max_value(self, value):
        self.max_value = value
    
    def get_min_value(self):
        return self.min_value
    
    def get_max_value(self):
        return self.max_value

def minimax_decision(state, is_p1):
    # store all the possible resulting utilities
    actions = P1_ACTIONS if is_p1 else P2_ACTIONS
    results = []
    for action in actions:
        print('Evaluating action ' + str(action))
        if state.is_valid_action(action):
            results.append(min_value(state.result(action), is_p1))
        else:
            results.append(INT_MIN)
    
    # maximize the result and return it
    return results.index(max(results))

def min_value(state, is_p1):
    # print(str(state) + '\n')
    # input('')

    if state.is_terminal_state():
        return state.get_utility()
    
    min_utility = state.get_min_value()
    
    # compute the min from this node if we haven't already
    if not min_utility:
        min_utility = INT_MAX
        actions = P2_ACTIONS if is_p1 else P1_ACTIONS
        
        for action in actions:
            if state.is_valid_action(action):
                min_utility = min(min_utility, max_value(state.result(action), is_p1))
        
        state.set_min_value(min_utility)
    
    return min_utility

def max_value(state, is_p1):
    # print(str(state) + '\n')
    # input('')

    if state.is_terminal_state():
        return state.get_utility()

    max_utility = state.get_max_value()

    # compute the max from this node if we haven't already
    if not max_utility:
        max_utility = INT_MIN
        actions = P1_ACTIONS if is_p1 else P2_ACTIONS
        
        for action in actions:
            if state.is_valid_action(action):
                max_utility = max(max_utility, min_value(state.result(action), is_p1))
        
        state.set_max_value(max_utility)
    
    return max_utility

if __name__ == '__main__':
    init_board = ([NUM_STONES for i in range((NUM_PITS - 2) // 2)] + [0]) * 2
    init_state = state(init_board)

    print(minimax_decision(init_state, IS_P1))
