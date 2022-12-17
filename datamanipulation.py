import pandas as pd
import numpy as np

class DataManipulation:

    def __init__(self, modifiedfile_path_param= 'csv_files/transaction_data_decoded.csv',transaction_flag_param='Transaction ID is duplicate!',
                 suspicious_flag_param=' Suspicious transaction ', arr_digital_param = ["Remittance to Another Bank", "Collection from Another Bank", ],
                 arr_cash_param=["Cash Withdrawal", "Credit in Cash", "Credit Card Withdrawal"], categories_param = ['Digital', 'Cash']):
        self.modifiedfile_path=modifiedfile_path_param
        self.transaction_flag=transaction_flag_param
        self.suspicious_flag=suspicious_flag_param
        self.arr_digital=arr_digital_param
        self.arr_cash=arr_cash_param
        self.categories=categories_param

    def data_modify(self, decoded_data):
        try:
         data = pd.read_csv(decoded_data, sep='|', low_memory=False)

         #Replacing null/NA values with space
         modified_data = data.fillna(" ")
         modified_data['sample_nullcol']=''

         #Removing entire columns if all column values are null
         temp_data = modified_data.replace('', np.nan)
         for col in temp_data.columns:
             temp_col_data = pd.DataFrame(temp_data[col])
             if (temp_col_data.isna().all().bool()):
                 modified_data.drop(col, axis=1, inplace=True)

         return self.flag_assign(modified_data)
        except Exception as err:
            print("Error in data modifying - ", err)

    def flag_assign(self, modified_data):
        try:
         # Duplicating data to test
         modified_data.loc[len(modified_data)] = [1056320, "T00695247", "A00002378", "Credit", " ", 700.0, 700.0, '', '', '', 2013, 1, 1, '2013-01-01','11:02:40', '2013-01-01T11:02:40']
         modified_data.loc[len(modified_data)] = [1056321,"T00695247","A00002378","Credit"," ",500.0,500.0,'Old Age Pension','Bank of America','',2022,1,1,'2022-01-01','11:02:41','2022-01-01T11:02:41']

         # Adding cash or digital types based on operation and NAN if operaton is null
         modified_data = self.transaction_types(modified_data);

         #finding duplicated trx data
         trans_id_list = np.where(modified_data['trans_id'].duplicated(), modified_data['trans_id'], 'Not Applicable')
         modified_data['Flag']=''

         #Updating flag for duplicate trx
         modified_data = self.update_flag(modified_data, trans_id_list, self.transaction_flag)

         #suspicious transactions
         modified_data['Flag'] = np.where(modified_data['TransactionType'] == 'nan',
                                         modified_data['Flag'] + self.suspicious_flag, modified_data['Flag'])

         #Transforming data to csv
         if(self.transform_to_csv(modified_data, self.modifiedfile_path)):
             print("Modified transaction_data_decoded csv file")
         return modified_data
        except Exception as err:
            print("Error in assigning flags - ", err)

    def transform_to_csv(self, modified_data, file_name):
        try:
         modified_data.to_csv(file_name, index=False)
         return True
        except Exception as err:
            print("Error in transforming data to csv file", err)

    def transaction_types(self, modified_data):
        try:
            conditions = [(modified_data['operation'].isin(self.arr_digital)), (modified_data['operation'].isin(self.arr_cash))]
            modified_data['TransactionType'] = np.select(conditions, self.categories, np.NAN)
            return modified_data
        except Exception as err:
            print("Error in adding transaction types - ", err)

    def update_flag(self, modified_data, trxId_list, status):
        try:
            modified_data['Flag'] = np.where(modified_data["trans_id"].isin(trxId_list), modified_data['Flag'] + status, modified_data['Flag'])
            return modified_data
        except Exception as err:
            print("Error in updating flag - ", err)
