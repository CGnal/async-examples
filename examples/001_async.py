import asyncio


async def myFirstComputation(x: int):
    """Example of a simple async computation (we mock computation using sleep)"""
    print(f"Entering co-routing {x}")
    await asyncio.sleep(x)
    print(f"Computation done with result: {x}")
    return x+1


async def processFuture(future):
    """Print result of the computation"""
    result = await future
    print(result)
    return result


async def main():
    """
    Basic async main to be executed by scheduling it in the event-loop
    """

    print("Starting main async process...")

    computations = [myFirstComputation(2), myFirstComputation(1)]

    tasks = [asyncio.create_task(c) for c in computations]

    await asyncio.sleep(1)

    print("Compuration instantiated...")

    allResults = await asyncio.gather(*tasks)

    return allResults

async def main_as_completed():
    """
    Resolve computations using as_completed, that only returns values once their computation is finished
    """

    computations = [myFirstComputation(2), myFirstComputation(1)]

    allResults = []
    for future in asyncio.as_completed(computations):
        fut = await future
        print(f"Future {fut} computed")
        allResults.append(fut)

    return allResults

if __name__ == "__main__":

    # Instantiate the event-loop
    # loop = asyncio.get_event_loop()

    # Create the task on the event-loop
    # task = loop.create_task(main_as_completed())

    # Run the loop until we complete the task
    # loop.run_until_complete(task)

    asyncio.run(main())

