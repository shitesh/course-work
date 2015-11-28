import argparse
import copy
import itertools
import re
import os

from collections import deque

dict_KB = {}
tautology_dict = {}
query_list = []
stack = deque([])
infinite_loop_detector = []

def backward_chaining(goal_list, dict_mapping, level=0):
    new_goals = []
    answers_list = []

    if not goal_list:
        answers_list.append(dict_mapping)
        return answers_list

    current_goal = goal_list.pop(0)

    current_goal = substitute(dict_mapping, current_goal)
    if current_goal in infinite_loop_detector:
        return answers_list

    infinite_loop_detector.append(current_goal)

    operator, arg_list, is_negated = get_operator_parameters(current_goal)
    all_sentences = dict_KB.get(operator)
    for sentence in all_sentences:
        print 'considering %s' %(sentence)
        lhs, rhs = standardize_variables(sentence)
        dict_mapping_copy = copy.deepcopy(dict_mapping)
        unify(current_goal, rhs, dict_mapping_copy)
        print 'mapping: %s' %(dict_mapping_copy)
        if dict_mapping_copy:

            if not lhs and len(new_goals) > 0:
                new_goals.extend(goal_list)
                lower_level_answers = backward_chaining(copy.deepcopy(new_goals), copy.deepcopy(dict_mapping_copy),level+1)
                for answer in lower_level_answers:
                    answers_list.append(answer)
            elif not lhs and len(new_goals) == 0:
                answers_list.append(dict_mapping)
            else:
                new_goals.extend(lhs)
                new_goals.extend(goal_list)
                lower_level_answers = backward_chaining(copy.deepcopy(new_goals), copy.deepcopy(dict_mapping_copy), level+1)
                if not lower_level_answers:
                    new_goals = []
                for answer in lower_level_answers:
                    answers_list.append(answer)
        else:
            new_goals = []
    return answers_list

def is_symbol(s):
    return isinstance(s, str) and s[:1].isalpha()

def is_variable(s):
    return is_symbol(s) and s[0].islower()

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

def get_operator_parameters(clause):
    m = re.search(r"\((.*)\)", clause)
    arg_list =  str(m.group(1)).split(',')
    operator = clause.split('(')[0]
    is_negated = False
    if operator[0] == '~':
        #todo: do we need to do this
        is_negated = True

    arg_list = [arg.strip() for arg in arg_list]
    return operator.strip(), arg_list, is_negated

def process_clause(clause):
    global tautology_dict, dict_KB
    if '=>' in clause:
        all_predicate, consequent = clause.split('=>')
        operator, arg_list, is_negated = get_operator_parameters(consequent)
    else:
        operator, arg_list, is_negated = get_operator_parameters(clause)

    clause_list = dict_KB.setdefault(operator.strip(), [])
    clause_list.append(clause)

def read_file(file_obj):
    num_queries = int(file_obj.readline())
    count = 0
    while count < num_queries:
        query_list.append(file_obj.readline().strip())
        count += 1

    num_clauses = int(file_obj.readline().strip())
    count = 0
    while count < num_clauses:
        clause = file_obj.readline().strip()
        process_clause(clause)
        count += 1

def unify(variable, goal, dict_mapping):
    temp_dict = {}
    print 'inside unify'
    print variable
    print goal
    operator, variable_list1, is_negated = get_operator_parameters(variable)
    operator, variable_list2, is_negated = get_operator_parameters(goal)

    for index in xrange(0, len(variable_list1)):
        if is_variable(variable_list1[index]):
            dict_mapping[variable_list1[index]] = variable_list2[index]
            continue
        if is_variable(variable_list2[index]):
            dict_mapping[variable_list2[index]] = variable_list1[index]
            continue
        if variable_list1[index] != variable_list2[index]:
            dict_mapping.clear()
            break

def is_valid(operator, arg_list):
    if tautology_dict.has_key(operator) and arg_list in tautology_dict.get(operator):
        return True
    return False

def substitute(dict_substitution, clause):
    operator, arg_list, is_negated = get_operator_parameters(clause)

    substituted_arg = []
    for arg in arg_list:
        if is_variable(arg) and dict_substitution.has_key(arg):
            substituted_arg.append(dict_substitution[arg])
        else:
            substituted_arg.append(arg)

    new_arg_str = ','.join([str(x) for x in substituted_arg])
    result = '%s(%s)' %(operator, new_arg_str)
    return result


def standardize_variables(rule):
    if '=>' not in rule:
        predicates_list = []
        cons_operator, cons_arg_list, is_negated = get_operator_parameters(rule)
    else:
        all_predicate, consequent = rule.split('=>')
        predicates_list = all_predicate.split('^')
        cons_operator, cons_arg_list, is_negated = get_operator_parameters(consequent)

    variable_list = []
    variable_list.extend(cons_arg_list)
    for predicate in predicates_list:
        operator, arg_list, is_negated = get_operator_parameters(predicate.strip())
        variable_list.extend(arg_list)

    variable_list = list(set(variable_list))
    dict_mapping = {}
    for variable in variable_list:
        if is_variable(variable):
            dict_mapping[variable] = 'v%d' %(standardize_variables.counter.next())
        else:
            dict_mapping[variable] = variable

    rhs = '%s(%s)'%(cons_operator, ','.join(str(dict_mapping[variable]) for variable in cons_arg_list))
    lhs = []
    for predicate in predicates_list:
        operator, arg_list, is_negated = get_operator_parameters(predicate)
        standardize_predicate = '%s(%s)' %(operator, ','.join(str(dict_mapping[x]) for x in arg_list))
        lhs.append(standardize_predicate)

    return lhs, rhs

standardize_variables.counter = itertools.count()

def fol_bc_ask(query):
    answer_list = backward_chaining(query, {})
    print 'answer %s'%(answer_list)
    if answer_list:
        return 'TRUE'
    else:
        return 'FALSE'


if __name__ == '__main__':
    file_obj = read_command_line()
    read_file(file_obj)
    out_file = open('output.txt', 'w')
    for query in query_list:
        print 'processing %s'%(query)
        result = fol_bc_ask([query])
        out_file.write('%s\n' %(result))


    out_file.close()
