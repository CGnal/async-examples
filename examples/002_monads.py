from functools import reduce, wraps
from typing import Callable, TypeVar, Any, List

from pymonad.either import Either, Right, Left
from pymonad.tools import curry


class TooHigh(ValueError):
    pass

class Odd(ValueError):
    pass


def safe(f: Callable) -> Callable:
    """Decorator to convert unsafe functions to safe functions, that returns Either monads"""
    @wraps(f)
    def wrap(*args, **kwargs) -> Either:
        try:
            return Right(f(*args, **kwargs))
        except Exception as e:
            return Left(e)
    return wrap

@safe
def mustBeEven(x: int) -> int:
    """Return the value if even, return an exception otherwise"""
    if x % 2 == 0:
        return x
    else:
        raise Odd("Number if odd")


@curry(2)
def mustBeLowerThan(value: int, x: int) -> Either[Exception, int]:
    """Return the value if lower than a threshold, return an exception otherwise"""
    if (x < value):
        return Right(x)
    else:
        return Left(TooHigh(x))


def handleError(e: Exception):
    """Function that provides business logic to handle errors"""
    if isinstance(e, TooHigh):
        return "Value too high"
    elif isinstance(e, Odd):
        return "The number must be even"
    else:
        raise e


T = TypeVar("T", bound=Any)

@curry(2)
def pipeline(steps: List[Callable[[T], Either[Exception, T]]], value) -> Either[Exception, T]:
    return reduce(lambda either, step: either.then(step), steps, Either.insert(value))

def getValue(value: T) -> T:
    return value

if __name__ == "__main__":

    # myValue = Either.insert(2)\
    #     .then(mustBeEven)\
    #     .then(mustBeLowerThan(5))\
    #     .either(handleError, getValue)

    process = pipeline([mustBeEven, mustBeLowerThan(5)])

    myValue = Either.insert(2).then(process).either(handleError, getValue)

    print(myValue)


