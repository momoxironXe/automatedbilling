import argparse
import math
import pandas as pd
import os
from tinydb import TinyDB, Query
import utility





print("\n\nStarting " + utility.file_name_selector.DCAT + "...\n")

folder_list = utility.load_data_folder()
raw_folder_path = "./raw"
file_name = utility.file_name_selector.DCAT



for directory in folder_list:
    directory:str
    directory= directory.upper()


    print(f"Loading Data... {directory}")


    file_name_selected = os.path.join(raw_folder_path, directory, file_name)
    df = pd.read_csv(file_name_selected, delimiter='\t', skiprows=1)

    # Make rows
    rows = list()

    # Check Correct Row
    for _, r in df.iterrows():
        row = list(r)
        # Check if there is invalid field
        isValid = True

        for index in range(len(row)):
            if type(row[index]).__name__ == "float":
                isValid = False
                break

            row[index] = row[index].strip().replace("$","")

        if isValid: # valid filed so add row
            rows.append(row)
        else: # invalid field
            continue

    rows.pop(0) # Remove header



    print(f"Saving Data To Database... {directory}")

    data_dict_list = []
    for raw in rows:

        data_dict = {
            "Category": raw[0],
            "TypeOfClaim": raw[1],
            "BillingClinic": raw[2],
            "RosterPhys": raw[3],
            "PatienHN": raw[4],
            "FeeCode": raw[5],
            "AmountPaid": raw[6],
         }
        

        data_dict_list.append({file_name:data_dict})


    result =utility.data_insert_multi_if_not_exist(directory,file_name, data_dict_list)
    if result:
        print(f"Finished... {directory}\n")
    else:
        print(f"Already Exists In Database... {directory }  {file_name}\n")






