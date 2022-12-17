import pandas as pd

from datamanipulation import DataManipulation
from reusable_entities.emailfeature import EmailFeature

class DataProcessing:
    def __init__(self, trxtype_param='Cash', min_balance_param=800, modifiedfile_path_param='csv_files/cash_transactions_data.csv'):
        self.transaction_type = trxtype_param
        self.min_balance = min_balance_param
        self.modifiedfile_path = modifiedfile_path_param

    def find_maxcashtransactions(self, modifiedData):
        try:
         datamanipulation_obj = DataManipulation()

         #Filtering data based on cash for every year
         cashtrx_yearly_df = modifiedData.query("TransactionType == '"+self.transaction_type+"'").groupby('year')
         cash_df=cashtrx_yearly_df.size()
         cash_df=pd.DataFrame({'Year': cash_df.index, 'No. of transactions': cash_df.values})

         #Finding transaction type done the most
         cash_trxtype=cashtrx_yearly_df.apply(DataProcessing.max_cash_operationtype)
         cash_trxtype=pd.DataFrame({'Year': cash_trxtype.index, 'Preferred transaction type': cash_trxtype.values})

         #Merging the dataframes
         final_df=pd.merge(cash_df,cash_trxtype, on='Year')

         #Transforming the data to CSV
         if(datamanipulation_obj.transform_to_csv(final_df, self.modifiedfile_path)):
             print("Created "+ self.modifiedfile_path +" file")
        except Exception as err:
            print("Error in finding max cash transactions - ", err)


    def max_cash_operationtype(final_data):
        return final_data['operation'].value_counts().idxmax()


    def sendmails_minbal_accounts(self, modifiedData):
        try:
         #Finding latest transaction for account ID
         filtered_data = modifiedData.groupby('account_id').apply(lambda df: df.sort_values(by='fulldatewithtime', ascending=False).iloc[0, :])[['account_id', 'balance']]
         balance_accts_df = filtered_data[filtered_data.balance < self.min_balance]
         mails_count=len(balance_accts_df)

         #Sending mails to min bal accounts
         balance_accts_df.apply(EmailFeature.sending_mail, axis=1)
         print("Sent mails to low balance accounts - "+str(mails_count))
        except Exception as err:
           print("Error in sending alert mails to low balance accounts - ", err)


