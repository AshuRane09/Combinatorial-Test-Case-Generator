import sys

from datetime import datetime

from os import system, name

from qlpsoalgo import QlPSO
# from qlpsomain import qlpso1

from itertools import combinations
import xlwt
from xlwt import Workbook
import pandas as pd
import numpy as np
import gspread as gc
import math
from oauth2client.service_account import ServiceAccountCredentials


import sys

from datetime import datetime

from os import system, name

from qlpsoalgo import QlPSO

import pandas as pd

import numpy as np

from itertools import combinations
import xlwt
from xlwt import Workbook
  

wb = Workbook()
  

sheet1 = wb.add_sheet('Sheet 2')
inp = []

combo = []

#f = open("result.txt", "a+")
#f1=pd.read_excel("/Users/HP/Desktop/Folders/FIN/New folder/QLPSO/new/myfile.xlsx")
#f1 = pd.read_excel("/Users/pavanhattalli/Documents/Internship/Codes/QLPSO_TEST/myfile2.xlsx")
f1 = pd.read_excel("myfile.xlsx")
df1=f1
parameter_list = {}

for i,j in f1.iterrows():

    if "Select" in j[0] and "Infeasible Input" not in j[1]:

        combo.append(j[1].split(','))

for i in combo:

    count = 0

    for j in i:

        count += 1

    inp.append(count)

count = 1

for i in combo:

    for j in i:

        parameter_list[count] = j

        count += 1



def screen_clear():

   if name == 'nt':

      _ = system('cls')

  

   else:

      _ = system('clear')





def convert_to_arrays(dimensions):

    #print("dimensions=",dimensions)

    opts = []



    for d in dimensions:

        r = []

        for _i in range(d[1]):

            r.append(range(d[0]))

        opts += r

    return opts





def do_ql_optimization(dimensions):

    input_list = []



    for d in dimensions:

        input_list.append("%i^%i" % d)

        #print(input_list)



    pairwise= QlPSO(convert_to_arrays(dimensions))

    oppairs = QlPSO(convert_to_arrays(dimensions))

    n = len(list(pairwise))

    #f = open("result.txt", "a")

    #print()

    #f.write("\n")

    #f.write("INPUT : {:s}: QLPSO BEST SOLUTION {:d} TESTCASES GENERATED".format(" * ".join(input_list), n) + "\n")

    

    #print()

    print("\n\nINPUT : {:s}: QLPSO BEST SOLUTION {:d} TESTCASES GENERATED".format(" * ".join(input_list), n))



    a = list(oppairs)
    #print("\n\n\n")
    #print(a)
    #print("Total Test Cases  :  ",len(a))
    data = pd.DataFrame()

    

    #f.write(str(a))

    values=int(input_list[0][0])

    test_cases=[]

    '''for x in range(len(a)):

        b=[]

        for y in range(len(a[0])):

            b.append((values*y)+(a[x][y]+1))

        test_cases.append(b)
    '''
    inp2=[]
    counter=1
    
    #Converting Index Based Test Cases into Integers
    for i in range(len(inp)):
        inp3=[]
        for j in range(inp[i]):
            inp3.append(counter)
            counter=counter+1
        inp2.append(inp3)
        
    for x in range(len(a)):
        b=[]
        counter=0
        for y in a[x]:
            b.append(inp2[counter][y])
            counter=counter+1
        test_cases.append(b)
    counter=1

    tc_string = []
    #print(parameter_list)
    #Converting Integer Testcases back into string parameters
    for i in test_cases:

        tc = []

        for j in i:

            tc.append(parameter_list[j]) 

        tc_string.append(tc)     

    data["TEST CASES"] = test_cases

    index = [z for z in range(1,len(test_cases)+1)]

    data[""] = index

    data.set_index([""],inplace = True)

    #f.write("TEST CASES : \n%s" % data) 

    #f.write("REMAINING PAIRS = %s" %(oppairs.rem_pairs))

    

    #print("Max unique pairs=",oppairs.maxUniquePairs)

    #print("Result:\n",data)

    #print("\nNumber of test Cases: ",len(test_cases))

    data1 = pd.DataFrame()

    data1["TEST"] = tc_string

    #print(data1)
    #f.write("\n\n-----------TEST CASES-----------\n")
    
    '''for i in (tc_string):
        f.write("\n"+str(counter)+" "+str(i))
        print("\n"+str(counter)+" "+str(i))
        counter=counter+1
    print(inp)
    '''
    for i in range(len(tc_string)):
        for j in range(len(tc_string[i])):
            sheet1.write(i,j,tc_string[i][j])
    
    wb.save('QLPSO_Results.xlsx')
    
try:

    screen_clear()

    

    start = datetime.now()

    #print()

    num_inputs=len(inp)

    #print(num_inputs)

    str_parameter = ""

    lst = []

    k=0

    lst1 = []
    temp = set()
    for x in range(num_inputs):

        num_parameter=1

        num_values=inp[x]

        str_parameter = str_parameter + '(' + str(num_values) + ',' + str(num_parameter) + '),'
        lst.append(num_values)

        lst.append(num_parameter)
    print("lst=",lst)
    for i in range(0,len(lst)-1,2):
        lst1.append((lst[i],lst[i+1]))
    print(lst1)
    
        
    str_parameter = str_parameter[:-1]
    
    do_ql_optimization((lst1))
    '''
    if num_inputs==3:
           
        do_ql_optimization(((lst[0], lst[1]), (lst[2], lst[3]), (lst[4], lst[5])))

    elif num_inputs==4:

        do_ql_optimization(((lst[0], lst[1]), (lst[2], lst[3]), (lst[4], lst[5]), (lst[6], lst[7])))    

    elif num_inputs==5:

        do_ql_optimization(((lst[0], lst[1]), (lst[2], lst[3]), (lst[4], lst[5]), (lst[6], lst[7]), (lst[8], lst[9])))

    elif num_inputs==6:

        do_ql_optimization(((lst[0], lst[1]), (lst[2], lst[3]), (lst[4], lst[5]),(lst[6], lst[7]),(lst[8], lst[9]),(lst[10], lst[11])))
    '''
    end = datetime.now()

    time_taken = end - start

    #print()

    print('Required Time for execution : ',time_taken) 



except Exception as err:

    print("Unexpected error:", sys.exc_info()[0])

    print(err)

    print("Invalid Inputs given. Please try again")





percent = {}
for param, value in zip(df1["parameter"], df1["values"]):
    if "%" in value:
        print(value)
        res = any(chr.isdigit() for chr in value)
        if res:
            temp = int(''.join(filter(str.isdigit, value)))
            percent[param] = temp

df1 = df1[df1["parameter"].str.contains("Select") == True]






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

df1['parameter'] = df1["parameter"].apply(Select)
df1['parameter'] = df1["parameter"].apply(Concession)

ql = []
for param, value in zip(df1["parameter"], df1["values"]):
    if "Infeasible Input" in value:
        continue
    else:
        ql.append(param)
        
        
ql


df2=pd.read_excel("QLPSO_Results.xlsx",header=None,names=ql,skiprows=1)


main_df1 = df2


z = []
for param, value in zip(df1["parameter"], df1["values"]):
    if "Infeasible Input" in value:
        z.append(param)
final_infeasible = list(map(str.strip, z))
print(final_infeasible)

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

print(final_infe)




last_final = []
for singers in final_infe:
    last = []
    for singer in singers:
        last.append(singer.title())
    last_final.append(last)

print(last_final)





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

df1.index

df2=df1.reset_index()
df3=df1.set_index('Concession Type Name')


df3.drop('Concession Category Name',axis=1,inplace=True)

df3.reset_index(inplace=True)
Abb = dict(df3.values)

journey = {"Sleeper":"SL","First":"1st","AC-I":"1AC","AC First":"1AC","Second":"2nd","AC-II":"2AC","AC-III":"3AC","CC":"CC"}

# percentage['2']

Abb

main_df1.fillna(value='NA', inplace=True)


concessions = []
for row in main_df1.to_dict(orient="records"):
    alist = []
    jour = row['Journey Class']
    jour = jour.strip()
    for i in list(row.values())[2:]:
        i=str(i)
        i = i.strip()
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
                x1 = y[0] + (int(percentage['2'])/100)*y[1]
                alist.append(x1)
            elif len(y) == 3:
                x1 = y[0] + (int(percentage['3'])/100)*y[1]
                alist.append(x1)
            else:
                x1 = y[0] + (int(percentage['If No. of concession types selected more than 3'])/100)*y[1]
                alist.append(x1)
            continue
        alist.append(df.loc[journey[jour]][Abb[i]])
    
    cleanedList = [x for x in alist if (math.isnan(x) == False)]
    cleanedList.sort(reverse=True)
    concession = 0
    if len(cleanedList) > 3:
        concession = cleanedList[0] + cleanedList[1] *(int(percentage['If No. of concession types selected more than 3'])/100)
    elif len(cleanedList) == 3:
        concession = cleanedList[0] + cleanedList[1]*(int(percentage['3'])/100)

    elif len(cleanedList) == 2:
        concession = cleanedList[0] + cleanedList[1]*(int(percentage['2'])/100)

    elif len(cleanedList) == 1:
        concession = cleanedList[0]
    else:
        concession = 0

    if concession > 100:
        concession = percentage['Maximum Allowed Concession']
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

main_df1.to_excel("QLPSO_Final.xlsx")
