import asyncio
from time import sleep

from functools import reduce, wraps
from typing import Callable, TypeVar, Any

from pymonad.either import Left, Right, Either
from pymonad.promise import Promise, _Promise
from pymonad.tools import curry

import numpy as np


def safe(f: Callable) -> Callable:
    """Decorator to convert unsafe functions to safe functions, that returns Either monads"""
    @wraps(f)
    def wrap(*args, **kwargs) -> Either:
        try:
            return Right(f(*args, **kwargs))
        except Exception as e:
            return Left(e)
    return wrap


class Odd(ValueError):
    pass

class RandomError(Exception):
    pass

async def mySafeComputation(x: int):
    """
    Example of a simple async computation (we mock computation using sleep). Raising exception randomly
    """
    if np.random.randint(0,10)>8:
        return Left(RandomError(f"Random Error with {x}"))

    waiter = x % 2 + 1

    print(f"Computation with {x} - {waiter}")
    await asyncio.sleep(waiter)
    print(f"Results of {x}")
    return Right(x+1)

@safe
def mustBeEven(x: int) -> int:
    """Return the value if even, return an exception otherwise"""
    if x % 2 == 0:
        return x
    else:
        raise Odd("Number is odd")


async def processFuture(future):
    """Print result of the computation"""
    result = await future
    print(result)
    return result

def errorHandling(x):
    """Function that provides business logic to handle errors"""
    print(f"Error {x}")
    return Left(x)

T = TypeVar("T", bound=Any)

@curry(2)
def pipeline(steps: Callable[[T], Either[Exception, T]], value: T) -> _Promise[Either[Exception, T]]:
    promise = Promise.insert(Right(value))
    return reduce(lambda either, step: either.then(lambda x: x.bind(step)), steps, promise)


from aiolimiter import AsyncLimiter

async def throttle(c, rate_limit):
    """Controlling rate at which computation resolution is achieved"""
    async with rate_limit:
        return await c


def getProcess() -> Callable[[int], _Promise[Either[Exception, int]]]:
    """Return function that create a computation given an input"""
    return pipeline([
        mySafeComputation,
        lambda x: Right(x * 3),
        mustBeEven
    ])

async def loopOverRange(input_range, process):
    """Tasks to be resolved by a given worker"""

    computations = [Promise.insert(i).then(process) for i in input_range]

    rate_limit = AsyncLimiter(max_rate=10, time_period=10)

    await asyncio.sleep(1)

    print("Compuration instantiated...")

    return await asyncio.gather(*[throttle(c, rate_limit) for c in computations])



def basicMain(ibatch, input_range):
    """Worker main"""
    print(f"Running batch {ibatch}")
    return asyncio.run(
        loopOverRange(
            input_range, getProcess()
        )
    )


def main():
    print("Starting...")

    from cgnal.utils.dict import groupIterable
    from concurrent.futures import ProcessPoolExecutor
    import concurrent

    batch_size = 10
    total_range = list(range(100))

    futures = []

    jobs = groupIterable(total_range, batch_size)

    with ProcessPoolExecutor(max_workers=2) as executor:
        for ibatch, batch in enumerate(jobs):
            futures.append(executor.submit(basicMain, ibatch, batch))

    concurrent.futures.wait(futures)

    print([future.result() for future in futures])

if __name__ == "__main__":

    main()


