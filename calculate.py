from tinydb import TinyDB, Query
from tinydb import where
from math import fsum
import calendar
from datetime import date , timedelta


db = TinyDB('DataBase.json')
tables = db.tables()

def get_price(table, file_name , key, variable , select):
    maximum_special_payment_ltc = db.table(table).search(Query()[file_name][key]==variable)
    data = maximum_special_payment_ltc[0][file_name][select]
    return float(data.replace(",",""))




Annual_cc_db = TinyDB('Annual_CC_DataBase.json')
def get_annual_capitation(file_name , Sex ,  age , key):
    data = Annual_cc_db.search((Query()["Annual Capitation Calculator.csv"]["Sex"]==Sex.lower()) & (Query()["Annual Capitation Calculator.csv"]["Age"]==str(age)))
    data = data[0][file_name][key]
    return float(data.replace(";","."))




def currency_value(currency):
    formatted_number = formatted_number = format(currency, ",.2f")
    return formatted_number


def Group_performance():
    date_info = list()
    Group_Access_bonus_potential = list()
    Enrolled_patient_group_outside_use = list()
    Your_group_access_bonus = list()
    Your_group_access_bonus_percent = list()


    counter_selector = -1 
    for table in tables:
        counter_selector= counter_selector + 1


        date_info.append(table)
        # Group’s performance:

        # Group Access bonus potential = Maximum special payment (sum of both LTC and Non-LTC) from group (BANT in this case)
        # Enrolled patient group outside use = Enrolled patient outside use total (sum of both LTC and Non-LTC) from group (BANT in this case)
        # Your group access bonus $ = Access bonus payment (sum of both LTC and Non-LTC)
        # Your group access bonus % = Access bonus payment / Group Access bonus potential * 100%

        maximum_special_payment_ltc =  get_price(table,"Ladak RA - Raw.037" , "Item" , "LTC MAXIMUM SPECIAL PAYMENT" ,"Value")
        maximum_special_payment_non_ltc = get_price(table,"Ladak RA - Raw.037" , "Item" , "NON-LTC MAXIMUM SPECIAL PAYMENT" ,"Value")
        Group_Access_bonus_potential.append(maximum_special_payment_ltc + maximum_special_payment_non_ltc)


        enrolled_patient_outside_use_ltc = get_price(table,"Ladak RA - Raw.037" , "Item" , "LTC ENROLLED PATIENTS OUTSIDE USE TOTAL" ,"Value")
        enrolled_patient_outside_use_non_ltc = get_price(table,"Ladak RA - Raw.037" , "Item" , "NON-LTC ENROLLED PATIENTS OUTSIDE USE TOTAL" ,"Value")
        Enrolled_patient_group_outside_use.append(enrolled_patient_outside_use_ltc + enrolled_patient_outside_use_non_ltc)


        access_bonus_payment_ltc = get_price(table,"Ladak RA - Raw.037" , "Item" , "LTC ACCESS BONUS PAYMENT" ,"Value")
        access_bonus_payment_non_ltc = get_price(table,"Ladak RA - Raw.037" , "Item" , "NON-LTC ACCESS BONUS PAYMENT" ,"Value")
        Your_group_access_bonus.append(access_bonus_payment_ltc + access_bonus_payment_non_ltc)

        
        Your_group_access_bonus_percent.append(Your_group_access_bonus[counter_selector] / Group_Access_bonus_potential[counter_selector] * 100)


    print("\n\n")
    print("## ACCESS BONUS SUMMARY ##\n")
    print("# Group’s performance #")

    print(f"------------------------------------- ", end="")
    for _ in date_info:
        print(f"----------{_}---------- ", end="")
    print("")


    print("Group Access Bonus Potential        "  ,end="")
    for _ in Group_Access_bonus_potential:
        print(f"           ${currency_value(_)}        ", end="")
    print("")


    print("Enrolled Patient Group Outside Use  "  ,end="")
    for _ in Enrolled_patient_group_outside_use:
        print(f"           ${currency_value(_)}         ", end="")
    print("")


    print("Your Group Access Bonus $           "  ,end="")
    for _ in Your_group_access_bonus:
        print(f"           ${currency_value(_)}         ", end="")
    print("")

    print("Capture Rate %                     "  ,end="")
    for _ in Your_group_access_bonus_percent:
        print(f"            {round(_,1)} %            ", end="")
    print("")



def your_performance():
    net_change_in_roster = list()
    access_bonus_potential = list()
    enrolled_patient_outside_use = list()
    Your_Access_Bonus= list()
    Capture_Rate = list()

    counter_selector = -1 
    for table in tables:
        counter_selector= counter_selector + 1


        #-----------------------------------------------------
        #Your performance:

        # Net change in roster = total number of enrolled patients (derived from roster list as XML)
        # Access bonus potential = Maximum special payment (LTC + non LTC) found in Payment summary report for the individual provider (BANT-037699 in this case)
        # Enrolled patient outside use = Enrolled patients outside use total (LTC + non LTC)


        net_change_in_roster.append(db.table(table).search(Query()["Roster List as XML.xml"].exists()).__len__())


        LTC_MAXIMUM_SPECIAL_PAYMENT_SUB_GROUP = get_price(table,"Ladak RA - Raw.037" , "Item" , "LTC MAXIMUM SPECIAL PAYMENT SUB_GROUP" ,"Value")
        NON_LTC_MAXIMUM_SPECIAL_PAYMENT_SUB_GROUP = get_price(table,"Ladak RA - Raw.037" , "Item" , "NON-LTC MAXIMUM SPECIAL PAYMENT SUB_GROUP" ,"Value")
        access_bonus_potential.append(LTC_MAXIMUM_SPECIAL_PAYMENT_SUB_GROUP + NON_LTC_MAXIMUM_SPECIAL_PAYMENT_SUB_GROUP)

        LTC_ENROLLED_PATIENTS_OUTSIDE_USE_TOTAL_SUB_GROUP  = get_price(table,"Ladak RA - Raw.037" , "Item" , "LTC ENROLLED PATIENTS OUTSIDE USE TOTAL SUB_GROUP" ,"Value")
        NON_LTC_ENROLLED_PATIENTS_OUTSIDE_USE_TOTAL_SUB_GROUP = get_price(table,"Ladak RA - Raw.037" , "Item" , "NON-LTC ENROLLED PATIENTS OUTSIDE USE TOTAL SUB_GROUP" ,"Value")
        enrolled_patient_outside_use.append(LTC_ENROLLED_PATIENTS_OUTSIDE_USE_TOTAL_SUB_GROUP + NON_LTC_ENROLLED_PATIENTS_OUTSIDE_USE_TOTAL_SUB_GROUP)


        Your_Access_Bonus.append( access_bonus_potential[counter_selector] - enrolled_patient_outside_use[counter_selector])
        Capture_Rate.append(Your_Access_Bonus[counter_selector] / access_bonus_potential[counter_selector] * 100)



    print(f"-------------------------------------------------------------------------------------------------")

    print("# Your performance #")

    print("Net Change in Roster           "  ,end="")
    for _ in net_change_in_roster:
        print(f"                  {_}         ", end="")
    print("")

    print("Access Bonus Potential             "  ,end="")
    for _ in access_bonus_potential:
        print(f"           ${currency_value(_)}           ", end="")
    print("")

    print("Enrolled Patient Outside Use        "  ,end="")
    for _ in enrolled_patient_outside_use:
        print(f"          ${currency_value(_)}              ", end="")
    print("")

    print("Your Access Bonus                   " , end="")
    for _ in Your_Access_Bonus:
        print(f"          ${currency_value(_)}            ", end="")
    print("")

    print("Capture Rate                        " , end="")
    for _ in Capture_Rate:
        print(f"          {currency_value(_)} %              ", end="")
    print("")






def get_data(table, file_name , key, variable , select):
    maximum_special_payment_ltc = db.table(table).search(Query()[file_name][key]==variable)
    data = maximum_special_payment_ltc[0][file_name][select]
    return float(data.replace(",",""))





from datetime import datetime

def calculate_age(date_of_birth):
    try:
        dob = datetime.strptime(date_of_birth, "%Y-%m-%d")
        current_date = datetime.now()
        age = current_date.year - dob.year - ((current_date.month, current_date.day) < (dob.month, dob.day))
        return age
    except ValueError:
        return "Invalid date format"


def get_total_Outside_Use(table_name ,  health_number):
    found_items=[]

    table = db.table(table_name)
    data = table.search((Query()["Ladak OU - Raw.040"]["HealthNumber"]==health_number) )
    found_items.extend(data)

    sum_list = list()
    for item in found_items:
        item = item["Ladak OU - Raw.040"]
        paid = item["FeePaid"]
        for pay in paid:
            sum_list.append(pay)
    sum = 0 
    for item in sum_list:
        sum = fsum([sum ,float(item)])
        
    return sum


def get_annual_capitation_2(table_name , health_number):
    NetworkBaseRatePayment = 0 
    CompCareCapitation = 0
    MemberDay = 0
    


    table = db.table(table_name)
    data = table.search((Query()["Roster List as XML.xml"]["HealthNumber"]==health_number))
    if len(data) > 0:
        NetworkBaseRatePayment = float(data[0]['Roster List as XML.xml']['NetworkBaseRatePayment'])
        CompCareCapitation = float(data[0]['Roster List as XML.xml']['CompCareCapitation'])
        MemberDay =  int(data[0]['Roster List as XML.xml']['MemberDay'])

        member_capitation  = (NetworkBaseRatePayment + CompCareCapitation)/MemberDay
        annual_capitation = member_capitation*365
        RosterStart = data[0]['Roster List as XML.xml']['RosterStart']
        return (member_capitation  ,annual_capitation , RosterStart)


    return False

def last_day_of_month(year, month):
    _, last_day = calendar.monthrange(year, month)
    return last_day

def find_start_start_service_and_end(table_name , health_number): 
    data = db.table(table_name).search(Query()["Ladak OU - Raw.040"]["HealthNumber"]==health_number)
    ServiceDate = data[0]["Ladak OU - Raw.040"]["ServiceDate"]
    StartDate = ServiceDate[-1]
    EndDate = ServiceDate[0]

    return StartDate , EndDate

def get_service_code(table_name , health_number):
    fee_code_price_dict = {}

    data = db.table(table_name).search(Query()["DCP File as Tab Separated File.txt"]["PatienHN"]==health_number)
    if len(data) != 0:
        
        for item in data:
            fee_code_price_dict[item["DCP File as Tab Separated File.txt"]['FeeCode']] = item["DCP File as Tab Separated File.txt"]['AmountPaid']
    
    return fee_code_price_dict


def feecode_to_shadow(feecode):
    data = Annual_cc_db.search(Query()["Service_code_Fee.csv"]["code"]==feecode)
    if len(data) != 0:
        fee = data[0]['Service_code_Fee.csv']['fee']
        return fee
    



counter_selector = -1 
for table in tables:
    counter_selector= counter_selector + 1
    OU_info  = db.table(table).search(Query()["Ladak OU - Raw.040"].exists())
    

    print(f"-------------------------------------------------------------------------------------------------")
    for info in OU_info:
        info = info["Ladak OU - Raw.040"]


        exist_in_roster = get_annual_capitation_2(table, info["HealthNumber"])
        if not exist_in_roster:
            continue
        else:
            member_capitation  ,annual_capitation , RosterStart = exist_in_roster

        
        print( info["LastName"] + " , " + info["FirstName"] )
        sex = "Male" if info["SexCode"] == "M" else "Female"
        print("Sex: " + sex)
        age = calculate_age(info["DateOfBirth"])
        print("Age: " + str(age))
        print("Health Number: " + info["HealthNumber"])
        #annual_capitation = get_annual_capitation("Annual Capitation Calculator.csv" , info["SexCode"] , age, "Total")
        print("Annual Capitation: " + str(round(annual_capitation,2 )) + "$")
        print("")

        total_Outside_Use = get_total_Outside_Use(table, info["HealthNumber"])
        return_value_percentage = (total_Outside_Use / annual_capitation) * 100
        print("% Return: " + str(round(return_value_percentage)) + "%")
        print("Outside Use: " + str(total_Outside_Use))

        start , end  = find_start_start_service_and_end(table , info["HealthNumber"])
        end_data_split = end.split("-")
        last_day_of_month_value = last_day_of_month(int(end_data_split[0]) , int(end_data_split[1]))
        
        start_data_split = start.split("-")
        one_day = timedelta(days=1)
        start_data = date(int(start_data_split[0]) , int(start_data_split[1]) , int(start_data_split[2])) + one_day
        end_data = date(int(end_data_split[0]) , int(end_data_split[1]) , int(end_data_split[2]))
        last_data = date(int(end_data_split[0]) , int(end_data_split[1]) , last_day_of_month_value)

        day_diff = last_data - start_data

        Capitation = member_capitation * day_diff.days  * -1
        Capitation = round(Capitation,2)
        print("Capitation: " + str(Capitation) + "$")



        total_shadow = 0
        fee_dict =  get_service_code(table , info["HealthNumber"])
        if len(fee_dict) != 0:
             
            for key , price in fee_dict.items():
                #print("Service Code: " + key)
                fee = feecode_to_shadow(key)
                if fee != None:
                    if "." in fee:
                        fee = float(fee)
                        total_shadow += (fee * 0.806)
                        #print("Fee: " + str(fee))

                    elif "%" in fee:
                        price = float(price)
                        total_shadow += (price * 0.3)
                        #print("Fee: " + str(price))

        total_shadow = round(total_shadow,2)
        print("Shadow Billing Top Up: " +  str(total_shadow) + "$" )



        Net_Revenue = 0 
        Net_Revenue = total_Outside_Use +  Capitation + total_shadow
        Net_Revenue = round(Net_Revenue,2)

        print("Net Revenue ($):" +  str(Net_Revenue)+ "$" )

        print("")

        print ("Service List:")
        for index in range(len(info["ServiceDate"])):
            print("     " + info["ServiceDate"][index] + " " + info["FreeCode"][index] + " " + info["Description"][index] )

        print(f"-------------------------------------------------------------------------------------------------")


        













print("\n")
