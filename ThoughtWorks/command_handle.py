'''
Created on 2018.7.27

@author: yangji
'''
import re
from command_exception import *
import numpy as np
'''
        command_example='3 3
                         0,1 0,2;0,0 1,0;0,1 1,1;0,2 1,2;1,0 1,1;1,1 1,2;1,1 2,1;1,2 2,2;2,0 2,1'
        '''
Error_Type = {
                'INF': 'Invalid number format.',
                'NOR': 'Number out of range.',
                'ICF': 'Incorrect command format.',
                'MFE': 'Maze format error.'
                } 
def replace(berep_arr, rep_coorList, rep2):
    for l_, c_ in rep_coorList:
        berep_arr[l_, c_] = rep2
    return berep_arr
def iter_NumJudgeAnd2Int(e):
#     print(e)
    if isinstance(e, (list, tuple)):
        res = True
        for i, ee in enumerate(e):
            res_, NET, e_r = iter_NumJudgeAnd2Int(ee)
            if res_ == False:
                res = res_
                break
            e[i] = e_r
    else:
        try:
            ie = int(e)
            return True, None, ie
        except:
            return False, 'INF', None
    return res, NET, e
def invalidNum_checkoutAnd2Int(num_strList,command):
    '''[ [3, 3], [[(0,1),(0,2)],[(1,1),(0,2)]...] ]'''
    try:
        unusualChar_pattern = '[^\d+,，；; \t\r\f\\\\n]'
        x = '\\n' in command
        if not x:
            unusualChar_pattern = '[^\d+,，；; \s]'
        unusual_charList = re.findall(unusualChar_pattern, command)
        for i, l in enumerate(num_strList):
            correct_int, _, l = iter_NumJudgeAnd2Int(l)
            if not correct_int or unusual_charList != []:
                raise CommandError(Error_Type['INF'])
            num_strList[i] = l
        return True, num_strList
    except BaseException as e:
        raise_error(Error_Type['INF'])  
        return False, None 
def numOR_checkoutAnd2ArrList(num_intList):
    '''
        [ [3, 5], [[(0,1),(0,4)],[(1,1),(0,2)]] ]
    '''
    try:
        size = np.array(num_intList[0])
        l_index = size[0]
        c_index = size[1]
        coor = np.array(num_intList[1])
        l_oor = (coor[...,0] >= l_index).any()
        c_oor = (coor[...,1] >= c_index).any()
        size_ = [l_index * 2 + 1, c_index * 2 + 1]
        if l_oor or c_oor:
            raise CommandError(Error_Type['NOR'])
        return True,[size_,coor]
    except BaseException as e:
        raise_error(Error_Type['NOR'])
        return False, [None, None]
def strFormat_checkout(command_list):
    try:
        res = command_list
        line_num = len(res)
        maze_sizeStr = res[0]
        maze_size_pattern = '\d+'
        maze_size_listSize = len(re.findall(maze_size_pattern, maze_sizeStr))
#         print(line_num, maze_size_listSize)
        if line_num != 2 or maze_size_listSize != 2:
            raise CommandError(Error_Type['ICF'])
        return True
    except BaseException as e:
        raise_error(Error_Type['ICF']) 
        return False 
def numFormat_checkout(num_strList):
    try:
        for e in num_strList:
            num_ee = len(e)
            if num_ee != 2:
                raise CommandError(Error_Type['ICF'])
        return True
    except BaseException as e:
        raise_error(Error_Type['ICF'])
        return False
def connect_checkout(size, coor_list, num_intList):
    try:
        kernel = [[0, 1, 2],
                  [1, 1, 1],
                  [0, 1, 0]]
        l, c = size
        l_step = (l-3) // 2 + 1
        c_step = (c-3)// 2 + 1
        block0 = np.zeros((l, c))
        block = replace(block0, coor_list, 1)
        coor_cpList = num_intList[1]
        for c1, c2 in coor_cpList:
            c1 = np.array(c1)
            c2 = np.array(c2)
            minus = np.absolute(c1 - c2)
            minus_sum = np.sum(minus)
            if minus_sum > 1:
                raise CommandError(Error_Type['MFE'])
        for l_ in range(l_step):
            for c_ in range(c_step):
                b = block[2*l_:2*l_+3,2*c_:2*c_+3]
                res = np.sum(b * kernel)
                if res < 2:
                    raise CommandError(Error_Type['MFE'])
        return True
    except BaseException as e:
        raise_error(Error_Type['MFE'])
        return False
    
def command2list(command):
    x = '\\n' in command
    if x:
        command = re.sub(r'\\n', '\n', command)
    lines = re.split('\n', command)
    command_list = [l.strip() for l in lines]
    return command_list    

def commandList2numStrList(command_list):
    '''command_list format [l1_data, l2_data]    
        l1_data ['3 3'] 
        l2_data ["0,1 0,2;0,0 1,0;0,1 1,1;0,2 1,2;1,0 1,1;1,1 1,2;1,1 2,1;1,2 2,2;2,0 2,1"]
        output format {[3, 3], [[(0,1),(0,2)],[(1,1),(0,2)]...]}
    '''
    num_strList = []
    for i, l in enumerate(command_list):
        if i == 0:
            value = re.split(' ', l)
        else:
            each_connect = re.split('[;；]', l)              # ['0,1 1,1', '1,1 2,1']
            each_connect_coordinate = map(lambda connect: re.split('[ +\t+]', connect.strip()),
                                           each_connect)# [['0,1','1,1'], ['1,1','2,1']]         
            value = list(map(lambda coordinate_cp: list(map(lambda coor4one: re.split('[,，]', coor4one), 
                                                            coordinate_cp)), 
                            each_connect_coordinate))
        num_strList.append(value)    
    return num_strList
def  numIntList2coordinate(num_intList):
    coor = num_intList[1]
    coor_list = []
    for one_cp in coor:
        cp = np.array(one_cp)
        cp = cp * 2 + 1
        mid = np.mean(cp, 0).astype(np.int).reshape(1, 2)
        z= np.concatenate((cp, mid), axis = 0)
        z_l = list(z)
        for e in z_l:
            coor_list.append(e)
    return coor_list
def commandFormat_check(command):
    command_list = command2list(command)
    check_res = strFormat_checkout(command_list)
    if not check_res:
        return False, None, None
    num_strList = commandList2numStrList(command_list)
    unmF_check = numFormat_checkout(num_strList[1])
    if not unmF_check:
        return False, None, None
    check_res_, num_intList = invalidNum_checkoutAnd2Int(num_strList,command)
    if not check_res_:
        return False, None, None
    norCheck_res, [size,_] = numOR_checkoutAnd2ArrList(num_intList)
    if not norCheck_res:
        return False, None, None
    coor_list = numIntList2coordinate(num_intList)
    conn_check = connect_checkout(size, coor_list, num_intList)
    if not conn_check:
        return False, None, None
    return True, size, coor_list
if __name__ == "__main__":
    c = '''3 3 \n 0,1 0,2;0,0 1,0;0,1 1,1;0,2 1,2;1,0 1,1;1,1 1,2;1,1 2,1;1,2 2,2;2,0 2,1'''
    commandFormat_check(c)