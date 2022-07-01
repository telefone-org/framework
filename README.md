# Telefone framework

[//]: # (Links to examples)
[text formatting]: https://github.com/telefone-org/framework/blob/main/examples/high_level/formatting_example.py
[middleware]: https://github.com/telefone-org/framework/blob/main/examples/high_level/setup_middleware.py
[file uploading]: https://github.com/telefone-org/framework/blob/main/examples/high_level/file_upload_example.py
[blueprints]: https://github.com/telefone-org/framework/blob/main/examples/high_level/load_blueprints.py
[FSM]: https://github.com/telefone-org/framework/blob/main/examples/high_level/use_state_dispenser.py

![Current version](https://img.shields.io/pypi/v/telefone?label=Current+version&style=for-the-badge)
![Package downloads](https://img.shields.io/pypi/dw/telefone?style=for-the-badge)
![Repo size](https://img.shields.io/github/repo-size/telefone-org/framework?label=Repo+size&style=for-the-badge)

## Highlights

Telefone framework is a Python interface to Telegram Bot API. It acts as a layer of convenience, providing useful tools to build powerful bots, and has many features like [text formatting], [file uploading], [blueprints], [middleware] and [FSM].

It does all of that while maintaining high performance and blazing speed, and is also widely customizable thanks to its thought out architecture.

```bash script
pip install telefone
```

## Examples

This example shows how easy it is to build a Telegram bot. Your bot is up and running in only **six** lines of code!

```python
from telefone import Bot

bot = Bot("your-token")


@bot.on.message()
async def handler(_) -> str:
    return "Hello world!"

bot.run_forever()
```

Are you interested yet? Then check out [all of our high-level examples](https://github.com/telefone-org/framework/tree/main/examples/high_level).

## License

This project is [MIT licensed](https://github.com/telefone-org/framework/blob/main/LICENSE). Copyright © 2022 exthrempty
