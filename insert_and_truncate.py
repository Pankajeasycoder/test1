import pandas as pd
import mysql.connector

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

    # Commit changes and close connections
    conn.commit()
    cursor.close()
    conn.close()

# Example usage
excel_file = r'C:\Users\iesl43\Documents\Downloads\newcsv.csv'
table_name = 'intrun'

truncate_and_insert_data(excel_file, table_name)
