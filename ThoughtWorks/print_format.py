'''
Created on 2018.7.28

@author: yangji
'''
import numpy as np
from command_handle import replace
    
def print_mazeText(print_mat):
    for l in print_mat:
        l_ = ''
        for e in l:
            l_ += e + '  '
        print(l_)
        
    