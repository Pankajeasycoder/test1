import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

# Define the path to the CSV file
csv_file_path = 'newcsv.csv'

# Read the CSV file into a DataFrame without specifying usecols
df = pd.read_csv(csv_file_path)

# Print the DataFrame to verify the data
print(df)

# URL encode the password
password = 'admin@1234'
password_encoded = quote_plus(password)

# Create a SQLAlchemy engine to connect to the MySQL database
engine = create_engine(f'mysql+pymysql://root:{password_encoded}@localhost/automaticdata')


# Read the CSV file directly into the SQL database
with engine.connect() as connection:
    # Define the table creation query
    create_query = f'''
        CREATE TABLE IF NOT EXISTS my_tab (
            {open(csv_file_path).readline().strip().replace(',', ' TEXT, ')} TEXT
        );
    '''
    
    # Execute the table creation query
    connection.execute(create_query)
    
    # Load data from the CSV file into the MySQL table
    load_query = f'''
        LOAD DATA LOCAL INFILE '{csv_file_path}'
        INTO TABLE my_tab
        FIELDS TERMINATED BY ','
        LINES TERMINATED BY '\n'
        IGNORE 1 LINES;
    '''
    
    # Execute the data loading query
    connection.execute(load_query)

# Close the database connection
engine.dispose()
