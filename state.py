from config import *

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
    
    # def __str__(self):
    #     result = ''

    #     # result += '           6    5    4     3    2    1\n'
    #     result += '     13   12   11    10    9    8    7\n'
    #     result += '        --------------------------------\n'

    #     result += '    '
    #     for i in range(13, 9, -1): result += ' ' + '{:02d}'.format(self.board[i]) + ' |'
    #     result += '|'
    #     for i in range(9, 6, -1): result += ' ' + '{:02d}'.format(self.board[i]) + ' |'
    #     result += ' P2\n'

    #     result += '    ----------------------------------------\n'
        
    #     result += '     P1 |'
    #     for i in range(0, 3): result += ' ' + '{:02d}'.format(self.board[i]) + ' |'
    #     for i in range(3, 7): result += '| ' + '{:02d}'.format(self.board[i]) + ' '
    #     result += '\n'

    #     result += '        --------------------------------\n'
    #     # result += '           1    2    3     4    5    6\n'
    #     result += '           0    1    2     3    4    5    6\n'

    #     return result
    
    def __str__(self):
        result = ''

        # result += '           6    5    4     3    2    1\n'
        result += '      9    8     7    6    5\n'
        result += '        --------------------------------\n'

        result += '    '
        for i in range(9, 6, -1): result += ' ' + '{:02d}'.format(self.board[i]) + ' |'
        result += '|'
        for i in range(6, 4, -1): result += ' ' + '{:02d}'.format(self.board[i]) + ' |'
        result += ' P2\n'

        result += '    ----------------------------------------\n'
        
        result += '     P1 |'
        for i in range(0, 2): result += ' ' + '{:02d}'.format(self.board[i]) + ' |'
        for i in range(2, 5): result += '| ' + '{:02d}'.format(self.board[i]) + ' '
        result += '\n'

        result += '        --------------------------------\n'
        # result += '           1    2    3     4    5    6\n'
        result += '           0    1     2    3    4\n'

        return result
    
    def result(self, chosen_pit):
        # return the precomputed next state if we have it
        #================================================
        if self.result_of[chosen_pit]:
            return self.result_of[chosen_pit]

        # we don't have the next state precomputed => compute and store it
        #=================================================================
        next_board = self.board[:]

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
        # self.result_of[chosen_pit] = next_state

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