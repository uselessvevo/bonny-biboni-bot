import os
import importlib

from Tools.Core.settings import Global
from Tools.Common.i18n import Locales


def main():
    # Do I need to make "to_check" fields and iter through keys
    # those and keys of global settings?
    if os.name == 'nt' and not os.getenv('MAGICK_HOME'):
        raise EnvironmentError('ImageMagick env var not found')
    if not Global.get('bot_token', None):
        raise Exception('Bot token is empty!')

    Locales.load_aliases()
    Locales.load_translations()

    # Should I add token argument?
    application = importlib.import_module(Global.get('module')[0])
    getattr(application, Global.get('module')[1])()


if __name__ == '__main__':
    main()
