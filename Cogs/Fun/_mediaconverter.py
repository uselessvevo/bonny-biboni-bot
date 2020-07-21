"""
Description: ffmpeg functions
Version: 0720/prototype
Author: useless_vevo
"""
import os
import random
import subprocess
from pathlib import Path

from collections import OrderedDict

from Tools.Core.settings import Global

from ._tools import hash_filename


class AudioConverter:
    _ffmpeg = Global.get('ffmpeg_path', 'ffmpeg')  # ffmpeg command or path
    _sounds = os.path.join(os.path.dirname(__file__), 'Resources', 'Sounds')  # sounds directory
    _files_map = OrderedDict({})  # files map (filename : file path, ...)
    _is_filled = False  # eh?

    @classmethod
    def init(cls):
        if cls._is_filled:
            raise RuntimeError('Files map (files_map) is already filled')

        for file in Path(cls._sounds).rglob('*.*'):
            section = file.parts[-2]
            if not cls._files_map.get(section):
                cls._files_map[section] = {}
            cls._files_map[section].update({file.stem: file.as_posix()})
        cls._is_filled = True

    @classmethod
    async def get_alphabet(cls, section):
        return cls._files_map.get(section)

    @classmethod
    async def _concatenate_files(cls, files):
        output_file = hash_filename(str(random.random()), prefix=str(random.random()), file_format='mp3')
        output_file = os.path.join(os.path.dirname(__file__), 'Resources', 'Sounds', output_file)
        # ffmpeg -i "concat:file1.wav|file2.wav| . . ." -c copy hashed_file.wav
        command = f'{cls._ffmpeg} -i "concat:{"|".join(files)}" -c copy "{output_file}"'

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.wait()

        return {'output': output_file, 'code': process.returncode}

    @classmethod
    async def text_to_speech(cls, section, *text):
        """
        Convert text to speech (audio)
        Args:
            section (str) - directory name (f.e. "hl vox")
            text (str) - text to convert. If not found - return default value from dict
        Returns:
            hashed file path
        """
        if not cls._files_map.get(section):
            return False
        return await cls._concatenate_files([cls._files_map[section].get(t.strip()) for t in text])


AudioConverter.init()
