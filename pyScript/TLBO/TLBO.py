import random
import math
import itertools,time
from itertools import combinations
import sys
import pandas as pd

list_of_dimensions = []                                                                  
num_rows = []
all_map = {}
dictionary_of_parameters = {}

unwanted_pairs_list = []


def form_pairs(l,ele):                                                                      
    pairs = []
    for i in l:
        pairs.append([ele,i])
    return pairs

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
        
        for j in range(i+1,len(l)):
            temp_list2 = temp_list2 + list_of_dimensions[j]  
        
        for k in range(len(list_of_dimensions[i])):
            temp_list3 = []
            temp_list3 = temp_list3 + temp_list2
            all_pairs = all_pairs + form_pairs(temp_list3,list_of_dimensions[i][k])

    return all_pairs

def generate_random_particles(num_of_particles,size_of_each_dimension):       
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
    return particle_list,tp

def assign_random_position(size_of_each_dimension):
    
    maxValue = max(size_of_each_dimension)
    intial_pos = []
    
    for i in range(len(size_of_each_dimension)):
        temp_variable = random.randint(0,maxValue-1)
        intial_pos.append(temp_variable)

def unique_pairs(values_list):
    temp_pairs = []
    for comb in combinations(values_list, 2):
        temp_pairs.append(list(comb))
    return temp_pairs
        
def fitness_function(particle,max_fitness_value,output_particle_list,covered_pairs):
    pairs_generated_by_particle = unique_pairs(particle)
    count = 0
    for i in pairs_generated_by_particle:
        if i not in covered_pairs:
            count += 1
    #print("\n\n ----------> MAX FITNESS VALUE: "+ str(max_fitness_value))
    #print("\n\n ----------> MAX COUNT VALUE: "+ str(count))

    if count >= (max_fitness_value - 70) and count <= max_fitness_value:
        for i in range(len(pairs_generated_by_particle)):
            covered_pairs.append(pairs_generated_by_particle[i])
        output_particle_list.append(particle)
    fitness_value = count
    return fitness_value
        

def TLBO(particle_list,domains_for_each_dimension,no_of_iter,max_fitness_value):
    covered_pairs = []
    output_particle_list = []
    no_of_particles = len(particle_list)
    for p in range(no_of_iter):
        for j in range(no_of_particles):
            fitness_value_of_particles = []
            mean_particle = [0]*len(particle_list[0])
            
            for i in particle_list:
                fitness_value = fitness_function(i,max_fitness_value,output_particle_list,covered_pairs)
                fitness_value_of_particles.append(fitness_value)
                
            for i in range(len(particle_list[0])):
                sum1 = 0
                for k in range(len(particle_list)):
                    sum1 = sum1 + particle_list[k][i]
                mean_particle[i] = (sum1/len(particle_list))
                
            for i in range(len(mean_particle)):
                mean_particle[i] = round(mean_particle[i])

            teacher_particle_index = fitness_value_of_particles.index(max(fitness_value_of_particles))
            teacher_particle = particle_list[teacher_particle_index]
            
            # print("\nMean : ",mean_particle)
            # print("\nTeacher : ",teacher_particle)
            # print("\nFitness : ",fitness_value_of_particles)
                                    
            teaching_factor = random.randint(1,2)                    
            random_values = [0]*len(particle_list[0])
            for i in range(len(particle_list[0])):
                r = random.uniform(0,1)
                r = round(r,1)
                random_values[i] = r
                
            new_particle_teacher_phase = [0]*len(particle_list[0])
                
            for i in range(len(particle_list[0])):       #teacherPhase
                new_particle_teacher_phase[i] = particle_list[j][i] + random_values[i] * (teacher_particle[i] - teaching_factor * mean_particle[i])
                
            for i in range(len(particle_list[0])):
                new_particle_teacher_phase[i] = round(new_particle_teacher_phase[i])
                if new_particle_teacher_phase[i] < domains_for_each_dimension[i][0]:
                    new_particle_teacher_phase[i] = domains_for_each_dimension[i][0]
                elif new_particle_teacher_phase[i] > domains_for_each_dimension[i][1]:
                    new_particle_teacher_phase[i] = domains_for_each_dimension[i][1]
                
#             print('\nnew particle teacher phase: ',new_particle_teacher_phase)    
            
            #check here is new the best
            new_fitness_value = fitness_function(new_particle_teacher_phase,max_fitness_value,output_particle_list,covered_pairs)
            if new_fitness_value >= fitness_value_of_particles[j]:
                particle_list[j] = new_particle_teacher_phase
                fitness_value_of_particles[j] = new_fitness_value
            
            
            non_selected_indices = []
            for i in range(no_of_particles):
                if i != j:
                    non_selected_indices.append(i)
            partner_particle_index = random.choice(non_selected_indices)
            partner_particle = particle_list[partner_particle_index]
            
            random_values = [0]*len(particle_list[0])
            for i in range(len(particle_list[0])):
                r = random.uniform(0,1)
                r = round(r,1)
                random_values[i] = r
            
            new_particle_learner_phase = [0]*len(particle_list[0])
            
            if fitness_value_of_particles[j] < fitness_value_of_particles[partner_particle_index] :
                for i in range(len(particle_list[0])):
                    new_particle_learner_phase[i] = particle_list[j][i] + random_values[i]*(particle_list[j][i] - partner_particle[i])
            elif fitness_value_of_particles[j] >= fitness_value_of_particles[partner_particle_index] : 
                for i in range(len(particle_list[0])):
                    new_particle_learner_phase[i] = particle_list[j][i] - random_values[i]*(particle_list[j][i] - partner_particle[i])
                    
            for i in range(len(particle_list[0])):
                new_particle_learner_phase[i] = round(new_particle_learner_phase[i])
                if new_particle_learner_phase[i] < domains_for_each_dimension[i][0]:
                    new_particle_learner_phase[i] = domains_for_each_dimension[i][0]
                elif new_particle_learner_phase[i] > domains_for_each_dimension[i][1]:
                    new_particle_learner_phase[i] = domains_for_each_dimension[i][1]  
                    
            #check here is new the best
#             print('\nnew particle learner phase: ',new_particle_learner_phase)    
            new_fitness_value = fitness_function(new_particle_learner_phase,max_fitness_value,output_particle_list,covered_pairs)
            #print("\n --------------------> New Fitness: ", new_fitness_value)
            if new_fitness_value >= fitness_value_of_particles[j]:
                particle_list[j] = new_particle_learner_phase
                fitness_value_of_particles[j] = new_fitness_value
    return output_particle_list



def runTLBO():

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
                input_file = pd.read_excel("myfile.xlsx")
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
                            row_zero = row_zero.upper()
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

        if num_inputs==7:
            size_of_each_dimension = [num_rows[0], num_rows[1], num_rows[2], num_rows[3], num_rows[4], num_rows[5], num_rows[6]]
        elif num_inputs==11:
            size_of_each_dimension = [num_rows[0], num_rows[1], num_rows[2], num_rows[3], num_rows[4], num_rows[5], num_rows[6], num_rows[7], num_rows[8], num_rows[9], num_rows[10]]
        elif num_inputs==12:
            size_of_each_dimension = [num_rows[0], num_rows[1], num_rows[2], num_rows[3], num_rows[4], num_rows[5], num_rows[6], num_rows[7], num_rows[8], num_rows[9], num_rows[10], num_rows[11]]
        elif num_inputs==13:
            size_of_each_dimension = [num_rows[0], num_rows[1], num_rows[2], num_rows[3], num_rows[4], num_rows[5], num_rows[6], num_rows[7], num_rows[8], num_rows[9], num_rows[10], num_rows[11], num_rows[12]]
        elif num_inputs==14:
            size_of_each_dimension = [num_rows[0], num_rows[1], num_rows[2], num_rows[3], num_rows[4], num_rows[5], num_rows[6], num_rows[7], num_rows[8], num_rows[9], num_rows[10], num_rows[11], num_rows[12], num_rows[13]]

        print(size_of_each_dimension)
        no_of_particles = 150
    elif flagg == 1:
        no_of_dimensions = 4
        size_of_each_dimension = [3,3,3,3]
        no_of_particles = 18
    else:
        no_of_dimensions = int(input('Enter Number of Dimensions : '))
        size_of_each_dimension = [int(x) for x in input('Enter Size of Each Dimension : ').split()]
        no_of_particles = int(input("Enter number of particles : "))

    #print("Enter range of iteration : ", end=" ")
    #range_of_iter = [int(x) for x in input().split()] 

    range_of_iter = range(2)


    #break_loop = int(input("Enter no. to break loop for coverge:"))
    break_loop = 1

    domains_for_each_dimension = []
    intial_ub= 1
    for i in size_of_each_dimension:
        ub = intial_ub 
        lb = intial_ub + i - 1
        domains_for_each_dimension.append([ub,lb])
        intial_ub += i
        
    for i in range(len(domains_for_each_dimension)):
        print("\nDomain of dimension {} : {}".format(i+1,domains_for_each_dimension[i]))
    
        
    pairs = generate_pairs(size_of_each_dimension)
    print("\nTotal pairs : {} ".format(len(pairs)))

    total_pairs = len(pairs)


    output_particle_list = []
    max_output_particle_list_len = 0
    max_output_particle_list = []


    while break_loop != 0:
        
        no_of_iter = random.randint(range_of_iter[0],range_of_iter[1])
        particle_list,particle_pos = generate_random_particles(no_of_particles,size_of_each_dimension)
        
        max_fitness_value = len(unique_pairs(particle_list[0]))
        # print("\n--------------------> max fitness value: ", max_fitness_value)
        # print("\n--------------------> Pairs total: ", len(pairs))
        # print("\n--------------------> No of iter : ", no_of_iter)
        minimum_number_of_particles_required =  len(pairs)//max_fitness_value
        
        print("minimum number of particles required : ",minimum_number_of_particles_required)
        
        #print("\nparticle list is -----> ",particle_list)
        output_particle_list = TLBO(particle_list,domains_for_each_dimension,no_of_iter,max_fitness_value)
        print("\nOutput Particle List : ",output_particle_list)
        
        if max_output_particle_list_len <= len(output_particle_list):
            max_output_particle_list_len = len(output_particle_list)
            max_output_particle_list = output_particle_list
        
        if(len(output_particle_list)) == minimum_number_of_particles_required:
            print("\n\n------------Got Full Coverage------------\n")
            break
        break_loop = break_loop - 1
    print("\nLength of Max Output Particle List : ",len(max_output_particle_list),"\n")
    print("\nMax Output Particle List : ",max_output_particle_list)

    remove_unwanted_values_from_map(max_output_particle_list)

    print("\n ----------------------------- END ------------------------------------- ")

    
    rem_pairs = len(output_particle_list)
    coverage = ((total_pairs - rem_pairs)/ total_pairs) * 100

    f = open("result.txt", "a")

    f.write("\n\n Total Pairs: ")
    f.write(str(total_pairs))

    f.write("\n Covered Pairs: ")
    f.write(str(total_pairs - rem_pairs))

    f.write("\n\n --------------> Total coverage with TLBO ")
    f.write("{:.2f}".format(coverage))
    f.write("% coverage <--------------\n\n")

    # -----------------------------------------------------------------------------------------------------------------

    #exit_value = int(input('\nPress any key to exit...'))
                    
#### ----- New function written on 25th Oct '20. Use this function to remove unwanted directly from XLS file.
def remove_unwanted_values_from_map(pppp):
    print(">>>>> Remove unwanted pairs from MAP <<<<<<<\n")
    print("Unwanted:  " + str(unwanted_pairs_list)+"\n")
    all_keys = list(dictionary_of_parameters.keys())
    print("all_keys: " + str(all_keys)+"\n")

    print(pppp)

    output_pairs = []
    item_vs_unwanted_items_category = []

    for unwanted_pair in unwanted_pairs_list:
        unwanted_elements = unwanted_pair.split(',')
        # Remove space from 2nd key so that it will match the dictionary key.
        if len(unwanted_elements) > 1:
            for k in all_keys:
                unwanted_elements[0] = unwanted_elements[0].replace(k, '')

            # Remove 1st space occurance
            unwanted_elements[0] = unwanted_elements[0].replace(' ', '', 1)
            unwanted_elements[1] = unwanted_elements[1].replace(' ', '', 1)
            # here we are sure that there are 2 elements in this list
            item_vs_unwanted_items_category.append(unwanted_elements)
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
        
        for unwanted_elements in item_vs_unwanted_items_category:
            value = unwanted_elements[0]
            if value in (pr.upper() for pr in pair):
                remove_lst = dictionary_of_parameters[unwanted_elements[1]]
                for item in remove_lst:
                    if item in pair:
                        pair.remove(item)
        print("Generated Pair After Removals: "+str(pair))
        output_pairs.append(pair)
    
    print_in_file(output_pairs)

    return output_pairs

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

    f.write("\n\nTotal test cases generated by TLBO Algorithm that covers all the possible tests: ")
    f.write(str(counter))
    #f.write("]")

#runTLBO()
