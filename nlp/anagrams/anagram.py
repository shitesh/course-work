# Write a Python program which will take a string as the first parameter, and write an output file called
# anagram_out.txt which contains of all the anagrams (permutations) of the string, one per line, sorted alphabetically.
import sys


def print_word(out_file, input_list):
    word = ''.join([chr(input) for input in input_list])
    out_file.write('%s\n' % word)

def get_next_word_list(input_list):
    max_index = -1*len(input_list) - 1
    current_index, next_index = None, None
    for index in xrange(-1, max_index, -1):
        next_index = index - 1
        if next_index == max_index:
            return None
        if input_list[next_index] < input_list[index]:
            current_index = next_index
            break

    min_right_index = current_index + 1
    for index in xrange(current_index+1, 0):
        if input_list[current_index] < input_list[index] < input_list[min_right_index]:
            min_right_index = index

    if input_list[min_right_index] > input_list[current_index]:
        input_list[current_index], input_list[min_right_index] = input_list[min_right_index], input_list[current_index]
        input_list = input_list[:current_index+1]+input_list[current_index + 1:][::-1]
        return input_list

    return None


def process_string_for_anagram(input_str, out_file):
    input_list = list(input_str)
    input_list = [ord(char) for char in input_list]

    input_list.sort()
    print_word(out_file, input_list)

    while input_list:
        next_word_list = get_next_word_list(input_list)
        if not next_word_list:
            break
        print_word(out_file, next_word_list)
        input_list = next_word_list

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Usage: python anagram.py <word>'
        sys.exit(1)
    out_file = open('anagram_out.txt', 'w')
    process_string_for_anagram(sys.argv[1], out_file)
    out_file.close()