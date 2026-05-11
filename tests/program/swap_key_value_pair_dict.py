input_dict=eval(input())
def swap_key_value_pairs(input_dict):
    swapped_dict = {}

    for key, value in input_dict.items():
        swapped_dict[value] = key

    return swapped_dict

result = swap_key_value_pairs(input_dict)
print(result)