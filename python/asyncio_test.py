import asyncio


class Trying:
    def __init__(self):
        self.task = []

    async def print_somthing(self):  # get_namespace
        if self.task:
            await asyncio.wait(self.task)
        print('print_somthing')

    async def something_async(self):
        print('something_async start')
        await self.print_somthing()
        self.task.append(asyncio.ensure_future(
            self.other_async()  # create_namepsace
        ))
        await asyncio.sleep(6)
        self.task.pop()
        print('something_async done')

    async def other_async(self):
        print('other_async start')
        await asyncio.sleep(3)
        print('other_async done')


if __name__ == '__main__':
    trying = Trying()

    loop = asyncio.get_event_loop()
    tasks = [
        loop.create_task(trying.something_async()),
        loop.create_task(trying.something_async()),
        loop.create_task(trying.something_async()),
        loop.create_task(trying.something_async()),
    ]
    loop.run_until_complete(asyncio.wait(tasks))
    print(trying.task)
