import pandas as pd
from itertools import product
import numpy as np
from SA.simulation_annealing import runSA
#from PSO.PSO import runPSO
import gspread as gc
import math
from oauth2client.service_account import ServiceAccountCredentials


df=pd.read_excel('myfile.xlsx')

percent = {}
for param, value in zip(df["parameter"], df["values"]):
    if "%" in value:
        print(value)
        res = any(chr.isdigit() for chr in value)
        if res:
            temp = int(''.join(filter(str.isdigit, value)))
            percent[param] = temp

df = df[df["parameter"].str.contains("Select") == True]



keys_values = percent.items()
percentage = {str(key): str(value) for key, value in keys_values}

def Select(param):
    parameter = param.split(" ")
    parameter = [x.capitalize() for x in parameter]
    print(parameter)
    if parameter[0] == "Select":
        return " ".join(parameter[1:])
    else:
        return param

def Concession(param):
    x = param.split(" ")
    if x[-1] == "Concession":
        return " ".join(x[:-1])
    else:
        return param

df['parameter'] = df["parameter"].apply(Select)
df['parameter'] = df["parameter"].apply(Concession)


data= runSA(df)

main_df = pd.DataFrame(data["output_pair"], columns = data["all_key"])
main_df.index = np.arange(1,len(main_df)+1)

main_df1 = main_df

z = []
for param, value in zip(df["parameter"], df["values"]):
    if "Infeasible Input" in value:
        z.append(param)
final_infeasible = list(map(str.strip, z))

final = []
for x in final_infeasible:
    j = x.split(" And ")
    final.append(j)

final_infe = []
for i in final:
    infe = []
    for k in i:
        if "-" in k:
            al = k.split("-")
            infe = al
        else:
            infe.append(k)
            
    final_infe.append(infe)


last_final = []
for singers in final_infe:
    last = []
    for singer in singers:
        last.append(singer.title())
    last_final.append(last)

for i in last_final:
    if len(i) == 3:
        main_df1.loc[main_df1[i[0]] == i[1],i[2]] = "NA"
    elif len(i) == 2:
        main_df1.loc[main_df1[i[0]] == "",i[1]] = "NA"

pd.DataFrame.drop_duplicates(main_df1,inplace=True)
main_df1.index = np.arange(1,len(main_df1)+1)
main_df1 = main_df1.rename_axis(index="Test Case No.")


gc1 = gc.service_account(filename='creds.json')
sh=gc1.open_by_key('1mezaJvNJ_jR-I-keGnJVUGyolyfsrWD5LWU2QLM_Gu8')
worksheet2 = sh.get_worksheet(1)
res2 = worksheet2.get_all_records()

df = pd.DataFrame.from_dict(res2)

df.set_index('', inplace=True)

worksheet3 = sh.get_worksheet(2)
res3 = worksheet3.get_all_records()
df1 = pd.DataFrame.from_dict(res3)


df2=df1.reset_index()
df3=df1.set_index('Concession Type Name')


df3.drop('Concession Category Name',axis=1,inplace=True)

df3.reset_index(inplace=True)
Abb = dict(df3.values)

journey = {"Sleeper":"SL","First":"1st","AC-I":"1AC","AC First":"1AC","Second":"2nd","AC-II":"2AC","AC-III":"3AC","CC":"CC"}

main_df1.fillna(value='NA', inplace=True)

concessions = []
for row in main_df1.to_dict(orient="records"):
    alist = []
    jour = row['Journey Class']
    jour = jour.strip()
    for i in list(row.values())[2:]:
        i=str(i)
        i = i.strip()
        #print(i)
        if i == "NA":
            alist.append(np.NaN)
            continue
        elif i == "Adult":
            alist.append(np.NaN)
            continue
        elif i == "NS":
            alist.append(np.NaN)
            continue
        elif " and " in i:
            x = i.split(' and ')
            stripped = [s.strip() for s in x]
            y = []
            for item in stripped:
                y.append(df.loc[journey[jour]][Abb[item]])
            y.sort(reverse=True)
            if len(y) == 2:
                #x1 = y[0] + 0.05*y[1]
                x1 = y[0] + (int(percentage['2'])/100)*y[1]
                alist.append(x1)
            elif len(y) == 3:
                # x1 = y[0] + 0.07*y[1]
                x1 = y[0] + (int(percentage['3'])/100)*y[1]
                alist.append(x1)
            else:
                #x1 = y[0] + 0.10*y[1]
                x1 = y[0] + (int(percentage['If No. of concession types selected more than 3'])/100)*y[1]
                alist.append(x1)
            continue
        #print(Abb[i])
        alist.append(df.loc[journey[jour]][Abb[i]])
    #for j in alist:
        #print(type(j))
    
    #print(alist)
    cleanedList = [x for x in alist if (math.isnan(x) == False)]
    cleanedList.sort(reverse=True)
    #print(cleanedList)
    concession = 0
    if len(cleanedList) > 3:
        # concession = cleanedList[0] + cleanedList[1]*0.10
        concession = cleanedList[0] + cleanedList[1] *(int(percentage['If No. of concession types selected more than 3'])/100)
    elif len(cleanedList) == 3:
        # concession = cleanedList[0] + cleanedList[1]*0.07
        concession = cleanedList[0] + cleanedList[1]*(int(percentage['3'])/100)

    elif len(cleanedList) == 2:
        # concession = cleanedList[0] + cleanedList[1]*0.05
        concession = cleanedList[0] + cleanedList[1]*(int(percentage['2'])/100)

    elif len(cleanedList) == 1:
        concession = cleanedList[0]
    else:
        concession = 0
    #print(concession)

    if concession > 100:
        concession = percentage['Maximum Allowed Concession']
#     {:.2f}.format(concession)
    concession = round(float(concession), 2)

    concessions.append(concession)


main_df1['Expected Concession'] = concessions
main_df1['Actual Output'] = ""
main_df1["Remark (Pass/Fail)"]=""

def create_tuple_for_for_columns(df_a, multi_level_col):
    temp_columns = []
    for item in df_a.columns:
        temp_columns.append((multi_level_col, item))
    return temp_columns

columns = create_tuple_for_for_columns(main_df1, 'Automated Test suite for RRS (Condensed Form)')
main_df1.columns = pd.MultiIndex.from_tuples(columns)
main_df1.fillna(value='NA', inplace=True)
main_df1.replace(to_replace ="NS",
                 value =np.nan,inplace=True)

main_df1.to_excel("SA_Final.xlsx")
