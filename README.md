<h1 align="center">telefone</h1>

<p align="center">A modern Telegram Bot API framework built with speed and stability in mind</p>

<p align="center">
    <a href="https://pypi.org/project/telefone">
        <img src="https://img.shields.io/pypi/v/telefone?label=Current+version&style=flat-square">
    </a>
    <a href="https://github.com/telefone-org/framework">
        <img alt="GitHub repo size" src="https://img.shields.io/github/repo-size/telefone-org/framework?label=Repo+size&style=flat-square">
    </a>
    <a href="https://github.com/telefone-org/framework/blob/main/LICENSE">
        <img src="https://img.shields.io/pypi/l/telefone-types?label=License&style=flat-square">
    </a>
</p>

## Install

1) Stable version (recommended):

    ```shell script
    pip install -U telefone
    ```

2) Latest version (cutting-edge changes):

    ```shell script
    pip install -U https://github.com/telefone-org/framework/archive/main.zip
    ```

## Examples

```python
from telefone import Bot

bot = Bot("your-token")


@bot.on.message()
async def handler(_) -> str:
    return "Hello world!"

bot.run_forever()
```

## Advantages

### 🧹 Clean API

We're working hard to make the experience more flawless for developers. We have a lot better code structure and more comprehensive constructs in contrast to our competition.

### 🧑‍🔧 Frequent updates

We aim to release a feature a week, because we have a lot in planning and are as interested in developing this framework as you are in using it!

## Contributing

You can file an issue or send a PR to help us maintain this project. We are always glad to see your support. Thank you!

## License

© 2022 exthrempty
