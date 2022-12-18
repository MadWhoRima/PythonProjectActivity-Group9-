import unittest,uu

from datatransformation import DataTransformation
from datamanipulation import DataManipulation

sourcefile_path= "csv_files/transaction_data_encoded"
decodedfile_path= "csv_files/transaction_data_decoded.csv"

class TestDatatransformation(unittest.TestCase):

    uu.decode(sourcefile_path, decodedfile_path)
    datamanipulation_obj = DataManipulation(arr_digital_param = ["Collection from Another Bank"],
                 arr_cash_param=["Cash Withdrawal", "Credit in Cash", "Credit Card Withdrawal","Remittance to Another Bank"])
    data = datamanipulation_obj.data_modify(decodedfile_path)

    uu.decode(sourcefile_path, decodedfile_path)
    datamanipulation_obj_1= DataManipulation()
    data1 = datamanipulation_obj_1.data_modify(decodedfile_path)

    #To find pensioner update method by passing different bank and interest
    def test_pensioner_update(self):
        datatransformation_obj=DataTransformation(bank_name_param='Bank of New York Mellon Corp.',interest_rate_param=9, modifiedfile_path_param='csv_files/tests/bonus_to_pensioners_test.csv')
        datatransformation_obj.pensioner_update(self.data)

    #To find the digital/cash ratio - both trx types
    def test_digital_cash_ratio(self):
        datatransformation_obj = DataTransformation()
        datatransformation_obj.digital_cash_ratio(self.data)

    #To find the digital/cash ratio with only one trx type
    def test_digital_cash_ratio_1(self):
        datatransformation_obj = DataTransformation()
        datatransformation_obj.digital_cash_ratio(self.data1)

    #To find pensioner update error by passing string
    def test_pensioner_update_error(self):
        datatransformation_obj = DataTransformation(interest_rate_param='abc')
        datatransformation_obj.pensioner_update(self.data)
