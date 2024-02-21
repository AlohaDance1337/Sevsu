from dotenv import load_dotenv
load_dotenv()

from core import bot

import asyncio, os

async def main():
    
    import logging

    logging.basicConfig(level=logging.INFO, filename='main.log', filemode="w",
                      format="%(asctime)s - [%(levelname)s] -  %(name)s - " +
                              "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s \n")
    # logging.basicConfig(level=logging.INFO)

    await bot.run(os.getenv('token_bot'))
    

if __name__ == "__main__":
    asyncio.run(main())