import sqlite3

class BaseManager:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.db = sqlite3.connect('db.sqlite3')
        self.cursor = self.db.cursor()

    def close(self):
        """ Close the database """

        self.db.commit()
        print("Close database.")
        self.db.close()

    def db_info(self):
        """List all the table in the database"""
        self.cursor.execute(
                "SELECT name from sqlite_master WHERE type='table'"
            )

        tables = self.cursor.fetchall()
        
        # Print out the informaion
        print("="*10, end=" ")
        print("Database", end=" ")
        print("="*10, end="\n\n")
        print("List tables:")
        for table in tables:
            print("\t{}".format(table))

        print("-"*10)
        print("Total tables: {}".format(len(tables)))
        return tables
         

    def table_info(self,table_name):
        """ Print out the state of a table """

        # Select total rows
        self.cursor.execute(
                'SELECT COUNT(*) FROM {tn};'.format(tn=table_name)
            )
        count = self.cursor.fetchall()
        
        # Get the table's column information
        # (id, name, type, notnull, default_value, primary_key)
        self.cursor.execute(
                'PRAGMA TABLE_INFO({})'.format(table_name)
            )
        cols_info = self.cursor.fetchall()
        
        # Print out the information
        print("="*10, end=" ")
        print(table_name, end=" ")
        print("="*10, end="\n\n")
        print("Column info:")
        for col in cols_info:
            print("\t{}".format(col))
        print("-"*10)
        print("Total rows: {}".format(count))
        return cols_info

class Manager(BaseManager):

    def __init__(self, username="sqlite", password="sqlite"):
        super().__init__(username, password)                 
    	# Check if the database is empty
	self.cursor.execute("SELECT name from sqlite_master WHERE type='table'")
	if len(self.cursor.fetchall()) == 0:
		
		# Create User table
		self.cursor.execute(
				"CREATE TABLE users (username TEXT PRIMARY KEY, password TEXT NOT NULL, email TEXT NOT NULL);"
			)
		
		# Create transaction table
		self.cursor.execute(
				"CREATE TABLE trans (tid INTEGER PRIMARY KEY AUTOINCREMENT, date DATE NOT NULL, money INTEGER NOT NULL, note TEXT);"
			)

		# Insert admin user into the user table
		self.cursor.execute(
				"INSERT INTO users (username, password, email) VALUES ('admin', 'admin', 'example@gmail.com');"
			)
		self.db.commit()

    def sql(self, cmd):
        """SQL command(cmd) to select the data from the table"""
        try:
            self.cursor.execute(cmd)
        except:
            print("Invalue SQL commnd...")
            return None
        
        rows = self.cursor.fetchall()
        return rows

if __name__ == "__main__":
    manager = Manager()
    
    manager.db_info()
    
    while True:
        opt = input("""What do you wanna do?\n'e' for exit\n'q' for query\n't' for table_info\n?> """)
        if opt == 'e':
            manager.db_info()
            break
        elif opt == 'q':
            cmd = input("> ")
            manager.sql(cmd)
        elif opt == 't':
            t = input("Which table? ")
            manager.table_info(t)
        else:
            print("Invalid option")


