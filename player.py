from config import *
import random

class player():
    def __init__(self, player_type, is_p1):
        self.is_p1 = is_p1
        self.player_type = 0

        if player_type == 'random':      self.player_type = RANDOM
        elif player_type == 'minimax':   self.player_type = MINIMAX
        elif player_type == 'alphabeta': self.player_type = ALPHABETA
        elif player_type == 'human':     self.player_type = HUMAN
        else:
            print('Incorrect player type: ' + player_type + '\n')
            print_usage()
            exit(1)
    
    def move(self, current_state):
        if self.player_type == RANDOM:      return random_decision(current_state, self.is_p1)
        elif self.player_type == MINIMAX:   return minimax_decision(current_state, self.is_p1)
        elif self.player_type == ALPHABETA: return alphabeta_decision(current_state, self.is_p1)
        elif self.player_type == HUMAN:     return human_decision(current_state, self.is_p1)

def random_decision(state, is_p1):
    actions = P1_ACTIONS if is_p1 else P2_ACTIONS
    random.shuffle(actions)
    for action in actions:
        if state.is_valid_action(action):
            print('Player ' + ('1' if is_p1 else '2') + '\'s turn: ' + str(action))
            return action

def minimax_decision(state, is_p1):
    # store all the possible resulting utilities
    actions = P1_ACTIONS if is_p1 else P2_ACTIONS
    results = []
    for action in actions:
        print('Evaluating action ' + str(action))
        if state.is_valid_action(action):
            if is_p1:
                results.append(min_value(state.result(action), is_p1))
            else:
                results.append(max_value(state.result(action), is_p1))
        else:
            if is_p1:
                results.append(INT_MIN)
            else:
                results.append(INT_MAX)
    
    # return the optimal result
    action = 0
    if is_p1:
        action = actions[results.index(max(results))]
    else:
        action = actions[results.index(min(results))]
    print('Player ' + ('1' if is_p1 else '2') + '\'s turn: ' + str(action))
    return action

def min_value(state, is_p1):
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

def human_decision(state, is_p1):
    actions = P1_ACTIONS if is_p1 else P2_ACTIONS

    while True:
        input_action = int(input('Player ' + ('1' if is_p1 else '2') + '\'s turn: '))
        if input_action in actions and state.is_valid_action(input_action):
            return input_action
        else:
            print('Illegal action: ' + str(input_action))
