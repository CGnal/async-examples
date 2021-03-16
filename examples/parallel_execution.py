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


async def loopOverRange(input_range):
    print(f"Starting on range {input_range}...")

    rate_limit = AsyncLimiter(4, 5)

    process = pipeline([mySafeComputation, mySafeComputation, mySafeComputation])

    computations = [process(i) for i in input_range]

    allResults = await asyncio.gather(*[throttle(c, rate_limit) for c in computations])

    print(allResults)

    return allResults

def basicMain(ibatch, input_range):
    print(f"Running batch {ibatch}")
    return asyncio.run(loopOverRange(input_range))


def main():
    print("Starting...")

    from cgnal.utils.dict import groupIterable
    from concurrent.futures import ProcessPoolExecutor
    import concurrent

    batch_size = 100
    total_range = list(range(1000))

    futures = []

    with ProcessPoolExecutor(max_workers=2) as executor:
        for ibatch, batch in enumerate(groupIterable(total_range, batch_size)):
            futures.append(executor.submit(basicMain, ibatch, batch))

    concurrent.futures.wait(futures)

    print([future.result() for future in futures])

if __name__ == "__main__":

    main()


