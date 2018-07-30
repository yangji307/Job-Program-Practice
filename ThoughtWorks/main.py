'''
Created on 2018.7.29

@author: yangji
'''
import sys
from maze import *
from print_format import print_mazeText
def Main(*args):
    command = args[0]
    maze = MazeFactory.Create(command)
    if maze == None:
        return False
    mazeText = maze.Render()
    print_mazeText(mazeText)
if __name__ == "__main__":
    while_flag = True
    cmd_flag = False
    command_sys = sys.argv[1:]
    if command_sys != []:
        command = command_sys[0]
        cmd_flag = True
    while while_flag:
        if cmd_flag:
            while_flag = False
        else:
            command = input('input command: ')
            if command == 'q' or command == 'Q':
                break
        if Main(command) == False:
            continue
