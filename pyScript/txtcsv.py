import pandas as pd
import re
import numpy as np


def conversion():
    f = open("result.txt", "r")
    lines = f.readlines()
    del lines[0]
    del lines[-9:-1]
    del lines[-1]

    df1 = pd.DataFrame(
        columns=['Test Case No', 'Gender', 'Passenger Type', 'Journey Class', 'Disabled Passenger', 'Patient',
                 'Awardees', 'Widow', 'Student', 'youth', 'Kisan', 'Artists and sportsmen', 'Medical Professionals',
                 'Other'])
    sr = []
    for x in lines:
        sr.append(x.split()[0])

    df1['Test Case No'] = sr
    mainlist = []
    for x in lines:
        y = re.findall(r"'(.*?)'", x, re.DOTALL)
        mainlist.append(y)

    gender = {}
    passenger_type = {}
    Journey_Class = {}
    Disabled_Passenger = {}
    Patient = {}
    Awardees = {}
    widow = {}
    student = {}
    youth = {}
    kisan = {}
    artists = {}
    medical = {}
    others = {}
    for alist, no in zip(mainlist, sr):
        for x in alist:
            if x in ["Male", "Female"]:
                gender[no] = x
            if x in ['Child', 'Adult', 'Senior Citizen']:
                passenger_type[no] = x
            if x in ['1A', '2A', '3A', 'CC', 'FS', 'SS', 'SL']:
                Journey_Class[no] = x
            if x in ['Handicapped', 'Mentally Retarded', 'Blind', 'Deaf Dumb']:
                Disabled_Passenger[no] = x
            if x in ['Cancer', 'heart', 'kidney', 'thalassemia', 'TB', 'AIDS', 'Haemophilia', 'Leprosy']:
                Patient[no] = x
            if x in ['President Medal', 'Indian Police', 'Shram', 'Teachers', 'Bravery']:
                Awardees[no] = x
            if x in ['General', 'SC', 'school rural', 'girls rural', 'exams', 'research', 'foreign', 'cadets']:
                student[no] = x
            if x in ['project', 'seva', 'interview NonGov', 'interview st', 'scouts']:
                youth[no] = x
            if x in ['agricultural', 'travel', 'training', 'conferences']:
                kisan[no] = x
            if x in ['performance', 'travel', 'state tour', 'nat tour', 'mounting', 'press']:
                artists[no] = x
            if x in ['Doctors', 'Nurses']:
                medical[no] = x
            if x in ['Delegates', 'sewa', 'Social Service', 'tours', 'Ambulance Brigade']:
                others[no] = x
            if x in ['war', 'IPKF', 'Parliamentary', 'Defence', 'Kargil']:
                widow[no] = x

    df1['Gender'] = df1['Test Case No'].map(gender)
    df1['Passenger Type'] = df1['Test Case No'].map(passenger_type)
    df1['youth'] = df1['Test Case No'].map(youth)
    df1['Journey Class'] = df1['Test Case No'].map(Journey_Class)
    df1['Disabled Passenger'] = df1['Test Case No'].map(Disabled_Passenger)
    df1['Patient'] = df1['Test Case No'].map(Patient)
    df1['Awardees'] = df1['Test Case No'].map(Awardees)
    df1['Widow'] = df1['Test Case No'].map(widow)
    df1['Student'] = df1['Test Case No'].map(student)
    df1['Kisan'] = df1['Test Case No'].map(kisan)
    df1['Artists and sportsmen'] = df1['Test Case No'].map(artists)
    df1['Medical Professionals'] = df1['Test Case No'].map(medical)
    df1['Other'] = df1['Test Case No'].map(others)

    df1.replace(np.nan, "NA", inplace=True)
    df1.set_index(["Test Case No"], inplace=True)
    df1.to_csv("result.csv")
