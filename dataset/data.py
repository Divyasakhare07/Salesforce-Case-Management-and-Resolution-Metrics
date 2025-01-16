from faker import Faker
import random
import datetime
import csv

# Initialize Faker instance
fake = Faker()

# Function to generate random cases
def generate_cases(num_cases):
    cases = []

    # Calculate number of closed and open cases
    num_closed_cases = (num_cases * 3) // 4  # 3:1 ratio, closed cases
    num_open_cases = num_cases - num_closed_cases

    # Define the start and end date for the year 2024
    start_date = datetime.datetime(2024, 1, 1)
    end_date = datetime.datetime(2024, 12, 31)

    # Generate closed cases
    for _ in range(num_closed_cases):
        opened_date = fake.date_time_between(start_date=start_date, end_date=end_date)
        closed_date = opened_date + datetime.timedelta(days=random.randint(1, 15))

        # Determine priority with a 3:2 ratio for low vs. other priorities
        priority = random.choices(
            ["Low", "Medium", "High"], 
            weights=[3, 1, 1],  # Low has a higher weight
            k=1
        )[0]

        case = {
            "status": "Closed",  # Set status as "Closed" for closed cases
            "case_type": random.choices(["Billing", "General", "Technical"], weights=[5, 3, 3], k=1)[0],
            "priority": priority,
            "Opened_date": opened_date,
            "Closed_date": closed_date,
            "customer_satisfaction_score": random.randint(1, 10),  # Scores between 1 and 10
            "first_contact_resolution": random.choice([True, False]),
            "Customer Region": random.choices(["Midwest", "Northeast", "Southeast", "Southwest", "West"], weights=[10, 4, 6, 2, 1], k=1)[0],
            "case_origin": random.choices(["Email", "Phone", "Web"], weights=[2, 5, 1], k=1)[0]  # Weighted case origin
        }
        cases.append(case)

    # Generate open cases
    for _ in range(num_open_cases):
        opened_date = fake.date_time_between(start_date=start_date, end_date=end_date)

        # Determine priority with a 3:2 ratio for low vs. other priorities
        priority = random.choices(
            ["Low", "Medium", "High"], 
            weights=[3, 2.5, 1],  # Low has a higher weight 
            k=1
        )[0]

        case = {
            "status": random.choice(["New", "Working", "Waiting on customer", "Escalated"]),  # Valid statuses for open cases
            "case_type": random.choices(["Billing", "General", "Technical"], weights=[5, 3, 3], k=1)[0],
            "priority": priority,
            "Opened_date": opened_date,
            "Closed_date": None,  # Keep as None for open cases
            "customer_satisfaction_score": None,
            "first_contact_resolution": random.choice([True, False]),
            "Customer Region": random.choices(["Midwest", "Northeast", "Southeast", "Southwest", "West"], weights=[10, 4, 6, 2, 1], k=1)[0],
            "case_origin": random.choices(["Email", "Phone", "Web"], weights=[2, 5, 1], k=1)[0]  # Weighted case origin
        }
        cases.append(case)

    return cases

# Generate 1000 sample cases
num_cases = 10000
case_data = generate_cases(num_cases)

# Write to CSV file
output_file = "case_data.csv"
fieldnames = ["status", "case_type", "priority", "Opened_date", "Closed_date", "customer_satisfaction_score", "first_contact_resolution", "Customer Region", "case_origin"]

with open(output_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for case in case_data:
        # Format Opened_date in ISO 8601 format
        opened_date_str = case['Opened_date'].strftime('%Y-%m-%dT%H:%M:%S') + 'Z'
        case["Opened_date"] = opened_date_str.strip()  # Remove any extra spaces

        # Write Closed_date in ISO 8601 format or keep as empty string if None
        if case["Closed_date"] is not None:
            closed_date_str = case['Closed_date'].strftime('%Y-%m-%dT%H:%M:%S') + 'Z'
            case["Closed_date"] = closed_date_str.strip()  # Remove any extra spaces
        else:
            case["Closed_date"] = ""  # Keep it as empty for open cases

        writer.writerow(case)

print(f"Data written to {output_file}")
