import csv
import pandas as pd
import numpy as np


if __name__ == "__main__":
    steps = np.arange(10, 0, -5)
    mean = np.zeros(len(steps))
    for i, nb in enumerate(steps):
        print(i)
        print(nb)