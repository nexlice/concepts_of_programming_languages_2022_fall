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

# define code_token
code_token = []

for line in code_line:
    # split()
    # https://docs.python.org/3/library/stdtypes.html?highlight=rstrip#str.rstrip
    # return a list of words in the string, using sep as the delimeter string.

    # split line into tokens
    tokens = line.split()
    print(line, end='')

    # define each token types
    for token in tokens:
        code_token.append(la.lexical(token))

#print(code_token)

# Define lookup
def lookup(token):
    for key in symbolTable:
        if token == key:
            return token
    return token_class.UNKNOWN



def program(code_token):
    statements(code_token)

def statements(code_token):
    statement(code_token)
    statements_new(code_token)

def statements_new(code_token):
    if code_token == None:
        return True

    for token in code_token:
        if semi_colon(token):
            if (code_token.index(token) == len(code_token) - 1):
                code_token_tmp = None
                break
            else:
                code_token_tmp = code_token[code_token.index(token) + 1 :]
                break
    statements(code_token_tmp)

def statement(code_token):
    if code_token == None:
        return True
    if ident(code_token[0][0]):
        if assignment_op(code_token[1][0]):
            symbolTable[code_token[0][1]] = expression(code_token[2:])
    else:
        return False

def expression(code_token):
    term(code_token)
    term_tail(code_token)

def term_tail(code_token):
    # epsilon
    if code_token == None:
        return True

    code_token_tmp = code_token

    for token in code_token:
        # (TODO) two adds?
        if add_operator(token):
            code_token_tmp = code_token[code_token.index(token) + 1 :]
            break
    term(code_token_tmp)
    term_tail(code_token_tmp)

def term(code_token):
    factor(code_token)
    factor_tail(code_token)

def factor_tail(code_token):
    # epsilon
    if code_token == None:
        return True

    code_token_tmp = code_token
    
    for token in code_token:
        # (TODO) two mults?
        if mult_operator(token):
            code_token_tmp = code_token[code_token.index(token) + 1 :]
            break
    factor(code_token_tmp)
    factor_tail(code_token_tmp)

def factor(code_token):
    if (ident(code_token[0])):
        ident(code_token[0])
    elif (const(code_token[0])):
        const(code_token[0])
    elif (left_paren(code_token[0])):
        expression(code_token[1:])
    #right_paren()

def const(token):
    if (token == token_class.CONST_INT):
        return True
    else:
        return False

def ident(token):
    if (token == token_class.IDENT):
        return True
    else:
        return False

def assignment_op(token):
    if (token == token_class.OP_ASSIGN):
        return True
    else:
        return False

def semi_colon(token):
    if (token == token_class.SEMICOLON):
        return True
    else:
        return False

def add_operator(token):
    if (token == token_class.OP_ADD):
        return True
    else:
        return False

def mult_operator(token):
    if (token == token_class.OP_MULT):
        return True
    else:
        return False

def left_paren(token):
    if (token == token_class.PAREN_LEFT):
        return True
    else:
        return False

def right_paren(token):
    if (token == token_class.PAREN_RIGHT):
        return True
    else:
        return False

program(code_token)