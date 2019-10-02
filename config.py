# game configuration
NUM_STONES = 4
NUM_PITS = 14

# set numbers for players 1 and 2
P1_STORE = (NUM_PITS - 2) // 2
P2_STORE = NUM_PITS - 1
P1_ACTIONS = [i for i in range(P1_STORE)]
P2_ACTIONS = [i for i in range(P1_STORE + 1, P2_STORE)]
IS_P1 = 1
IS_P2 = 0

# plus and minus infinity
POS_INF = float('inf')
NEG_INF = float('-inf')

# the four player types
RANDOM = 0
MINIMAX = 1
ALPHABETA = 2
HUMAN = 3

# minimax and alpha-beta specific-settings
MINIMAX_MAX_DEPTH = 7
ALPHABETA_MAX_DEPTH = 7
count_states = False