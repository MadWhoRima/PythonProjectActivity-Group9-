import uu

from datamanipulation import DataManipulation
from datatransformation import DataTransformation
from dataprocessing import DataProcessing

sourcefile_path= "csv_files/transaction_data_encoded"
decodedfile_path= "csv_files/transaction_data_decoded.csv"

def main_execution():

    #Decoding file
    uu.decode(sourcefile_path, decodedfile_path)

    datamanipulation_obj=DataManipulation()
    final_data = datamanipulation_obj.data_modify(decodedfile_path)

    #Finding Max transactions
    dataprocessing_obj=DataProcessing()
    dataprocessing_obj.find_maxcashtransactions(final_data)

    #Sending alert emails to min account balance holders
    #dataprocessing_obj.sendmails_minbal_accounts(final_data)

    #Pensioner flag
    datatransformation_obj=DataTransformation()
    datatransformation_obj.pensioner_update(final_data)

    #Max Cash ratio
    datatransformation_obj.digital_cash_ratio(final_data)


if __name__ == '__main__':
    main_execution()
