import argparse
import copy
import itertools
import re
import os
from collections import deque

dict_KB = {}
tautology_list = []
query_list = []
infinite_loop_detector = []
dict_predicate_variable = {}

def merge(dict1, dict2):
    dict3 = {}

    for key, value in dict1.iteritems():
        dict3[key] = value

    for key, value in dict2.iteritems():
        if not dict3.has_key(key):
            dict3[key] = value

    for key, value in dict3.iteritems():
        if is_variable(value) and dict3.has_key(value):
            dict3[key] = dict3[value]

    return dict3

def check(dict1, dict2):
    for key, value in dict1.iteritems():
        if dict1[key] != dict2[key]:
            print 'different'


def backward_chaining(goal_list, dict_mapping, level=0):
    global tautology_list
    new_goals = []
    answers_list = []

    if not goal_list:
        answers_list.append(dict_mapping)
        return answers_list

    current_goal = goal_list.pop(0)

    current_goal = substitute(dict_mapping, current_goal)

    operator, arg_list, is_negated = get_operator_parameters(current_goal)
    all_sentences = dict_KB.get(operator)

    if current_goal in infinite_loop_detector:
        return answers_list

    if current_goal.strip() not in infinite_loop_detector and current_goal.strip() not in tautology_list:
        infinite_loop_detector.append(current_goal.strip())

    for sentence in all_sentences:
        lhs, rhs = standardize_variables(sentence)
        dict_mapping_copy = copy.deepcopy(dict_mapping)
        unify(current_goal, rhs, dict_mapping_copy)

        if dict_mapping_copy:
            if not lhs and len(goal_list) > 0:
                new_goals.extend(goal_list)
                lower_level_answers = backward_chaining(copy.deepcopy(new_goals), copy.deepcopy(dict_mapping_copy))
                if not lower_level_answers:
                    new_goals = []
                for answer in lower_level_answers:
                    answers_list.append(answer)
            elif not lhs and len(goal_list) == 0:
                answers_list.append(dict_mapping_copy)
            else:
                new_goals.extend(lhs)
                new_goals.extend(goal_list)
                lower_level_answers = backward_chaining(copy.deepcopy(new_goals), copy.deepcopy(dict_mapping_copy))
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
        is_negated = True

    arg_list = [arg.strip() for arg in arg_list]
    return operator.strip(), arg_list, is_negated

def process_clause(clause):
    global tautology_list, dict_KB
    if '=>' in clause:
        all_predicate, consequent = clause.split('=>')
        operator, arg_list, is_negated = get_operator_parameters(consequent)
    else:
        tautology_list.append(clause)
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


    for key, value_list in dict_KB.iteritems():
        final_list = []
        implication_list = []
        fact_list = []
        for value in value_list:
            if '=>' in value:
                implication_list.append(value.strip())
            else:
                fact_list.append(value.strip())
        if fact_list:
            final_list.extend(fact_list)
        if implication_list:
            final_list.extend(implication_list)

        dict_KB[key] = final_list

def unify(variable, goal, dict_mapping):
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

    for key, value in dict_mapping.iteritems():
        if is_variable(value) and dict_mapping.has_key(value):
            dict_mapping[key] = dict_mapping[value]

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
    global dict_predicate_variable
    dict_existing_mapping = {}
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
    if answer_list:
        return 'TRUE'
    else:
        return 'FALSE'


if __name__ == '__main__':
    file_obj = read_command_line()
    read_file(file_obj)
    out_file = open('output.txt', 'w')
    for query in query_list:
        # clear predicate mapping and infinite loop list
        dict_predicate_variable.clear()
        infinite_loop_detector = []
        try:
            result = fol_bc_ask([query])
            out_file.write('%s\n' %(result))
        except:
            out_file.write('FALSE\n')
            continue

    out_file.close()
