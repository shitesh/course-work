""" This script is a pythonic representation of Mancala game. Given an input file with a state, this will output the
    next steps based on greedy, minimax and alpha beta pruning concepts.

"""
import argparse
import os

class BoardGame(object):
    def __init__(self, player_1_list, player_2_list, player_1_mancala, player_2_mancala):
        self.cost_list = []
        self.cost_list.extend(player_1_list)
        self.cost_list.append(player_1_mancala)
        self.cost_list.extend(player_2_list)
        self.cost_list.append(player_2_mancala)

        self.num_pits = len(player_1_list)

def read_file(file_obj):
    method_num = int(file_obj.readline().strip())
    player_num = int(file_obj.readline().strip())
    cutoff_depth = int(file_obj.readline().strip())

    player_2_list = [int(i) for i in file_obj.readline().strip().split(' ')]
    player_1_list = [int(i) for i in file_obj.readline().strip().split(' ')]

    player_2_mancala = int(file_obj.readline().strip())
    player_1_mancala = int(file_obj.readline().strip())

    obj = BoardGame(player_1_list, player_2_list, player_1_mancala, player_2_mancala)

    return method_num, player_num, cutoff_depth, obj

def perform_greedy(board_obj, player_num, cutoff_depth=1):
    pass

def perform_minimax(board_obj, player_num, cutoff_depth=1):
    pass

def perform_alpha_beta(board_obj, player_num, cutoff_depth=1):
    pass

def this_is_sparta(board_obj, player_num, cutoff_depth=1):
    pass

DICT_NUM_TO_TASK = { 1: perform_greedy,
                     2: perform_minimax,
                     3: perform_alpha_beta,
                     4: this_is_sparta
}

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        raise parser.error("Given file doesn't exist")
    else:
        return open(arg, 'r')

def read_command_line():
    parser = argparse.ArgumentParser("ManCala Game")
    parser.add_argument("-i", dest="input_file", required=True, help="input file with required details",
                        type=lambda x: is_valid_file(parser, x))
    arguments = parser.parse_args()
    return arguments.input_file

if __name__=='__main__':
    file_obj = read_command_line()
    method_name, player_num, cutoff_depth, obj = read_file(file_obj)

    DICT_NUM_TO_TASK[method_name](obj, player_num, cutoff_depth)


    #todo: has to go in that method implementation
    output_file = open('output.txt', 'w')
