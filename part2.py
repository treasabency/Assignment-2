import csv
import re
#Most likely will combine them all into one function so it's easier to write to file
def round_age(f, lat_avg_dict, long_avg_dict, city_dict, symptom_dict):
    with open("covidResult.csv", "w") as output:
        writer = csv.writer(output, delimiter = ",")
        with open(f) as covid_file:
            reader = csv.reader(covid_file)
            col_name = next(reader)
            writer.writerow(col_name)
            for num, row in enumerate(reader):
                #question 1
                province = row[4]
                if "-" in row[1]:
                    low_age, high_age = (row[1].strip()).split("-")
                    #print(low_age, "   ", high_age)
                    rounded_age = (int(low_age) + int(high_age))/2
                    #print("rounded age: ", round(rounded_age))
                    row[1] = round(rounded_age)
                #question 2
                #8, 9, 10 index for dates
                symptom_day, symptom_month, symptom_year = row[8].split(".")
                admission_day, admission_month, admission_year = row[9].strip().split('.')
                confirm_day, confirm_month, confirm_year = row[10].strip().split('.')
                row[8] = ".".join((symptom_month, symptom_day, symptom_year))
                row[9] = ".".join((admission_month, admission_day, admission_year))
                row[10] = ".".join((confirm_month, confirm_day, confirm_year))
                #question 3, 4, 5
                #3: dictionaries of province:[list of latitude] and province:[list of longitude]
                    #if new provice, create new element in dict, else add to dict[province]
                    #if NaN, skip
                    #run until it writes everything currently to covidResult.csv
                    #then open covidResult.csv and check for NaN
                if row[6] == "NaN":
                    lat_avg = lat_avg_dict.get(province)
                    row[6] = lat_avg
                if row[7] == "NaN":
                    long_avg = long_avg_dict.get(province)
                    row[7] = long_avg
                #4: dictionary of province: [(city, count)]
                city_name = row[3]
                if city_name == "NaN":
                    row[3] = city_dict[province][1]
                #5: 
                if row[11] == "NaN":
                    row[11] = '; '.join(symptom_dict[province][1])
                writer.writerow(row)
    

#extra function
def print_all(f):
    with open(f) as covid_file:
        reader = csv.reader(covid_file)
        for num, row in enumerate(reader):
            print(num, row)
def get_lat_long(f):
    lat_dict = {}
    long_dict = {}
    with open(f) as file:
        reader = csv.reader(file)
        col_name = next(reader)
        for num, row in enumerate(reader):
            lat = row[6]
            long = row[7]
            province = row[4]
            if lat != "NaN":
                if province not in lat_dict:
                    lat_dict[province] = [lat]
                else:
                    lat_dict[province].append(lat)
            if long != "NaN":
                if province not in long_dict:
                    long_dict[province] = [long]
                else:
                    long_dict[province].append(long)
    return lat_dict, long_dict
def convert_to_average(l_dict):
    int_values = []
    for province, values in l_dict.items():
        for string in values:
            int_values.append(float(string))
        l_dict[province] = round(sum(int_values)/len(values), 2)
    return l_dict

def get_city_dict(f):
    city_prov_dict = {}
    with open(f) as file:
        reader = csv.reader(file)
        col_name = next(reader)
        for _, row in enumerate(reader):
            city = row[3]
            province = row[4]
            if city != "NaN":
                #kind of a bad way of doing it, but it works
                province_list = city_prov_dict.get(province)
                if province not in city_prov_dict:
                    city_prov_dict[province] = [[1, city]]
                else:
                    in_list = False
                    for i in range(0, len(province_list)):
                        if province_list[i][1] == city:
                            province_list[i][0] += 1
                            in_list = True
                    if not in_list:
                        city_prov_dict[province].append([1, city])
    for province, list_city in city_prov_dict.items():
        city_prov_dict[province] = sorted(list_city, key = lambda e: (-e[0], e[1]))
        city_prov_dict[province] = city_prov_dict[province][0]
    return city_prov_dict

def get_symptom_dict(f):
    symptom_dict = {}
    with open(f) as file:
        reader = csv.reader(file)
        col_name = next(reader)
        for _, row in enumerate(reader):
            symptoms_str = row[11].strip()
            province = row[4]
            symptoms_list = re.split('; |;', symptoms_str)
            symp_list_2 = symptom_dict.get(province)
            if symptoms_str != "NaN":
                if province not in symptom_dict:
                    symptom_dict[province] = [[1, symptoms_list]]
                else: 
                    in_list = False
                    for i in range(0, len(symp_list_2)):
                        if symp_list_2[i][1] == symptoms_list:
                            symp_list_2[i][0] += 1
                            in_list = True
                    if not in_list:
                        symptom_dict[province].append([1, symptoms_list])
    for province, symptoms in symptom_dict.items():
        symptom_dict[province] = sorted(symptoms, key = lambda e: (-e[0], e[1]))
        symptom_dict[province] = symptom_dict[province][0]
    return symptom_dict


lat_dict, long_dict = get_lat_long("covidTrain.csv")
lat_average_dict = convert_to_average(lat_dict)
long_average_dict = convert_to_average(long_dict)
city_dict = get_city_dict("covidTrain.csv")
symptom_dict = get_symptom_dict("covidTrain.csv")
round_age("covidTrain.csv", lat_average_dict, long_average_dict, city_dict, symptom_dict)

