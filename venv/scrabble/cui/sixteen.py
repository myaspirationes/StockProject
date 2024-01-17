import requests
import logging
import time,    asyncio
import aiohttp
import concurrent.futures  # 引入并发执行库


logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s: %(message)s')

def server_delay_5s():

    TOTAL_NUMBER = 100
    BASE_URL = 'https://ssr4.scrape.center/detail/{id}'
    start_time = time.time()
    for id in range(1, TOTAL_NUMBER + 1):
        url = BASE_URL.format(id=id)
        logging.info('scraping %s', url)
        response = requests.get(url)
    end_time = time.time()
    logging.info('total time %s seconds', end_time - start_time)


def async_first():
    async def execute(x):
       print('Number:', x)
    coroutine = execute(15)
    print('Coroutine:', coroutine)
    print('After calling execute')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(coroutine)
    print('After calling loop')

def async2nd():
    async def execute(x):
        print('Number:', x)
        return x

    coroutine = execute(1)
    print('Coroutine:', coroutine)
    print('After calling execute')
    loop = asyncio.get_event_loop()
    task = loop.create_task(coroutine)
    print('Task:', task)
    loop.run_until_complete(task)
    print('Task:', task)
    print('After calling loop')


def async3rd():
    async def execute(x):
        print('Number:', x)
        return x

    coroutine = execute(1)
    print('Coroutine:', coroutine)
    print('After calling execute')
    task = asyncio.ensure_future(coroutine)
    print('Task:', task)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(task)
    print('Task:', task)
    print('After calling loop')


async def request():
    url = 'https://www.baidu.com/'
    status = requests.get(url)
    return status.status_code

def async5times():


    tasks = [asyncio.ensure_future(request()) for _ in range(5)]
    print('Tasks:', tasks)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))

    for task in tasks:
        print('Task Result:', task.result())


def async10pic():
    start = time.time()

    async def request():
        url = 'https://ssr4.scrape.center/'
        print('Waiting for', url)
        response =await requests.get(url)
        print('Get response from', url, 'response', response)

    tasks = [asyncio.ensure_future(request()) for _ in range(10)]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))

    end = time.time()
    print('Cost time:', end - start)

def async10pic_1():
    start = time.time()

    async def get(url):
        return requests.get(url)

    async def request():
        url = 'https://ssr4.scrape.center/'
        print('Waiting for', url)
        response = await get(url)
        print('Get response from', url, 'response', response)

    tasks = [asyncio.ensure_future(request()) for _ in range(10)]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))

    end = time.time()
    print('Cost time:', end - start)




# 仅仅将涉及 IO 操作的代码封装到 async 修饰的方法里面是不可行的！
# 我们必须要使用支持异步操作的请求方式才可以实现真正的异步
# ，所以这里就需要 aiohttp 派上用场了


def httpaio():
    start = time.time()

    async def get(url):
        session = aiohttp.ClientSession()
        response = await session.get(url)
        await response.text()
        await session.close()
        return response

    async def request():
        url = 'https://ssr4.scrape.center/'
        print('Waiting for', url)
        response = await get(url)
        print('Get response from', url, 'response', response)

    tasks = [asyncio.ensure_future(request()) for _ in range(10)]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))

    end = time.time()
    print('Cost time:', end - start)


def aiohttp1():
    def test(number):
        start = time.time()

        async def get(url):
            session = aiohttp.ClientSession()
            response = await session.get(url)
            await response.text()
            await session.close()
            return response

        async def request():
            url = 'https://www.baidu.com/'
            await get(url)

        tasks = [asyncio.ensure_future(request()) for _ in range(number)]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.wait(tasks))

        end = time.time()
        print('Number:', number, 'Cost time:', end - start)

    for number in [1, 3, 5, 10, 15, 30, 50, 75, 100, 200, 500]:
        test(number)



async def fetch_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()




async def main():
    urls = ['https://ssr4.scrape.center/', 'https://ssr4.scrape.center/page/2']
    tasks = [fetch_url(url) for url in urls]
    results = await asyncio.gather(*tasks)
    for result in results:
        print(result)





if __name__ == '__main__':
    # server_delay_5s()
    # async_first()
    # async2nd()
    # async3rd()
    # async5times()

    # async10pic_1()
    asyncio.run(main())

    # httpaio()
    # aiohttp1()

