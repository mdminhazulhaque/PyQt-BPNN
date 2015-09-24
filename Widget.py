#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
from BPNN import BPNN

'''
---0---
|     |
1     2
|     |
---3---
|     |
4     5
|     |
---6---
'''

pat_train = [
    # 0  1  2  3  4  5  6
    [[1, 1, 1, 0, 1, 1, 1], [0, 0, 0, 0]], # 0
    [[0, 0, 1, 0, 0, 1, 0], [0, 0, 0, 1]], # 1
    [[1, 0, 1, 1, 1, 0, 1], [0, 0, 1, 0]], # 2
    [[1, 0, 1, 1, 0, 1, 1], [0, 0, 1, 1]], # 3
    [[0, 1, 1, 1, 0, 1, 0], [0, 1, 0, 0]], # 4
    [[1, 1, 0, 1, 0, 1, 1], [0, 1, 0, 1]], # 5
    [[1, 1, 0, 1, 1, 1, 1], [0, 1, 1, 0]], # 6
    [[1, 1, 1, 0, 0, 1, 0], [0, 1, 1, 1]], # 7
    [[1, 1, 1, 1, 1, 1, 1], [1, 0, 0, 0]], # 8
    [[1, 1, 1, 1, 0, 1, 1], [1, 0, 0, 1]], # 9
    ]

class Widget(QWidget):
    
    def __init__(self):
        
        print('Creating Neural Network...')
        self.bpnn = BPNN(7, 7, 4)
        print('Training patterns...')
        self.bpnn.train(pat_train, iterations=100000)
        print('Training complete!')
        
        super().__init__()
        uifile = os.path.join(os.path.dirname(__file__), 'Widget.ui')
        self.ui = loadUi(uifile, self)
        
        # list to store which bits are selected
        self.bits = [0] * 7
        
        # connect only bit buttons to toggle slot
        for elem in self.ui.children():
            name = elem.objectName()
            if name[:3] == 'bit':
                elem.clicked.connect(self.toggle)
        
        # connect check button to check slot
        self.ui.buttonCheck.clicked.connect(self.check)
        
    def toggle(self):
        sender = self.sender()
        
        # take last number ie 'bit3' to '3'
        btnID = int(sender.objectName()[-1:])
        
        # toggle and set color
        if self.bits[btnID] == 0:
            sender.setStyleSheet("background-color: red");
            self.bits[btnID] = 1
        else:
            sender.setStyleSheet("background-color: none");
            self.bits[btnID] = 0
            
    def check(self):
        
        # get bit pattern from ui drawing
        test_pat = self.bits
        
        # get predicted pattern
        pat_predicted = self.bpnn.test(test_pat)
        
        # match predicted pattern with output patterns
        for pat in pat_train:
            if pat[1] == pat_predicted:
                self.ui.result.setText("Possible number: <b>" + str(i) + "</b>")
                return
            
        self.ui.result.setText("Unknown pattern")
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Widget()
    w.show()
    sys.exit(app.exec_())
