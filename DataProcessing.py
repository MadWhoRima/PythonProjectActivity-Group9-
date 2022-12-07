import pandas as pd

from DataManipulation import DataManipulation
from ExternalCode.EmailFeature import EmailFeature

modifiedfile_path='CSVFiles/Cash_transactions_data.csv'
transaction_type='Cash'

class DataProcessing:

    def find_maxcashtransactions(modifiedData):
        try:
         #Filtering data based on cash for every year
         Cashtrxyearly_df = modifiedData.query("TransactionType == '"+transaction_type+"'").groupby('year')
         cash_df=Cashtrxyearly_df.size()
         cash_df=pd.DataFrame({'Year': cash_df.index, 'No. of transactions': cash_df.values})

         #Finding transaction type done the most
         cash_trxtype=Cashtrxyearly_df.apply(DataProcessing.max_cash_operationtype)
         cash_trxtype=pd.DataFrame({'Year': cash_trxtype.index, 'Preferred transaction type': cash_trxtype.values})

         #Merging the dataframes
         final_df=pd.merge(cash_df,cash_trxtype, on='Year')

         #Transforming the data to CSV
         if(DataManipulation.transform_to_csv(final_df, modifiedfile_path)):
             print("Created Cash_transactions_data csv file")
        except:
            print("Error in finding max cash transactions")


    def max_cash_operationtype(final_data):
        return final_data['operation'].value_counts().idxmax()


    def sendmails_minbal_accounts(modifiedData):
        try:
         #Finding latest transaction for account ID
         filtered_data = modifiedData.groupby('account_id').apply(lambda df: df.sort_values(by='fulldatewithtime', ascending=False).iloc[0, :])[['account_id', 'balance']]
         df = filtered_data[filtered_data.balance < 800]
         mails_count=len(df)

         #Sending mails to min bal accounts
         df.apply(EmailFeature.sending_mail, axis=1)
         print("Sent mails to low balance accounts - "+str(mails_count))
        except:
           print("Error in sending alert mails to low balance accounts")
