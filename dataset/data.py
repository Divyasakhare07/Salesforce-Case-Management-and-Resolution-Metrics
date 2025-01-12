import random
import csv
from faker import Faker

fake = Faker()

def generate_case_data(num_cases=100):
    case_data = []
    for _ in range(num_cases):
        case_data.append({
            'Case ID': fake.uuid4(),
            'Status': random.choice(['Open', 'Closed', 'Escalated']),
            'Case Origin': random.choice(['Phone', 'Email', 'Web']),
            'Priority': random.choice(['Low', 'Medium', 'High']),
            'Case Type': random.choice(['Technical', 'Billing', 'General']),
            'Opened Date': fake.date_this_year(),
            'Closed Date': fake.date_this_year() if random.choice([True, False]) else None,
            'Resolution Time': random.randint(1, 72),  # Hours
            'First Contact Resolution': random.choice([True, False]),
            'Escalation Flag': random.choice([True, False]),
            'Customer Satisfaction Score': random.randint(1, 10)
        })
    return case_data

# Generate 100 fake cases
fake_cases = generate_case_data(100)

# Define the path to save the CSV
csv_file_path = "c:/Salesforce Case Management/dataset/fake_case_data.csv"

# Define CSV fieldnames (column names)
fieldnames = ['Case ID', 'Status', 'Case Origin', 'Priority', 'Case Type', 'Opened Date', 'Closed Date',
              'Resolution Time', 'First Contact Resolution', 'Escalation Flag', 'Customer Satisfaction Score']

# Write data to CSV file
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()  # Write the header row
    writer.writerows(fake_cases)  # Write the case data

print(f"Data saved to {csv_file_path}")
