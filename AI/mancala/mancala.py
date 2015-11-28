""" This script is a pythonic representation of Mancala game. Given an input file with a state, this will output the
    next steps based on greedy, minimax and alpha beta pruning concepts.

"""
import argparse
import copy
import os
from collections import deque

MIN_DEFAULT_VALUE = 40000
MAX_DEFAULT_VALUE = -40000

DICT_OPPOSITE_PLAYER_NUM = {1: 2, 2: 1}

class BoardGame(object):
    def __init__(self, player_1_list, player_2_list, player_1_mancala, player_2_mancala):
        self.board_list = []
        self.index_name = {}
        self.board_list.extend(player_1_list)
        self.board_list.append(player_1_mancala)
        self.board_list.extend(player_2_list[::-1])
        self.board_list.append(player_2_mancala)

        self.num_pits = len(player_1_list)

        for index in xrange(0,self.num_pits):
            self.index_name[index] = 'B%s'%(index+2)

        for index in xrange(2 * self.num_pits, self.num_pits, -1):
            self.index_name[index] = 'A%s'%(len(self.board_list) - index)

    def get_index_name(self):
        return self.index_name

    def get_num_pits(self):
        return self.num_pits

    def get_board_list(self):
        return self.board_list

    def get_value_at_index(self, index):
        return self.board_list[index]

    def get_player_1_eval_score(self):
        return self.board_list[self.num_pits] - self.board_list[-1]

    def get_player_2_eval_score(self):
        return self.board_list[-1] - self.board_list[self.num_pits]

    def get_player_range(self, player_num):
        if player_num == 1:
            return 0, self.num_pits, 1, 2
        elif player_num == 2:
            return 2 * self.num_pits, self.num_pits, -1, 1

    def get_eval_score(self, player_num):
        if player_num == 1:
            return self.get_player_1_eval_score()
        elif player_num == 2:
            return self.get_player_2_eval_score()

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

            if (player_num == 1 and last_index < mancala_index) or(player_num == 2 and last_index > skip_index):
                #if self.board_list[last_index] == 1 and self.board_list[other_index] != 0:
                if self.board_list[last_index] == 1:
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
    output_file = open('next_state.txt', 'w')

    if player_num == 1:
        max_board_obj = check_player1_best_move(board_obj)
    else:
        max_board_obj = check_player2_best_move(board_obj)

    output_file.write('%s' % (max_board_obj.get_board_state()))
    output_file.close()

class Node(object):

    def __init__(self, board_obj, player_num, method, name, value, depth, next_move, children_list, alpha=None, beta=None):
        self.board_obj = board_obj
        self.player_num = player_num
        self.method = method
        self.name = name
        self.value = value
        self.next_move = next_move
        self.depth = depth
        self.children_list = children_list
        self.best_state = None
        self.alpha = alpha
        self.beta = beta

    def get_log(self):
        value = self.value
        if self.value == MAX_DEFAULT_VALUE:
            value = '-Infinity'
        elif self.value == MIN_DEFAULT_VALUE:
            value = 'Infinity'
        return '%s,%s,%s\n' %(self.name, self.depth, value)

    def get_alpha_beta_log(self):
        value = self.value
        if self.value == MAX_DEFAULT_VALUE:
            value = '-Infinity'
        elif self.value == MIN_DEFAULT_VALUE:
            value = 'Infinity'
        alpha = self.alpha if self.alpha != MAX_DEFAULT_VALUE else '-Infinity'
        beta = self.beta if self.beta != MIN_DEFAULT_VALUE else 'Infinity'

        return '%s,%s,%s,%s,%s\n' %(self.name, self.depth, value, alpha, beta)

    def get_alpha(self):
        return self.alpha

    def get_beta(self):
        return self.beta

    def get_name(self):
        return self.name

    def get_value(self):
        return self.value

    def get_player_num(self):
        return self.player_num

    def get_children_list(self):
        return self.children_list

    def get_board(self):
        return self.board_obj

    def get_next_move(self):
        return self.next_move

    def get_depth(self):
        return self.depth

    def get_method_name(self):
        return self.method

    def get_best_state(self):
        return  self.best_state

    def set_alpha(self, alpha):
        self.alpha = alpha

    def set_beta(self, beta):
        self.beta = beta

    def set_next_move(self, next_move):
        self.next_move = next_move

    def set_best_state(self, board_obj):
        self.best_state = board_obj

    def set_children_list(self, children_list):
        self.children_list = children_list

    def set_name(self, name):
        self.name = name

    def set_method_name(self, method):
        self.method = method

    def set_depth(self, depth):
        self.depth = depth

    def set_player_num(self, player_num):
        self.player_num = player_num

    def set_value(self, value):
        self.value = value

def perform_minimax(board_obj, player_num, cutoff_depth):
    output_file = open('next_state.txt', 'w')
    log_file = open('traverse_log.txt', 'w')

    log_file.write('Node,Depth,Value\n')
    name = 'root'
    value = MAX_DEFAULT_VALUE
    dict_index_name = board_obj.get_index_name()
    dict_opposite_method = {'min': 'max', 'max': 'min'}

    main_player = player_num
    start_index, end_index, reverse, other_player = board_obj.get_player_range(player_num)
    children_list = [int(i) for i in xrange(start_index, end_index, reverse)]
    num_of_runs = len(children_list)
    stack = deque([])

    root_node = Node(board_obj, player_num, 'max', name, value, 0, False, children_list)
    if root_node.get_board().is_game_over():
        root_node.set_children_list([])
        root_node.set_value(root_node.get_board().get_eval_score(main_player))
        root_node.set_best_state(root_node.get_board())
        log_file.write(root_node.get_log())
    else:
        log_file.write('root,0,-Infinity\n')

    stack.appendleft(root_node)

    while(num_of_runs):
        current_node = stack.popleft()
        if current_node.get_children_list():
            current_node_copy = copy.deepcopy(current_node)
            if current_node.get_next_move():
                depth = current_node.get_depth()
            else:
                depth = current_node.get_depth()+1

            child_index = current_node.get_children_list().pop(0)
            stack.appendleft(current_node)

            if current_node.get_board().get_value_at_index(child_index) == 0:
                continue

            extra_move, pit_empty = current_node_copy.get_board().next_turn(current_node.get_player_num(), child_index)
            current_node_copy.set_best_state(None)
            current_node_copy.set_name(dict_index_name[child_index])
            current_node_copy.set_depth(depth)

            if current_node_copy.get_board().is_game_over():
                value = current_node_copy.get_board().get_eval_score(main_player)
                children_list = []
                current_node_copy.set_children_list(children_list)
                current_node_copy.set_value(value)
                log_file.write(current_node_copy.get_log())
                stack.appendleft(current_node_copy)
                continue

            elif extra_move:
                start_index, end_index, reverse, other_player = board_obj.get_player_range(current_node.get_player_num())
                children_list = [int(i) for i in xrange(start_index, end_index, reverse)]
                method_name = current_node.get_method_name()
                #if cutoff_depth != depth:
                if method_name == 'max': value = MAX_DEFAULT_VALUE
                if method_name == 'min': value = MIN_DEFAULT_VALUE
                #else:
                #    value = current_node_copy.get_board().get_eval_score(main_player)
                next_move = True
                player_num = current_node.get_player_num()

            else:
                start_index, end_index, reverse, other_player = board_obj.get_player_range(DICT_OPPOSITE_PLAYER_NUM[current_node.get_player_num()])
                children_list = [int(i) for i in xrange(start_index, end_index, reverse)] if cutoff_depth != depth else []

                player_num = DICT_OPPOSITE_PLAYER_NUM[current_node.get_player_num()]
                method_name = dict_opposite_method[current_node.get_method_name()]
                if cutoff_depth != depth:
                    if method_name == 'max': value = MAX_DEFAULT_VALUE
                    if method_name == 'min': value = MIN_DEFAULT_VALUE
                else:
                    value = current_node_copy.get_board().get_eval_score(main_player)
                next_move = False

            current_node_copy.set_children_list(children_list)
            current_node_copy.set_method_name(method_name)
            current_node_copy.set_value(value)
            current_node_copy.set_next_move(next_move)
            current_node_copy.set_player_num(player_num)
            log_file.write(current_node_copy.get_log())
            stack.appendleft(current_node_copy)
        else:
            if stack:
                parent_node = stack.popleft()
                if parent_node.get_depth() == 0:
                    num_of_runs -=1

                if parent_node.get_method_name() == 'max':
                    if parent_node.get_value() < current_node.get_value():
                        parent_node.set_value(current_node.get_value())
                        if parent_node.get_depth() == 1:
                            if current_node.get_best_state():
                                parent_node.set_best_state(current_node.get_best_state())
                            else:
                                parent_node.set_best_state(current_node.get_board())

                        if parent_node.get_depth() == 0:
                            parent_node.set_best_state(current_node.get_board())
                            if current_node.get_best_state():
                                parent_node.set_best_state(current_node.get_best_state())

                if parent_node.get_method_name() == 'min':
                    if parent_node.get_value() > current_node.get_value():
                        parent_node.set_value(current_node.get_value())
                        if parent_node.get_depth() == 1:
                            parent_node.set_best_state(parent_node.get_board())

                stack.appendleft(parent_node)
                log_file.write(parent_node.get_log())
            else:
                break

    output_file.write(root_node.get_best_state().get_board_state())
    output_file.close()
    log_file.close()

def perform_alpha_beta(board_obj, player_num, cutoff_depth):
    output_file = open('next_state.txt', 'w')
    log_file = open('traverse_log.txt', 'w')

    log_file.write('Node,Depth,Value,Alpha,Beta\n')


    name = 'root'
    value = MAX_DEFAULT_VALUE
    dict_index_name = board_obj.get_index_name()
    dict_opposite_method = {'min': 'max', 'max': 'min'}

    main_player = player_num
    start_index, end_index, reverse, other_player = board_obj.get_player_range(player_num)
    children_list = [int(i) for i in xrange(start_index, end_index, reverse)]
    num_of_runs = len(children_list)

    # set alpha beta to -infinity, infinity
    stack = deque([])
    root_node = Node(board_obj, player_num, 'max', name, value, 0, False, children_list, MAX_DEFAULT_VALUE, MIN_DEFAULT_VALUE)
    if root_node.get_board().is_game_over():
        root_node.set_children_list([])
        root_node.set_value(root_node.get_board().get_eval_score(main_player))
        root_node.set_best_state(root_node.get_board())
        log_file.write(root_node.get_alpha_beta_log())
    else:
        log_file.write('root,0,-Infinity,-Infinity,Infinity\n')

    stack.appendleft(root_node)

    while(num_of_runs):
        current_node = stack.popleft()
        if current_node.get_children_list():
            current_node_copy = copy.deepcopy(current_node)
            if current_node.get_next_move():
                depth = current_node.get_depth()
            else:
                depth = current_node.get_depth()+1

            child_index = current_node.get_children_list().pop(0)
            stack.appendleft(current_node)

            if current_node.get_board().get_value_at_index(child_index) == 0:
                continue

            extra_move, pit_empty = current_node_copy.get_board().next_turn(current_node.get_player_num(), child_index)
            current_node_copy.set_best_state(None)
            current_node_copy.set_name(dict_index_name[child_index])
            current_node_copy.set_depth(depth)

            if current_node_copy.get_board().is_game_over():
                value = current_node_copy.get_board().get_eval_score(main_player)
                children_list = []
                current_node_copy.set_children_list(children_list)
                current_node_copy.set_value(value)
                log_file.write(current_node_copy.get_alpha_beta_log())
                #TODO: consider this case
                stack.appendleft(current_node_copy)
                continue

            elif extra_move:
                start_index, end_index, reverse, other_player = board_obj.get_player_range(current_node.get_player_num())
                children_list = [int(i) for i in xrange(start_index, end_index, reverse)]
                method_name = current_node.get_method_name()
                #if cutoff_depth != depth:
                if method_name == 'max': value = MAX_DEFAULT_VALUE
                if method_name == 'min': value = MIN_DEFAULT_VALUE
                #else:
                #    value = current_node_copy.get_board().get_eval_score(main_player)
                next_move = True
                player_num = current_node.get_player_num()
            else:
                start_index, end_index, reverse, other_player = board_obj.get_player_range(DICT_OPPOSITE_PLAYER_NUM[current_node.get_player_num()])
                children_list = [int(i) for i in xrange(start_index, end_index, reverse)] if cutoff_depth != depth else []

                player_num = DICT_OPPOSITE_PLAYER_NUM[current_node.get_player_num()]
                method_name = dict_opposite_method[current_node.get_method_name()]
                if cutoff_depth != depth:
                    if method_name == 'max': value = MAX_DEFAULT_VALUE
                    if method_name == 'min': value = MIN_DEFAULT_VALUE
                else:
                    value = current_node_copy.get_board().get_eval_score(main_player)
                next_move = False

            current_node_copy.set_children_list(children_list)
            current_node_copy.set_method_name(method_name)
            current_node_copy.set_value(value)
            current_node_copy.set_next_move(next_move)
            current_node_copy.set_player_num(player_num)
            log_file.write(current_node_copy.get_alpha_beta_log())
            stack.appendleft(current_node_copy)
        else:
            if stack:
                parent_node = stack.popleft()
                if parent_node.get_depth() == 0:
                    num_of_runs -=1

                if parent_node.get_method_name() == 'max':
                    if parent_node.get_value() < current_node.get_value():
                        parent_node.set_value(current_node.get_value())
                        if parent_node.get_depth() == 1:
                            if current_node.get_best_state():
                                parent_node.set_best_state(current_node.get_best_state())
                            else:
                                parent_node.set_best_state(current_node.get_board())
                        if parent_node.get_depth() == 0:
                            parent_node.set_best_state(current_node.get_board())
                            if current_node.get_best_state():
                                parent_node.set_best_state(current_node.get_best_state())

                    #handle the alpha case
                    if parent_node.get_value() >= parent_node.get_beta():
                        parent_node.set_children_list([])

                    elif parent_node.get_value() > parent_node.get_alpha():
                        parent_node.set_alpha(parent_node.get_value())


                if parent_node.get_method_name() == 'min':
                    if parent_node.get_value() > current_node.get_value():
                        parent_node.set_value(current_node.get_value())
                        if parent_node.get_depth() == 1:
                            parent_node.set_best_state(parent_node.get_board())

                    # handle the beta case
                    if parent_node.get_value() <= parent_node.get_alpha():
                        parent_node.set_children_list([])

                    elif parent_node.get_value() < parent_node.get_beta():
                        parent_node.set_beta(parent_node.get_value())

                stack.appendleft(parent_node)
                log_file.write(parent_node.get_alpha_beta_log())
            else:
                break

    output_file.write(root_node.get_best_state().get_board_state())
    output_file.close()
    log_file.close()


DICT_NUM_TO_TASK = { 1: perform_greedy,
                     2: perform_minimax,
                     3: perform_alpha_beta,
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
    method_name, player_num, cutoff_depth, obj = read_file(file_obj)
    DICT_NUM_TO_TASK[method_name](obj, player_num, cutoff_depth)
