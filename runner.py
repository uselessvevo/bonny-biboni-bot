import importlib

from CloudyKit.Core.settings import Global


def main():
    if Global.get('bot_token', None) is None:
        raise Exception('Bot token is empty!')

    application = importlib.import_module(Global.get('module')[0])
    application = getattr(application, Global.get('module')[1])()


if __name__ == '__main__':
    main()
