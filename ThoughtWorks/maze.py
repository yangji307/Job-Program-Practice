'''
Created on 2018.7.27

@author: yangji
'''
from command_handle import commandFormat_check, replace

class MazeFactory(object):
    @staticmethod
    def Create(command):
        '''
        command_example='3 3
                         0,1 0,2;0,0 1,0;0,1 1,1;0,2 1,2;1,0 1,1;1,1 1,2;1,1 2,1;1,2 2,2;2,0 2,1'
        '''
        command_correct, size, coor_list = commandFormat_check(command)
        if command_correct == True:
            maze = Maze(size, coor_list)
            return maze
        return None
class Maze(object):
    def __init__(self, size, coor_list):
        self.size = size
        self.coor_list = coor_list
    def Render(self):
        l = self.size[0]
        c = self.size[1]
        mazeText = [['[W]' for c_ in range(c)] for l_ in range(l)]
        for l_, c_ in self.coor_list:
            mazeText[l_][c_] = '[R]'
        return mazeText
        
if __name__ == "__main__":
    pass