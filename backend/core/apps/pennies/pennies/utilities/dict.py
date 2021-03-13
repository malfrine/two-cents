from typing import Any


def get_value_from_dict(key, d: dict):
    if key not in d:
        raise ValueError(f"{key} not in dictionary: {d}")
    return d[key]


def remove_from_dict(key, d: dict):
    if key not in d:
        raise ValueError(f"{key} not in dictionary: {d}")
    d.pop(key)


def add_to_dict(key, d: dict, value: Any):
    if key in d:
        raise ValueError(f"{key} already exists in dictionary: {d}")
    d[key] = value
