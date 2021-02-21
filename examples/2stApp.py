#!/usr/bin/env python
from dStorage.core import dStorage

def main():
    App = dStorage([],[])
    App.setdb("test","my_table")
    App.l_pdindex()
    App.litems()
    App.loaddata(0)
    App.display()

    
    
if __name__ == "__main__":
    main()
