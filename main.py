from asyncio import run

from bot import run as bot_run

async def main():
    await bot_run()

if __name__ == "__main__":
    run(main=main())
