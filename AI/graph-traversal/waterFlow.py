import argparse
import os
from collections import deque
from heapq import heappush, heappop

class UCSPriorityQueue(object):
    def __init__(self):
        self.node_dict = {}
        self.cost_dict = {}
        self.cost_list = []

    def update_costs(self, node_name, path_cost):
        if path_cost in self.cost_dict:
            self.cost_dict[path_cost].append(node_name)
            self.cost_dict[path_cost].sort()
        else:
            self.cost_dict[path_cost] = [node_name]
            heappush(self.cost_list, path_cost)

    def insert(self, node_name, path_cost):
        if node_name in self.node_dict:
            current_cost = self.node_dict[node_name]
            if path_cost < current_cost:
                self.node_dict[node_name] = path_cost

                #update cost_dict and cost list with latest path costs
                self.update_costs(node_name, path_cost)

                # remove node name from current cost value in cost_list
                node_list = self.cost_dict[current_cost]
                node_list.delete(node_name)
                if not node_list:
                    del(self.cost_dict[current_cost])
                    self.cost_list.remove(current_cost)
                else:
                    self.cost_dict[current_cost] = node_list
        else:
            self.node_dict[node_name] = path_cost
            self.update_costs(node_name, path_cost)

    def pop_next(self):
        if self.cost_list:
            cost = heappop(self.cost_list)
            node_name_list = self.cost_dict.get(cost)
            node_name = node_name_list[0]
            del(self.node_dict[node_name])
            del(node_name_list[0])

            if node_name_list:
                heappush(self.cost_list, cost)
                self.cost_dict[cost] = node_name_list
            else:
                del(self.cost_dict[cost])
            return node_name
        return None

def perform_ucs():
    #todo: what if the total cost of two paths become same
    pass

def perform_dfs(test_dict):
    stack = deque([])
    visited_list = []

    source_node = test_dict['source_node']
    adjacency_dict = test_dict['adjacency_dict']
    destination_node_list = test_dict['destination_node_list']
    start_time = test_dict['start_time']

    path_cost = start_time - 1
    stack.appendleft(source_node)
    visited_list.append(source_node)

    while stack:
        current_node = stack.popleft()
        path_cost += 1

        if current_node in destination_node_list:
            return current_node, path_cost

        if current_node in adjacency_dict:
            for node in adjacency_dict[current_node]:
                if node not in visited_list:
                    stack.appendleft(node)
                    visited_list.append(node)
    # program reached here means parsing is over and none of the goal states are reached
    return None, -1

def perform_bfs(test_dict):
    #todo: not maintaining an explored set as it is not required in this case. check on this.
    queue = deque([])
    visited_list = []

    source_node = test_dict['source_node']
    adjacency_dict = test_dict['adjacency_dict']
    destination_node_list = test_dict['destination_node_list']
    start_time = test_dict['start_time']

    path_cost = start_time - 1
    queue.appendleft(source_node)
    visited_list.append(source_node)
    while queue:
        current_node = queue.popleft()
        path_cost += 1

        if current_node in destination_node_list:
            return current_node, path_cost

        if current_node in adjacency_dict:
            for node in adjacency_dict[current_node]:
                if node not in visited_list:
                    queue.append(node)
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
        if not output:
            output_file_obj.write("None")
        else:
            output_file_obj.write("%s %s\n"%(output, time))
    output_file_obj.close()
