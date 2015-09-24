import argparse
import os
from collections import deque
from heapq import heappush, heappop, heapify

class UCSPriorityQueue(object):
    def __init__(self):
        self.node_dict = {}
        self.cost_list = []

    def rebuild_heap(self):
        self.cost_list = [(value, key) for key, value in self.node_dict.iteritems()]
        heapify(self.cost_list)

    def insert(self, node_name, path_cost):
        # although updating priorities and recreating heap makes more logical sense, but when number of nodes is high
        # ~1 million, it takes long time because of O(n) to rebuild heap. Hence, having duplicates and handling it in
        #pop function makes the process fast.
        if node_name in self.node_dict:
            current_cost = self.node_dict[node_name]
            if path_cost < current_cost:
                self.node_dict[node_name] = path_cost
                heappush(self.cost_list, (path_cost, node_name))
        else:
            self.node_dict[node_name] = path_cost
            heappush(self.cost_list, (path_cost, node_name))

    def pop_next(self):
        while self.cost_list:
            path_cost, node_name = heappop(self.cost_list)
            if self.node_dict[node_name]!= path_cost:
                continue
            return node_name, path_cost

        return None, 0

    def has_elements(self):
        if self.cost_list:
            return True
        return False


def is_pipe_open(time, off_time_list):
    time %= 24
    for time_range in off_time_list:
        if time_range[0] <= time <= time_range[1]:
            return False
    return True


def perform_ucs(test_dict):
    priority_queue = UCSPriorityQueue()
    explored_list = []

    source_node = test_dict['source_node']
    adjacency_dict = test_dict['adjacency_dict']
    destination_node_list = test_dict['destination_node_list']
    start_time = test_dict['start_time']
    off_period_dict = test_dict['off_period_dict']

    priority_queue.insert(source_node, start_time)

    while priority_queue.has_elements():
        current_node, current_path_cost = priority_queue.pop_next()
        explored_list.append(current_node)
        if current_node in destination_node_list:
            return current_node, current_path_cost

        if current_node in adjacency_dict:
            for node, path_cost in adjacency_dict[current_node]:
                off_period_list = off_period_dict[(current_node, node)]
                if is_pipe_open(current_path_cost, off_period_list):
                    if node not in explored_list:
                        priority_queue.insert(node, current_path_cost + path_cost)
    return None, -1

def perform_dfs(test_dict):
    stack = deque([])
    visited_list = []

    source_node = test_dict['source_node']
    adjacency_dict = test_dict['adjacency_dict']
    destination_node_list = test_dict['destination_node_list']
    start_time = test_dict['start_time']

    stack.appendleft((source_node, start_time))

    while stack:
        current_node, path_cost = stack.popleft()
        if current_node in visited_list:
            continue

        visited_list.append(current_node)
        if current_node in destination_node_list:
            return current_node, path_cost

        if current_node in adjacency_dict:
            path_cost += 1
            for node in adjacency_dict[current_node]:
                if node not in visited_list:
                    stack.appendleft((node, path_cost))
    # program reached here means parsing is over and none of the goal states are reached
    return None, -1

def perform_bfs(test_dict):
    queue = deque([])
    visited_list = []

    source_node = test_dict['source_node']
    adjacency_dict = test_dict['adjacency_dict']
    destination_node_list = test_dict['destination_node_list']
    start_time = test_dict['start_time']

    queue.appendleft((source_node, start_time))
    visited_list.append(source_node)
    while queue:
        current_node, path_cost = queue.popleft()

        if current_node in destination_node_list:
            return current_node, path_cost

        if current_node in adjacency_dict:
            path_cost += 1
            for node in adjacency_dict[current_node]:
                if node not in visited_list:
                    queue.append((node, path_cost))
                    visited_list.append(node)
    # program reached here means parsing is over and none of the goal states are reached
    return None, -1

def read_file(file_obj):
    # handle exception here
    test_case_list = []
    num_test_case = int(file_obj.readline().strip())
    while num_test_case > 0:
        method_name = file_obj.readline().strip().lower()
        source_node = file_obj.readline().strip()
        destination_node_list = file_obj.readline().strip().split(' ')
        middle_node_list = file_obj.readline().strip().split(' ')

        num_pipes = int(file_obj.readline().strip())
        count = num_pipes
        adjacency_dict = {}
        off_period_dict = {}
        # different dictionary pattern for dfs/bfs and ucs as in usc path cost and timings does not matter
        if method_name in ['dfs', 'bfs']:
            while count > 0:
                line_parts = file_obj.readline().strip().split(' ')
                start_node = line_parts[0]
                end_node = line_parts[1]

                start_node_list = adjacency_dict.setdefault(start_node, [])
                start_node_list.append(end_node)
                if method_name == 'dfs':
                    start_node_list.sort(reverse=True)
                else:
                    start_node_list.sort()
                count -= 1

        elif method_name == 'ucs':
            while count>0:
                line_parts = file_obj.readline().strip().split(' ')
                start_node = line_parts[0]
                end_node = line_parts[1]

                path_length = int(line_parts[2])
                num_off_periods = int(line_parts[3])
                off_period_list = []
                if num_off_periods:
                    for off_period in line_parts[4:]:
                        start_time, end_time = map(int, off_period.split('-'))
                        off_period_list.append((start_time, end_time))

                off_period_list.sort()
                off_period_dict[(start_node, end_node)] = off_period_list

                start_node_list = adjacency_dict.setdefault(start_node, [])
                start_node_list.append((end_node, path_length))
                count -= 1


        start_time = int(file_obj.readline().strip())
        start_time %= 24
        test_case_dict = {'method_name': method_name, 'source_node': source_node, 'destination_node_list': destination_node_list,
                          'middle_node_list': middle_node_list, 'start_time': start_time, 'adjacency_dict': adjacency_dict,
                          'off_period_dict': off_period_dict
        }

        test_case_list.append(test_case_dict)
        #current test case is over, decrement number test case by 1 and read the blank line
        num_test_case -= 1
        file_obj.readline()

    return test_case_list

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        raise parser.error("Given file doesn't exist")
    else:
        return open(arg, 'r')

def read_command_line():
    parser = argparse.ArgumentParser("Plumbing System Path Finder")
    parser.add_argument("-i", dest="input_file", required=True, help="input file with required details",
                        type=lambda x: is_valid_file(parser, x))
    arguments = parser.parse_args()
    return arguments.input_file


DICT_NAME_TO_FUNC = {'dfs': perform_dfs,
                     'bfs': perform_bfs,
                     'ucs': perform_ucs
}


if __name__=='__main__':
    file_obj = read_command_line()
    # open output file
    output_file_obj = open("output.txt", 'w')

    tests_list = read_file(file_obj)
    for test_dict in tests_list:
        output, time = DICT_NAME_TO_FUNC[test_dict["method_name"]](test_dict)
        time %= 24
        if not output:
            output_file_obj.write("None\n")
        else:
            output_file_obj.write("%s %s\n"%(output, time))
    output_file_obj.close()
