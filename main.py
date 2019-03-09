import asyncio
import logging
from logging import Logger
import sys
from asyncio import sleep
from datetime import datetime

from socks import SOCKS5
from telethon import TelegramClient

from config import APP_API_HASH, APP_API_ID, PHONE_NUMBER


async def delete_read_messages(client: TelegramClient, logger: Logger):

    dialogs = await client.get_dialogs()

    for dialog in dialogs:
        messages = await client.get_messages(dialog, limit=10000)

        message_ids = [message.id for message in messages if not message.media_unread]
        logger.info(f'In dialog {dialog.title} will remove {len(message_ids)} messages')
        await client.delete_messages(dialog, message_ids)
        logger.info(f'Messages from dialog {dialog.title} removed')


async def main(client: TelegramClient, logger: Logger) -> None:
    await client.start()
    logger.info('Telegram client started')

    while True:
        current_time = datetime.now()
        # if True:
        if current_time.hour == 4 and current_time.minute == 0 and current_time.second == 0:
            logger.info("It's message removing time!")
            try:
                await delete_read_messages(client, logger)
            except Exception:
                logger.exception('Exception during message removing has occurred')
        await sleep(0.6)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename='/tmp/message_remover_log')
    bot_logger = logging.getLogger()
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    handler.setFormatter(formatter)
    bot_logger.addHandler(handler)

    proxy = None
    proxy = (SOCKS5, '51.144.86.230', 18001, True, 'usrTELE', 'avt231407')
    telegram_client = TelegramClient(PHONE_NUMBER.strip('+'),
                                     APP_API_ID,
                                     APP_API_HASH,
                                     proxy=proxy)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(telegram_client, bot_logger))
