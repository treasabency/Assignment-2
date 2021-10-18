import csv
#Most likely will combine them all into one function so it's easier to write to file
#question 1
def round_age(f):
    with open("covidResult.csv", "w") as output:
        writer = csv.writer(output, delimiter = ",")
        with open(f) as covid_file:
            reader = csv.reader(covid_file)
            for num, row in enumerate(reader):
                if "-" in row[1]:
                    low_age, high_age = (row[1].strip()).split("-")
                    #print(low_age, "   ", high_age)
                    rounded_age = (int(low_age) + int(high_age))/2
                    #print("rounded age: ", round(rounded_age))
                    row[1] = round(rounded_age)
                writer.writerow(row)
                
                
                
#extra function
def print_all(f):
    with open(f) as covid_file:
        reader = csv.reader(covid_file)
        for num, row in enumerate(reader):
            print(num, row)
round_age("covidTrain.csv")
#print_all("covidTrain.csv")