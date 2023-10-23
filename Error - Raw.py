import argparse
import os
from tinydb import TinyDB, Query
import utility


print("\n\nStarting " + utility.file_name_selector.Error + "...\n")

folder_list = utility.load_data_folder()
raw_folder_path = "./raw"
file_name = utility.file_name_selector.Error



for directory in folder_list:
    directory:str
    directory= directory.upper()


    print(f"Loading Data... {directory}")

    rows = list()
    row = [None] * 16

    with open(os.path.join(raw_folder_path, directory, file_name), 'r') as file:
        for line in file:
            if line[0:3] in ["HXH", "HXT"]: # Remove Uncorrected row
                tmp = line.split() # Split the string

                if line[0:3] == "HXH": # If Start with HXH
                    row[0] = tmp[0][3:13] # HealthNumber Field
                    row[1] = tmp[0][13:15] # CH Field
                    row[2] = tmp[0][15:23] # DOB Field
                    row[3] = tmp[0][23:31] # InvoceNumber Field
                    row[4] = tmp[0][31:35] # Type Field

                    if (len(tmp) > 1):
                        row[6] = tmp[1][0:4] # HospNumber Field
                        row[7] = tmp[1][4:12] # Admitted Field
                        row[8] = tmp[3] # Claim Errors Field


                if line[0:3] == "HXT": # If Start with HXT
                    row[9] = tmp[0][3:8] # Code Field
                    row[10] = tmp[1][0:6] # FeeUnit Field
                    row[11] = tmp[1][6:8] # Unit Field
                    row[12] = tmp[1][8:16] # Date Field
                    row[13] = tmp[1][16:19] # Diag Field

                    if (len(tmp) > 2):
                        row[15] = tmp[2][0:3] # CodeError Field


                if (row[9] != None): # Add new Row when Code field is full
                    rows.append(row)
                    row = [None] * 16


    print(f"Saving Data To Database... {directory}")

    data_dict_list=[]
    for raw in rows:
        data_dict = {
            "HealthNumber": raw[0],
            "CH": raw[1],
            "DOB": raw[2],
            "InvoiceNumber": raw[3],
            "Type": raw[4],
            "RefPhyNumber": raw[5],
            "HospNumber": raw[6],
            "Admitted": raw[7],
            "ClaimErrors": raw[8],
            "Code": raw[9],
            "FeeUnit": raw[10],
            "Unit": raw[11],
            "Date": raw[12],
            "Diag": raw[13],
            "EXP": raw[14],
            "CodeError": raw[15],

        }
        data_dict_list.append({file_name:data_dict})


    result =utility.data_insert_multi_if_not_exist(directory,file_name, data_dict_list)
    if result:
        print(f"Finished... {directory}\n")
    else:
        print(f"Already Exists In Database... {directory }  {file_name}\n")



    #HealthNumber, CH, DOB, InvoiceNumber, Type, RefPhyNumber, HospNumber, Admitted, ClaimErrors, Code, FeeUnit, Unit, Date, Diag, EXP, CodeError

