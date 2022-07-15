from telefone import Blueprint

# Make a blueprint of a bot.
bp = Blueprint()

# You can add auto_rules to blueprint labeler:
# bp.labeler.auto_rules.append(SomeRule())
# You can change config for blueprint labeler locally:
# bp.labeler.vbml_ignore_case = True


@bp.on.message(text=["bye", "cheers", "<!>later<!>"])
async def bye_handler(_) -> str:
    return "See you soon!"


@bp.on.message(text=["take<!>care<!>", "have a good<!>"])
async def goodbye_handler(_) -> str:
    return "You too, bye!"
