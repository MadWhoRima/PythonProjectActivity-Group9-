import pandas as pd
import numpy as np


class DataProcessing:

    def findMaxCashTransaction(modifiedData):
        return modifiedData['operation'].value_counts().idxmax()
