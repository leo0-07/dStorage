#!/usr/bin/env python
from dStorage.core import dStorage
import os
def main():
    App = dStorage([],[])
    dbpath = os.path.expanduser("~/Documentos")
    App.dpath=dbpath
    App.set_database("storm")
    App.table ="good"
    App.l_pdindex()
    App.loaddata(0)
    App.show()
    App.display()
    
    
if __name__ == "__main__":
    main()
