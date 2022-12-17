import unittest, uu

from dataprocessing import DataProcessing
from datamanipulation import DataManipulation

sourcefile_path= "csv_files/transaction_data_encoded"
decodedfile_path= "csv_files/transaction_data_decoded.csv"

class TestDataprocessing(unittest.TestCase):

    def test_findmaxcashtrx(self):
        data=self.decoded_data()
        dataprocessing_obj=DataProcessing(trxtype_param='Digital', modifiedfile_path_param = 'csv_files/digital_transactions_data.csv')
        dataprocessing_obj.find_maxcashtransactions(data)

    def test_sendmails(self):
        data = self.decoded_data()
        dataprocessing_obj2=DataProcessing(min_balance_param=500)
        dataprocessing_obj2.sendmails_minbal_accounts(data)

    def test_findmaxcashtrx_error(self):
        data = self.decoded_data()
        dataprocessing_obj = DataProcessing(trxtype_param='Digital', modifiedfile_path_param='csvfiles/digital_transactions_data.csv')
        dataprocessing_obj.find_maxcashtransactions(data)

    def test_sendmails_error(self):
        data = self.decoded_data()
        dataprocessing_obj = DataProcessing(min_balance_param='yae')
        dataprocessing_obj.find_maxcashtransactions(data)

    def decoded_data(self):
        uu.decode(sourcefile_path, decodedfile_path)
        datamanipulation_obj = DataManipulation()
        return datamanipulation_obj.data_modify(decodedfile_path)
