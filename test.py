import mysql.connector
from mysql.connector import errorcode

# Obtain connection string information from the portal
cnx = mysql.connector.connect(user="garotosdeprograma", password="Faculdade@157", host="faculdade-mysql.mysql.database.azure.com", port=3306, database="{faculdade-mysql}", ssl_ca="DigiCertGlobalRootG2.crt.pem", ssl_disabled=False)

config = {
  'host':'<faculdade-mysql.mysql.database.azure.com>',
  'user':'<garotosdeprograma>',
  'password':'<Faculdade@157>',
  'database':'<faculdade-mysql>'
}

# Construct connection string

try:
   conn = mysql.connector.connect(**config)
   print("Connection established")
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with the user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
  cursor = conn.cursor()

# Drop previous table of same name if one exists
cursor.execute("DROP TABLE IF EXISTS inventory;")
print("Finished dropping table (if existed).")

# Create table
cursor.execute("CREATE TABLE inventory (id serial PRIMARY KEY, name VARCHAR(50), quantity INTEGER);")
print("Finished creating table.")

# Insert some data into table
cursor.execute("INSERT INTO inventory (name, quantity) VALUES (%s, %s);", ("banana", 150))
print("Inserted",cursor.rowcount,"row(s) of data.")
cursor.execute("INSERT INTO inventory (name, quantity) VALUES (%s, %s);", ("orange", 154))
print("Inserted",cursor.rowcount,"row(s) of data.")
cursor.execute("INSERT INTO inventory (name, quantity) VALUES (%s, %s);", ("apple", 100))
print("Inserted",cursor.rowcount,"row(s) of data.")

# Cleanup
conn.commit()
cursor.close()
conn.close()
print("Done.")