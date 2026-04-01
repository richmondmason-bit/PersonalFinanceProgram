#Function to look through incomes to find specific dates or just print all.

#When checking for dates, it will first check the year, then the month, then the day as necessary. For example, 
# if its looking between 1/1/24 and 1/1/26, it will check a date that is 1/1/25, and just see the year puts it guranteed inbetween and print it

#Function that does the same thing for expenses.

#Function that allows all expenses of a specific catergory to be displayed, alongside total cost. Might also incorparate so it can pair with date check

#Allow them to search for all incomes and expenses between a certain time, and when found, 
# print them, their total value alone, and then the net, whether its positive or negative.

#All of these things needing to be displayed will be sent to the pygame terminal

#When given an income, save the amount, date, and source to the csv

#When given an expense, save the amount, date, and category to the csv

#If they choose to edit something, it will ask them either income or expenses, then if its income it will ask a time period, 
# and then display all incomes within that date, and let them choose

#if they choose expenses, it will instead ask for category first, and then time period. After a selection is made on which wants to be changed, 
# remove that value from the respective csv, by reading the file, and then writing, 
# but skipping over the selected point, and then have them input a new value, before appending that to the right csv.

#Find the percent of each expense category compared to the total, and then send it to the terminal so that the pie chart can be created