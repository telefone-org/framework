from telefone import BaseStateGroup, Bot, BotUpdateType, Message
from telefone.tools.keyboard import InlineButton, InlineKeyboard

from telefone_types.updates import CallbackQueryUpdate

# Make a bot with a token from an environment variable.
bot = Bot(__import__("os").getenv("token"))

# Declare a dialog flow of questionnaire.
class QuestionnaireState(BaseStateGroup):
    NAME, AGE, THING = "name", "age", "thing"


# Make a keyboard for picking a favorite thing.
THING_KEYBOARD = (
    InlineKeyboard()
    .add(InlineButton("👟 Shoe", callback_data="a shoe"))
    .row()
    .add(InlineButton("🏓 Racket", callback_data="a racket"))
    .add(InlineButton("💣 Bomb", callback_data="a bomb"))
    .get_markup()
)


@bot.on.message(command="start")
async def start_handler(msg: Message) -> None:
    # Start conversation with the user.
    await msg.answer(
        "Hi! I am a regular bot. Nothing special about me. "
        "I really want to become your friend!\n\n"
        "Tell me about yourself. What's your name?"
    )
    await bot.state_dispenser.set(msg.from_.id, QuestionnaireState.NAME)


@bot.on.message(state=QuestionnaireState.NAME)
async def name_handler(msg: Message) -> None:
    # Handle name entered by user.
    if not msg.text.isalpha():
        await msg.answer(
            "Your name must be alphabetic. "
            "I recognize and appreciate your uniqueness, but "
            "it's hard for me to believe there are actual people named like that."
        )
        return

    await msg.answer(f"So nice to see you, {msg.text}. How old are you?")
    await bot.state_dispenser.set(msg.from_.id, QuestionnaireState.AGE, name=msg.text)


@bot.on.message(state=QuestionnaireState.AGE)
async def age_handler(msg: Message) -> None:
    # Get a value from state context.
    name = msg.state_peer.payload["name"]

    # Handle age entered by user.
    if not msg.text.isdigit():
        await msg.answer(
            "Your age must be a number. How would it even be something else?"
        )
        return

    await msg.answer(
        f"{msg.text} years old? That's a great age! How about your favorite thing?",
        reply_markup=THING_KEYBOARD,
    )
    await bot.state_dispenser.set(
        msg.from_.id, QuestionnaireState.THING, name=name, age=int(msg.text)
    )


@bot.on.raw_update(
    BotUpdateType.CALLBACK_QUERY, CallbackQueryUpdate, state=QuestionnaireState.THING
)
async def final_handler(upd: CallbackQueryUpdate) -> None:
    # Get both values from state context.
    name = upd.state_peer.payload["name"]
    age = upd.state_peer.payload["age"]

    # Handle favorite thing entered by user.
    await upd.ctx_api.edit_message_text(
        upd.from_.id, upd.message.message_id, text="Alright."
    )
    await upd.ctx_api.send_message(
        upd.from_.id,
        f"Your name is {name} and you are {age} years old. Your favorite thing is {upd.data}. "
        "Your data will be shamelessly used for advertisement purposes. Goodbye.",
    )

    await bot.state_dispenser.delete(upd.from_.id)


bot.run_forever()
