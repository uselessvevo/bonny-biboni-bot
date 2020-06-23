"""
Description: i18n module/ISO 639-2 Code (modified for the uselessbot)
Version: 0620/prototype
Author: useless_vevo
TODO:
* Migrate to OOP
* Add file handler (with parameter "auto_reload")
"""
import os
import itertools

from CloudyKit.Common.filetools import read_json

# Base tools
from CloudyKit.Common.basetools import get_filename_path
from CloudyKit.Common.basetools import normalize_module_path

# Management
from CloudyKit.Core.manager import Guilds
from CloudyKit.Core.settings import Global


class Localization:
    def __init__(self):
        self.translations = {'alias': {}}
        self.load_aliases({
            get_filename_path(normalize_module_path(i))
            for i in (*Global.get('modules_to_load'), 'Bot.bot')
        })
        self.load_translations()

    def load_aliases(self, modules):
        for module in modules:
            # Read "aliases.json" file
            data = read_json(os.path.join(module, 'Resources', 'Locales', 'aliases.json'))
            self.translations['alias'].update(data)

    def load_translations(self, locales=None, modules=None):
        if not locales:
            locales = {g.get('locale') for g in Guilds.guilds.values()}
        elif isinstance(locales, (list, tuple)):
            locales = set(locales)
        else:
            raise TypeError(f'Locales must be list or tuple type. Got {type(locales)}')

        if not modules:
            modules = {*Global.get('modules_to_load'), 'Bot.bot'}
        elif isinstance(modules, (list, tuple)):
            modules = set(modules)
        else:
            raise TypeError(f'Modules must be list or tuple type. Got {type(modules)}')

        for module in modules:
            for locale in locales:
                if locale not in self.translations:
                    self.translations.update({locale: {}})

                self.translations[locale].update(
                    read_json(os.path.join(module, 'Resources', 'Locales', f'{locale}.json'))
                )


Locales = Localization()


def tr(text, ctx=None, emoji=False, emoji_side=0, spaces=3, **kwargs):
    """
    Get translated string
    Args:
        text (str) - translatable string
        ctx (discord context)
        emoji (bool or str) - emoji key name
        emoji_side (int) - emoji side in string; left - 0, right - 1
        spaces (int) - space between string and emoji
        kwargs arguments for text format
    Returns:
        formatted string or empty dict
    """
    # Get guild locale from ctx
    # If DMs
    if ctx and ctx.guild:
        locale = Guilds.get_guild_info(ctx.guild.id, 'locale', 'eng')
        text = Locales.translations[locale].get(text, text)
    else:
        text = Locales.translations[Global.get('default_locale')].get(text, text)
    text = text.format(**kwargs)

    if isinstance(emoji, str):
        if emoji_side == 0:
            text = f'{text}{" " * spaces}:{emoji}:'
        elif emoji_side == 1:
            text = f':{emoji}:{" " * spaces}{text}'

    return text


def alias(key):
    return Locales.translations.get('alias', {}).get(key, [])
