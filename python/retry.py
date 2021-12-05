import asyncio

from retrying_async import retry

counter = 0

async def kn():
    print("T ", counter)
    raise TypeError("hede")

@retry(attempts=3, delay=3, retry_exceptions=(TypeError, ))
async def fn():
    global counter

    counter += 1
    print(counter)

    try:
        if counter == 1:
            await kn()
    except TypeError as e:
        print(e)
        raise ValueError
    except Exception as e:
        raise Exception(e)

async def main():
    await fn()

loop = asyncio.get_event_loop()

loop.run_until_complete(main())

assert counter == 2

loop.close()
