import os
import sys


def get_configs_path():
    ''' Gets the absolute path of the given file and return the full path'''
    '''__file__ is a pointer , it contains the path of the file being executed'''
    '''__file__ if printed from the interpreted , throws undefined error , should be executed from the file'''
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), '../configs/')

def get_libs_path():
     return os.path.dirname(os.path.abspath(__file__))

def get_scripts_path():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), '../scripts/')


  
conf_file = open(os.path.join(get_configs_path(),'test.json'))
