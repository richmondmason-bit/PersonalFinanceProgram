# SAVINGS GOAL TRACKER PSEUDOCODE
information =  "data.csv"
# when the program starts, load the savings file (goal amount and saved amount)
# if the file does not exist, then set goal = 0 and saved = 0

# function set_savings_goal()
def set_savings_goal():
# ask the user to enter a savings goal amount
    amount = input("Please enter a savings goal amount: ")
# convert the input to a float
    amount == float
# if the goal is greater than 0, then save it to the file
    if amount > 0 
# otherwise print an error message
# after saving, return to the main menu

# function add_savings()
def add_savings():
    pass
# load the current goal and saved amount
# ask the user how much money they want to add to savings
# convert the amount to a float
# add the amount to the saved total
# save the updated saved total back into the file
# print the new savings total

# function view_progress()
def view_progress():
    pass
# load the goal and saved amount
# if the goal is 0, print that no goal is set
# otherwise calculate progress percent = (saved / goal) * 100
# print the goal amount
# print the saved amount
# print the percent completed
# if saved >= goal, print that the goal has been reached

# function save_savings_data()
def save_savings_data():
    pass
# open the csv file in write mode
# write the goal and saved values into the file
# close the file

# function load_savings_data()
def load_savings():
    pass
# open the csv file in read mode
# read the goal and saved values
# return the goal and saved values

# BUDGETING SYSTEM PSEUDOCODE

# when the program starts, load the budget file
# the file should store category, budget limit, and amount spent

# function set_budget(category, limit)
def set_budget(category, limit):
# ask the user to enter a category name
    category = input("Please enter the name of the category you would like to start budgeting in: ")
# ask the user to enter a budget limit for that category
    limit = input(f"Please enter the budget limit you would like to save for {category}: ")
# if the category already exists, update the limit
    if category in category:
        print(f"{category} exists!")

# if the category does not exist, create a new category
    elif 

# save the updated budget data to the file


# function add_expense(category, amount)
def add_expense(category, amount):
    pass
# load the budget data
# ask the user for the category and expense amount
# if the category exists, add the expense amount to the spent total
# if the category does not exist, print an error message
# save the updated budget data

# function compare_budget()
def compare_budget():
    pass
# load the budget data
# for each category in the budget data
# get the budget limit and amount spent
# print the category name
# print the budget limit and amount spent
# if spent > limit, print over budget warning
# if spent == limit, print budget exactly used
# if spent < limit, print remaining budget amount

# function save_budget_data()
def dave_budget_data():
    pass
# open the csv file in write mode
# write each category, limit, and spent amount into the file
# close the file

# function load_budget_data()
def load_budget():
    pass
# open the csv file in read mode
# read each row and store in a dictionary or list
# return the budget data