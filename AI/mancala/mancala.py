""" This script is a pythonic representation of Mancala game. Given an input file with a state, this will output the
    next steps based on greedy, minimax and alpha beta pruning concepts.

"""
import argparse
import copy
import os

DICT_ID_NAME = {0: 'B2', 1:'B3', 2:'B4', 6:'A2', 5:'A3', 4:'A2'}
class BoardGame(object):
    def __init__(self, player_1_list, player_2_list, player_1_mancala, player_2_mancala):
        self.board_list = []

        self.board_list.extend(player_1_list)
        self.board_list.append(player_1_mancala)
        self.board_list.extend(player_2_list[::-1])
        self.board_list.append(player_2_mancala)

        self.num_pits = len(player_1_list)

    def get_num_pits(self):
        return self.num_pits

    def get_board_list(self):
        return self.board_list

    def get_player_1_eval_score(self):
        return self.board_list[self.num_pits] - self.board_list[-1]

    def get_player_2_eval_score(self):
        return self.board_list[-1] - self.board_list[self.num_pits]

    def get_player_range(self, player_num):
        if player_num == 1:
            return 0, self.num_pits, 1, 2
        elif player_num == 2:
            return 2 * self.num_pits, self.num_pits, -1, 1

    def get_player_reversed_range(self, player_num):
        if player_num == 1:
            return 2 * self.num_pits, self.num_pits, -1, 2
        elif player_num == 2:
            return 0, self.num_pits, 1, 1

    def is_game_over(self):
        player_1_coin_sum = sum(self.board_list[: self.num_pits])
        player_2_coin_sum = sum(self.board_list[self.num_pits+1: -1])
        if not player_1_coin_sum or not player_2_coin_sum:
            self.board_list[-1] += player_2_coin_sum
            self.board_list[self.num_pits] += player_1_coin_sum
            for i in xrange(0, len(self.board_list)-1):
                if i == self.num_pits:
                    continue
                self.board_list[i] = 0
            return True
        return False

    def get_board_state(self):
        board_state = '%s\n' %(' '.join(str(x) for x in self.board_list[-2:self.num_pits:-1]))
        board_state = '%s%s\n' %(board_state, ' '.join(str(x) for x in self.board_list[:self.num_pits]))
        board_state = '%s%s\n' %(board_state, self.board_list[-1])
        board_state = '%s%s\n' %(board_state, self.board_list[self.num_pits])

        return board_state

    def next_turn(self, player_num, start_index):
        pit_empty = True
        if player_num == 1:
            mancala_index = self.num_pits
            skip_index = len(self.board_list) - 1
        elif player_num == 2:
            mancala_index = len(self.board_list) - 1
            skip_index = self.num_pits

        num_coins = self.board_list[start_index]
        if not num_coins:
            return False, pit_empty

        pit_empty = False
        self.board_list[start_index] = 0
        start_index += 1
        last_index = len(self.board_list)
        while num_coins > 0:
            for index in xrange(start_index,last_index):
                if index == skip_index:
                    continue
                self.board_list[index] += 1
                num_coins -= 1
                if num_coins == 0:
                    last_index = index
                    break
            start_index = 0

        extra_move = False
        if last_index == mancala_index:
            extra_move = True

        else:
            other_index = 2* self.get_num_pits() - last_index

            if (player_num == 1 and last_index < mancala_index) or(player_num == 2 and last_index > skip_index+1):
                if self.board_list[last_index] == 1 and self.board_list[other_index] != 0:
                    coins_added = self.board_list[other_index] + 1
                    self.board_list[last_index] = 0
                    self.board_list[other_index] = 0
                    self.board_list[mancala_index] += coins_added
        return extra_move, pit_empty

def check_player1_best_move(board_obj):
    first_run = True
    num_pits = board_obj.get_num_pits()
    max_eval_obj = board_obj
    if board_obj.is_game_over(): return board_obj

    for index in xrange(0, num_pits):
        board_obj_copy = copy.deepcopy(board_obj)
        extra_move, pit_empty = board_obj_copy.next_turn(1, index)
        if board_obj_copy.is_game_over(): return board_obj_copy

        if not pit_empty:
            if extra_move:
                board_obj_copy = check_player1_best_move(board_obj_copy)
            if first_run:
                first_run = False
                max_eval_obj = board_obj_copy

            if board_obj_copy.get_player_1_eval_score() > max_eval_obj.get_player_1_eval_score():
                max_eval_obj = board_obj_copy


    return max_eval_obj

def check_player2_best_move(board_obj):
    first_run = True
    num_pits = board_obj.get_num_pits()
    max_eval_obj = board_obj
    if board_obj.is_game_over(): return board_obj

    for index in xrange(2*num_pits, num_pits, -1):
        board_obj_copy = copy.deepcopy(board_obj)
        extra_move, pit_empty = board_obj_copy.next_turn(2, index)
        if board_obj_copy.is_game_over(): return board_obj_copy
        if not pit_empty:
            if extra_move:
                board_obj_copy = check_player2_best_move(board_obj_copy)
            if first_run:
                first_run = False
                max_eval_obj = board_obj_copy

            if board_obj_copy.get_player_2_eval_score() > max_eval_obj.get_player_2_eval_score():
                max_eval_obj = board_obj_copy

    return max_eval_obj

def perform_greedy(board_obj, player_num, cutoff_depth=1):
    if player_num == 1:
        max_board_obj = check_player1_best_move(board_obj)
    else:
        max_board_obj = check_player2_best_move(board_obj)

    output_file = open('next_state.txt', 'w')
    output_file.write('%s' % (max_board_obj.get_board_state()))
    output_file.close()

def get_all_board_states(board_obj, board_list, player_num):
    start_index, end_index, reverse, other_player = board_obj.get_player_range(player_num)
    for index in xrange(start_index, end_index, reverse):
        board_obj_copy = copy.deepcopy(board_obj)
        next_move, pit_empty = board_obj_copy.next_turn(player_num, index)
        if not pit_empty:
            if next_move:
                get_all_board_states(board_obj_copy, board_list, player_num)
            else:
                board_list.append(board_obj_copy)

def max_play(board_obj, current_depth, cutoff_depth, player_num):
    board_list = []
    output_list = []
    output_value_list = []

    get_all_board_states(board_obj, board_list, player_num)
    if current_depth == cutoff_depth:
        for board_obj in board_list:
            output_list.append(board_obj)
            output_value_list.append(board_obj.get_player_2_eval_score())
        return output_list, output_value_list


    start_index, end_index, reverse, other_player = board_obj.get_player_range(player_num)

    for board_obj in board_list:
        child_list, child_values = min_play(board_obj, current_depth+1, cutoff_depth, other_player)
        max_value = max(child_values)
        output_list.append(board_obj)
        output_value_list.append(max_value)

    return output_list, output_value_list

def min_play(board_obj, current_depth, cutoff_depth, player_num):
    board_obj_list = []
    output_list = []
    output_value_list = []

    get_all_board_states(board_obj, board_obj_list, player_num)
    if current_depth == cutoff_depth:
        for board_obj in board_obj_list:
            output_list.append(board_obj)
            output_value_list.append(board_obj.get_player_2_eval_score())
        return output_list, output_value_list

    start_index, end_index, reverse, other_player = board_obj.get_player_range(player_num)
    for board_obj in board_obj_list:
        child_list, child_values = max_play(board_obj, current_depth+1, cutoff_depth, other_player)
        min_value = min(child_values)
        output_list.append(board_obj)
        output_value_list.append(min_value)

    return output_list, output_value_list

def perform_minimax(board_obj, player_num, cutoff_depth=1, current_depth=0):
    level_1_list, level_1_value = min_play(board_obj, current_depth+1, cutoff_depth, player_num)
    max_score = -10000
    max_obj = None
    for i in xrange(0, len(level_1_list)):
        if level_1_value[i] > max_score:
            max_score = level_1_value[i]
            max_obj = level_1_list[i]

    print max_obj.get_board_state()
    print max_score


def perform_alpha_beta(board_obj, player_num, cutoff_depth=1):
    pass

def competition(board_obj, player_num, cutoff_depth=1):
    pass

DICT_NUM_TO_TASK = { 1: perform_greedy,
                     2: perform_minimax,
                     3: perform_alpha_beta,
                     4: competition
}

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
    log_file = open('traverse_log.txt', 'w')
    output_file = open('next_state_minimax.txt', 'w')
    method_name, player_num, cutoff_depth, obj = read_file(file_obj)
    DICT_NUM_TO_TASK[method_name](obj, player_num, cutoff_depth)
