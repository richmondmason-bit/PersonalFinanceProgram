#Function to look through incomes to find specific dates or just print all.
import csv
def search_income(sd,ed,extra):
    try:
        with open('docs\income.csv', 'r') as csv_file:
            content = csv.reader(csv_file)
            headers = next(content)
            incomes = []
            for line in content:
                incomes.append({headers[0]: line[0], headers[1]: line[1], headers[2]: line[2]})
            passed = []
    except:
        print("File not found")
    else:
        if extra != None:
            for line in extra:
                passed.append(line)
        for line in incomes:
            if int(sd[0,1,2,3]) < int(line[0][0,1,2,3]) and int(ed[0,1,2,3]) > int(line[0][0,1,2,3]):
                passed.append(line)
            elif int(sd[5,6]) < int(line[0][5,6]) and int(ed[5,6]) > int(line[0][5,6]) and int(sd[0,1,2,3]) == int(line[0][0,1,2,3]):
                passed.append(line)
            elif int(sd[5,6]) < int(line[0][5,6]) and int(ed[5,6]) > int(line[0][5,6]) and int(ed[0,1,2,3]) == int(line[0][0,1,2,3]):
                passed.append(line)
            elif int(sd[8,9]) <= int(line[0][8,9]) and int(ed[8,9]) >= int(line[0][8,9]) and int(sd[0,1,2,3]) == int(line[0][0,1,2,3]) and int(line[0][5,6]) == int(sd[5,6]):
                passed.append(line)
            elif int(sd[8,9]) <= int(line[0][8,9]) and int(ed[8,9]) >= int(line[0][8,9]) and int(ed[0,1,2,3]) == int(line[0][0,1,2,3]) and int(line[0][5,6]) == int(ed[5,6]):
                passed.append(line)
    return passed

def search_expenses_date(sd,ed):
    try:
        with open('docs\Expenses.csv', 'r') as csv_file:
            content = csv.reader(csv_file)
            headers = next(content)
            expenses = []
            for line in content:
                expenses.append({headers[0]: line[0], headers[1]: line[1], headers[2]: line[2]})
            passed = []
    except:
        print("File not found")
    else:
        for line in expenses:
            if int(sd[0,1,2,3]) < int(line[0][0,1,2,3]) and int(ed[0,1,2,3]) > int(line[0][0,1,2,3]):
                passed.append(line)
            elif int(sd[5,6]) < int(line[0][5,6]) and int(ed[5,6]) > int(line[0][5,6]) and int(sd[0,1,2,3]) == int(line[0][0,1,2,3]):
                passed.append(line)
            elif int(sd[5,6]) < int(line[0][5,6]) and int(ed[5,6]) > int(line[0][5,6]) and int(ed[0,1,2,3]) == int(line[0][0,1,2,3]):
                passed.append(line)
            elif int(sd[8,9]) <= int(line[0][8,9]) and int(ed[8,9]) >= int(line[0][8,9]) and int(sd[0,1,2,3]) == int(line[0][0,1,2,3]) and int(line[0][5,6]) == int(sd[5,6]):
                passed.append(line)
            elif int(sd[8,9]) <= int(line[0][8,9]) and int(ed[8,9]) >= int(line[0][8,9]) and int(ed[0,1,2,3]) == int(line[0][0,1,2,3]) and int(line[0][5,6]) == int(ed[5,6]):
                passed.append(line)
            else:
                print("Ran into error")
    return passed
#When checking for dates, it will first check the year, then the month, then the day as necessary. For example, 
# if its looking between 1/1/24 and 1/1/26, it will check a date that is 1/1/25, and just see the year puts it guranteed inbetween and print it

#Function that does the same thing for expenses.

#Function that allows all expenses of a specific catergory to be displayed, alongside total cost. Might also incorparate so it can pair with date check

def search_expenses_cat(cate):
    try:
        with open('docs\Expenses.csv', 'r') as csv_file:
            content = csv.reader(csv_file)
            headers = next(content)
            expenses = []
            for line in content:
                expenses.append({headers[0]: line[0], headers[1]: line[1], headers[2]: line[2]})
            passed = []
    except:
        print("File not found")
    else:
        for line in expenses:
            if line[2] == "items" and cate == '1':
                passed.append(line)
            elif line[2] == "bills" and cate == '2':
                passed.append(line)
            elif line[2] == "outing" and cate == '3':
                passed.append(line)
            elif line[2] == "miscellaneous" and cate == '4':
                passed.append(line)
            else:
                print("Ran into error")
    return passed
#Allow them to search for all incomes and expenses between a certain time, and when found, 
# print them, their total value alone, and then the net, whether its positive or negative.
def net_income_and_expenses(sd,ed):
    collective_in = search_income(sd,ed,None)
    collective_ex = search_expenses_date(sd,ed)
    for thing in collective_in:
        net_in += int(thing[2])
    for thing in collective_ex:
        net_ex += int(thing[2])
    net_tot = net_in - net_ex
    return net_in, net_ex, net_tot
#All of these things needing to be displayed will be sent to the pygame terminal