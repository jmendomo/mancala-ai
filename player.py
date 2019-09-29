from config import *
import random
import time

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
            print(('' if is_p1 else ' ') + str(action))
            return action

def minimax_decision(state, is_p1):
    # store all the possible resulting utilities
    actions = P1_ACTIONS if is_p1 else P2_ACTIONS
    results = []

    for action in actions:
        print('Evaluating action ' + str(action))
        if state.is_valid_action(action):
            next_state, additional_move = state.result(action)
            if is_p1:
                if additional_move: results.append(max_value(next_state, is_p1))
                else:               results.append(min_value(next_state, is_p1))
            else:
                if additional_move: results.append(min_value(next_state, is_p1))
                else:               results.append(max_value(next_state, is_p1))
        else:
            if is_p1: results.append(INT_MIN)
            else:     results.append(INT_MAX)
    
    # return the optimal result
    action = 0
    if is_p1:
        action = actions[results.index(max(results))]
    else:
        action = actions[results.index(min(results))]
    print(('' if is_p1 else ' ') + str(action))

    return action

def min_value(state, is_p1):
    if state.is_terminal_state():
        return state.get_utility()
    
    min_utility = INT_MAX
    actions = P2_ACTIONS if is_p1 else P1_ACTIONS
    
    for action in actions:
        if state.is_valid_action(action):
            next_state, additional_move = state.result(action)
            if additional_move: min_utility = min(min_utility, min_value(next_state, is_p1))
            else:               min_utility = min(min_utility, max_value(next_state, is_p1))
    
    return min_utility

def max_value(state, is_p1):
    if state.is_terminal_state():
        return state.get_utility()

    max_utility = INT_MIN
    actions = P1_ACTIONS if is_p1 else P2_ACTIONS
    
    for action in actions:
        if state.is_valid_action(action):
            next_state, additional_move = state.result(action)
            if additional_move: max_utility = max(max_utility, max_value(next_state, is_p1))
            else:               max_utility = max(max_utility, min_value(next_state, is_p1))
    
    return max_utility

def alpha_beta(state, alpha, beta, is_p1):
  
    actions = P1_ACTIONS if is_p1 else P2_ACTIONS
    results = []
    
    if is_p1:
    max_utility = float("-inf")
    for action in actions:
        print('Evaluating action ' + str(action))
        utility = alpha_beta(state.result(action), alpha, beta, False)
        max_utility = max(max_utility, utility)
        alpha = max(alpha, utility)
        if beta <= alpha:
            break
        return max_utility
        return action
        
    print('Player ' + ('1' if is_p1 else '2') + '\'s turn: ' + str(action))

    else:
        min_utility = float("inf")
        for action in actions:
            print('Evaluating action ' + str(action))
            utility = alpha_beta(state.result(action), alpha, beta, True)
            min_utility = max(min_utility, utility)
            beta = max(betaa, utility)
            if beta <= alpha:
                break
        return min_utility
        return action
    
    print('Player ' + ('1' if is_p1 else '2') + '\'s turn: ' + str(action))

def human_decision(state, is_p1):
    actions = P1_ACTIONS if is_p1 else P2_ACTIONS

    while True:
        print('Enter player ' + ('1' if is_p1 else '2') + '\'s move: ', end='', flush=True, file=sys.stderr)
        input_action = int(input())
        if input_action in actions and state.is_valid_action(input_action):
            print(('' if is_p1 else ' ') + str(input_action))
            return input_action
        else:
            print('Illegal move', file=sys.stderr)
