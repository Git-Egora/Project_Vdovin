import os
import asyncio
from aiogram import Bot, Dispatcher

from handlers.commands import router
from handlers.callback import call_router
from middleware.logging_middleware import LoggingMiddleware

async def main():
    try:
        token = os.getenv('BOT_TOKEN')
        bot = Bot(token)
        dp = Dispatcher()
        
        dp.include_router(router)
        dp.include_router(call_router)

        dp.message.outer_middleware(LoggingMiddleware())

        print("Bot's started...")
        
        await dp.start_polling(bot)
    except Exception as ex:
        print(f'There is an exeption {ex}')

if __name__ == '__main__':
    try:    
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')