def clear_empty_strings(input_list: list[str]) -> list[str]:
    return [item for item in input_list if item.strip()]