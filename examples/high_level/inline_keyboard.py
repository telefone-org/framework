from telefone import Bot, Message, InlineKeyboard, InlineButton, BotUpdateType, UpdateTypes

# Make a bot with a token from an environment variable.
bot = Bot(__import__("os").getenv("token"))
# Configure match rule to ignore case in which messages are sent.
bot.labeler.vbml_ignore_case = True


# Decorator to send inline keyboard (button)
@bot.on.message(text=["keyboard", "buttons"])
async def keyboard_handler(msg: Message):
    KEYBOARD = (
        InlineKeyboard(resize_keyboard=True)
        .add(Button(text="Hello!", callback_data="hi"))
        .get_markup()
    )
    await message.answer("Your keyboard:", reply_markup=KEYBOARD)


# You can handle CALLBACK_QUERY like this.
@bot.on.raw_update(BotUpdateType.CALLBACK_QUERY, UpdateTypes.CallbackQueryUpdate)
async def callback_handler(upd: UpdateTypes.CallbackQueryUpdate):
    # In this example you can check your callback_data.
    if upd.data == "hi":
        # We sending message to the chat  from whick we clicked on the inline button.
        await update.ctx_api.send_message(
            update.message.chat.id, "I'm working because I have callback_data = hi"
        )

# The main polling task
bot.run_forever()
