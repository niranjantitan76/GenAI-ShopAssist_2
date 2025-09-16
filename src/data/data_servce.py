# data/data_service.py

import pandas as pd
import numpy as np
from typing import List, Dict
import pandas as pd
from IPython.display import display, HTML,Markdown
# Set the display width to control the output width
pd.set_option('display.width', 100)
# Read the dataset and read the Laptop Dataset
df = pd.read_csv('laptop_data.csv')

# This service is responsible for all data-related operations.
# It reads from the CSV file and can handle data processing.

class DataService:
    def __init__(self, file_path='laptop_data.csv'):
        """Initializes the service by loading the data from a CSV file."""
        self.laptops_df = pd.read_csv(file_path)

    def get_all_laptops(self) -> List[Dict]:
        """Returns all laptops as a list of dictionaries."""
        return self.laptops_df.to_dict('records')

    def find_laptops_by_preference(self, user_prefs: Dict) -> List[Dict]:
        """
        Mocks finding laptops based on user preferences.
        In a real scenario, this would involve a complex query or a vector search.
        """
        df = self.laptops_df.copy()

        # Simple mock filtering based on user preferences
        if 'usage' in user_prefs:
            df = df[df['usage'].str.contains(user_prefs['usage'], case=False, na=False)]
        if 'budget' in user_prefs:
            df = df[df['budget'] == user_prefs['budget']]
        if 'ram' in user_prefs:
            df = df[df['ram'] == user_prefs['ram']]
        if 'processor' in user_prefs:
            df = df[df['processor'].str.contains(user_prefs['processor'], case=False, na=False)]

        # Return the top 3 matching laptops
        return df.to_dict('records')[:3]


# Instantiate the service to be used by other modules
data_service = DataService()
