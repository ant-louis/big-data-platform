import csv
import pandas as pd
import numpy as np


if __name__ == "__main__":
    steps = np.arange(10, 0, -5)
    steps = np.append(steps, 1)
    print(steps)