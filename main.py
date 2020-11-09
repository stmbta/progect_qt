import sys
import sqlite3

from PyQt5 import uic 
from PyQt5.QtSql import * 
from PyQt5.QtWidgets import QApplication, QMainWindow


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Main1.ui', self)  
        self.buttonGroup_1.buttonClicked.connect(self.run)
        self.buttonGroup_2.buttonClicked.connect(self.run)
        self.pushButton.clicked.connect(self.reaction)
        self.pushButton_2.clicked.connect(self.cclear)

    
    def cclear(self):
        global elem1, elem2, elements
        self.textbrowser.SetText('')
        self.textbrowser_2.SetText('')
        self.textbrowser_3.SetText('')
        elem1, elem2 = None, None
        elements = None


    def reaction(self):
        global elements, elem1, elem2 
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        cur.execute("""
                        SELECT * FROM table
                        WHERE elems = elements
                        """)
        result = cur.fetchall()
        if not result:
            elements = elem2 + elem1
            cur.execute("""
                        SELECT * FROM table
                        WHERE elems = elements)
                        """)
            result = cur.fetchall()
        if not result:
            result = 'компоненты не реагируют'
        self.texbrowser.SetText(result)

        con.commit()
        con.close()
        

    def run(self):
        global elem1, elem2, elements
        if not elem1:
            elem1 = self.sender().text()
            self.textbrowser_2.setText(self.sender().text())
        else:
            elem2 = self.sender().text()
            self.textbrowser_3.setText(self.sender().text())
            
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
