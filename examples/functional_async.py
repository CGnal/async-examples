import asyncio
from time import sleep

from functools import reduce

from pymonad.either import Left, Right, Either
from pymonad.promise import Promise, _Promise
from pymonad.tools import curry

maxLimit = 5

class TooLarge(Exception):
    pass

async def myFirstComputation(x: int):
    if x > 5:
        raise TooLarge(x)

    waiter = x % 2 + 1

    print(f"Computation with {x} - {waiter}")
    await asyncio.sleep(waiter)
    print(f"Results of {x}")
    return x+1


async def mySafeComputation(x: int):
    if x > 5:
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


async def main():
    print("Starting...")

    process = pipeline([mySafeComputation])

    computations = [Promise.insert(Right(i)).then(lambda x: x.bind(mySafeComputation)) for i in [4,5,6]]

    # computations = [process(i) for i in [4,5,6]]

    # computations = [createComputation(3)]

    await asyncio.sleep(1)

    print("Compuration instantiated...")

    allResults = [await processFuture(future) for future in asyncio.as_completed(computations)]

    print(allResults)

    return allResults

if __name__ == "__main__":

    asyncio.run(main())


