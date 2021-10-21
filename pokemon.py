import csv

# Question 1

def percentage_level():
    with open('pokemonTrain.csv') as infile: 
        reader = csv.DictReader(infile)
        level = []
        final = []
        for row in reader:
            level.append(row['level'])
        for i in range(0,len(level)):
            if float(level[i]) >= 40.0:
                final.append(float(level[i]))
    with open('pokemon1.txt', 'a') as output:
        output.write("Percentage of fire type Pokemons at or above level 40 = ")
        output.write(str(round(sum(final)/ len(final))))

# Question 2

def missingTypeFix():
    with open('pokemonTrain.csv') as infile: 
        reader = csv.DictReader(infile)
        final = {}
        for row in reader:
            if row['type'] != 'NaN':
                if row['type'] in final.keys():
                    final[row['type']].append(row['weakness'])
                else:
                    final[row['type']] = [row['weakness']]

        for key in final:
            value = final[key]
            final[key] = max(set(value), key = value.count)      

        result = {}
        for key in final:
            result[final[key]] = key

    with open('pokemonTrain.csv') as infile: 
        reader = csv.reader(infile)
    
        with open('pokemon2.csv','w',newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            
            for row in reader:
                if row[4] == 'NaN':
                    row[4] = result[row[5]]
                    writer.writerow(row)
                else:
                    writer.writerow(row)

# Question 3

def missingValFix():  
    aThreshAtk = []
    bThreshAtk = []
    aThreshDef = []
    bThreshDef = []
    aThreshHp = []
    bThreshHp = []
    threshold = 40
    with open('pokemonTrain.csv') as infile: 
        reader = csv.reader(infile)
        
        next(reader, None)
        
        for row in reader:
                if int(row[2]) > threshold:
                    if row[6] != 'NaN':
                        aThreshAtk.append(int(row[6]))
                    if row[7] != 'NaN':
                        aThreshDef.append(int(row[7]))
                    if row[8] != 'NaN':
                        aThreshHp.append(int(row[8]))
                else:
                    if row[6] != 'NaN':
                        bThreshAtk.append(int(row[6]))
                    if row[7] != 'NaN':
                        bThreshDef.append(int(row[7]))
                    if row[8] != 'NaN':
                        bThreshHp.append(int(row[8]))
        
        aAvgAtk = round(sum(aThreshAtk)/len(aThreshAtk), 1)
        aAvgDef = round(sum(aThreshDef)/len(aThreshDef), 1)
        aAvgHp = round(sum(aThreshHp)/len(aThreshHp), 1)
        bAvgAtk = round(sum(bThreshAtk)/len(bThreshAtk), 1)
        bAvgDef = round(sum(bThreshDef)/len(bThreshDef), 1)
        bAvgHp = round(sum(bThreshHp)/len(bThreshHp), 1)
        
        with open('pokemon2.csv') as infile: 
            reader = csv.DictReader(infile)
            with open('pokemonResult.csv','w',newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames = reader.fieldnames, delimiter = ',')

                writer.writeheader()
                for row in reader:
                    if int(row['level']) > threshold:
                        if row['atk'] == 'NaN':
                            row['atk'] = aAvgAtk
                        if row['def'] == 'NaN':
                            row['def'] = aAvgDef
                        if row['hp'] == 'NaN':
                            row['hp'] = aAvgHp
                        writer.writerow(row)
                    else:
                        if row['atk'] == 'NaN':
                            row['atk'] = bAvgAtk
                        if row['def'] == 'NaN':
                            row['def'] = bAvgDef
                        if row['hp'] == 'NaN':
                            row['hp'] = bAvgHp
                        writer.writerow(row)

# Question 4

def pokemonTypes():
    personalities = {}
    with open('pokemonResult.csv') as infile: 
        reader = csv.DictReader(infile)
        for row in reader:
            if row['type'] in personalities.keys():
                if row['personality'] not in personalities[row['type']]:
                    personalities[row['type']].append(row['personality'])
            else:
                personalities[row['type']] = [row['personality']]

    l = sorted(personalities.items())
    with open('pokemon4.txt', 'a') as output:
        output.write("Pokemon type to personality mapping:\n")
        output.write("\n")
        for i in range(0,len(l)):
            output.write(l[i][0])
            output.write(": ")
            val = sorted(l[i][1])
            for j in range(0, len(val)-1):
                output.write(val[j])
                output.write(", ")
            output.write(val[len(val)-1])
            output.write("\n")

# Question 5

def avgHP():
    hp = []
    with open('pokemonResult.csv') as infile: 
        reader = csv.DictReader(infile)
        for row in reader:
            if(row['stage'] == '3'):
                hp.append(float(row['hp']))
    avg = sum(hp)/ len(hp)
    with open('pokemon5.txt', 'a') as output:
        output.write("Average hit point for Pokemons of stage 3.0 = ")
        output.write(str(round(avg)))

percentage_level()
missingTypeFix()
missingValFix()
pokemonTypes()
avgHP()