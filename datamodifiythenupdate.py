import pandas as pd
import mysql.connector

def check_data_modified(cursor, table_name, new_df):
    # Check if the table has any data
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    
    if count == 0:
        return False
    
    # Optionally, implement your logic to check if the data is modified.
    # For simplicity, let's assume we compare the number of rows in the table and the new DataFrame
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    existing_row_count = cursor.fetchone()[0]
    
    if existing_row_count != len(new_df):
        return True
    
    # You could add more sophisticated checks here if needed
    return False

def truncate_and_insert_data(excel_file, table_name):
    # Load Excel file into a DataFrame
    df = pd.read_csv(excel_file)

    # Connect to MySQL
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='admin@1234',
        database='newdata'
    )
    cursor = conn.cursor()

    # Check if data is available or modified
    if check_data_modified(cursor, table_name, df):
        # Truncate the table
        truncate_query = f"TRUNCATE TABLE {table_name}"
        cursor.execute(truncate_query)
        
        # Prepare the insert query
        insert_query = f"""
            INSERT INTO {table_name} 
            (sno, name, age, salary, contact)
            VALUES
            (%s, %s, %s, %s, %s)
        """

        # Iterate over DataFrame and insert rows into MySQL table
        for index, row in df.iterrows():
            data = tuple(row)
            cursor.execute(insert_query, data)

        # Commit changes
        conn.commit()
        print("Data truncated and new data inserted.")
    else:
        print("No data available or no modification detected. Truncate and insert skipped.")

    # Close connections
    cursor.close()
    conn.close()

# Example usage
excel_file = r'C:\Users\iesl43\Documents\Downloads\newcsv.csv'
table_name = 'dbs'

truncate_and_insert_data(excel_file, table_name)
