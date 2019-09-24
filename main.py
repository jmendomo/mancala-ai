#!/usr/bin/python3
import sys

'''
 13   12   11   10     9    8    7        ========> Pit numbers
    --------------------------------
 00 | 04 | 04 | 04 || 04 | 04 | 04 | P2
----------------------------------------
 P1 | 04 | 04 | 04 || 04 | 04 | 04 | 00
    --------------------------------
       0    1    2     3    4    5    6   ========> Pit numbers
'''

NUM_STONES = 4
NUM_PITS = 14
ACTIONS = [i for i in range(NUM_PITS)]

class state():
    def __init__(self, board):
        self.board = board
        self.is_terminal = False
        self.utility = 0

        if (sum(self.board[0:6]) == 0) or (sum(self.board[7:13]) == 0):
            self.is_terminal = True
            self.utility = self.board[6] - self.board[13]

        self.min = 0
        self.max = 0
        self.result_of = {i:None for i in range(NUM_PITS)}
    
    def result(self, chosen_pit):
        # return the precomputed next state if we have it
        #================================================
        if self.result_of[chosen_pit]:
            return self.result_of[chosen_pit]

        # we don't have the next state precomputed => compute and store it
        #=================================================================
        next_board = self.board[:]

        start_pit = chosen_pit + 1
        end_pit = chosen_pit + board[chosen_pit]
        
        # make sure we don't accidentally fill-in the opponent's store
        pit_to_skip = -1
        if chosen_pit < 6 and end_pit >= 13:
            pit_to_skip = 13
        if chosen_pit > 6 and (end_pit % NUM_PITS) >= 6:
            pit_to_skip = 6

        # empty the current pit and fill in others
        next_board[chosen_pit] = 0
        for pit in range(start_pit, end_pit + 1):
            pit %= NUM_PITS
            if pit == pit_to_skip:
                continue
            next_board[pit] += 1
        
        # update the dictionary of resultant states
        next_state = state(next_board)
        self.result_of[chosen_pit] = next_state

        return next_state
    
    def is_terminal_state(self):
        return self.is_terminal
    
    def is_valid_action(self, chosen_pit):
        return ((chosen_pit >= 0 and chosen_pit < 13) and
                (chosen_pit != 6) and
                (self.board[chosen_pit] != 0))
    
    def get_utility(self):
        return self.utility

def minimax_decision(state):
    # store all the possible resulting utilities
    results = []
    for action in ACTIONS:
        if state.is_valid_action(action):
            results.append(min_value(state.result(action)))
        else:
            results.append(-sys.maxint - 1)
    
    # maximize the result and return it
    return results.index(max(results))

def min_value(state):
    if state.is_terminal_state():
        return state.get_utility()
    
    min_utility = sys.maxint
    
    for action in ACTIONS:
        min_utility = min(min_utility, max_value(state.result(action)))
    
    return min_utility

def max_value(state):
    if state.is_terminal_state():
        return state.get_utility()
    
    max_utility = -sys.maxint - 1
    
    for action in ACTIONS:
        max_utility = max(max_utility, min_value(state.result(action)))
    
    return max_utility

if __name__ == '__main__':
    init_board = ([NUM_STONES for i in range(NUM_PITS)] + [0]) * 2
    init_state = state(init_board)
