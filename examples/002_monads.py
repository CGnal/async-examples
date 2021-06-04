from typing import Callable

from pymonad.tools import curry
from pymonad.either import Either, Right, Left

from functools import reduce, wraps


class TooHigh(ValueError):
    pass

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
        raise Odd("Number if odd")


@curry(2)
def mustBeLowerThan(value: int, x) -> Either:
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

    myValue = Either.insert(2).then(process).either(handleError, getValue)

    print(myValue)


