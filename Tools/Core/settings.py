"""
Description: Main constants
Version: 0620/prototype
Author: useless_vevo
"""
# Common
from Tools.Common.filetools import write_json
from Tools.Common.filetools import read_json


def _get_global_settings():
    """ Read Tools/Settings/global.json """
    from pathlib import Path

    config_file = f'Settings/global.json'
    if not Path(config_file).exists():
        write_json(config_file, {})

    settings = read_json(config_file)
    return settings


Global = _get_global_settings()
