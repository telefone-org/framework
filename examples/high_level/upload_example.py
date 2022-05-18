from typing import NoReturn

from telefone import Bot, Message
from telefone.api.utils import File

# Make a bot with a token from an environment variable.
bot = Bot(__import__("os").getenv("token"))


# Register a handler that will upload files.
@bot.on.message(command="upload")
async def upload_handler(msg: Message) -> NoReturn:
    # Let's upload a picture of fresh red apples.
    await msg.ctx_api.send_photo(
        chat_id=msg.chat.id,
        caption="Testing pictures!",
        # Open the file and pass its contents directly in `photo` param.
        photo=await File.from_path("examples/files/apples.webp"),
    )

    # To set the mood, let's upload a recording of soothing melody.
    await msg.ctx_api.send_audio(
        chat_id=msg.chat.id,
        caption="Telefone for the win!",
        # Open the file and pass its contents directly in `audio` param.
        audio=await File.from_path("examples/files/music.mp3"),
    )

    # You can use raw bytes to create a file. Here we are downloading
    # some sample image from Lorem Picsum using built-in HTTP client.
    content = await msg.ctx_api.http_client.request_content("https://picsum.photos/500")

    # Now we are using the same file helper class, but it is being fed
    # an array of raw bytes. Note that we must explicitly set the name
    # for these types of files. Let's give this file a very generic
    # name of `image.jpg`.
    photo = File.from_bytes(content, "image.jpg")

    # Now that we've created the file, let's send it.
    await msg.ctx_api.send_photo(
        caption="Look, mom! I pulled this photo from the Internet!",
        chat_id=msg.chat.id,
        photo=photo,
    )


# Run loop > loop.run_forever() > with tasks created in loop_wrapper before.
# The main polling task for bot is bot.run_polling()
bot.run_forever()
