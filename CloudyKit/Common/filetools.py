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


def read_json_many(*files, keys=None):
    """
    Args:
        files (str|tuple|list) - filename
        keys (any type) - if you don't want to automatically create keys from filename
        if the number of files is not equal to the number of keys it will raise QuanityError
    """
    # Clear duplicates
    files = list(set(files))
    collect = {}

    if keys is not None and len(files) != keys:
        raise Exception('The number of files is not equal to the number of keys')

    for index, file in enumerate(files):
        # make key from filename without extension
        key = os.path.normpath(file).split(os.sep)[-1].split('.')[0]
        if os.path.exists(file):
            with open(file, encoding="utf-8") as output:
                collect[key] = json.load(output)
        else:
            collect[key] = {}

    return collect


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
