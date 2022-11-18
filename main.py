# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import uu
import pandas as pd
import numpy as np

from DataManipulation import DataManipulation
from DataProcessing import DataProcessing


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    uu.decode("../../../../PycharmProjects/pythonProject/transaction_data_encoded", "transaction_data_decoded")
    final_data = DataManipulation.data_modify('transaction_data_decoded')
    print(final_data.groupby('year').size())
    yearly_max_transaction = final_data.groupby('year').apply(DataProcessing.findMaxCashTransaction)
    print(yearly_max_transaction)
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    # print(data.shape)
    # print(modifiedData.shape)
    # print(data.isnull().sum())
    # print(modifiedData.isnull().sum())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
