from aiogram import loggers, Bot
from aiogram.client.session.middlewares.base import NextRequestMiddlewareType
from aiogram.methods import TelegramMethod
from aiogram.methods.base import TelegramType, Response
from aiogram.client.session.middlewares.request_logging import RequestLogging


class RequestLoggingMiddleware(RequestLogging):

    async def __call__(
        self,
        make_request: NextRequestMiddlewareType[TelegramType],
        bot: Bot,
        method: TelegramMethod[TelegramType],
    ) -> Response[TelegramType]:

        if type(method) not in self.ignore_methods:
            loggers.middlewares.info(
                msg=f'Make request with method={type(method).__name__} by bot id={bot.id}',
                exc_info=True
            )

        return await make_request(bot=bot, method=method)
