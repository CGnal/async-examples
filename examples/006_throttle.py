import asyncio
from time import sleep

from typing import Callable, TypeVar, Any, List

from functools import reduce, wraps
from typing import Callable

from pymonad.either import Left, Right, Either
from pymonad.promise import Promise, _Promise
from pymonad.tools import curry
import numpy as np


class RandomError(Exception):
    pass

async def mySafeComputation(x: int):
    if np.random.randint(0,10)>8:
        return Left(RandomError(f"Random Error with {x}"))

    waiter = np.random.randint(0,5) # x % 2 + 1

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


T = TypeVar("T", bound=Any)

@curry(2)
def pipeline(steps: List[Callable[[T], Either[Exception, T]]], value) -> _Promise[Either[Exception, T]]:
    return reduce(lambda promise, step: promise.then(step), steps, Promise.insert(value))\
        .map(lambda x: Right(x)).catch(errorHandling)


from aiolimiter import AsyncLimiter

async def throttle(c, rate_limit):
    async with rate_limit:
        return await c

class Odd(ValueError):
    pass

def safe(f: Callable) -> Callable:
    @wraps(f)
    def wrap(*args, **kwargs) -> Either:
        try:
            return Right(f(*args, **kwargs))
        except Exception as e:
            return Left(e)
    return wrap

@safe
def mustBeEven(x: int) -> int:
    if x % 2 == 0:
        return x
    else:
        raise Odd("Number is odd")

async def main():
    print("Starting...")

    process: Callable[[int], _Promise[Either[Exception, int]]] = pipeline([
        # getDataFromAPI,
        mySafeComputation,
        # writeToDb
    ])

    computations = [Promise.insert(i).then(process) for i in range(50)]

    await asyncio.sleep(1)

    print("Compuration instantiated...")

    rate_limit = AsyncLimiter(max_rate=10, time_period=10)

    return await asyncio.gather(*[throttle(c, rate_limit) for c in computations])


if __name__ == "__main__":

    asyncio.run(main())


