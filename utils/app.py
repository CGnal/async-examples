from typing import Optional

from fastapi import FastAPI

import numpy as np
from time import sleep, time

app = FastAPI()

@app.get("/")
def root():
    return {"time": time()}

@app.get("/waiting")
def randomWaitingTime():
    value = np.random.uniform(0, 1)
    if value>0.7:
        raise ValueError
    else:
        sleep(value*5)
    return {"waitingTime": value}

