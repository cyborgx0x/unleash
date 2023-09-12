import sqlite3
import pandas as pd
import numpy as np

# Connect to the database
conn = sqlite3.connect('sample.db')

# Create a table
conn.execute('''CREATE TABLE ratings
             (user_id INT, item_id INT, rating INT)''')

# Insert some sample data
data = [(1, 1, 5), (1, 2, 4), (1, 3, 3), (2, 1, 2), (2, 2, 3), (2, 3, 4)]
conn.executemany('INSERT INTO ratings VALUES (?, ?, ?)', data)

# Commit the changes
conn.commit()

# Query the data from the database
df = pd.read_sql_query("SELECT * from ratings", conn)

# Close the connection
conn.close()