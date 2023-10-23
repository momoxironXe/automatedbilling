import csv
import os
from tinydb import TinyDB, Query
import utility





print("\n\nStarting " + utility.file_name_selector.Service_fee + "...\n")




raw_folder_path = "./raw"
file_name = utility.file_name_selector.Service_fee
file_name_selected = os.path.join(raw_folder_path, file_name)
data_dict={}

print(f"Saving Data To Database... {file_name}")


# Open the CSV file
with open(file_name_selected, 'r') as file:
    # Create a CSV reader object
    reader = csv.reader(file)
    header = next(reader)



    data_dict_list = []
    # Read and process each row in the CSV file
    for row in reader:

        data_dict = {
            "code": row[0],
            "fee": row[1],
            }
        data_dict_list.append({file_name:data_dict})




db = TinyDB('Annual_CC_DataBase.json')
check_exists_data =  db.search( Query()[file_name].exists() )
if len(check_exists_data) == 0:
    db.insert_multiple(data_dict_list)





