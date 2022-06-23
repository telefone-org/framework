try:
    emoji = __import__("emoji")
except ImportError as e:
    raise RuntimeError(
        "You need to install `emoji` package in order to use `telefone.tools.text.emoji`."
    ) from e

emojize, deemojize = emoji.emojize, emoji.demojize
