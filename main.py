import sys
import sqlite3

from PyQt5 import uic 
from PyQt5.QtSql import * 
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Main1.ui', self)  
        self.buttonGroup_1.buttonClicked.connect(self.run)
        self.buttonGroup_2.buttonClicked.connect(self.run)
        self.pushButton.clicked.connect(self.reaction)
        self.pushButton_2.clicked.connect(self.cclear)
        self.pushButton_3.clicked.connect(self.coeff)
        self.pushButton_4.clicked.connect(self.second_form_open)
        self.elem1 = None
        self.elem2 = None

    
    def second_form_open(self):
        self.second_form = SecondForm(self, 'sjfj')
        self.second_form.show()


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
        self.textBrowser_2.setText(result[0][0])
        self.textBrowser.setText(result[0][2])
        self.textBrowser_3.setText(result[0][1])
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
            result = (("компоненты не реагируют"), ),
        self.textBrowser.setText(result[0][0])
        cur.execute("""
                        INSERT INTO histtable(elem1,elem2,product) VALUES(?, ?, ?)
                        """, (self.elem1, self.elem2, result[0][0]))

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


class SecondForm(QWidget):
        def __init__(self, *args):
            super().__init__()
            uic.loadUi('firstwindow.ui', self)
            con = sqlite3.connect('database.db')
            cur = con.cursor()
            result = cur.execute("""
                        SELECT elem1, elem2, product FROM histtable
                        WHERE product != 0
                        """).fetchall()
            con.commit()
            con.close()
            for x in range(len(result)):
                result[x] = f'{result[x][0]} + {result[x][1]} = {result[x][2]}'
            result = result[-1:-16:-1]
            self.textBrowser.setText('\n'.join(result))
            print(result)

        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
