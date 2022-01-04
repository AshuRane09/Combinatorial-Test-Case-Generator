import random
import math
import itertools
import time
from itertools import combinations
import sys
import pandas as pd
import json

# ----------------------------------------------------------------------------------------------------------

# Global variables
list_of_dimensions = []
# gBest = []
covered_pairs = []

num_rows = []
all_map = {}
dictionary_of_parameters = {}

unwanted_pairs_list = []
# ----------------------------------------------------------------------------------------------------------

class Particle:

    def __init__(self, num_dimensions, positions, particle_list):
        self.particle_values = particle_list
        self.particle_position = positions
        self.particle_velocity = []
        self.iter_pbest = []
        self.pbest = -1
        self.iter_gbest = []
        self.gbest = -1

        for i in range(0, num_dimensions):
            self.particle_velocity.append(random.uniform(-1, 1))

# Forming Pairs
def form_pairs(l, ele):
    pairs = []
    for i in l:
        pairs.append([ele, i])
    return pairs

# ----------------------------------------------------------------------------------------


# Generating all possible pairs
def generate_pairs(l):

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

        for j in range(i+1, len(l)):
            temp_list2 = temp_list2 + list_of_dimensions[j]

        for k in range(len(list_of_dimensions[i])):
            temp_list3 = []
            temp_list3 = temp_list3 + temp_list2
            all_pairs = all_pairs + \
                form_pairs(temp_list3, list_of_dimensions[i][k])

    return all_pairs

# ----------------------------------------------------------------------------------------------------------


# Generating random particles
def generate_random_particles(num_of_particles, size_of_each_dimension):

    particle_list = []
    tp = []

    for i in range(num_of_particles):
        tp1 = []
        temp_list = []
        for j in range(len(size_of_each_dimension)):
            temp_variable = random.randint(0, size_of_each_dimension[j]-1)
            temp_list.append(list_of_dimensions[j][temp_variable])
            tp1.append(temp_variable)
        particle_list.append(temp_list)
        tp.append(tp1)
#     print(tp)
    return particle_list, tp

# ----------------------------------------------------------------------------------------------------------


def assign_random_position(size_of_each_dimension):
    maxValue = max(size_of_each_dimension)
    intial_pos = []

    for i in range(len(size_of_each_dimension)):
        temp_variable = random.randint(0, maxValue-1)
        intial_pos.append(temp_variable)

# ------------------------------------------------------------------------------------------------------------


def runPSO(df):
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
                # input_file = pd.read_excel("myfile.xlsx")
                input_file=df
                #print('---- Input file: '+input_file)
                all_columns = []

                for i in input_file.columns:
                    #print('Columns::::' + i)
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
                            #row_zero = row_zero.upper()
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
                #print('Unwanted pairs List >>>>>>> ::'+str(unwanted_pairs_list))

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

                #print("Something....")
                #print(dictionary_of_parameters)

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

                #print("\n\n--------------------------")
                #print("All map " + str(all_map))
                #print("\n\n--------------------------")
                #print("test case "+str(num_rows))

                num_inputs = len(num_rows)
                
                #print('Num Rows: '+str(num_inputs))

                excel_flag = 0
            except Exception as err:
                print("\nError : File not in same directory or file name does not exist !!!]\n" + err)

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

        #print(size_of_each_dimension)
        no_of_particles = 300

    '''if flagg == 1:
        no_of_dimensions = 4
        size_of_each_dimension = [3, 3, 3, 3]
        no_of_particles = 5
    else:
        no_of_dimensions = int(input('Enter Number of Dimensions : '))
        size_of_each_dimension = [int(x) for x in input(
            'Enter Size of Each Dimension : ').split()]
        no_of_particles = int(input("Enter number of particles : "))'''


    no_of_iter = 500
    #int(input("Enter the number of iterations : "))

    pairs = generate_pairs(size_of_each_dimension)
    particle_list, particle_pos = generate_random_particles(
        no_of_particles, size_of_each_dimension)

    total_pairs = len(pairs)

    # particle_pos = [[0,0,0,0],[1,1,1,1],[2,2,2,2],[1,0,2,0],[2,1,1,0]]
    # particle_list = [[1,4,7,10],[2,5,8,11],[3,6,9,12],[2,4,9,10],[3,5,8,10]]

    #print("\nTotal pairs : {} \nPairs :- {}".format(len(pairs), pairs))
    #print("\nparticle list is -----> ", particle_list)

    # particle_object_list = []
    # for i in range(no_of_particles):
    #     particle_object_list.append(Particle(no_of_dimensions,particle_pos[i]))

    particle_object_list = []
    for i in range(no_of_particles):
        particle_object_list.append(
            Particle(no_of_dimensions, particle_pos[i], particle_list[i]))

    #print("Particle object list :- ", particle_object_list)

    #display(particle_object_list)

    # -------------------------------------------------------------------------------------------------------------------
    # driver code

    selected_pairs = []
    # no_of_iter = 5
    ic = 0
    accuracy = []
    while no_of_iter > 0 and len(pairs) > 0:
        #print("\n\n--------- Iteration no. {} ------------".format(ic+1))
        ic += 1
        no_of_iter = no_of_iter - 1

        pbest_in_iter = []

        pairs_in_while = []
        for i in range(no_of_particles):
           # print("\nparticles is : ", particle_object_list[i].particle_values)
            particle_object_list[i].pbest, pairs_in_while = unique_pairs(
                particle_object_list[i].particle_values, pairs_in_while, pairs)
            #print("It's pbest is :- ", particle_object_list[i].pbest)
            pbest_in_iter.append(particle_object_list[i].pbest)

    #     print("Unique pairs generated in this iteration :- ",pairs_in_while)

        iter_gbest = max(pbest_in_iter)
        #print("\n**********GBEST OF THIS ITERATION IS************", iter_gbest)

        flag = 0

        all_gbest_particles = []

        if iter_gbest != 0:
            for i in range(no_of_particles):
                if particle_object_list[i].pbest == iter_gbest:
                    #print("hey adding result")
                    temp2 = particle_object_list[i].particle_values.copy()
                    if temp2 not in selected_pairs:
                        all_gbest_particles.append(temp2)
                        #selected_pairs.append(temp2)
                        #print("selected pairs is now ",selected_pairs)
                        flag = 1
    #                     break

        if flag == 1:
            for k in all_gbest_particles:
                selected_pairs.append(k)
                #print("selected particles are now ", len(selected_pairs))
                for c in combinations(k, 2):
                    try:
                        #print("removing this item from pairs list :- ", list(c))
                        pairs.remove(list(c))
                    except:
                        #print("{} is not present in pairs (already removed in previous iterations)".format(
                            list(c)
            #print(len(selected_pairs))
        for i in range(no_of_particles):
            update_velocity(particle_object_list[i], iter_gbest, no_of_dimensions, size_of_each_dimension)

        #print("\nNow number of pairs left are ", len(pairs))
        #print("remaining pairs are :- ", len(pairs))
        for i in range(no_of_particles):
            update_position(particle_object_list[i], size_of_each_dimension, no_of_dimensions)

        for i in range(no_of_particles):
            update_values(particle_object_list[i], size_of_each_dimension, no_of_dimensions)
        acf = ((len(pairs)/(total_pairs)*100))
        accuracy.append(acf)
        #print("\n\Accuracy:", (len(pairs)/len(total_pairs)*100))
    # -----------------------------------------------------------------------------------------------------------------
    f = open("accuracy.txt", "w")
    final_accuracy = round(max(accuracy),2)
    f.write("Accuracy : ")
    f.write(str(final_accuracy))
    f.close()
    data = remove_unwanted_values_from_map(selected_pairs)
    return data

#def display(particle_object_list):
    #for i in range(len(particle_object_list)):
        #print("\n------ Particle {} initialization details ------".format(i+1))
        #print("particle position :- ",particle_object_list[i].particle_position)
        #print("particle values :- ", particle_object_list[i].particle_values)
        #print("particle velocity :- ",particle_object_list[i].particle_velocity)
        #print("particle iter_best :- ",particle_object_list[i].iter_pbest)
        #print("particle iter_gbest :- ",particle_object_list[i].iter_gbest)

def unique_pairs(values_list, pairs_in_while, pairs):

    temp_pbest = 0
    temp_pairs = []
    for comb in combinations(values_list, 2):
        temp_pairs.append(list(comb))

    for i in range(len(temp_pairs)):
        if (not temp_pairs[i] in pairs_in_while) and temp_pairs[i] in pairs:
            temp_pbest += 1
            pairs_in_while.append(temp_pairs[i])
        else:
            #print("this pair is repeated ", temp_pairs[i])
            pass

    return temp_pbest, pairs_in_while

# --------------------------------------------------------------------------------------------------------------


def update_velocity(particle_object, gbest, no_of_dimensions, size_of_each_dimension):
    w = 0.9
    c1 = 0.8
    c2 = 0.3

    pos = particle_object.particle_position
    #print("\n--Update velocity --\npositions are :- ", pos)
    vel_upd = []
    #print("previous velocities are ", particle_object.particle_velocity)
    for i in range(no_of_dimensions):
        r1 = random.random()
        r2 = random.random()

        vel_cog = c1 * r1 * (particle_object.pbest - pos[i])
        vel_soc = c2 * r2 * (gbest - pos[i])

        res = w * particle_object.particle_velocity[i] + vel_cog + vel_soc

        # res = math.tanh(res)            #to map between -1 and 1
        if res < (-1 * size_of_each_dimension[i]):
            res = float(-1 * size_of_each_dimension[i])
        elif res > size_of_each_dimension[i]:
            res = float(size_of_each_dimension[i])
        vel_upd.append(res)

    particle_object.particle_velocity = vel_upd
    #print("updated velocity are :- ", vel_upd)

# -----------------------------------------------------------------------------------------------------------------

def update_position(particle_object, size_of_each_dimension, no_of_dimensions):

    #print("\nprevios positions are :- ", particle_object.particle_position)
    for i in range(no_of_dimensions):
        res = particle_object.particle_position[i] + \
            particle_object.particle_velocity[i]
#         res = round(res)

        if res > size_of_each_dimension[i]-1:
            #             res = size_of_each_dimension[i]-1
            res = random.randint(0, size_of_each_dimension[i]-1)
        elif res < 0:
            #             res = 0
            res = random.randint(0, size_of_each_dimension[i]-1)
        else:
            res = round(res)

        particle_object.particle_position[i] = res

    #print("updated positions are :- ", particle_object.particle_position)


# --------------------------------------------------------------------------------------------------------------------

def update_values(particle_object, size_of_each_dimension, no_of_dimensions):

    #print("\nprevious particle values are :- ",particle_object.particle_values)
    for i in range(no_of_dimensions):
        if i == 0:
            particle_object.particle_values[i] = particle_object.particle_position[i] + 1
        else:
            s = sum(size_of_each_dimension[0:i]) + \
                particle_object.particle_position[i]
            particle_object.particle_values[i] = s + 1

    #print("updated particle values are :- ", particle_object.particle_values)


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
        #Remove space from 2nd key so that it will match the dictionary key.
        #if len(unwanted_elements) > 1:
            #for k in all_keys:
                #unwanted_elements[0] = unwanted_elements[0].replace(k, '')

            # Remove 1st space occurance
            #unwanted_elements[0] = unwanted_elements[0].replace(' ', '', 1)
            #unwanted_elements[1] = unwanted_elements[1].replace(' ', '', 1)
            # here we are sure that there are 2 elements in this list
            #item_vs_unwanted_items_category.append(unwanted_elements)
            #for l in unwanted_elements:
                #print("L>>> "+str(l))

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
        #print("Generated Test Cases After Removals: "+str(pair))
        output_pairs.append(pair)
        
    data = {
        "output_pair":output_pairs,
        "all_key":all_keys
    }
    # data = json.dumps(data)
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

    f.write("\n\nTotal test cases generated by PSO Algorithm that covers all the possible tests: ")
    f.write(str(counter))
    #f.write("]")
    f.close()

# runPSO()
