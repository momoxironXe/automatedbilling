import argparse
import xml.etree.ElementTree as ET
import os
import utility


print("\n\nStarting " + utility.file_name_selector.OU + "...\n")

folder_list = utility.load_data_folder()
raw_folder_path = "./raw"
file_name = utility.file_name_selector.OU



for directory in folder_list:
    directory:str
    directory= directory.upper()


    print(f"Loading Data... {directory}")

    #---------------------------------------

    tree = ET.parse(os.path.join(raw_folder_path, directory, file_name))
    root = tree.getroot()

    # Make rows
    rows = list()

    # Extract Rows
    for element in root.findall(".//PATIENT"):
        row = list()


        row.append(element.find(".//PATIENT-LAST-NAME").text)    
        row.append(element.find(".//PATIENT-FIRST-NAME").text)    
        row.append(element.find(".//PATIENT-HEALTH-NUMBER").text)    
        row.append(element.find(".//PATIENT-BIRTHDATE").text)    
        row.append(element.find(".//PATIENT-SEX").text)    


        list_service = list()
        list_item = [".//SERVICE-DATE" , ".//SERVICE-CODE" , ".//SERVICE-DESCRIPTION" , ".//SERVICE-AMT"]

        for item in list_item:
            list_data  = element.findall(item)
            for date in list_data:
                list_service.append(date.text)
            row.append(list_service.copy())
            list_service.clear()


    
        rows.append(row) # Add new Row 



    print(f"Saving Data To Database... {directory}")

    data_dict_list = []
    for raw in rows:
        data_dict = {
            "LastName": raw[0],
            "FirstName": raw[1],
            "HealthNumber": raw[2],
            "DateOfBirth": raw[3],
            "SexCode": raw[4],
            "ServiceDate": raw[5],
            "FreeCode": raw[6],
            "Description": raw[7],
            "FeePaid": raw[8],
        }
        data_dict_list.append({file_name:data_dict})


    result =utility.data_insert_multi_if_not_exist(directory,file_name, data_dict_list)
    if result:
        print(f"Finished... {directory}\n")
    else:
        print(f"Already Exists In Database... {directory }  {file_name}\n")






