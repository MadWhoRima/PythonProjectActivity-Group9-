import unittest,uu

from datatransformation import DataTransformation
from datamanipulation import DataManipulation

sourcefile_path= "csv_files/transaction_data_encoded"
decodedfile_path= "csv_files/transaction_data_decoded.csv"

class TestDataprocessing(unittest.TestCase):

    def test_pensioner_update(self):
        data = self.decoded_data()
        datatransformation_obj=DataTransformation(bank_name_param='Bank of New York Mellon Corp.',interest_rate_param=9)
        datatransformation_obj.pensioner_update(data)

    def test_digital_cash_ratio(self):
        data = self.decoded_data()
        datatransformation_obj = DataTransformation()
        datatransformation_obj.digital_cash_ratio(data)

    def test_pensioner_update_error(self):
        data = self.decoded_data()
        datatransformation_obj = DataTransformation(interest_rate_param='abc')
        datatransformation_obj.pensioner_update(data)

    def decoded_data(self):
        uu.decode(sourcefile_path, decodedfile_path)
        datamanipulation_obj = DataManipulation()
        return datamanipulation_obj.data_modify(decodedfile_path)

