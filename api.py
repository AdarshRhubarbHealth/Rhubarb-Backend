from flask import Flask, request, jsonify
import pandas as pd
from fuzzywuzzy import fuzz

# Initialize the Flask application
app = Flask(__name__)

# Load the data
file_path = r'Sample_data(1).xlsx'  # existing path of the database
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

# Function to check allergies
def check_allergies(consumer_name, ingredients):
    consumer_name = consumer_name.strip().lower()
    info = consumer_info.get(consumer_name, {})
    allergies = info.get('allergies', [])
    preservatives = info.get('preservatives', [])
    gmo = info.get('gmo', [])
    inverted_sugar_flag = info.get('inverted_sugar', 'N')
    usda_organic_seal_flag = info.get('usda_organic_seal', 'N')
    xanthan_gum_flag = info.get('xanthan_gum', 'N')

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
        return f"Red Signal: {'; '.join(red_alerts)}"
    return "Green Signal: You're Ready to consume this !!^_^!!"

# Define the API endpoint
@app.route('/check_allergies', methods=['POST'])
def api_check_allergies():
    # Parse the request JSON data
    data = request.get_json()
    consumer_name = data.get('consumer_name')
    ingredients = data.get('ingredients', [])

    if not consumer_name or not ingredients:
        return jsonify({"error": "Invalid input"}), 400

    # Perform the allergy check
    result = check_allergies(consumer_name, ingredients)

    # Return the result as a JSON response
    return jsonify({"result": result})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
