"""
    This script implements the Gale Shapley algorithm which finds stable matchings for a given set of men and women with
    each having their own preference set.

    This particular script assumes equal number of male and female. Also, the preference list for each man/woman is
    assumed to contain all the entries i.e. none of preference is partial.


"""
import random


def read_input_file(input_file_location):
    dict_male_preference = {}
    dict_female_preference = {}
    input_file = open(input_file_location, 'r')

    for line in input_file:
        elements = line.strip().split(' ')
        if elements[0] == 'M':
            dict_male_preference[elements[1]] = elements[2].split(',')
        else:
            dict_female_preference[elements[1]] = elements[2].split(',')

    return dict_male_preference, dict_female_preference

def write_output_file(output_file_location, dict_mapping):
    output_file = open(output_file_location, 'w')

    for key, value in dict_mapping.iteritems():
        #print value, key
        output_file.write('%s,%s\n' %(value, key))

    output_file.close()


def create_mappings(dict_male_preference, dict_female_preference):
    dict_mapping = {}
    male_list = list(dict_male_preference.keys())

    while male_list:
        current_male = random.choice(male_list)
        male_list.remove(current_male)

        male_preference_list = dict_male_preference[current_male]

        for female in male_preference_list:
            if dict_mapping.has_key(female):
                female_preference_list = list(dict_female_preference[female])
                #check preference order
                if female_preference_list.index(current_male) < female_preference_list.index(dict_mapping[female]):
                    male_list.append(dict_mapping[female])
                    dict_mapping[female] = current_male
                    break
            else:
                dict_mapping[female] = current_male
                break

        female_index = male_preference_list.index(female)
        dict_male_preference[current_male] = male_preference_list[female_index+1:]

    return dict_mapping


if __name__=='__main__':
    dict_male_preference, dict_female_preference = read_input_file("preference_list.txt")
    dict_mapping = create_mappings(dict_male_preference, dict_female_preference)
    write_output_file("mapping_list.txt", dict_mapping)