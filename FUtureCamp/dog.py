'''
Created on 2018年7月27日

@author: yangji
'''
from functools import reduce
import math
def main(n):
    max_2steps = n // 2
    ways = 2
    if n == max_2steps:
        ways = 1
        if n == 0:
            ways = 0 
        return ways
    for i in range(0, max_2steps-1):
        two_times = max_2steps - i - 1
        one_times = n - two_times*2
        steps = two_times + one_times
        l_num = one_times
        if one_times > two_times:
            l_num = two_times
        u = int(reduce(lambda x,y:x*y,(u_ for u_ in range(steps, steps-l_num, -1))))
        l = int(reduce(lambda x,y:x*y,(l_ for l_ in range(l_num, 0, -1))))
        n_ = u // l
        ways += n_
    return ways

if __name__ == "__main__":
    for i in range(100):
        n = main(i)
        print(i, n)
#     main(10)