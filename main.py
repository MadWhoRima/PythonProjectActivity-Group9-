import uu

from datamanipulation import DataManipulation
from datatransformation import DataTransformation
from dataprocessing import DataProcessing

sourcefile_path= "csv_files/transaction_data_encoded"
decodedfile_path= "csv_files/transaction_data_decoded.csv"

def main_execution(name):

    #Decoding file
    uu.decode(sourcefile_path, decodedfile_path)
    final_data = DataManipulation.data_modify(decodedfile_path)

    #Finding Max transactions
    DataProcessing.find_maxcashtransactions(final_data)

    #Sending alert emails to min account balance holders
    DataProcessing.sendmails_minbal_accounts(final_data)

    #Pensioner flag
    DataTransformation.pensioner_update(final_data)

    #Max Cash ratio
    DataTransformation.digital_cash_ratio(final_data)



if __name__ == '__main__':
    main_execution('PyCharm')
