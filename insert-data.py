import pandas as pd
import mysql.connector

# Load Excel file into a DataFrame
# excel_file = r'C:\Users\iesl43\Documents\Downloads\On-time-delivery-data.csv'
# df = pd.read_csv(excel_file)

excel_file = r'C:\Users\iesl43\Documents\Downloads\newcsv.csv'
df = pd.read_csv(excel_file)
df["salary"] = df["salary"].astype(int)

df.to_csv("newcsv.csv", index=False)
# Connect to MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='admin@1234',
    # database='csvfiledata'
    database='newdata'
)
cursor = conn.cursor()

# Iterate over DataFrame and insert rows into MySQL table
for index, row in df.iterrows():
    # insert_query = """
    #     INSERT INTO weather_data 
    #     (zipcode, total_items, precipitation_rate, water_runoff, snow_depth, 
    #     temperature, temperature_at_1500m, min_temperature, max_temperature, 
    #     pressure, wind_gust_speed, total_cloud_cover, dev_point_temperature, 
    #     relative_humidity, wind_speed, classification_ontime)
    #     VALUES
    #     (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    # """
    insert_query = """
        INSERT INTO dbs 
        (sno, name, age, salary, contact)
        VALUES
        (%s, %s, %s, %s, %s)
    """
    data = tuple(row)
    cursor.execute(insert_query, data)

# Commit changes and close connections
conn.commit()
cursor.close()
conn.close()
