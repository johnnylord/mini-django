import sqlite3
import re   

class dbmanager:

    def __init__(self, name):
        """
        It will connect to DB if not exist it will build one 
        Example : db = dbmanager(database_name)
        """
        # connect to "name.db" if not exist it will build automatically
        self.db_name = name
        self.connection = sqlite3.connect(name+'.db')
        self.cursor = self.connection.cursor()
        # a table list that save all entry form in table
        # initailize by _find_table_name
        self._table_names = []
        self._find_table_name()
        # a table dictionary that save all scheme in certain table
        self._table_schemes = {}
        self._find_scheme()

    
    def create_table(self, table_name, table_entrys):
        '''
        creat table using table name 
        if not exist create new one , if it exist will not let you create
        the sql table will follow the table entry form you define 
        the form of entry is like 
        entry = {
            'unix':'REAL',
            'dates':'TEXT',
            'keyword':'TEXT',
            'value':'REAL'
        }
        '''
        # update table infomation in attribute
        self._add_table_name(table_name)
        self.entry = table_entrys
        first_statement = 'CREATE TABLE IF NOT EXISTS '+table_name+'('
        for entry in table_entrys:
            first_statement = first_statement + entry + ' ' + table_entrys[entry] + ','
        # delete , which is in the end of first_statement
        first_statement = first_statement[:-1]
        first_statement = first_statement + ')'
        self.cursor.execute(first_statement) 
        self._save()
        # update table scheme infomation in attribute
        # scheme will tell you  the entry type in the table
        self._add_table_scheme(table_name)


    def insert_entry(self, table_name, table_entry):
        '''
        this will add new entry(data) in your table
        depends on table name(if not exist it will send error)
        table_entry should follow the scheme which is defined when creating table before
        '''
        statement = 'INSERT INTO ' + table_name + ' VALUES('
        for entry in table_entry:
            if type(entry) is str:
                appendstr = "'" + entry + "'"
            elif type(entry) is int:
                appendstr = str(entry)
            
            statement = statement + appendstr + ','
        # delete , in the end of the statement
        # add ) in the end of statement make it legal in SQL language
        statement = statement[:-1]
        statement = statement + ')'
        # if table or entry type conflict except will occur
        try:
            self.cursor.execute(statement)
        except sqlite3.OperationalError:
            print("Insert Entry Failed : Table Name " + table_name + " isn't found")

        self._save()

    def delete_entry(self, table_name, condition):
        '''
        delete specific entry from table
        depending on the name of table and constraints (like value < 5 and value > 3)
        '''
        statement = "DELETE FROM " + table_name + " WHERE " + condition
        try:
            self.cursor.execute(statement)
            self._save()
        except sqlite3.OperationalError:
            print("Delete Entry Failed : Table name " + table_name + " isn't found")


    def update_entry(self, table_name, update, condition):
        """
        update specific entry
        depending on the name of table and constraint , and update it to certain value 
        """
        statement = "UPDATE " + table_name + " SET " + update + " WHERE " + condition
        try:
            self.cursor.execute(statement)
            self._save()
        except sqlite3.OperationalError:
            print("Update Entry Failed : Table name " + table_name + " isn't found")
    
    def list_data(self, table_name, constraint):
        '''
        It will list all the data in specific table 
        and you can add constraints to find the infomation you want from table
        '''
        # if table name not found it will send except
        try:
            self.cursor.execute("SELECT " + constraint + " FROM " + table_name)
            table = self.cursor.fetchall()
            print(table) 
        except sqlite3.OperationalError:
            print("List Data Failed : Table name " + table_name + " isn't found")

    def list_table(self):
        '''
        List all table scheme in the database
        '''
        for table in self._table_names:
            print(table)

    def list_table_scheme(self, table_name):
        '''
        List certain table scheme in the database
        '''
        print(self._table_schemes[table_name])


    def _list_scheme(self,table_name):
        '''
        List scheme of specific table scheme used by list_table_scheme and list_table these two function
        '''
        self.cursor.execute("SELECT sql FROM sqlite_master WHERE TYPE = 'table' AND name = '" + table_name + "'")
        table_schemes = self.cursor.fetchall()
        # if table_name is not found except will occur because table_schemes will be null
        try:
            schemes = table_schemes[0][0][13:]
            print(schemes)
        except IndexError:
            print("List Scheme Failed : Table name " + table_name + " isn't found")

    # find all tables in certain database
    def _find_table_name(self):
        '''
        used to initialize table name (an attibute)
        '''
        self.cursor.execute("SELECT name FROM sqlite_master WHERE TYPE = 'table';")
        tables = self.cursor.fetchall()
        for table in tables:
            self._table_names.append(table[0])

    def _find_scheme(self):
        '''
        used to initialze table scheme (an attribute)
        '''
        for table_name in self._table_names:
            self.cursor.execute("SELECT sql FROM sqlite_master WHERE TYPE = 'table' AND name = '" + table_name + "'")
            table_schemes = self.cursor.fetchall()
            tab_scheme = table_schemes[0][0][13:]
            self._table_schemes[table_name] = tab_scheme

    def _add_table_name(self, table_name):
        '''
        every time call create_table will add table name in _table_names attibute
        '''
        if table_name not in self._table_names :
            self._table_names.append(table_name)

    def _add_table_scheme(self, table_name):
        '''
        every time call create_table will add table scheme in _table_schemes attribute
        '''
        self.cursor.execute("SELECT sql FROM sqlite_master WHERE TYPE = 'table' AND name = '" + table_name + "'")
        table_schemes = self.cursor.fetchall()
        # because table_schemes contains CREATE TABLE these invalid words we delete them
        tab_scheme = table_schemes[0][0][13:]
        self._table_schemes[table_name] = tab_scheme

 
    def _save(self):
        '''
        save the difference you change before
        '''
        self.connection.commit()

