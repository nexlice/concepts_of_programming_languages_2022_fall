
from sys import argv
import token_class
import lexical_analyzer as la
import re

# argv[0] is always main.py

# python internal functions
# open()
# https://docs.python.org/ko/3/library/functions.html?highlight=open#open
# 'r' open in read mode.
txt = open(argv[1], 'r')

print(re.split(r'[\s]', txt.read()))