from app.sql.sql_based_db import SQLBasedDB
from app.sql.example_table import ExampleTable, OtherTable

db = SQLBasedDB("test.db")

db.add_tables(ExampleTable, OtherTable)

obj1 = ExampleTable.new(some_int=0, text="")

obj2 = OtherTable.new(some_int=0, text="", example_table_id=obj1.id)

_obj1 = obj2.example_table

print(_obj1.text)

