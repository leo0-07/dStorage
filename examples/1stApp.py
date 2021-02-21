#!/usr/bin/env python
from dStorage.core import dStorage

def main():
    App = dStorage([0, "", "", ""],["id", "name", "last_name"])
    App.setdb("test","my_table")
    App.cdBase()
    App.cad()
    
if __name__ == "__main__":
    main()
