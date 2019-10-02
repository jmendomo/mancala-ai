from config import *
import random
import sys
import time

states_expanded = list()

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
    
    def get_player_type(self):
        return self.player_type

def print_move(action, is_p1):
    if is_p1: action += 1
    else:     action -= P1_STORE
    print(('' if is_p1 else ' ') + str(action))

def random_decision(state, is_p1):
    actions = P1_ACTIONS if is_p1 else P2_ACTIONS
    random.shuffle(actions)
    for action in actions:
        if state.is_valid_action(action):
            print_move(action, is_p1)
            return action

def minimax_decision(state, is_p1):
    # store all the possible resulting utilities
    actions = P1_ACTIONS if is_p1 else P2_ACTIONS
    results = []

    if count_states: states_expanded.append(0)

    for action in actions:
        if state.is_valid_action(action):
            next_state, additional_move = state.result(action)
            if count_states: states_expanded[-1] += 1
            if is_p1:
                if additional_move: results.append(max_value(next_state, is_p1, 1))
                else:               results.append(min_value(next_state, is_p1, 1))
            else:
                if additional_move: results.append(min_value(next_state, is_p1, 1))
                else:               results.append(max_value(next_state, is_p1, 1))
        else:
            if is_p1: results.append(NEG_INF)
            else:     results.append(POS_INF)
    
    # return the optimal result
    action = 0
    if is_p1:
        action = actions[results.index(max(results))]
    else:
        action = actions[results.index(min(results))]
    print_move(action, is_p1)

    return action

def min_value(state, is_p1, depth):
    if state.is_terminal_state() or depth == MINIMAX_MAX_DEPTH:
        return state.get_utility()
    
    min_utility = POS_INF
    actions = P2_ACTIONS if is_p1 else P1_ACTIONS
    
    for action in actions:
        if state.is_valid_action(action):
            next_state, additional_move = state.result(action)
            if count_states: states_expanded[-1] += 1
            if additional_move:
                min_utility = min(min_utility, min_value(next_state, is_p1, depth + 1))
            else:
                min_utility = min(min_utility, max_value(next_state, is_p1, depth + 1))
    
    return min_utility

def max_value(state, is_p1, depth):
    if state.is_terminal_state() or depth == MINIMAX_MAX_DEPTH:
        return state.get_utility()

    max_utility = NEG_INF
    actions = P1_ACTIONS if is_p1 else P2_ACTIONS
    
    for action in actions:
        if state.is_valid_action(action):
            next_state, additional_move = state.result(action)
            if count_states: states_expanded[-1] += 1
            if additional_move:
                max_utility = max(max_utility, max_value(next_state, is_p1, depth + 1))
            else:
                max_utility = max(max_utility, min_value(next_state, is_p1, depth + 1))
    
    return max_utility

def alphabeta_decision(state, is_p1):
    # store all the possible resulting utilities
    actions = P1_ACTIONS if is_p1 else P2_ACTIONS
    results = []

    if count_states: states_expanded.append(0)

    alpha = NEG_INF
    beta = POS_INF

    for action in actions:
        if state.is_valid_action(action):
            next_state, additional_move = state.result(action)
            if count_states: states_expanded[-1] += 1
            if is_p1:
                if additional_move: results.append(max_value_ab(next_state, 1, alpha, beta, is_p1))
                else:               results.append(min_value_ab(next_state, 1, alpha, beta, is_p1))
            else:
                if additional_move: results.append(min_value_ab(next_state, 1, alpha, beta, is_p1))
                else:               results.append(max_value_ab(next_state, 1, alpha, beta, is_p1))
        else:
            if is_p1: results.append(NEG_INF)
            else:     results.append(POS_INF)
    
    # return the optimal result
    action = 0
    if is_p1:
        action = actions[results.index(max(results))]
    else:
        action = actions[results.index(min(results))]
    print_move(action, is_p1)

    return action

def min_value_ab(state, depth, alpha, beta, is_p1):
    if state.is_terminal_state() or depth == ALPHABETA_MAX_DEPTH:
        return state.get_utility()
    
    min_utility = POS_INF
    actions = P2_ACTIONS if is_p1 else P1_ACTIONS
    
    for action in actions:
        if state.is_valid_action(action):
            next_state, additional_move = state.result(action)
            if count_states: states_expanded[-1] += 1
            if additional_move: 
                min_utility = min(min_utility, min_value_ab(next_state, depth + 1, alpha, beta,
                                  is_p1))
            else:               
                min_utility = min(min_utility, max_value_ab(next_state, depth + 1, alpha, beta,
                                  is_p1))

            if min_utility <= alpha:
                return min_utility
            beta = min(beta, min_utility)
    
    return min_utility

def max_value_ab(state, depth, alpha, beta, is_p1):
    if state.is_terminal_state() or depth == ALPHABETA_MAX_DEPTH:
        return state.get_utility()

    max_utility = NEG_INF
    actions = P1_ACTIONS if is_p1 else P2_ACTIONS
    
    for action in actions:
        if state.is_valid_action(action):
            next_state, additional_move = state.result(action)
            if count_states: states_expanded[-1] += 1
            if additional_move:
                max_utility = max(max_utility, max_value_ab(next_state, depth + 1, alpha, beta,
                                  is_p1))
            else:               
                max_utility = max(max_utility, min_value_ab(next_state, depth + 1, alpha, beta,
                                  is_p1))
            
            if max_utility >= beta:
                return max_utility
            alpha = max(alpha, max_utility)

    return max_utility

def human_decision(state, is_p1):
    actions = P1_ACTIONS if is_p1 else P2_ACTIONS

    while True:
        print('Enter player ' + ('1' if is_p1 else '2') + '\'s move: ', end='', flush=True,
              file=sys.stderr)
        input_action = int(input())

        if is_p1: input_action -= 1
        else:     input_action += P1_STORE

        if input_action in actions and state.is_valid_action(input_action):
            print_move(input_action, is_p1)
            return input_action
        else:
            print('Illegal move', file=sys.stderr)
