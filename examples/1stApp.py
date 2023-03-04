#!/usr/bin/env python
from dStorage.core import dStorage
import os
def main():
    dbpath = os.path.expanduser("~/Documentos")
    App = dStorage(["id", "name", "last_name"],[1, "gratitude", "gratidão"])
    App.dpath=dbpath
    App.set_database("storm")
    App.table ="good"
    App.cdBase()

    App.cad()
    
    
if __name__ == "__main__":
    main()
