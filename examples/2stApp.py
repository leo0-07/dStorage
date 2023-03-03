#!/usr/bin/env python
from dStorage.core import dStorage

def main():
    App = dStorage([],[])
    App.setdb("spell","list")
    App.l_pdindex()
    App.litems()
    App.display()

    
    
if __name__ == "__main__":
    main()
