from telefone import Blueprint

# Make a blueprint of a bot.
bp = Blueprint()


@bp.on.message(text=["hi", "hello", "hey<!>"])
async def hi_handler(_) -> str:
    return "Glad to see you!"


@bp.on.message(text=["good morning", "good afternoon", "good evening"])
async def hello_handler(_) -> str:
    return "Welcome!"
