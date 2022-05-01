from telefone import Bot, BotUpdateType, Message, TelegramAPIError, UpdateTypes

# Make a bot with a token from an environment variable.
bot = Bot(__import__("os").getenv("token"))
# Configure match rule to ignore case in which messages are sent.
bot.labeler.vbml_ignore_case = True


# Use message, chat_message or private_message decorators to handle
# corresponding types of messages. To define special logic you can use
# built-in rules or make your own by inheriting from tottle.dispatch.rules.abc.ABCRule.
@bot.on.private_message(text=["hi", "hello", "howdy"])
async def message_handler(_) -> str:
    # Match (text for short) rule compares previously set and newly received text and validates it.
    # After it is satisfied, following lines will be executed.

    # This line returns specific value to answer message from user
    # (see https://github.com/telefone-org/framework/blob/main/telefone/framework/dispatch/return_manager/bot/base.py).
    return "Howdy, partner!"


# A good example of how you can use this mechanic is to kick people that say inappropriate things from the chat.
# Also, in this example we'll be using another great shortcut to answer properly.
@bot.on.chat_message(lev=["shit", "fuck", "bastard", "asshole"])
async def chat_message_handler(msg: Message):
    # Levenstein (lev for short) rule measures the differences between previously set and newly received
    # string sequence. After it is satisfied, following lines will be executed.

    try:
        # This is a basic API call. Please notice that the bot.api (or blueprint api)
        # is not accessible in case multibot is used, so we strongly recommend you to use
        # ctx_apis everywhere you can.
        await bot.api.ban_chat_member(chat_id=msg.chat.id, user_id=msg.from_.id)
    except TelegramAPIError[400]:
        # This line, when executed, will call shortcut method to answer message from user
        # (see https://github.com/telefone-org/framework/blob/main/telefone/tools/dev/mini_types/message.py).
        await msg.answer(f"An error occured while kicking a chat member.")


# You can also handle other types of updates besides messages. To do that, use raw_update decorator
# and provide it with a type and a dataclass of update that you want to handle.
@bot.on.raw_update(BotUpdateType.EDITED_MESSAGE, UpdateTypes.EditedMessageUpdate)
async def edited_message_handler(upd: UpdateTypes.EditedMessageUpdate):
    # This line contains ctx_api call we talked about in the previous example. This is the only way
    # we can send messages from raw update handlers.
    await upd.ctx_api.send_message(upd.chat.id, "Hm? I heard you edit a message.")


# Runs loop > loop.run_forever() > with tasks created in loop_wrapper before,
# read the loop wrapper documentation to comprehend this.
# The main polling task for bot is bot.run_polling()
bot.run_forever()
