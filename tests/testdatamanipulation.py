import unittest, uu, pandas as pd

from datamanipulation import DataManipulation

sourcefile_path= "csv_files/transaction_data_encoded"
decodedfile_path= "csv_files/transaction_data_decoded.csv"
modifiedfile_path1= 'csv_files/tests/transaction_data_decoded_test.csv'

class TestDataManipulation(unittest.TestCase):

    #testcase to verify datamodify workflow
   def test_datamodify(self):
       uu.decode(sourcefile_path, decodedfile_path)
       return self.object_creation().data_modify(decodedfile_path)

   #testcase to verify flg assign method error by passing unmatched columns
   def test_flagassign_error(self):
      self.object_creation().data_modify(modifiedfile_path1)

    #checking transformtocsv menthod by passing unknown directory
   def test_transformcsv(self):
       data = pd.read_csv(modifiedfile_path1, sep='|', low_memory=False)
       self.object_creation().transform_to_csv(data, 'csvfiles/transaction_data_decoded_s.csv')

    #To check transactions type method by passing None data
   def test_transaction_types_error(self):
       datamanipulation_obj1 = DataManipulation()
       data=datamanipulation_obj1.data_modify(decodedfile_path)
       datamanipulation_obj1.transaction_types(data)

   def object_creation(self):
       datamanipulation_obj = DataManipulation()
       return datamanipulation_obj
