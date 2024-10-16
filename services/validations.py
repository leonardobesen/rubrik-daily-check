def remove_empty_strings_from_list(my_list: list[str]) -> list[str]:
    return [item for item in my_list if item.strip()]