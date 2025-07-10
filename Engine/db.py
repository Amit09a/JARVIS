import csv
import sqlite3 

conn = sqlite3.connect('jarvis.db')

cursor = conn.cursor()

#query = "CREATE TABLE IF NOT EXISTS sys_command" \
#"(id integer primary key," \
#" name VARCHAR(100)," \
#" path VARCHAR(1000))"

#cursor.execute(query)

# query = "INSERT INTO sys_command VALUES (null,'Clock app', '//System//Applications//Clock.app')"
# cursor.execute(query)
# conn.commit()


#query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100), url VARCHAR(1000))"
#cursor.execute(query)

# query = "INSERT INTO web_command VALUES (null,'youtube', 'https://www.youtube.com/')"
# cursor.execute(query)
# conn.commit()

#query = "INSERT INTO web_command VALUES (null,'github', 'https://github.com/')"
#cursor.execute(query)
#conn.commit()

# query = "INSERT INTO web_command VALUES (null,'spotify', 'https://open.spotify.com/')"
# cursor.execute(query)
# conn.commit()

#cursor.execute("DELETE FROM web_command WHERE id = ?", (5,))
#conn.commit()



# make sure the name of the entry has no space and should be in lower case


#### 1. Create contacts Table 


# Create a table with the desired columns
#cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (id integer primary key, name VARCHAR(200), mobile_no VARCHAR(255), email VARCHAR(255) NULL)''')

#desired_columns_indices = [0, 20]

# Read data from CSV and insert into SQLite table for the desired columns
# with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
#     csvreader = csv.reader(csvfile)
#     for row in csvreader:
#         selected_data = [row[i] for i in desired_columns_indices]
#         cursor.execute(''' INSERT INTO contacts (id, 'name', 'mobile_no') VALUES (null, ?, ?);''', tuple(selected_data))

# # Commit changes and close connection
# conn.commit()
# conn.close()

#query = 'Avika'
#query = query.strip().lower()

#cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
#results = cursor.fetchall()
#print(results[0][0])