import re

def find_non_numerics(my_list):
    non_numeric_indices = []
    for i, item in enumerate(my_list):
        #if not any(char.isdigit() for char in item):
        if not re.match(r'^\d+(\.\d+)?$', item):
            non_numeric_indices.append(i)
    return non_numeric_indices


def extract_kilograms(product):
    match = re.search(r'(\d+)\s*kg', product,re.IGNORECASE)
    if match:
        return match.group(1)
    return None