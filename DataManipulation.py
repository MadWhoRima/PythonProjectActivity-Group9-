import pandas as pd
import numpy as np

#sneha mISHRA
class DataManipulation:

    def data_modify(decoded_data):
        print('inside dataModify')
        data = pd.read_csv(decoded_data, sep='|', low_memory=False)
        modified_data = data.fillna(" ")
        return DataManipulation.flag_assign(modified_data)

    def flag_assign(modified_data):
        print('inside modifiedData')
        modified_data['Flag'] = np.where(modified_data['trans_id'].duplicated().any(), 'Transaction ID is duplicate!',
                                         " ")
        modified_data['Flag'] = np.where(modified_data['operation'] == " ", 'Suspicious transaction', " ")
        DataManipulation.transform_to_csv(modified_data)
        return modified_data

    def transform_to_csv(modified_data):
        print('inside transformTOCSV')
        modified_data.to_csv('transaction_data_modified', index=False)
