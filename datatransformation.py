import numpy as np
import pandas as pd

from datamanipulation import DataManipulation

modifiedfile_path= 'csv_files/bonus_to_pensioners.csv'
bank_name='Bank of America'
category='Old Age Pension'
interest_rate=5
flag_status=" Pensioner-Bonus Interest Credited "

class DataTransformation:

    def pensioner_update(modified_Data):
        try:
         #Filtering data with the given values and finding latest balance on top of filtered data
         pensioner_df = modified_Data.query("bank == '"+bank_name+"' and k_symbol=='"+category+"'")
         filtered_data = pensioner_df.groupby('account_id').apply(lambda df: df.sort_values(by='fulldatewithtime', ascending=False).iloc[0, :])[['trans_id']]
         ls_trans_id = list(filtered_data["trans_id"].values.tolist())

         #Updating balance for the transaction IDs which satisfy the given conditions
         interest=interest_rate/100
         modified_Data['balance'] = np.where(modified_Data["trans_id"].isin(ls_trans_id), (modified_Data['balance'] + (interest * modified_Data['balance'])) , modified_Data['balance'])

         #update existing flag for trx IDs
         modified_Data=DataManipulation.update_flag(modified_Data, ls_trans_id, flag_status)

         #Transforming the data to CSV
         if (DataManipulation.transform_to_csv(modified_Data, modifiedfile_path)):
             print("Created bonus_to_pensioners csv file")
        except:
            print("Error in updating pension balance")

    def digital_cash_ratio(modified_data):
        try:
         #filtered data with bank value and operation not null
         cf = modified_data.query("bank ! = ' ' and TransactionType !='nan'")
         df = cf.groupby(['bank', 'TransactionType']).size()
         df = df.reset_index()
         df.columns = ['bank', 'TransactionType', 'TypeCount']

         #Finding ratio for all banks
         bank_ratio=df.groupby(['bank']).apply(DataTransformation.trxtypes_ratio)
         bankratio_df=pd.DataFrame({'BankName': bank_ratio.index, 'RatioCount': bank_ratio.values})

         #Finding max ratio and bank with max ratio
         max_ratio=max(bankratio_df.loc[:, "RatioCount"])
         max_ratio_index = bankratio_df.index[bankratio_df["RatioCount"]==max_ratio].values[0]
         bank_with_maxratio=bankratio_df.at[max_ratio_index,'BankName']

         print(bank_with_maxratio+" with "+str(max_ratio))
        except:
            print("Error in finding Digital/cash ratio")

    def trxtypes_ratio(df):
        trxtypes_list = df['TransactionType'].values

        # Checking if transaction type has both cash and digital trxs for a bank
        if len(trxtypes_list) == 2:
            Cash_trxCount = df[df.TransactionType == 'Cash'].TypeCount.values[0]
            Digital_trxCount = df[df.TransactionType == 'Digital'].TypeCount.values[0]
            ratio = Digital_trxCount / Cash_trxCount
        #When one of the value is missing then finding ratio with existing type
        elif len(trxtypes_list) == 1:
            type_value = trxtypes_list[0]

            if type_value == 'Digital':
                digital_Count = df[df.TransactionType == type_value].TypeCount.values[0]
                ratio = digital_Count
            else:
                cash_Count = df[df.TransactionType == type_value].TypeCount.values[0]
                ratio = cash_Count
        return ratio




