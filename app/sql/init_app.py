from app.sql.sql_based_db import SQLBasedDB
from app.sql.example_table import ExampleTable

db = SQLBasedDB("test.db")

db.add_tables(ExampleTable)

obj1 = ExampleTable.new(some_int=0, text="")
