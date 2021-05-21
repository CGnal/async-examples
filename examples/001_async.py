import asyncio
from time import sleep

async def myFirstComputation(x: int):
    print(f"Computation with {x}")
    await asyncio.sleep(x)
    # sleep(x)
    print(f"Results of {x}")
    return x+1


# async def processFuture(future):
#     result = await future
#     print(result)
#     return result

async def main():
    print("Starting...")

    computations = [myFirstComputation(2), myFirstComputation(1)]

    # tasks = [asyncio.create_task(c) for c in computations]

    await asyncio.sleep(1)

    print("Compuration instantiated...")

    # allResults = await asyncio.gather(*tasks)

    for future in asyncio.as_completed(computations):
        fut = await future
        print(fut)

    # allResults = [await processFuture(future) for future in asyncio.as_completed(computations)]

    # print(allResults)

    return None

if __name__ == "__main__":

    asyncio.run(main())


