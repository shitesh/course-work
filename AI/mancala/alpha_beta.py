from minimax import *



def perform_alpha_beta(board_obj, player_num, cutoff_depth):
    output_file = open('next_state.txt', 'w')
    log_file = open('traverse_log.txt', 'w')

    log_file.write('Node,Depth,Value,Alpha,Beta\n')
    log_file.write('root,0,-Infinity,-Infinity,Infinity\n')

    name = 'root'
    value = MAX_DEFAULT_VALUE
    dict_index_name = board_obj.get_index_name()
    dict_opposite_method = {'min': 'max', 'max': 'min'}

    main_player = player_num
    start_index, end_index, reverse, other_player = board_obj.get_player_range(player_num)
    children_list = [int(i) for i in xrange(start_index, end_index, reverse)]
    num_of_runs = len(children_list)

    # set alpha beta to -infinity, infinity
    root_node = Node(board_obj, player_num, 'max', name, value, 0, False, children_list, MAX_DEFAULT_VALUE, MIN_DEFAULT_VALUE)
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
