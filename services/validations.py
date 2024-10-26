def is_str_list_effectively_empty(my_list: list[str]):
    return not my_list or all(not str(item).strip() for item in my_list)