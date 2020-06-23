"""
Description: Main constants
Version: 0620/prototype
Author: useless_vevo
"""
# Common
from CloudyKit.Common.filetools import write_json
from CloudyKit.Common.filetools import read_json


def _get_global_settings():
    """ Read CloudyKit/Configs/global.json """
    from pathlib import Path

    config_file = f'CloudyKit/Configs/global.json'
    if not Path(config_file).exists():
        write_json(config_file, {})

    settings = read_json(config_file)
    return settings


Global = _get_global_settings()
