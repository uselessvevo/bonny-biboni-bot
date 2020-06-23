"""
Description: useful tools
Version: 0620/prototype
Author: useless_vevo
"""
# Base standard libraries
import os
import time
from pathlib import Path

# Standard libraries for discord


def get_relative_path(*path):
    path = os.path.join(*path)
    return str(path).replace(os.sep, '/')


def get_posix_path(*path):
    return Path(*path).as_posix()


def get_filename_extension(file):
    return Path(file).suffix


def get_filename_without_extension(file):
    return Path(file).stem


def get_filename_path(file):
    return os.path.split(file)[0]


def normalize_module_path(path):
    return path.replace('.', os.sep)


def touch(path, make_dir=True):
    if not os.path.exists(path):
        folder = os.path.dirname(os.path.abspath(path))
        if make_dir:
            os.makedirs(folder)

        with open(path, 'a'):
            os.utime(path, None)


def remove_file(*path):
    file = Path(*path).absolute()

    if file.exists():
        os.remove(file)
        return file

    return False


def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts) * 1000)
        else:
            print('%r  %2.2f ms' % (method.__name__, (te - ts) * 1000))

        return result

    return timed
