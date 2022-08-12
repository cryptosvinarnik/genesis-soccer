import aiohttp
import asyncio

from loguru import logger


async def subscribe_on_soccer(worker: str, queue: asyncio.Queue) -> bool:
    i = 0

    while not queue.empty():
        email = await queue.get()

        params = {
            "u": "861e8fb93f9e284d2278a4fa4",
            "id": "8830eb7d3e",
            "f_id": "009e66e0f0",
            "c": "jQuery3410908869135896811_1660317858192",
            "tags": "4872213",
            "EMAIL": email,
            "b_861e8fb93f9e284d2278a4fa4_8830eb7d3e": "",
            "_": "1660317858193",
        }

        async with aiohttp.ClientSession() as session:
            async with session.get("https://genesisleaguesports.us8.list-manage.com/subscribe/post-json", params=params) as resp:
                if "Thank" in await resp.text():
                    logger.success(
                        f"{worker} - {email} successfully registered")
                else:
                    logger.error(f"{worker} - {email} - error!")

        i += 1

        if i % 4 == 0:
            logger.info("Sleeping 60 seconds...")
            await asyncio.sleep(60)


async def main(emails):
    queue = asyncio.Queue()

    for email in emails:
        queue.put_nowait(email)

    tasks = [asyncio.create_task(subscribe_on_soccer(
             f"Worker {i}", queue)) for i in range(5)]

    await asyncio.gather(*tasks)
