from pymonad.tools import curry
from pymonad.either import Either, Right, Left

from functools import reduce

@curry(2)
def func(a, b):
    return a + b

class TooHigh(ValueError):
    pass

class Odd(ValueError):
    pass

def mustBeEven(x: int) -> Either:
    if x % 2 == 0:
        return Right(x)
    else:
        return Left(Odd(x))

@curry(2)
def mustBeLowerThan(value: int, x):
    if (x < value):
        return Right(x)
    else:
        return Left(TooHigh(x))


def handleError(e: Exception):
    if isinstance(e, TooHigh):
        return "Value too high"
    elif isinstance(e, Odd):
        return "The number must be even"
    else:
        raise e


@curry(2)
def pipeline(steps, value) -> Either:
    return reduce(lambda either, step: either.then(step), steps, Either.insert(value))

def getValue(value):
    return value

if __name__ == "__main__":

    # myValue = Either.insert(2)\
    #     .then(mustBeEven)\
    #     .then(mustBeLowerThan(5))\
    #     .either(handleError, getValue)

    process = pipeline([mustBeEven, mustBeLowerThan(5)])

    myValue = process(9).either(handleError, getValue)

    print(myValue)


