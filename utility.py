import os
from tinydb import TinyDB, Query
from tinydb.operations import add
db = TinyDB('DataBase.json')
raw_folder_path = "./raw" 

class file_name_selector:
    DCAT = "DCP File as Tab Separated File.txt"
    Error = "Error - Raw.848"
    OU = "Ladak OU - Raw.040"
    RA = "Ladak RA - Raw.037"
    Roster = "Roster List as XML.xml"
    Annual_CC = "Annual Capitation Calculator.csv"
    Service_fee = "Service_code_Fee.csv"







def data_insert_if_not_exist(date , type , data_dict):
    messages_table = db.table(date)

    check = messages_table.search( Query()[type] == data_dict )
    if len(check) == 0:
        messages_table.insert({type:data_dict})


def data_insert_multi_if_not_exist(date  ,type, data_dict):
    messages_table = db.table(date)
    check_exists_data =  messages_table.search( Query()[type].exists() )
    if len(check_exists_data) == 0:
        messages_table.insert_multiple(data_dict)
        return True
    else:
        return False



def check_table_exist(date):
    tables = db.tables()
    if date in tables:
        return True
    else:
        return False
    
def check_folder_exist(folder_list):

    allow_folder_list = []
    for directory in folder_list:
        if not check_table_exist(directory):
            allow_folder_list.append(directory)
        else:
            print(f"Already Exists... {directory}\n")

    return allow_folder_list










def load_data_folder():
    print("______________ Directory Detected ______________")


    data_folder_list = []
    for root, dirs, files in os.walk(raw_folder_path):
        for directory in dirs:
            data_folder_list.append(directory)
            print("detected directory: " + directory)

    print("________________________________________________\n")

    return data_folder_list



def RA_get_file_raw(data_folder_list):
    RA = {}
    for directory in data_folder_list:
        with open("raw/"+directory+"/Ladak RA - Raw.037", 'r') as file:
            RA[directory] = file.read()
        
    return RA




def currency_value(currency):
    number = float(currency.replace(",", ""))
    return number



def extract_LTC_and_NON_LTC(file_data ,name):
    

    data_split_by_word =file_data.split(name)
    data_split_by_word = data_split_by_word[1:3] # select only LTC and NON-LTC
    data_split_by_word = [x.strip() for x in data_split_by_word] 

    data_LTC = data_split_by_word[0].split(" ")[0]
    data_NON_LTC = data_split_by_word[1].split(" ")[0]

    value =  {}
    value["LTC"] = currency_value(data_LTC)
    value["NON-LTC"] = currency_value(data_NON_LTC)
    return value
