def merge_tuples(tuple1, tuple2):
    # Merge the tuples
    merged_tuple = tuple1 + tuple2

    # Remove duplicates
    unique_elements = []
    for item in merged_tuple:
        if item not in unique_elements:
            unique_elements.append(item)

    # Create a new tuple with unique elements
    result_tuple = tuple(unique_elements)

    return result_tuple

t1 = eval(input())
t2 = eval(input())
print(merge_tuples(t1,t2))