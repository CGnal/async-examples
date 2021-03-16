import asyncio
from time import sleep

from functools import reduce

from pymonad.either import Left, Right, Either
from pymonad.promise import Promise, _Promise
from pymonad.tools import curry

class TooLarge(Exception):
    pass

async def mySafeComputation(x: int):
    if x > 80:
        return Left(x)

    waiter = x % 2 + 1

    print(f"Computation with {x} - {waiter}")
    await asyncio.sleep(waiter)
    print(f"Results of {x}")
    return Right(x+1)


async def processFuture(future):
    result = await future
    print(result)
    return result

def errorHandling(x):
    print(f"Error {x}")
    return Left(x)


@curry(2)
def pipeline(steps, value) -> _Promise[Either]:
    promise = Promise.insert(Right(value))
    return reduce(lambda either, step: either.then(lambda x: x.bind(step)), steps, promise)


from aiolimiter import AsyncLimiter

async def throttle(c, rate_limit):
    async with rate_limit:
        return await c


async def main():
    print("Starting...")

    process = pipeline([mySafeComputation])

    computations = [process(i) for i in range(100)]

    rate_limit = AsyncLimiter(50, 5)

    await asyncio.sleep(1)

    print("Compuration instantiated...")

    allResults = await asyncio.gather(*[throttle(c, rate_limit) for c in computations])

    print(allResults)

    return allResults

if __name__ == "__main__":

    asyncio.run(main())


