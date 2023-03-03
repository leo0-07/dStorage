#!/usr/bin/env python
from dStorage.core import dStorage

def main():
    App = dStorage([0, "", "", ""],["id", "name", "last_name"])
    App.setdb("test","my_table")
    print("Application ",App.database)
    print("Application ",App.table)
    App.cdBase()
    App.cad()
    
if __name__ == "__main__":
    main()
