import csv
import os
from tinydb import TinyDB, Query
import utility





print("\n\nStarting " + utility.file_name_selector.Annual_CC + "...\n")




raw_folder_path = "./raw"
file_name = utility.file_name_selector.Annual_CC
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
            "Sex": row[0],
            "Age": row[1],
            "Base Rate": row[2],
            "Comp Care Fee": row[3],
            "Access Bonus": row[4],
            "Total": row[5],
            }
        data_dict_list.append({file_name:data_dict})




db = TinyDB('Annual_CC_DataBase.json')
check_exists_data =  db.search( Query()[file_name].exists() )
if len(check_exists_data) == 0:
    db.insert_multiple(data_dict_list)





