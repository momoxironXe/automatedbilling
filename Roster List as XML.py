import argparse
import xml.etree.ElementTree as ET
import os
from tinydb import TinyDB, Query
import utility


print("\n\nStarting " + utility.file_name_selector.Roster + "...\n")

folder_list = utility.load_data_folder()
raw_folder_path = "./raw"
file_name = utility.file_name_selector.Roster



for directory in folder_list:
    directory:str
    directory= directory.upper()


    print(f"Loading Data... {directory}")
    #---------------------------------------
    # Read File as XML
    tree = ET.parse(os.path.join(raw_folder_path, directory, file_name))
    root = tree.getroot()

    # Make rows
    rows = list()
    tmp = root[1]

    # Extract correct rows and fields
    for x in range(5, len(tmp) - 15):
        row = list()
        for y in range(16):
            row.append(tmp[x][y].text)

        rows.append(row)

    print(f"Saving Data To Database... {directory}")
        
    data_dict_list = []
    for raw in rows:

        data_dict = {
            "HealthNumber": raw[0],
            "SexCode": raw[1],
            "DateOfBirth": raw[2],
            "Age": raw[3],
            "PatientName": raw[4],
            "Status": raw[5],
            "RosterStart": raw[6],
            "RosterEnd": raw[7],
            "TermCode": raw[8],
            "ConsentStatus": raw[9],
            "ActivityStart": raw[10],
            "ActivityEnd": raw[11],
            "MemberDay": raw[12],
            "ReasonCode": raw[13],
            "NetworkBaseRatePayment": raw[14],
            "CompCareCapitation": raw[15],
         }
        

        data_dict_list.append({file_name:data_dict})


    result =utility.data_insert_multi_if_not_exist(directory,file_name, data_dict_list)
    if result:
        print(f"Finished... {directory}\n")
    else:
        print(f"Already Exists In Database... {directory }  {file_name}\n")

