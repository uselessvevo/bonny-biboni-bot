"""
Description: file tools: json and that's it
Version: 0520/prototype
Author: useless_vevo
"""
import os
import json


def read_json(file):
    """
    Args:
        file (str or os.PathLike)
    Returns:
        dict
    """
    if os.path.exists(file):
        with open(file, encoding='utf-8') as output:
            return json.load(output)
    return {}


def write_json(file, data, mode='w+', exist_ok=False):
    """
    Args:
        data (dict) - data to save
        file (str) - file path
        mode (str) - write mode
        exist_ok (bool) - True - create file if doesn't exist
    """
    data = json.dumps(data, sort_keys=False, indent=4, ensure_ascii=False)
    with open(file, mode, encoding='utf-8') as output:
        output.write(data)
