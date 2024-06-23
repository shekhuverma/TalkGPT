import asyncio

q = asyncio.Queue()


asyncio.run(q.put("shekhar"))


async def stt(q: asyncio.Queue):
    while True:
        await q.put("shekhar")
        # await asyncio.sleep(1)


async def printer(q: asyncio.Queue):
    while True:
        # await asyncio.sleep(1)
        print(await q.get())
        q.task_done()


async def main():
    t1 = asyncio.create_task(stt(q))

    t2 = asyncio.create_task(printer(q))

    asyncio.gather(t1, t2)


asyncio.run(main())
# asyncio.run(printer(q))
