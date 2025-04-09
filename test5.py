import asyncio


async def astream():
    for i in range(10):
        yield i

async def func():
    x = astream()
    print(type(x))

x = "hello world ac dc ef azzz"
y = iter(x.split(" "))
print(type(y))
print(y)
# asyncio.run(func())
