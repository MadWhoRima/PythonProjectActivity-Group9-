import pandas as pd
import numpy as np

modifiedfile_path='CSVFiles/transaction_data_decoded.csv'
transaction_flag='Transaction ID is duplicate!'
suspicious_flag=' Suspicious transaction '

arr_digital = ["Remittance to Another Bank"]
arr_cash = ["Cash Withdrawal", "Credit in Cash", "Credit Card Withdrawal", "Collection from Another Bank"]
categories = ['Digital', 'Cash']

class DataManipulation:

    def data_modify(decoded_data):
        try:
         data = pd.read_csv(decoded_data, sep='|', low_memory=False)

         #Replacing null/NA values with space
         modified_data = data.fillna(" ")

         #Removing entire columns if all column values are null
         temp_data = modified_data.replace('', np.nan)
         for col in temp_data.columns:
             x = pd.DataFrame(temp_data[col])
             if (x.isna().all().bool()):
                 modified_data.drop(col, axis=1, inplace=True)

         return DataManipulation.flag_assign(modified_data)
        except:
            print("Error in data modifying")

    def flag_assign(modified_data):
        try:
         # Duplicating data
         modified_data.loc[len(modified_data)] = [1056320, "T00695247", "A00002378", "Credit", " ", 700.0, 700.0, '', '', '', 2013, 1, 1, '2013-01-01','11:02:40', '2013-01-01T11:02:40']
         modified_data.loc[len(modified_data)] = [1056321,"T00695247","A00002378","Credit"," ",500.0,500.0,'Old Age Pension','Bank of America','',2022,1,1,'2022-01-01','11:02:41','2022-01-01T11:02:41']

         # Adding cash or digital types based on operation
         modified_data = DataManipulation.transaction_types(modified_data);

         #finding transaction duplicate data
         #modified_data['Flag'] = np.where(modified_data['trans_id'].duplicated(), transaction_flag,  '')
         trans_id_list = np.where(modified_data['trans_id'].duplicated(), modified_data['trans_id'], 'Not Applicable')
         modified_data['Flag']=''

         #Updating flag for duplicate trx
         modified_data = DataManipulation.update_flag(modified_data, trans_id_list, transaction_flag)

         #Suspicious transactions
         #modified_data=DataManipulation.flag_concat(modified_data, "operation", " Suspicious transaction " )
         #trans_id_list = np.where(modified_data['operation'] == ' ', modified_data['trans_id'], "Not Applicable")
         modified_data['Flag'] = np.where(modified_data['TransactionType'] == 'nan',
                                         modified_data['Flag'] + suspicious_flag, modified_data['Flag'])

         #Transforming data to csv
         if(DataManipulation.transform_to_csv(modified_data, modifiedfile_path)):
             print("Modified transaction_data_decoded csv file")
         return modified_data
        except:
            print("Error in assigning flags")

    def transform_to_csv(modified_data, file_name):
        try:
         modified_data.to_csv(file_name, index=False)
         return True
        except:
            print("Error in transaforming data to csv file")

    def transaction_types(modified_data):
        try:
            conditions = [(modified_data['operation'].isin(arr_digital)), (modified_data['operation'].isin(arr_cash))]
            modified_data['TransactionType'] = np.select(conditions, categories, np.NAN)
            return modified_data
        except:
            print("Error in adding transaction types")

    def update_flag(modified_data, trxId_list, status):
        try:
            modified_data['Flag'] = np.where(modified_data["trans_id"].isin(trxId_list), modified_data['Flag'] + status, modified_data['Flag'])
            return modified_data
        except:
            print("Error in updating flag")


