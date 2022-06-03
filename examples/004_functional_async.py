import asyncio
from functools import reduce
from typing import Callable, TypeVar, Any, List

from pymonad.either import Left, Right, Either
from pymonad.promise import Promise, _Promise
from pymonad.tools import curry

maxLimit = 5


class TooLarge(Exception):
    pass


async def mySafeComputation(x: int):
    """
    Example of a simple async computation (we mock computation using sleep). Raising exception when
    value is too large
    """
    if x > 5:
        raise TooLarge(x)

    waiter = x % 2 + 1

    print(f"Computation with {x} - {waiter}")
    await asyncio.sleep(waiter)
    print(f"Results of {x}")
    return x + 1


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
def pipeline(steps: List[Callable[[T], Either[Exception, T]]], value) -> _Promise[Either[Exception, T]]:
    return reduce(lambda promise, step: promise.then(step), steps, Promise.insert(value)) \
        .map(lambda x: Right(x)).catch(errorHandling)


async def getDataFromAPI(x: int) -> _Promise[int]:
    """Fake getting data from the db"""
    return Promise.insert(x)


async def writeToDb(x: int) -> _Promise[int]:
    """Fake writing data to a db"""
    return Promise.insert(x)


def getProcess() -> Callable[[int], _Promise[Either[Exception, int]]]:
    return pipeline([
        getDataFromAPI,
        mySafeComputation,
        writeToDb
    ])


async def main():
    print("Starting...")

    process: Callable[[int], _Promise[Either[Exception, int]]] = pipeline([
        getDataFromAPI,
        mySafeComputation,
        writeToDb
    ])

    executions = [Promise.insert(i).then(process) for i in range(10)]

    await asyncio.sleep(1)

    print("Compuration instantiated...")

    return [await processFuture(future) for future in asyncio.as_completed(executions)]


if __name__ == "__main__":
    asyncio.run(main())
