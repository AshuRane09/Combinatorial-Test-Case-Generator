import random
import math
from itertools import combinations
import pandas as pd

#----------------------------------------------------------------------------------------------------------

list_of_dimensions = []                                                                  # Global variables
covered_pairs = []
                                                              
num_rows = []
all_map = {}
dictionary_of_parameters = {}

unwanted_pairs_list = []

#----------------------------------------------------------------------------------------------------------

def form_pairs(l,ele):                                                                      # Forming Pairs
    pairs = []
    for i in l:
        pairs.append([ele,i])
    return pairs

#----------------------------------------------------------------------------------------

def generate_pairs(l):                                                      # Generating all possible pairs
    
    all_pairs = []
    counter1 = 1
    
    for i in l:
        temp_list = []
        
        for j in range(i):
            temp_list.append(counter1)
            counter1 = counter1 + 1
        list_of_dimensions.append(temp_list)
        
    for i in range(len(l)):
        
        temp_list2 = []
        counter2 = 0
        
        for j in range(i+1,len(l)):
            temp_list2 = temp_list2 + list_of_dimensions[j]  
        
        for k in range(len(list_of_dimensions[i])):
            temp_list3 = []
            temp_list3 = temp_list3 + temp_list2
            all_pairs = all_pairs + form_pairs(temp_list3,list_of_dimensions[i][k])

    return all_pairs

#----------------------------------------------------------------------------------------------------------    
       
def generate_random_particles(num_of_particles,size_of_each_dimension):       # Generating random particles
    
    particle_list = []
    tp = []
    
    for i in range(num_of_particles):
        tp1 = []
        temp_list = []
        for j in range(len(size_of_each_dimension)):
            temp_variable = random.randint(0,size_of_each_dimension[j]-1)
            temp_list.append(list_of_dimensions[j][temp_variable])
            tp1.append(temp_variable)
        particle_list.append(temp_list)
        tp.append(tp1)
#     print(tp)
    return particle_list,tp

#----------------------------------------------------------------------------------------------------------

def assign_random_position(size_of_each_dimension):
    maxValue = max(size_of_each_dimension)
    intial_pos = []
    
    for i in range(len(size_of_each_dimension)):
        temp_variable = random.randint(0,maxValue-1)
        intial_pos.append(temp_variable)

#------------------------------------------------------------------------------------------------------------
def runSA(df):
    #flag = int(input("Enter 1 for default test case or any other number for custom input : "))
    #flag = int(
    #    input("Enter \n 0 - To take input from xls file \n 1 - For default test case \n Any other number for custom input : "))
    flagg = 0
    if flagg == 0:
        excel_input_flag = 1
        excel_flag = 1
        while(excel_flag):
    #mple        print('\n-----Note : Please add your xlsx file in same path before running or add exact path-----\n')
    #        name = input('Enter the name of excel file : ') 
            try: 
                #input_file = pd.read_excel("myfile.xlsx")
                input_file=df
                #print('---- Input file: '+input_file)
                all_columns = []

                for i in input_file.columns:
                    print('Columns::::' + i)
                    all_columns.append(str(i))

                all_rows = []

                #### -------- Create an array of array containing all the values
                infeasible_input_str = "Infeasible Input"
                for index,row in input_file.iterrows():
                    temp_list = []
                    col_counter = 0
                    #print("FULL ROW:::: " + str(row[0] + " SECOND:::: "+str(row[1])))
                    for i in all_columns:
                        #### -------- Remove Select, Concession, Category words from the params i.e. row[0], first column, to have a clean map
                        if col_counter == 0:
                            row_zero = row[i]
                            row_zero = row_zero.replace('Select ','')
                            row_zero = row_zero.replace(' Concession','')
                            row_zero = row_zero.replace(' Category','')
                            row_zero = row_zero.title()
                            #print("row_zero>>>>> "+str(row_zero))
                            temp_list.append(row_zero)

                            # If row contains 'Infeasible Input' then put them in filter OR unwanted list.
                            if infeasible_input_str in row[1]:
                                unwanted_pairs_list.append(row_zero)
                        if col_counter != 0:
                            for j in row[i].split(','):
                                if j not in temp_list and str(j) != infeasible_input_str:
                                    #print ("What is J:" + str(j))
                                    temp_list.append(j)
                        col_counter = col_counter + 1
                    #print('temp_list'+str(temp_list))
                    if len(temp_list) != 0:
                        all_rows.append(temp_list)

                #print('all_rows>>>>>>> ::'+str(all_rows))
                print('Unwanted pairs List >>>>>>> ::'+str(unwanted_pairs_list))

                #### -------- Create a dictionary with first element as key and others as parameters
                for i in all_rows:
                    temp_list = []
                    if (len(i) > 1):
                        for j in range(1,len(i)):
                            if type(i[j]) == str:
                                temp_list.append(i[j])
                    if len(temp_list) > 0:
                        dictionary_of_parameters[i[0]] = temp_list
                    # print(i[0])
                    # print(dictionary_of_parameters[i[0]])

                print("Something....")
                print(dictionary_of_parameters)

                all_keys = list(dictionary_of_parameters.keys())
                all_values = list(dictionary_of_parameters.values())

                #print("\n\n--------------------------")
                #print("All keys "+str(all_keys))

                temp_count = 0
                for i in dictionary_of_parameters.keys():
                    num_rows.append(len(dictionary_of_parameters[i]))
                    for j in range(len(dictionary_of_parameters[i])):
                        all_map[temp_count] = dictionary_of_parameters[i][j]
                        temp_count += 1

                print("\n\n--------------------------")
                print("All map " + str(all_map))
                print("\n\n--------------------------")
                print("test case "+str(num_rows))

                num_inputs = len(num_rows)

                print('Num Rows: '+str(num_inputs))

                excel_flag = 0
            except Exception as err:
                print("\nError : File not in same directory or file name does not exist !!!]\n" + str(err))

        no_of_dimensions = num_inputs
        size_of_each_dimension=[]
        for x in range(num_inputs):
            size_of_each_dimension.append(num_rows[x])

        # if num_inputs==7:
        #     size_of_each_dimension = [num_rows[0], num_rows[1], num_rows[2], num_rows[3], num_rows[4], num_rows[5], num_rows[6]]
        # elif num_inputs==11:
        #     size_of_each_dimension = [num_rows[0], num_rows[1], num_rows[2], num_rows[3], num_rows[4], num_rows[5], num_rows[6], num_rows[7], num_rows[8], num_rows[9], num_rows[10]]
        # elif num_inputs==12:
        #     size_of_each_dimension = [num_rows[0], num_rows[1], num_rows[2], num_rows[3], num_rows[4], num_rows[5], num_rows[6], num_rows[7], num_rows[8], num_rows[9], num_rows[10], num_rows[11]]
        # elif num_inputs==13:
        #     size_of_each_dimension = [num_rows[0], num_rows[1], num_rows[2], num_rows[3], num_rows[4], num_rows[5], num_rows[6], num_rows[7], num_rows[8], num_rows[9], num_rows[10], num_rows[11], num_rows[12]]
        # elif num_inputs==14:
        #     size_of_each_dimension = [num_rows[0], num_rows[1], num_rows[2], num_rows[3], num_rows[4], num_rows[5], num_rows[6], num_rows[7], num_rows[8], num_rows[9], num_rows[10], num_rows[11], num_rows[12], num_rows[13]]

        print(size_of_each_dimension)
        no_of_particles = 2
    
        
    pairs = generate_pairs(size_of_each_dimension)
    particle_list,particle_pos = generate_random_particles(no_of_particles,size_of_each_dimension)


    total_pairs = len(pairs)
    print("\nTotal pairs : {} \nPairs :- {}".format(total_pairs,pairs))
    print("\nparticle list is -----> ",particle_list)


    ideal = (no_of_dimensions) * (no_of_dimensions - 1) // 2
        
    print("\nIdeally any configuration should cover --> {} pairs".format(ideal))   


    # Temperature and Cooling Factor

    T = 15000 #200
    cf = 0.99842 #0.99842
    print("\n\tTemperature :- {} \n\tCooling factor :- {}".format(T,cf))

    # ch = int(input("\nDo you want to change these parameters ? Enter 1 for Yes..!! :- "))
    # if ch == 1:
    #     T = int(input("Enter starting temperature (T) :- "))
    #     cf = float(input("Enter Cooling Factor (cf) :- "))

    # ------------------------------------------------------------------------------------------------

    selected_conf = []
    count = 1
    overall_prob = []
    overall_prob_dash = []
    overall_un_pair = []
    overall_temp = []
    #print("no of iterations are :- ",no_of_iter)
    while T > 0.000000000001 and len(pairs) > 0:
        
        #print("\n\n*********** Iteration no. {} ************".format(count))
        count += 1
        #no_of_iter -= 1
        #print("\nT is now --> ",T)
        pairs_in_while = []
        
        select_iter = []
        prob = []
        prob_dash = []
        un_pair_list = []
        temperature = []
        for i in range(len(particle_list)):
            uniq_p,pairs_in_while = unique_pairs(particle_list[i],pairs_in_while, pairs)
            print("\nparticle {} is generating {} unique pairs ".format(particle_list[i],uniq_p))
            if uniq_p == ideal:
                select_iter.append(particle_list[i])
                prob.append(0)
                temperature.append(T)
                prob_dash.append(0)
                un_pair_list.append(uniq_p)
            elif uniq_p > (ideal // 17):
                diff = ideal - uniq_p
                p = math.exp(-(diff)/T)
                p_dash = random.uniform(0,1)
                if p_dash < p:
                    select_iter.append(particle_list[i])
                    un_pair_list.append(uniq_p)
                    temperature.append(T)
                    prob.append(p)
                    prob_dash.append(p_dash)
                    
        for k in select_iter:
            selected_conf.append(k)
            #print("selected pairs is now ",selected_conf)
            for c in combinations(k,2):
                try:
    #                 print("removing this item from pairs list :- ",list(c))
                    pairs.remove(list(c))
                except:
                    pass
    #                 print("{} is not present in pairs (already removed in previous iterations)".format(list(c)))
                    
                
        particle_list,particle_pos = generate_random_particles(no_of_particles,size_of_each_dimension)
        
        print("\nnew set of particles are :- \n",particle_list)
        
        overall_prob = overall_prob + prob
        
        overall_prob_dash = overall_prob_dash + prob_dash
        
        overall_un_pair = overall_un_pair + un_pair_list
        
        overall_temp = overall_temp + temperature
        
        T = T * cf
        
        
    rem_pairs = len(pairs)
    coverage = ((total_pairs - rem_pairs)/ total_pairs) * 100

    print("\nNumber of pairs left to be covered :- ",rem_pairs)

    #print("\nPairs left to be covered :- \n",pairs)

    df = pd.DataFrame()
    df['Configuration'] = selected_conf
    df['Distinct_pairs'] = overall_un_pair
    df['Temperature'] = overall_temp
    df['P_dash'] = overall_prob_dash
    df['P'] = overall_prob 

    print("\n\n -----------> {} configurations with {:.2f}% coverage <--------------\n\n".format(len(selected_conf),coverage))
    final_accuracy =round(coverage, 2)
    f = open("accuracy.txt", "w")
    f.write("Accuracy : ")
    f.write(str(final_accuracy))
    f.close()
    print(df)

    print ("\n\n ----------- selected -------------")
    print(selected_conf)

    data=remove_unwanted_values_from_map(selected_conf)

    # print("\n ----------------------------- END ------------------------------------- ")

    # f = open("result.txt", "a")

    # f.write("\n\n Total Pairs: ")
    # f.write(str(total_pairs))

    # f.write("\n Covered Pairs: ")
    # f.write(str(total_pairs - rem_pairs))

    # f.write("\n\n --------------> Total coverage with SA ")
    # f.write("{:.2f}".format(coverage))
    # f.write("% coverage <--------------\n\n")
    return data


def unique_pairs(values_list,pairs_in_while, pairs):
    
    uniq_p = 0
    temp_pairs = []
    for comb in combinations(values_list, 2):
        temp_pairs.append(list(comb))
    
    for i in range(len(temp_pairs)):
        if (not temp_pairs[i] in pairs_in_while) and temp_pairs[i] in pairs:
            uniq_p += 1
            pairs_in_while.append(temp_pairs[i])
        else:
            #print("this pair is repeated ",temp_pairs[i])
            pass

            
    return uniq_p,pairs_in_while
    
    
#### ----- New function written on 25th Oct '20. Use this function to remove unwanted directly from XLS file.
def remove_unwanted_values_from_map(pppp):
    #print(">>>>> Remove unwanted pairs from MAP <<<<<<<\n")
    #print("Unwanted:  " + str(unwanted_pairs_list)+"\n")
    all_keys = list(dictionary_of_parameters.keys())
    #print("all_keys: " + str(all_keys)+"\n")

    #print(pppp)

    output_pairs = []
    #item_vs_unwanted_items_category = []

    #for unwanted_pair in unwanted_pairs_list:
        #unwanted_elements = unwanted_pair.split(',')
        # Remove space from 2nd key so that it will match the dictionary key.
        #if len(unwanted_elements) > 1:
            #for k in all_keys:
                #unwanted_elements[0] = unwanted_elements[0].replace(k, '')

            # Remove 1st space occurance
            #unwanted_elements[0] = unwanted_elements[0].replace(' ', '', 1)
            #unwanted_elements[1] = unwanted_elements[1].replace(' ', '', 1)
            # here we are sure that there are 2 elements in this list
            #item_vs_unwanted_items_category.append(unwanted_elements)
            #for l in unwanted_elements:
            #    print("L>>> "+str(l))

    for pair in pppp:
        j = 0

        # Map numbers to readable strings to help them remove from the array
        for p in pair:
            #key = all_keys[j]
            #pair[j] = dictionary_of_parameters[key][p]
            pair[j] = all_map[(p-1)]
            j = j+1
        
        #for unwanted_elements in item_vs_unwanted_items_category:
            #value = unwanted_elements[0]
            #if value in (pr.upper() for pr in pair):
                #remove_lst = dictionary_of_parameters[unwanted_elements[1]]
                #for item in remove_lst:
                    #if item in pair:
                        #for i in range (len(pair)):
                            #if pair[i]==item:
                                #pair[i]='NA'
        #print("Generated Pair After Removals: "+str(pair))
        output_pairs.append(pair)
    data = {
        "output_pair":output_pairs,
        "all_key":all_keys
    }
    #print_in_file(output_pairs)
    
    return data

def print_in_file(output_pairs):
    f = open("result.txt", "w")
    #f.write("[")
    counter = 0
    f.write("Sr. No.\t\t Test case\n")
    for pair in output_pairs:
        counter = counter + 1
        f.write(str(counter))
        f.write("\t\t\t ")
        f.write(str(pair))
        f.write("\n")

    f.write("\n\nTotal test cases generated by SA Algorithm that covers all the possible tests: ")
    f.write(str(counter))
    #f.write("]")

#runSA()
