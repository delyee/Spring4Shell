import asyncio
import aiohttp
import aiofiles
import aioredis
import concurrent.futures
from math import ceil
from config import *


async def get_and_scrape_pages(links):
    redis = aioredis.from_url(REDIS_SERVER_URL, decode_responses=True, db=REDIS_SERVER_DB)
    async with aiohttp.ClientSession() as client:
        for link in links:
            try:
                async with client.get(link) as response:
                    '''if response.status != 200:
                        await errors_log.write(f"{link}\n")'''

                    content = await response.text()
                    await redis.set(link, content)
            except Exception as e:
                async with aiofiles.open(ERROR_LOG, "a+", encoding="utf-8") as errors_log:
                    await errors_log.write(f"{link} {e}\n")


async def start_scrapping(links):
    parted_domains = split_array(links, NUM_COROS)
    tasks = []

    for part in parted_domains:
        tasks.append(get_and_scrape_pages(part))

    await asyncio.gather(*tasks)


def prepare_scrapping(links):
    asyncio.run(start_scrapping(links))


def split_array(array, parts):
    part_len = ceil(len(array) / parts)
    return [array[part_len * k:part_len * (k + 1)] for k in range(parts)]


def main():
    with open("links.txt") as f:
        links = []
        for i in f.readlines():
            links.append(i.strip())

    parted_links = split_array(links, NUM_CPU_CORES)
    futures = []

    with concurrent.futures.ProcessPoolExecutor(NUM_CPU_CORES) as executor:
        for i in range(NUM_CPU_CORES):
            new_future = executor.submit(prepare_scrapping, links=parted_links.pop())
            futures.append(new_future)

    concurrent.futures.wait(futures)


if __name__ == "__main__":
    main()
