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
        self.pushButton_3.clicked.connect(self.coeff)
        self.elem1 = None
        self.elem2 = None


    def cclear(self):
        self.textBrowser.setText('')
        self.textBrowser_2.setText('')
        self.textBrowser_3.setText('')
        self.elem1, self.elem2 = None, None
        self.elements = None


    def coeff(self):
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        result = cur.execute(f"""
                        SELECT re1, re2, re3 FROM reactions
                        WHERE elems = ?
                        """, (self.elements,)).fetchall()
        self.textBrowser_2.setText(result[0])
        self.textBrowser.setText(result[2])
        self.textBrowser_3.setText(result[1])
        con.commit()
        con.close()


    def reaction(self):
        self.elements = self.elem1 + self.elem2
        con = sqlite3.connect('database.db')
        cur = con.cursor()
        result = cur.execute(f"""
                        SELECT product FROM reactions
                        WHERE elems = ?
                        """, (self.elements,)).fetchall()
        if not result:
            self.elements = self.elem2 + self.elem1
            result = cur.execute(f"""
                        SELECT product FROM reactions
                        WHERE elems = ?
                        """, (self.elements,)).fetchall()
        if not result:
            result = tuple('компоненты не реагируют')
        self.textBrowser.setText(result[0])

        con.commit()
        con.close()
        

    def run(self, button):
        if not self.elem1:
            self.elem1 = button.text()
            self.textBrowser_2.setText(button.text())
        else:
            self.elem2 = button.text()
            self.textBrowser_3.setText(button.text())
    
def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)
            
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
