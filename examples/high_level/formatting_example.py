from telefone import Bot, Message
from telefone.tools.text import html, markdown, ParseMode

# Make a bot with a token from an environment variable.
bot = Bot(__import__("os").getenv("token"))


@bot.on.message(command="markdown")
async def markdown_formatting_handler(msg: Message) -> None:
    # Let's use Markdown to format our message.
    await msg.answer(
        # This text is perfectly valid and escaping it isn't mandatory.
        markdown.underline("Here is Markdown formatted text:")
        + " "
        + markdown.bold(
            # You must escape the text if it contains
            # special characters like `*` or `_`. More details at
            # https://core.telegram.org/bots/api#markdownv2-style
            markdown.escape("This text is formatted and it's looking *awesome*!")
        )
        + " "
        + markdown.italic(markdown.escape("It's also italic!")),
        parse_mode=ParseMode.MARKDOWNV2,
    )


@bot.on.message(command="html")
async def html_formatting_handler(msg: Message) -> None:
    # Let's use HTML to format our message.
    await msg.answer(
        # This text is perfectly valid and escaping it isn't mandatory.
        html.underline("HTML stands for Hyper Text Markup Language.")
        + " "
        + html.strike(
            # You may want to escape the text if it contains
            # special characters like `&`, `<` or `>`. More details at
            # https://core.telegram.org/bots/api#html-style
            html.escape(
                "The <html> tag represents the root of an HTML document. "
                "The <body> tag defines the document's content "
                "& the <head> element is a container for metadata."
            )
        ),
        parse_mode=ParseMode.HTML,
    )


@bot.on.message(command="mention")
async def mention_handler(msg: Message) -> None:
    await msg.answer(
        markdown.mention("Look who's mentioned in Markdown!", msg.from_.id),
        parse_mode=ParseMode.MARKDOWNV2,
    )
    await msg.answer(
        html.mention(
            "What a shame! You are mentioned again, this time in HTML!", msg.from_.id
        ),
        parse_mode=ParseMode.HTML,
    )

# Run loop > loop.run_forever() > with tasks created in loop_wrapper before.
# The main polling task for bot is bot.run_polling()
bot.run_forever()
