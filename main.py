from sys import argv
import token_class
import lexical_analyzer as la

# argv[0] is always main.py

# python internal functions
# open()
# https://docs.python.org/ko/3/library/functions.html?highlight=open#open
# 'r' open in read mode.
txt = open(argv[1], 'r')

# print(txt)
# prints the instance of text not the content.

# read()
# read file's contents line by line

code_line = txt.readlines()

# Define the symbol table.
symbolTable = {}

# Define count_IDENT, count_CONST, count_OP
count_IDENT = 0
count_CONST = 0
count_OP = 0

# Define result message.
message_OK = '<OK>'
message_ERROR = '<ERROR>'
message_WARNING = '<WARNING>'

for line in code_line:
    # split()
    # https://docs.python.org/3/library/stdtypes.html?highlight=rstrip#str.rstrip
    # return a list of words in the string, using sep as the delimeter string.

    # split line into tokens
    tokens = line.split()
    print(line, end='')
    
    # define each token types
    for token in tokens:
        print(la.lexical(token))

    print("=================================")




# Define lookup
def lookup(token):
    for key in symbolTable:
        if token == key:
            return token
    return token_class.UNKNOWN



