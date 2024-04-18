import pandas as pd
import requests
import json
import os

from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

def read_arrests_records(filename):
    try:
        # Read the Excel file
        xls = pd.ExcelFile(filename)
        
        # Check if the sheet "Arrests(Booking) Records" exists
        if "Arrests(Booking) Records" in xls.sheet_names:
            # Read the specific sheet
            df = pd.read_excel(xls, sheet_name="Arrests(Booking) Records")
            
            # Select only the relevant columns
            relevant_columns = ["NCIC Offense Code", "Description of Crime", 
                                "NCIC Category", "Notes:", "CDC Category", 
                                "DoubleCheck Score", "Source"]
            df = df[relevant_columns]
            
            return df
        else:
            print("Sheet 'Arrests(Booking) Records' not found in the Excel file.")
            return None
    except Exception as e:
        print("An error occurred:", e)
        return None

# Example usage:
filename = "./data/example.xlsx"  # Replace with the path to your Excel file
arrests_data = read_arrests_records(filename)
if arrests_data is not None:
    print(arrests_data.head())  # Display the first few rows of the extracted data

# Upload to my API
url = os.getenv("API_URL")
headers = {"Content-Type": "application/json"}

for index, row in arrests_data.iterrows():
    data = json.dumps({
        "ncicOffenseCode": int(row["NCIC Offense Code"]),
        "description": row["Description of Crime"],
        "ncicCategory": row["NCIC Category"],
        "cdcCategory": row["CDC Category"],
        "doubleCheckScore": row["DoubleCheck Score"].lower(),
    })

    response = requests.post(url, data=data, headers=headers)
    if response.status_code == 200:
        print("Record uploaded successfully.")
    else:
        print("Failed to upload record. Status code:", response.status_code)
        print("Response message:", response.text)
