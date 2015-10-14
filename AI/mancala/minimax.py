import argparse
import copy
import os
from mancala import BoardGame
from collections import deque

MIN_DEFAULT_VALUE = 10000
MAX_DEFAULT_VALUE = -10000

stack = deque([])
DICT_OPPOSITE_PLAYER_NUM = {1: 2, 2: 1}

class Node(object):

    def __init__(self, board_obj, player_num, method, name, value, depth, next_move, children_list):
        self.board_obj = board_obj
        self.player_num = player_num
        self.method = method
        self.name = name
        self.value = value
        self.next_move = next_move
        self.depth = depth
        self.children_list = children_list
        self.best_state = None

    def get_debug(self):
        return '%s,%s,%s' %(self.name, self.depth, self.value)

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

    def set_best_state(self, best_state):
        self.best_state = best_state

def perform_minimax(board_obj, player_num, cutoff_depth, current_depth=0):
    name = 'root'
    value = MAX_DEFAULT_VALUE
    dict_index_name = board_obj.get_index_name()
    dict_opposite_method = {'min': 'max', 'max': 'min'}
    dict_opposite_val = {MIN_DEFAULT_VALUE: MAX_DEFAULT_VALUE, MAX_DEFAULT_VALUE: MIN_DEFAULT_VALUE}

    main_player = player_num
    start_index, end_index, reverse, other_player = board_obj.get_player_range(player_num)
    children_list = [int(i) for i in xrange(start_index, end_index, reverse)]
    num_of_runs = len(children_list)

    root_node = Node(board_obj, player_num, 'max', name, value, 0, False, children_list)
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
            current_node_copy.set_name(dict_index_name[child_index])
            current_node_copy.set_depth(depth)

            if extra_move:
                start_index, end_index, reverse, other_player = board_obj.get_player_range(current_node.get_player_num())
                children_list = [int(i) for i in xrange(start_index, end_index, reverse)]
                method_name = current_node.get_method_name()
                if cutoff_depth != depth:
                    if method_name == 'max': value = MAX_DEFAULT_VALUE
                    if method_name == 'min': value = MIN_DEFAULT_VALUE
                else:
                    value = current_node_copy.get_board().get_eval_score(main_player)
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
            print current_node_copy.get_debug()
            stack.appendleft(current_node_copy)
        else:
            if stack:
                parent_node = stack.popleft()

                if parent_node.get_method_name() == 'max':
                    if parent_node.get_value() < current_node.get_value():
                        parent_node.set_value(current_node.get_value())
                        if parent_node.get_depth() == 1:
                            parent_node.set_best_state(current_node.get_board())
                        if parent_node.get_depth() == 0:

                            num_of_runs -=1
                            parent_node.set_best_state(current_node.get_best_state())

                if parent_node.get_method_name() == 'min':
                    if parent_node.get_value() > current_node.get_value():
                        parent_node.set_value(current_node.get_value())
                        if parent_node.get_depth() == 1:
                            parent_node.set_best_state(parent_node.get_board())

                stack.appendleft(parent_node)
                print parent_node.get_debug()
            else:
                break

    print root_node.get_best_state().get_board_state()


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
    perform_minimax(obj, player_num, cutoff_depth)
