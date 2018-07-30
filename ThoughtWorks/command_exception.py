'''
Created on 2018.7.27

@author: yangji
'''

class CommandError(BaseException):
    def __init__(self, msg):
        self.msg = msg
       
def raise_error(error_type):
    try:
        raise CommandError(error_type)
    except CommandError as e:
        print(e)
        

if __name__ == "__main__":
    pass