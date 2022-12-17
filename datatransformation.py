import numpy as np
import pandas as pd

from datamanipulation import DataManipulation

class DataTransformation(DataManipulation):

    def __init__(self, bank_name_param='Bank of America', category_param='Old Age Pension', interest_rate_param=5, flag_status_param=" Pensioner-Bonus Interest Credited ",
                 modifiedfile_path_param='csv_files/bonus_to_pensioners.csv'):
        self.modifiedfile_path = modifiedfile_path_param
        self.bank_name = bank_name_param
        self.category = category_param
        self.interest_rate = interest_rate_param
        self.flag_status = flag_status_param

    def pensioner_update(self, modified_Data):
        try:
         #Filtering data with the given values and finding latest balance on top of filtered data
         pensioner_df = modified_Data.query("bank == '"+self.bank_name+"' and k_symbol=='"+self.category+"'")
         filtered_data = pensioner_df.groupby('account_id', group_keys=False).apply(lambda df: df.sort_values(by='fulldatewithtime', ascending=False).iloc[0, :])[['trans_id']]
         ls_trans_id = list(filtered_data["trans_id"].values.tolist())

         #Updating balance for the transaction IDs which satisfy the given conditions
         interest=self.interest_rate/100
         modified_Data['balance'] = np.where(modified_Data["trans_id"].isin(ls_trans_id), (modified_Data['balance'] + (interest * modified_Data['balance'])) , modified_Data['balance'])

         #update existing flag for trx IDs
         modified_Data=self.update_flag(modified_Data, ls_trans_id, self.flag_status)

         #Transforming the data to CSV
         if (self.transform_to_csv(modified_Data, self.modifiedfile_path)):
             print("Created "+ self.modifiedfile_path +" file")
        except Exception as err:
            print("Error in updating pension balance - ", err)

    def digital_cash_ratio(self, modified_data):
        try:
         #filtered data with bank value and operation not null
         cf = modified_data.query("bank ! = ' ' and TransactionType !='nan'")
         df = cf.groupby(['bank', 'TransactionType']).size()
         df = df.reset_index()
         df.columns = ['bank', 'TransactionType', 'TypeCount']

         #Finding ratio for all banks
         bank_ratio=df.groupby(['bank']).apply(self.trxtypes_ratio)
         bankratio_df=pd.DataFrame({'BankName': bank_ratio.index, 'RatioCount': bank_ratio.values})
         ratios_list=list(bankratio_df.loc[:, "RatioCount"])

         #Finding max ratio and bank with max ratio
         if all(i == 0 for i in ratios_list):
            print("All banks have only one either cash or digital transaction type hence cannot find ratio")
         else:
            max_ratio=max(bankratio_df.loc[:, "RatioCount"])
            max_ratio_index = bankratio_df.index[bankratio_df["RatioCount"]==max_ratio].values[0]
            bank_with_maxratio=bankratio_df.at[max_ratio_index,'BankName']
            print(bank_with_maxratio+" with "+str(max_ratio))
        except Exception as err:
            print("Error in finding Digital/cash ratio - ", err)

    def trxtypes_ratio(self, df):
        trxtypes_list = df['TransactionType'].values

        #Checking if transaction type has both cash and digital trxs for a bank
        if len(trxtypes_list) == 2:
            Cash_trxCount = df[df.TransactionType == 'Cash'].TypeCount.values[0]
            Digital_trxCount = df[df.TransactionType == 'Digital'].TypeCount.values[0]
            ratio = Digital_trxCount / Cash_trxCount
        #When one of the value is missing then finding ratio with existing type
        elif len(trxtypes_list) == 1:
            type_value = trxtypes_list[0]

            if type_value == 'Digital':
                digital_Count = df[df.TransactionType == type_value].TypeCount.values[0]
                ratio = 0
            else:
                cash_Count = df[df.TransactionType == type_value].TypeCount.values[0]
                ratio = 0
        return ratio
