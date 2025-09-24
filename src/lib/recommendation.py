import pandas as pd  # Importing the pandas library for data manipulation
import json
import os
from .dictionary_req import dictionary_present, dictionary_present_validated
from .chat_manager import chat_completions
from lib.product_mapping import product_map_layer
import ast
def compare_product_user_req(response_dic):
    print('Compare Layer')
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    laptop_df = pd.read_csv(os.path.join(BASE_DIR, "../data/updated_laptop.csv"))

    # laptop_df = pd.read_csv('../data/updated_laptop.csv')
    print(f'Laptop Req:{laptop_df.shape}')
    user_requirements = response_dic

    # Extracting user requirements from the input string (assuming it's a dictionary)
    # Since the function parameter already seems to be a string, we'll use it directly instead of extracting from a dictionary

    # Extracting the budget value from user_requirements and converting it to an integer
    budget = parse_budget(user_requirements)
    # budget
    # # Creating a copy of the DataFrame and filtering laptops based on the budget
    filtered_laptops = laptop_df.copy()
    if filtered_laptops['Price'].dtype != 'int64':
        filtered_laptops['Price'] = filtered_laptops['Price'].str.replace(',', '').astype(int)
    filtered_laptops = filtered_laptops[filtered_laptops['Price'] <= budget].copy()
    # filtered_laptops
    # # # Mapping string values 'low', 'medium', 'high' to numerical scores 0, 1, 2
    mappings = {'low': 0, 'medium': 1, 'high': 2}

    # # # Creating a new column 'Score' in the filtered DataFrame and initializing it to 0
    filtered_laptops['Score'] = 0

    for index, row in filtered_laptops.iterrows():
        # 2. Safely convert the laptop_feature string to a dictionary
        #    This is the core fix. We avoid calling the LLM here.
        try:
            # Use ast.literal_eval for safe evaluation of the string to a dict
            laptop_values = ast.literal_eval(row['laptop_feature'])
        except (ValueError, SyntaxError):
            print(f"Error parsing laptop_feature for index {index}. Skipping.")
            continue

        score = 0
        # Comparing user requirements with laptop features and updating scores
        for key, user_value in user_requirements.items():
            if key == 'Budget':
                continue  # Skipping budget comparison

            laptop_value = laptop_values.get(key, None)

            laptop_mapping = mappings.get(laptop_value, -1)
            user_mapping = mappings.get(user_value, -1)

            if laptop_mapping >= user_mapping:
                score += 1  # Incrementing score if laptop value meets or exceeds user value

        filtered_laptops.loc[index, 'Score'] = score  # Updating the 'Score' column in the DataFrame

        # Sorting laptops by score in descending order and selecting the top 3 products
    top_laptops = filtered_laptops.drop('laptop_feature', axis=1)
    top_laptops = top_laptops.sort_values('Score', ascending=False).head(3)

    # Converting the top laptops DataFrame to JSON format
    top_product_json = top_laptops.to_json(orient='records')

    print(f'Top products: {top_product_json}')
    return top_product_json


def parse_budget(user_requirements):
    budget_str = user_requirements.get("Budget", "").replace(",", "").strip()

    if not budget_str:
        return 0

    first_token = budget_str.split()[0]

    try:
        print(f'First token: {first_token}')
        return int(float(first_token))  # handles "50000.75" too
    except ValueError:
        return 0