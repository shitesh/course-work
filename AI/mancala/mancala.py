""" This script is a pythonic representation of Mancala game. Given an input file with a state, this will output the
    next steps based on greedy, minimax and alpha beta pruning concepts.

"""
import argparse
import os

def read_file(file_obj):
    pass

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
    output_file = open('output.txt', 'w')
