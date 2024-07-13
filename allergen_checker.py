import pandas as pd
from fuzzywuzzy import fuzz

# Load the data
file_path = r'C:\Users\KIIT\OneDrive - kiit.ac.in\Desktop\CodeBase\CodeBase\Rhubarb\Sample_data(1).xlsx' #existing path of the database
df = pd.read_excel(file_path, sheet_name='Sheet1')

# Extract relevant columns using the exact column names
consumer_data = df[['First Name', 'Last Name', 'Allergies', 'Preservatives Flag ', 'xanthan gum', 'GMO', 'Inverted Sugar', 'USDA Organic Seal']]

# Create a dictionary to map consumers to their allergies, preservatives, GMO components, and flags
consumer_info = {}
for _, row in consumer_data.iterrows():
    full_name = f"{row['First Name']} {row['Last Name']}".strip().lower()
    allergies = [allergy.strip() for allergy in row['Allergies'].split(',')]
    preservatives = [preservative.strip() for preservative in row['Preservatives Flag '].split(',')]
    gmo = [g.strip() for g in row['GMO'].split(',')] if pd.notna(row['GMO']) else []
    consumer_info[full_name] = {
        'allergies': allergies,
        'preservatives': preservatives,
        'gmo': gmo,
        'inverted_sugar': row['Inverted Sugar'].strip() if pd.notna(row['Inverted Sugar']) else 'N',
        'usda_organic_seal': row['USDA Organic Seal'].strip() if pd.notna(row['USDA Organic Seal']) else 'N',
        'xanthan_gum': row['xanthan gum'].strip() if pd.notna(row['xanthan gum']) else 'N'
    }

def check_allergies(consumer_name, ingredients):
    # Normalize the input consumer name to lowercase
    consumer_name = consumer_name.strip().lower()

    # Get the list of allergies, preservatives, GMO components, and other flags for the consumer
    info = consumer_info.get(consumer_name, {})
    allergies = info.get('allergies', [])
    preservatives = info.get('preservatives', [])
    gmo = info.get('gmo', [])
    inverted_sugar_flag = info.get('inverted_sugar', 'N')
    usda_organic_seal_flag = info.get('usda_organic_seal', 'N')
    xanthan_gum_flag = info.get('xanthan_gum', 'N')
    
    # Print consumer info for debugging
    print(f"\n\nInfo for {consumer_name}: Allergies - {allergies}, Preservatives - {preservatives}, GMO - {gmo}, Inverted Sugar - {inverted_sugar_flag}, USDA Organic Seal - {usda_organic_seal_flag}, Xanthan Gum - {xanthan_gum_flag}")
    
    # Check if any of the ingredients match the allergies, preservatives, GMO components, and other flags using fuzzy matching
    triggering_ingredients = {
        'allergies': set(),
        'preservatives': set(),
        'gmo': set(),
        'inverted_sugar': set(),
        'usda_organic_seal': set(),
        'xanthan_gum': set()
    }
    for ingredient in ingredients:
        for allergy in allergies:
            if fuzz.token_set_ratio(ingredient, allergy) > 80:
                triggering_ingredients['allergies'].add(ingredient)
        for preservative in preservatives:
            if fuzz.token_set_ratio(ingredient, preservative) > 80:
                triggering_ingredients['preservatives'].add(ingredient)
        for g in gmo:
            if fuzz.token_set_ratio(ingredient, g) > 80:
                triggering_ingredients['gmo'].add(ingredient)
        if inverted_sugar_flag == 'Y' and fuzz.token_set_ratio(ingredient, 'Inverted Sugar') > 80:
            triggering_ingredients['inverted_sugar'].add(ingredient)
        if usda_organic_seal_flag == 'Y' and fuzz.token_set_ratio(ingredient, 'USDA Organic Seal') > 80:
            triggering_ingredients['usda_organic_seal'].add(ingredient)
        if xanthan_gum_flag == 'Y' and fuzz.token_set_ratio(ingredient, 'xanthan gum') > 80:
            triggering_ingredients['xanthan_gum'].add(ingredient)
    
    red_alerts = []
    if triggering_ingredients['allergies']:
        red_alerts.append(f"Allergens found - {', '.join(triggering_ingredients['allergies'])}")
    if triggering_ingredients['preservatives']:
        red_alerts.append(f"Preservatives found - {', '.join(triggering_ingredients['preservatives'])}")
    if triggering_ingredients['gmo']:
        red_alerts.append(f"GMO components found - {', '.join(triggering_ingredients['gmo'])}")
    if triggering_ingredients['inverted_sugar']:
        red_alerts.append(f"Inverted Sugar found - {', '.join(triggering_ingredients['inverted_sugar'])}")
    if triggering_ingredients['usda_organic_seal']:
        red_alerts.append(f"USDA Organic Seal found - {', '.join(triggering_ingredients['usda_organic_seal'])}")
    if triggering_ingredients['xanthan_gum']:
        red_alerts.append(f"Xanthan Gum found - {', '.join(triggering_ingredients['xanthan_gum'])}")
    
    if red_alerts:
        return f"\n\nRed Signal: {'; '.join(red_alerts)}"
    return "\n\nGreen Signal"

# User input for consumer name and ingredients
consumer_name = input("Enter the consumer name: ").strip()
ingredients_input = input("Enter the list of ingredients separated by commas: ").strip()

# Convert the ingredients input string to a list
ingredients = [ingredient.strip() for ingredient in ingredients_input.split(',')]

# Check for allergies
signal = check_allergies(consumer_name, ingredients)
print(signal)  # Print the signal along with the specific allergens, preservatives, GMO components, inverted sugar, USDA organic seal, xanthan gum if any
print("\n")