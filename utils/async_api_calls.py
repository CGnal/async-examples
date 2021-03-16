import asyncio
from aiohttp import ClientSession
from aiohttp.client_reqrep import ClientResponse

from functools import reduce

from pymonad.either import Left, Right, Either
from pymonad.promise import Promise, _Promise
from pymonad.tools import curry

from aiolimiter import AsyncLimiter

class RestCaller(object):

    def __init__(self, session):
        self.session = session

    async def rest_call(self, url):
        print(f"Calling {url}")
        try:
            value = await self.session.request(method='GET', url=url)
            return Right(value)
        except Exception as e:
            return Left(e)


async def throttle(c, rate_limit):
    async with rate_limit:
        return await c

async def parse_response(raw: ClientResponse):
    try:
        json = await raw.json()
        return Right(json["waitingTime"])
    except:
        return Left(ValueError(raw))


@curry(2)
def pipeline(steps, value) -> _Promise[Either]:
    promise = Promise.insert(Right(value))
    return reduce(lambda either, step: either.then(lambda x: x.bind(step)), steps, promise)


async def main(rate_per_seconds: float, url: str):

    print("Starting...")

    async with ClientSession() as session:

        rate_limiter = AsyncLimiter(rate_per_seconds, 1)

        caller = RestCaller(session)

        processor = pipeline([caller.rest_call, parse_response])

        requests = [processor(url) for i in range(10)]

        allResults = await asyncio.gather(*[throttle(c, rate_limiter) for c in requests])

    print([result.either(lambda x: "Error", lambda x: x) for result in allResults])

    return allResults

if __name__ == "__main__":

    asyncio.run(main(2, "http://127.0.0.1:8000/waiting"))


