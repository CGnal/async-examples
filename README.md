## Functional Asyncrhonous Examples

This is a repo that provides some examples on how to throttle and make asynchronous functions in a
functional paradigm.

This package requires python 3.7, and requirements.txt provides the list of requirements needed to run the
examples under the "examples" folder.

Examples
========

The examples folder contains a number of simple self-contained scripts that can be used to test and explore
monads and async functionalities

- *001_async.py* Simple examples of usage of asynchronous utilities with asyncio
- *002_monads.py* Usage of pymonad library and application with the monad Either, for handling success/failure in a functional way
- *003_promises.py* Usage of Promise monads and combination of multiple promises
- *004_functional_async.py* Integration between Promise and Either monads with *not-safe* functions
- *005_functional_async_bis.py* Integration between Promise and Either monads with *safe* functions
- *006_throttle.py* Examples to throttle execution of promises with rate-limiting functionalities
- *007_parallel_execution.py* Integration between parallel and asynchronous functionalities

For the Either monads and Railway Oriented Programming pattern, please do refer to this amazing talk:
https://vimeo.com/113707214