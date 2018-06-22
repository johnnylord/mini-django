# User manual (dbmanager)

## class dbmanager (API)
### property
* #### table_name : [] 
    * save all table names in here
* #### table_schemes : {}
    * save all table entry data form here   

### method
* #### 1. create_table(table_name, table_entry_form) 
    * create table with certain entry form 
* #### 2. insert_entry(table_name, table_entry)
    * insert data(entry) into the table you want
* #### 3. delete_entry(table_name, constraint)
    * delete data(entry) in certain constraint 
* #### 4. update_entry(table_name, new_value, constraint)
    * update data(entry)  with new value in certain constraint
* #### 5. list_data(table_name)
    * list data of specific table
* #### 6. list_table()
    * list all table in this database
* #### 7. list_table_scheme(table_name)
    * list scheme of specific table 

## Example
* connect to database and create table
``` python=
# connect to db if db not exist it will create new one
import collections 

tutorial = dbmanager('databasename')
# using OrderedDict to make you dictionary in order
table_entry_structure_ordered = collections.OrderedDict(
        [('age','TEXT'), ('name','REAL'), ('school','TEXT')]
)



tutorial.create_table('table_name',table_structure)
```

* insert entry(data) to table
``` python=
age = 18
name = "Tim"
school = "Ncku"

table_entry = [age, name, school]
tutorial.insert_entry('table_name', table_entry)
```
* update entry(data) to table
``` python=
# update entry age to 20 whose age = 18
tutorial.update_entry("test","age = 20","age <= 18")
```
* delete entry(data) to table
``` python=
# delete entry age whose age larger than 20 and less than 30
tutorial.delete_entry("test","age > 20 and age < 30")
```

* list data(data of specific table)
``` python=
tutorial.list_data("table_name","*") 
```
* list scheme (data form in certain table)

``` python= 
tutorial.list_table_scheme('table_name')
# output will look like
# test2(dates TEXT,unix REAL,keyword TEXT,value REAL)
```


### simple example
```python=
from dbmanager import dbmanager
import collections         
# create or connect to database Test
tutorial = dbmanager('Test')

# table entry structure
table_entry_structure_ordered = collections.OrderedDict(
        [('age','TEXT'), ('name','REAL'), ('school','TEXT')]
)

# create table
tutorial.create_table("test",table_entry_structure_ordered)
# inserted data
table_entry = [18, 'Tim', 'NCKU']
tutorial.insert_entry("test",table_entry)
table_entry = [25, 'David', 'NTU']
tutorial.insert_entry("test",table_entry)
# show all the data in test table
# * means every column, you can specify any column you want
tutorial.list_data("test", "*")
# list all table;s name in this database
tutorial.list_table()
# update entry age to 20 whose age = 18
tutorial.update_entry("test","age = 20","age <= 18")
# delete entry age whose age larger than 20 and less than 30
tutorial.delete_entry("test","age > 20 and age < 30") 
```