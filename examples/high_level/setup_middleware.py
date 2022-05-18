from telefone import Bot, Message, BaseMiddleware
from telefone.tools import CtxStorage

# Make a bot with a token from an environment variable.
bot = Bot(__import__("os").getenv("token"))
# Make a storage in memory.
storage = CtxStorage({})

# Make a dummy type for storing user information.
User = __import__("collections").namedtuple("User", ("first_name", "last_name"))


class RegistrationMiddleware(BaseMiddleware[Message]):
    async def pre(self) -> dict:
        user = storage.get(self.update.from_.id)
        if user is None:
            await self.update.answer(
                f"User {self.update.from_.id} was registered in temporary storage"
            )
            user = User(
                self.update.from_.first_name,
                self.update.from_.last_name,
            )
            storage.set(self.update.from_.id, user)
        self.send({"user": user})


class InfoMiddleware(BaseMiddleware[Message]):
    async def post(self):
        await self.update.answer(
            f"Message was processed with:\n\n"
            f"View: {self.view=}\n"
            f"Handlers: {self.handlers=}"
        )


@bot.on.message(command="me")
async def who_am_i_handler(_, user: User) -> str:
    first_name = user.first_name.capitalize()
    return f"I remember you! {first_name} you are!"


# Register middlewares that we have created above.
bot.labeler.message_view.register_middleware(RegistrationMiddleware)
bot.labeler.message_view.register_middleware(InfoMiddleware)

# Run loop > loop.run_forever() > with tasks created in loop_wrapper before.
# The main polling task for bot is bot.run_polling()
bot.run_forever()
