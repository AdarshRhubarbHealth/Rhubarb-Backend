# import pandas as pd

# # Load the Excel data into a pandas DataFrame
# try:
#     data = pd.read_excel(r'C:\Users\KIIT\OneDrive - kiit.ac.in\Desktop\CodeBase\CodeBase\Rhubarb\Sample_data(1).xlsx')
# except FileNotFoundError:
#     print("Error: Excel file not found.")
#     exit()

# # Combine first name and last name to create a new column 'User Full Name'
# if 'First Name' in data.columns and 'Last Name' in data.columns:
#     data['User Full Name'] = data['First Name'] + ' ' + data['Last Name']
# else:
#     print("Error: 'First Name' or 'Last Name' column not found in the Excel file.")
#     exit()

# # Get user input
# user_full_name = input("Enter your full name: ")

# # Find the user's row in the DataFrame
# user_row = data[data['User Full Name'] == user_full_name]

# if not user_row.empty:
#     ingredient_list = input("Enter a list of ingredients (separated by commas): ").lower().split(',')

#     # Check if 'Inverted Sugar' is present in the user's row
#     if 'Inverted Sugar' in user_row.columns:
#         inverted_sugar_flag = user_row['Inverted Sugar'].values[0].upper() == 'Y'

#         # Check if 'inverted sugar' is present in the ingredient list
#         if inverted_sugar_flag and 'inverted sugar' in ingredient_list:
#             print("Red signal: Inverted sugar found in the list. It may be harmful for you to consume it.")
#         else:
#             print("Green signal: Inverted sugar not found in the list.")
#     else:
#         print("'Inverted Sugar' column not found in the Excel file.")
# else:
#     print("User not found in the database.")
import pandas as pd

# Load the Excel data into a pandas DataFrame
try:
    data = pd.read_excel(r'C:\Users\KIIT\OneDrive - kiit.ac.in\Desktop\CodeBase\CodeBase\Rhubarb\Sample_data(1).xlsx')
except FileNotFoundError:
    print("Error: Excel file not found.")
    exit()

# Combine first name and last name to create a new column 'User Full Name'
if 'First Name' in data.columns and 'Last Name' in data.columns:
    data['User Full Name'] = data['First Name'] + ' ' + data['Last Name']
else:
    print("Error: 'First Name' or 'Last Name' column not found in the Excel file.")
    exit()

# Get user input
user_full_name = input("Enter your full name: ")

# Find the user's row in the DataFrame
user_row = data[data['User Full Name'] == user_full_name]

if not user_row.empty:
    ingredient_list = [ingredient.strip().lower() for ingredient in input("Enter a list of ingredients (separated by commas): ").split(',')]

    # Check if any flagged ingredient is present
    if 'Inverted Sugar' in user_row.columns:
        inverted_sugar_flag = user_row['Inverted Sugar'].values[0].upper() == 'Y'
        if inverted_sugar_flag and 'inverted sugar' in ingredient_list:
            print("Red signal: Inverted sugar found in the list. It may be harmful for you to consume it.")
    if 'xanthan gum' in user_row.columns:
        xanthan_gum_flag = user_row['xanthan gum'].values[0].upper() == 'Y'
        if xanthan_gum_flag and 'xanthan gum' in ingredient_list:
            print("Red signal: Xanthan gum found in the list. It may be harmful for you to consume it.")
    if not (inverted_sugar_flag and 'inverted sugar' in ingredient_list) and not (xanthan_gum_flag and 'xanthan gum' in ingredient_list):
        print("Green signal: No flagged ingredients found in the list.")
else:
    print("User not found in the database.")