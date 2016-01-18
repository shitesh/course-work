import sys


def int_to_binary(value):
    bit_list = []

    while value:
        bit = value % 2
        bit_list.append(bit)
        value /= 2
    return bit_list   # returning values in reverse order as this will help in traversal later


def get_num_bytes(value):
    if value <= 127:
        pattern = [0]
        pattern.extend([-1]*7)
        return pattern

    elif value <= 2047:
        pattern = [1, 1, 0]
        pattern.extend([-1]*5)
        pattern.extend([1, 0])
        pattern.extend([-1]*6)
        return pattern

    elif value <= 65535:
        pattern = [1, 1, 1, 0]
        pattern.extend([-1]*4)
        pattern.extend([1, 0])
        pattern.extend([-1]*6)
        pattern.extend([1, 0])
        pattern.extend([-1]*6)
        return pattern

    else:
        # not handling this case as this is not a valid case as per the requirement
        return None


def get_byte_list(value):
    value_binary = int_to_binary(value)

    pattern = get_num_bytes(value)
    if not pattern:
        return pattern

    pattern_index = -1
    max_pattern_index = -1 * len(pattern)

    for bit in value_binary:
        while pattern_index >= max_pattern_index and pattern[pattern_index] != -1:
            pattern_index -= 1
        if pattern_index >= max_pattern_index:
            pattern[pattern_index] = bit

    pattern = [0 if bit == -1 else bit for bit in pattern]
    return pattern


def get_int_value(content):
    return ord(content[0])*256 + ord(content[1])


def get_byte_char(byte_list):
    char_list = []
    num_bytes = len(byte_list)/8
    start_index = 0
    while num_bytes:
        char_list.append(chr(int(''.join(str(bit) for bit in byte_list[start_index: start_index+8]), 2)))
        num_bytes -= 1
        start_index += 8
    return ''.join(char_list)


def process_file(input_file_location):
    output_file_location = 'utf8encoder_out.txt'
    out_file = open(output_file_location, 'wb')

    with open(input_file_location, 'rb') as file:
        content = file.read(2)
        while content:
            content_int_val = get_int_value(content)
            byte_list = get_byte_list(content_int_val)
            if not byte_list:
                out_file.write('\nINVALID INPUT DATA\n')
            out_file.write(get_byte_char(byte_list))
            content = file.read(2)

    out_file.close()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print'Please provide the input file name.'
    # not the ideal way. should have -i to read input file. but this is what is given in the problem.
    process_file(sys.argv[1])
