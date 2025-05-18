import logging
from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Any, Callable, Dict, Awaitable

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

class LoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]) -> Any:


        logging.info('До обработчика')
        if event.from_user and event.text:
            user_id = event.from_user.id
            username = event.from_user.username
            command = event.text
            logging.info(f'Пользователь с id: {user_id} и username: {username} использовал команду {command}')
        else:
            logging.warning('Получено сообщение без пользователя или текста.')
        
        try:
            res = await handler(event, data)
            logging.info('После обработчика.')
            return res
        except Exception as e:
            logging.error(f'Ошибка при получении сообщения: {e}')
            raise