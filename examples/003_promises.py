import asyncio

from pymonad.promise import Promise, _Promise

async def fakeComputation(x: int):
    print(f"Pre Call [{x}]")
    await asyncio.sleep(1 + x/3)
    print(f"Post Call [{x}]")
    return x

from typing import Awaitable

def async_func(func):
    """
    Transform simple function in async function using promises
    :param func: simple function
    :return: async function
    """

    async def getArgs(args):
        return await asyncio.gather(
            *[arg if isinstance(arg, Awaitable) else Promise.insert(arg) for arg in args]
        )

    async def getKwargs(kwargs):
        kwargsTasks = [arg.map(lambda x: (ith, x)) if isinstance(arg, Awaitable) else Promise.insert((ith, arg))
                       for ith, arg in kwargs.items()]
        return dict(await asyncio.gather(*kwargsTasks))

    async def async_wrap(*args, **kwargs):

        (_args, _kwargs) = await asyncio.gather(getArgs(args), getKwargs(kwargs))

        return func(*_args, **_kwargs)

    def wrapper(*args, **kwargs):
        return _Promise(lambda resolve, reject: async_wrap(*args, **kwargs), None)

    return wrapper

@async_func
def add(*args):
    return sum(args)

@async_func
def add(x, y):
    return x + y


@async_func
def my_func(x: int, y: int = 1, z: int = 1):
    return (x + 2*y)/z


async def main():

    x = Promise.insert(1).map(fakeComputation)

    y = Promise.insert(2).map(fakeComputation)

    z = Promise.insert(3).map(fakeComputation)

    # z = add(x, y)

    # promiseSum = add(x, y, z)
    promiseSum = my_func(x, y=1, z=z)

    final_result = promiseSum.map(fakeComputation)

    print("Here we have instantiated the computation, but we have not done anything")

    value = await final_result

    print(value)


if __name__ == "__main__":

    asyncio.run(main())

