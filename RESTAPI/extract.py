import psycopg2
import requests
import random

# PostgreSQL connection details
POSTGRESQL_DETAILS = {
    "host": "localhost",
    "database": "salesforce",
    "user": "***",
    "password": "***",
}

# Salesforce Authentication and API Details
SALESFORCE_TOKEN_URL = "***"
CLIENT_ID = "***"
CLIENT_SECRET = "***"
USERNAME = "***"
PASSWORD = "***"
SECURITY_TOKEN = "***"
FULL_PASSWORD = PASSWORD + SECURITY_TOKEN

# Step 1: Fetch data from Salesforce
def fetch_data_from_salesforce():
    # Authenticate with Salesforce
    auth_payload = {
        "grant_type": "password",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "username": USERNAME,
        "password": FULL_PASSWORD,
    }
    auth_response = requests.post(SALESFORCE_TOKEN_URL, data=auth_payload)
    auth_response.raise_for_status()
    auth_data = auth_response.json()
    
    access_token = auth_data["access_token"]
    instance_url = auth_data["instance_url"]

    # Fetch Salesforce data
    headers = {"Authorization": f"Bearer {access_token}"}
    query = "SELECT Id, Case_Type__c, Priority, Status, Opened_Date__c, Closed_Date__c, Customer_Region__c, Origin, Customer_Satisfaction_Score__c, First_Contact_Resolution__c FROM Case"
    url = f"{instance_url}/services/data/v57.0/query?q={query.replace(' ', '+')}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    return response.json()["records"]

# Step 2: Load raw data into PostgreSQL
def load_raw_data_to_postgresql(raw_data):
    try:
        conn = psycopg2.connect(**POSTGRESQL_DETAILS)
        cursor = conn.cursor()
        
        # Create raw data staging table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS case_raw (
            id VARCHAR PRIMARY KEY,
            case_type VARCHAR,
            priority VARCHAR,
            status VARCHAR,
            opened_date TIMESTAMP,
            closed_date TIMESTAMP,
            customer_satisfaction_score FLOAT,
            first_contact_resolution BOOLEAN,
            customer_region VARCHAR,
            case_origin VARCHAR
        );
        """)
        
        # Insert raw data into staging table
        insert_query = """
        INSERT INTO case_raw (
            id, case_type, priority, status, opened_date, closed_date, 
            customer_satisfaction_score, first_contact_resolution, customer_region, case_origin
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING;
        """
        transformed_data = [
            (
                record["Id"],
                record.get("Case_Type__c"),
                record.get("Priority"),
                record.get("Status"),
                record.get("Opened_Date__c"),
                record.get("Closed_Date__c"),
                record.get("Customer_Satisfaction_Score__c", 0),  # Default to 0
                record.get("First_Contact_Resolution__c", False),  # Default to False
                record.get("Customer_Region__c"),
                record.get("Origin", "Unknown"),  # Default to "Unknown"
            )
            for record in raw_data
        ]
        cursor.executemany(insert_query, transformed_data)
        conn.commit()
        
        print("Raw data successfully loaded into PostgreSQL staging table!")
    except Exception as e:
        print(f"Error while loading raw data: {e}")
    finally:
        cursor.close()
        conn.close()

# Step 3: Main ETL process
def main():
    print("Starting ETL process...")
    
    # Extract
    salesforce_data = fetch_data_from_salesforce()
    print(f"Extracted {len(salesforce_data)} records.")
    
    # Load raw data into PostgreSQL
    load_raw_data_to_postgresql(salesforce_data)
    
    print("ETL process completed!")

if __name__ == "__main__":
    main()
