import os
import utility






def extract_LTC_and_NON_LTC(file_data ,name):
    

    data_split_by_word =file_data.split(name)
    data_split_by_word = data_split_by_word[1:3] # select only LTC and NON-LTC
    data_split_by_word = [x.strip() for x in data_split_by_word] 

    data_LTC = data_split_by_word[0].split(" ")[0]
    data_NON_LTC = data_split_by_word[1].split(" ")[0]

    value =  {}
    value["LTC"] = data_LTC
    value["NON-LTC"] = data_NON_LTC
    return value



def extract_normal(file_data ,name):
    price = file_data.split(name)[1].strip()
    price =price.split(" ")[0]
    return price


def extract_normal_end(file_data ,name):

    price = file_data.split(name)[1]
    price = price.split("\n")[0].strip()
    price = price.split(" ")[-1]
    return price



def extract_data(file_data):



    data = None
    with open(file_data, 'r') as file:
        data = file.read()

    extract = {}

    #---------------------------------------------------------
    split_vale =  data.split("PREMIUM PAYMENTS")[1:][0]
    grope = split_vale.split("GROUP BILLING NUMBER:")[-1].split("\n")[0].strip()

    variable = "BLENDED PREMIUM    15.00%"
    value = extract_normal_end(split_vale , variable)
    extract[variable] = (grope,value)

    variable = "BLENDED PREMIUM    19.41%"
    value = extract_normal_end(split_vale , variable)
    extract[variable] = (grope,value)

    #---------------------------------------------------------


    #---------------------------------------------------------
    split_vale =  data.split("PREMIUM PAYMENTS")[1:][1]
    grope = split_vale.split("GROUP BILLING NUMBER:")[-1].split("\n")[0].strip()

    variable = "GERIATRIC GA       15.00%"
    value = extract_normal_end(split_vale , variable)
    extract[variable] = (grope,value)


    variable = "GERIATRIC IA       15.00%"
    value = extract_normal_end(split_vale , variable)
    extract[variable] = (grope,value)

    #---------------------------------------------------------




    #---------------------------------------------------------
    split_vale =  data.split("GROUP TOTAL - SUMMARY REPORT")[1]
    grope = split_vale.split("GROUP - ")[1].split(" ")[0]

    variable = "TOTAL FFS CLAIMS PAYMENT"
    value = extract_normal(split_vale , variable)
    extract[variable] = (grope,value)

    variable = "TOTAL AGE PREMIUM"
    value = extract_normal(split_vale , variable)
    extract[variable] = (grope,value)

    variable = "  GMLP  " # add space because we have multiple GMLP
    value = extract_normal(split_vale , variable)
    extract[variable.strip()] = (grope,value)

    variable = "TOTAL ACCESS BONUS PAYMENT"
    value = extract_normal(split_vale , variable)
    extract[variable] = (grope,value)

    variable = "OFFICE PRACTICE ADMIN PAYMENT"
    value = extract_normal(split_vale , variable)
    extract[variable] = (grope,value)
    #---------------------------------------------------------

    #---------------------------------------------------------

    variable = "THRESHOLD"
    value =  data.split("TOTAL PAID (A + B + C) - D = ")[2].split("\n")[0].strip()
    extract[variable] = (grope,value)

    #---------------------------------------------------------

    #---------------------------------------------------------
    split_vale =  data.split("GROUP LTC ACCESS BONUS SUMMARY REPORT")[1]
    grope = split_vale.split("GROUP:")[1].strip().split(" ")[0]


    variable = "MAXIMUM SPECIAL PAYMENT"
    value = extract_normal(split_vale , variable)
    extract["LTC "+variable] = (grope,value)


    variable = "ENROLLED PATIENTS OUTSIDE USE TOTAL"
    value = extract_normal(split_vale , variable)
    extract["LTC "+variable] = (grope,value)


    variable = "ACCESS BONUS CALCULATION"
    value = extract_normal(split_vale , variable)
    extract["LTC "+variable] = (grope,value)


    variable = "ACCESS BONUS PAYMENT"
    value = extract_normal(split_vale , variable)
    extract["LTC "+variable] = (grope,value)


    variable = "ACCESS BONUS RECONCILIATION"
    value = extract_normal(split_vale , variable)
    extract["LTC "+variable] = (grope,value)

    #---------------------------------------------------------


    #---------------------------------------------------------
    split_vale =  data.split("GROUP NON-LTC ACCESS BONUS SUMMARY REPORT")[1]
    grope = split_vale.split("GROUP:")[1].strip().split(" ")[0]


    variable = "MAXIMUM SPECIAL PAYMENT"
    value = extract_normal(split_vale , variable)
    extract["NON-LTC "+variable] = (grope,value)

    variable = "ENROLLED PATIENTS OUTSIDE USE TOTAL"
    value = extract_normal(split_vale , variable)
    extract["NON-LTC "+variable] = (grope,value)

    variable = "ACCESS BONUS CALCULATION"
    value = extract_normal(split_vale , variable)
    extract["NON-LTC "+variable] = (grope,value)

    variable = "ACCESS BONUS PAYMENT"
    value = extract_normal(split_vale , variable)
    extract["NON-LTC "+variable] = (grope,value)

    variable = "ACCESS BONUS RECONCILIATION"
    value = extract_normal(split_vale , variable)
    extract["NON-LTC "+variable] = (grope,value)
    #---------------------------------------------------------

    #---------------------------------------------------------
    split_vale =  data.split("GMLP REPORT")[1]
    grope = split_vale.split("GROUP:")[1].strip().split(" ")[0]


    variable = "TOTAL ENROLLED PATIENTS"
    value = extract_normal(split_vale , variable)
    extract["GMLP "+variable] = (grope,value)

    variable = "TOTAL MEMBER DAYS"
    value = extract_normal(split_vale , variable)
    extract["GMLP "+variable] = (grope,value)

    variable = "ADJUSTED MEMBER DAYS"
    value = extract_normal(split_vale , variable)
    extract["GMLP "+variable] = (grope,value)

    variable = "CURRENT MONTH GMLP PAYMENT"
    value = extract_normal(split_vale , variable)
    extract["GMLP "+variable] = (grope,value)

    variable = "ADJUSTED GMLP PAYMENT"
    value = extract_normal(split_vale , variable)
    extract["GMLP "+variable] = (grope,value)
    #---------------------------------------------------------



    #---------------------------------------------------------

    split_vale =  data.split("   PAYMENT SUMMARY REPORT")[1]
    grope = split_vale.split(" IDENTIFIER  :")[1].strip().split(" ")[0]

    variable = "BLENDED FEE-FOR-SERVICE PREMIUM"
    value = extract_normal(split_vale , variable)
    extract[variable + " 15%"] = (grope,value)


    special_vale =  split_vale.split(variable)[2]
    special_vale = variable + special_vale
    variable = variable
    value = extract_normal(special_vale , variable)
    extract[variable + " 19.41%"] = (grope,value)


    variable = "BASE RATE PAYMENT"
    value = extract_normal(split_vale , variable)
    extract[variable] = (grope,value)

    variable = "BASE RATE PAYMENT ADJUSTMENT"
    value = extract_normal(split_vale , variable)
    extract[variable] = (grope,value)

    variable = "TOTAL BASE RATE"
    value = extract_normal(split_vale , variable)
    extract[variable] = (grope,value)

    variable = "COMPREHENSIVE CARE CAPITATION PYMT"
    value = extract_normal(split_vale , variable)
    extract[variable] = (grope,value)

    variable = "COMPREHENSIVE CARE CAPITATION ADJ"
    value = extract_normal(split_vale , variable)
    extract[variable] = (grope,value)

    variable = "TOTAL COMPREHENSIVE CARE"
    value = extract_normal(split_vale , variable)
    extract[variable] = (grope,value)


    #---------------------------------------------------------

    #---------------------------------------------------------

    split_vale =  data.split("HR8LTC ACCESS BONUS: ")[1]
    # grope =# group same before


    variable = "MAXIMUM SPECIAL PAYMENT"
    value = extract_normal(split_vale , variable)
    extract["LTC "+variable + " SUB_GROUP" ] = (grope,value)

    variable = "ENROLLED PATIENTS OUTSIDE USE TOTAL"
    value = extract_normal(split_vale , variable)
    extract["LTC "+variable + " SUB_GROUP" ] = (grope,value)

    variable = "ACCESS BONUS CALCULATION"
    value = extract_normal(split_vale , variable)
    extract["LTC "+variable + " SUB_GROUP" ] = (grope,value)

    variable = "ACCESS BONUS PAYMENT"
    value = extract_normal(split_vale , variable)
    extract["LTC "+variable + " SUB_GROUP" ] = (grope,value)

    #---------------------------------------------------------

    #---------------------------------------------------------

    split_vale =  data.split("HR8NON-LTC ACCESS BONUS: ")[1]
    # grope =# group same before


    variable = "MAXIMUM SPECIAL PAYMENT"
    value = extract_normal(split_vale , variable)
    extract["NON-LTC "+variable + " SUB_GROUP" ] = (grope,value)

    variable = "ENROLLED PATIENTS OUTSIDE USE TOTAL"
    value = extract_normal(split_vale , variable)
    extract["NON-LTC "+variable + " SUB_GROUP" ] = (grope,value)

    variable = "ACCESS BONUS CALCULATION"
    value = extract_normal(split_vale , variable)
    extract["NON-LTC "+variable + " SUB_GROUP" ] = (grope,value)

    variable = "ACCESS BONUS PAYMENT"
    value = extract_normal(split_vale , variable)
    extract["NON-LTC "+variable + " SUB_GROUP" ] = (grope,value)
    #---------------------------------------------------------


    #---------------------------------------------------------

    split_vale =  data.split("HR8GMLP: ")[1]
    # grope =# group same before


    variable = "TOTAL ENROLLED PATIENTS  "
    value = extract_normal(split_vale , variable)
    extract["GMLP "+variable + " SUB_GROUP" ] = (grope,value)

    variable = "TOTAL MEMBER DAYS"
    value = extract_normal(split_vale , variable)
    extract["GMLP "+variable + " SUB_GROUP" ] = (grope,value)

    variable = "ADJUSTED MEMBER DAYS"
    value = extract_normal(split_vale , variable)
    extract["GMLP "+variable + " SUB_GROUP" ] = (grope,value)

    #---------------------------------------------------------



    #---------------------------------------------------------

    split_vale =  data.split("PREVENTIVE CARE")[1]
    # grope =# group same before


    variable = "INFLUENZA VACCINE"
    value = extract_normal(split_vale , variable)
    extract["PREVENTIVE CARE "+variable + " SUB_GROUP" ] = (grope,value)

    variable = "PAP SMEAR"
    value = extract_normal(split_vale , variable)
    extract["PREVENTIVE CARE "+variable + " SUB_GROUP" ] = (grope,value)

    variable = "MAMMOGRAPHY"
    value = extract_normal(split_vale , variable)
    extract["PREVENTIVE CARE "+variable + " SUB_GROUP" ] = (grope,value)

    variable = "CHILDHOOD IMMUNIZATION"
    value = extract_normal(split_vale , variable)
    extract["PREVENTIVE CARE "+variable + " SUB_GROUP" ] = (grope,value)

    variable = "COLORECTAL SCREENING"
    value = extract_normal(split_vale , variable)
    extract["PREVENTIVE CARE "+variable + " SUB_GROUP" ] = (grope,value)
    #---------------------------------------------------------




    split_vale =  data.split("HR8SPECIAL PREMIUMS:")[2]
    split_vale = split_vale.split("CURRENT FISCAL TOTAL ")[0]
    split_vale = split_vale.split(":")[1:]
    # grope =# group same before


    list_spacial_variable = ["HOSPITAL" , "LABOUR AND DELIVERY" , "OFFICE PROCEDURES" , "PALLIATIVE CARE" , "HOME VISITS" , "PRENATAL" , "LONG TERM CARE" , "PC-SMI"]

    for data in split_vale:



        value = data.split("\n")[-3]
        value = value.strip().split(" ")
        # remove empty from list
        value = [x for x in value if x != '']
        value = value[-2]

        variable = list_spacial_variable.pop(0)
        extract["SPECIAL "+variable  ] = (grope,value)




    return extract





print("\n\nStarting " + utility.file_name_selector.RA + "...\n")

folder_list = utility.load_data_folder()
raw_folder_path = "./raw"
file_name = utility.file_name_selector.RA



for directory in folder_list:
    directory:str
    directory= directory.upper()


    print(f"Loading Data... {directory}")
    
    file = os.path.join(raw_folder_path, directory, file_name)

    extract = extract_data(file)


    print(f"Saving Data To Database... {directory}")

    data_dict_list = []
    for key , value in extract.items():
        group = value[0]
        value = value[1]

        data_dict = {
            "Item": key,
            "Group ID": group,
            "Value": value,
        }
        

        data_dict_list.append({file_name:data_dict})


    result =utility.data_insert_multi_if_not_exist(directory,file_name, data_dict_list)
    if result:
        print(f"Finished... {directory}\n")
    else:
        print(f"Already Exists In Database... {directory }  {file_name}\n")


