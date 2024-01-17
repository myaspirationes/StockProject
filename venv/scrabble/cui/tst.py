import asyncio

async def hello():
    await asyncio.sleep(2)
    return "Hello"

async def world():
    await asyncio.sleep(1)
    return "World"

async def main():
    results = await asyncio.gather(hello(), world())
    print(results)


for i in range(1,10):

    asyncio.run(main())
