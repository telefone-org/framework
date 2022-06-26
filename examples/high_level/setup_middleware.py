from telefone import BaseMiddleware, Bot, Message
from telefone_types.objects import User

# Make a bot with a token from an environment variable.
bot = Bot(__import__("os").getenv("token"))


@bot.labeler.message_view.register_middleware
class SimpleMiddleware(BaseMiddleware[Message]):
    async def pre(self) -> None:
        """
        This middleware will be called before all handlers.
        It can be used for registering users, validating update data, etc.
        """
        await self.update.answer("Hello, world!")

    async def post(self) -> None:
        """
        This middleware will be called after all handlers. It can be used
        for logging and analyzing after update is processed.
        """
        await self.update.answer("Goodbye, world!")


@bot.labeler.message_view.register_middleware
class PassthroughMiddleware(BaseMiddleware[Message]):
    """
    You can actually have any number of pre and post middlewares.
    We are making another ones right there.
    """

    async def pre(self) -> None:
        """
        Often you might need to pass an argument from middleware to the handlers
        or stop processing the update altogether. In the first case, you should
        use `self.send()` method. In the second case, you should use `self.stop()`
        as shown below.
        """
        if self.update.from_.is_bot:
            self.stop("Messages from bots are not allowed to be handled.")

        self.send({"user": self.update.from_})

    async def post(self) -> None:
        """
        As was mentioned before, we can use post middlewares
        primarily for collecting and logging data. Let's print out
        a view and a list of handlers message was processed with.
        """
        await self.update.answer(
            "Message was processed with {0} view and {1} handlers.".format(
                self.view, ", ".join(str(h) for h in self.handlers)
            )
        )


@bot.on.message(command="profile")
async def who_am_i_handler(_, user: User) -> str:
    """
    A simple handler just to proof that middleware
    are working nice and sound.
    """
    first_name = user.first_name.capitalize()
    return f"I remember you! {first_name} you are!"


# Run loop > loop.run_forever() > with tasks created in loop_wrapper before.
# The main polling task for bot is bot.run_polling()
bot.run_forever()
