import os
import psycopg2

conn = psycopg2.connect(
        host= os.environ.get('RDS_HOSTNAME'),
        database= os.environ.get('RDS_DB_NAME'),
        user= os.environ['RDS_USERNAME'],
        password= os.environ['RDS_PASSWORD'])

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
cur.execute('DROP TABLE IF EXISTS users;')
cur.execute('CREATE TABLE users (id serial PRIMARY KEY,'
                                 'name varchar (150) NOT NULL,'
                                 'age varchar (50) NOT NULL,'
                                 'date_added date DEFAULT CURRENT_TIMESTAMP);'
                                 )

# Insert data into the table

cur.execute('INSERT INTO users (name, age)'
            'VALUES (%s, %s)',
            ('abdelali',
             '34',
            )
            )


cur.execute('INSERT INTO users (name, age)'
            'VALUES (%s, %s)',
            ('jadelmoula',
             '40'
            )
            )

conn.commit()

cur.close()
conn.close()
