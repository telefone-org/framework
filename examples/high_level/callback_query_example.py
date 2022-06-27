from telefone import Bot, BotUpdateType, InlineButton, InlineKeyboard, Message
from telefone_types.updates import CallbackQueryUpdate

# Make a bot with a token from an environment variable.
bot = Bot(__import__("os").getenv("token"))

# Create an inline keyboard with a button that will be used to trigger a callback.
INLINE_KEYBOARD = (
    InlineKeyboard()
    .add(InlineButton("🍎 Apple", callback_data="apple"))
    .add(InlineButton("🍊 Orange", callback_data="orange"))
    .row()
    .add(InlineButton("👟 Shoe", callback_data="shoe"))
    .get_markup()
)


@bot.on.message(command="start")
async def start_handler(msg: Message) -> None:
    # This is a handler that sends a simple inline keyboard
    # containing three buttons with their respective callback data.
    await msg.answer(
        "Pick any of these fruits on the keyboard!",
        reply_markup=INLINE_KEYBOARD,
    )


@bot.on.raw_update(
    BotUpdateType.CALLBACK_QUERY, CallbackQueryUpdate, callback_data=["apple", "orange"]
)
async def fruit_handler(upd: CallbackQueryUpdate) -> None:
    # To answer to a callback query, you can use <.answer()> method.
    # This would result in a small message showing up the screen.
    await upd.answer("You chose a fruit! Fruits are healthy and delicious 🍋")


@bot.on.raw_update(
    BotUpdateType.CALLBACK_QUERY, CallbackQueryUpdate, callback_data="shoe"
)
async def shoe_handler(upd: CallbackQueryUpdate) -> None:
    # If you need to grab user's attention, you can display an alert
    # with the content you want to show. To do that, pass `show_alert`
    # parameter to the <.answer()> method.
    await upd.answer("You chose a shoe! What the fuck", show_alert=True)


# Run loop > loop.run_forever() > with tasks created in loop_wrapper before.
# The main polling task for bot is bot.run_polling()
bot.run_forever()
