import unittest, uu

from dataprocessing import DataProcessing
from datamanipulation import DataManipulation

sourcefile_path= "csv_files/transaction_data_encoded"
decodedfile_path= "csv_files/transaction_data_decoded.csv"

class TestDataprocessing(unittest.TestCase):

    uu.decode(sourcefile_path, decodedfile_path)
    datamanipulation_obj = DataManipulation()
    data=datamanipulation_obj.data_modify(decodedfile_path)

    def test_findmaxcashtrx(self):
        dataprocessing_obj=DataProcessing(trxtype_param='Digital', modifiedfile_path_param = 'csv_files/tests/digital_transactions_data_test.csv')
        dataprocessing_obj.find_maxcashtransactions(self.data)

    def test_sendmails(self):
        dataprocessing_obj2=DataProcessing(min_balance_param=1)
        dataprocessing_obj2.sendmails_minbal_accounts(self.data)

    def test_findmaxcashtrx_error(self):
        dataprocessing_obj = DataProcessing(modifiedfile_path_param='csvfiles/digital_transactions_data_test.csv')
        dataprocessing_obj.find_maxcashtransactions(self.data)

    def test_sendmails_error(self):
        dataprocessing_obj = DataProcessing(min_balance_param='yae')
        dataprocessing_obj.sendmails_minbal_accounts(self.data)
