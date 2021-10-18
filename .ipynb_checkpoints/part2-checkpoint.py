import csv
#Most likely will combine them all into one function so it's easier to write to file
#question 1
def round_age(f):
    with open("covidResult.csv", "w") as output:
        writer = csv.writer(output, delimiter = ",")
        with open(f) as covid_file:
            reader = csv.reader(covid_file)
            col_name = next(reader)
            writer.writerow(col_name)
            for num, row in enumerate(reader):
                #question 1
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
                #print("symptoms: ", symptom_day, " : ", symptom_month, " : ",symptom_year)
                #print("admission: ", admission_day, " : ", admission_month, " : ",admission_year)
                #print("confirmation: ", confirm_day, " : ", confirm_month, " : ",confirm_year)
                row[8] = ".".join((symptom_month, symptom_day, symptom_year))
                row[9] = ".".join((admission_month, admission_day, admission_year))
                row[10] = ".".join((confirm_month, confirm_day, confirm_year))
                
                writer.writerow(row)
                
                
                
#extra function
def print_all(f):
    with open(f) as covid_file:
        reader = csv.reader(covid_file)
        for num, row in enumerate(reader):
            print(num, row)
round_age("covidTrain.csv")
#print_all("covidTrain.csv")
