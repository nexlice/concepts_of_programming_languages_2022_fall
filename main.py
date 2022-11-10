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

# split()
# https://docs.python.org/3/library/stdtypes.html?highlight=rstrip#str.rstrip
# return a list of words in the string, using sep as the delimeter string.
tokens = txt.read().split()

# define each token types
code_token = []

for token in tokens:
    code_token.append(la.lexical(token))

# append EOF
code_token.append((token_class.EOF, "EOF"))

# Define lookup
def lookup(token):
    for key in symbolTable:
        if token == key:
            return symbolTable[key]
    return token_class.UNKNOWN

# Define current location
cursor = 0
priorsemicolon = 0

# Define error message
errorMessage = ''

# Define LHS identifier
ident_LHS = ''

# Define RHS eval string
eval_RHS = ''
# all of the derivations uses cursor and code_token as global value.

def program():
    statements()

def statements():
    statement()
    statements_new()

def statements_new():
    global count_CONST, count_IDENT, count_OP, errorMessage, message_OK, message_ERROR, message_WARNING, cursor, code_token, ident_LHS, eval_RHS, symbolTable
    if semi_colon():

        # print the raw code.
        for i in range(cursor - 1):
            if i < priorsemicolon:
                continue
            print(code_token[i][1] + " ", end = '')
        print("")

        # print the results
        print(f'ID:{count_IDENT}; CONST:{count_CONST}; OP:{count_OP};')
        if errorMessage == '':
            print(message_OK)
        else:
            print(errorMessage)
        
        print("")
        print("===============================")
        print("")

        # when exiting the line, do the assignment operation to the symbol table.
        # if eval_RHS is Unknown, skip the evaluation of the string.
        if 'Unknown' in eval_RHS:
            symbolTable[ident_LHS] = 'Unknown'
        else:
            symbolTable[ident_LHS] = eval(eval_RHS)

        # new line starts.
        count_CONST = 0
        count_IDENT = 0
        count_OP = 0
        errorMessage = ''
        eval_RHS = ''
        ident_LHS = ''
        statements()
    else:
        # epsilon
        pass

def statement():
    global cursor
    global code_token
    global priorsemicolon
    global ident_LHS
    priorsemicolon = cursor
    if ident():
        # LHS 
        ident_LHS = code_token[cursor - 1][1]

        assignment_operator()
        expression()

def expression():
    term()
    term_tail()

def term_tail():
    global eval_RHS
    global errorMessage
    if add_operator():
        # concatenate the add operator to the eval string.
        if eval_RHS != 'Unknown':
            eval_RHS = eval_RHS + code_token[cursor - 1][1]

        # error handling
        # if + appears sequentially,
        # ignore the value and mover cursor.
        if add_operator():
            errorMessage = message_WARNING + f'\"중복 연산자({code_token[cursor - 1][1]}) 제거\"'
        term()
        term_tail()
    else:
        # epsilon
        pass

def term():
    factor()
    factor_tail()

def factor_tail():
    global eval_RHS
    if mult_operator():
        # concatenate the mult operator to the eval string.
        if eval_RHS != 'Unknown':
            eval_RHS = eval_RHS + code_token[cursor - 1][1]
        factor()
        factor_tail()
    else:
        # epsilon
        pass

def factor():
    global errorMessage
    global message_WARNING
    global eval_RHS
    global symbolTable
    if left_paren():
        expression()
        right_paren()

    elif ident():
        # RHS >> find the identifier.
        if code_token[cursor - 1][1] in symbolTable:
            # check if the identifier exists in the symbolTable.
            # lookup and find the value.
            # if the value is Unknown, change the eval string to Unknown.
            if lookup(code_token[cursor - 1][1]) == 'Unknown':
                eval_RHS = 'Unknown'

            # else append the value to the eval string.
            eval_RHS = eval_RHS + str(lookup(code_token[cursor - 1][1]))
        # if not, assert error message.
        else:
            # append the identifier to the symbol table with the value 'Unknown'
            symbolTable[code_token[cursor - 1][1]] = 'Unknown'
            # change the value into Unknown.
            eval_RHS = 'Unknown'
            # assert error message
            errorMessage = message_ERROR + f'\"정의되지 않은 변수({code_token[cursor - 1][1]})가 참조됨\"'
    elif const():
        # RHS
        # append the value to the eval string
        if eval_RHS != 'Unknown':
            eval_RHS = eval_RHS + code_token[cursor - 1][1]
        

def const():
    global code_token
    global cursor
    global count_CONST
    if code_token[cursor][0] == token_class.CONST_INT:
        # print("const" + str(cursor))
        cursor += 1
        count_CONST += 1
        return True
    else:
        return False

def ident():
    global code_token
    global cursor
    global count_IDENT
    if code_token[cursor][0] == token_class.IDENT:
        # print("ident" + str(cursor))
        cursor += 1
        count_IDENT += 1
        return True
    else:
        return False

def assignment_operator():
    global code_token
    global cursor
    if code_token[cursor][0] == token_class.OP_ASSIGN:
        # print("assignment" + str(cursor))
        cursor += 1
        return True
    else:
        return False

def semi_colon():
    global code_token
    global cursor
    if code_token[cursor][0] == token_class.SEMICOLON:
        # print("semi_colon" + str(cursor))
        cursor += 1
        return True
    else:
        return False

def add_operator():
    global code_token
    global cursor
    global count_OP
    if code_token[cursor][0] == token_class.OP_ADD:
        # print("add" + str(cursor))
        cursor += 1
        count_OP += 1
        return True
    else:
        return False

def mult_operator():
    global code_token
    global cursor
    global count_OP
    if code_token[cursor][0] == token_class.OP_MULT:
        # print("mult" + str(cursor))
        cursor += 1
        count_OP += 1
        return True
    else:
        return False

def left_paren():
    global code_token
    global cursor
    if code_token[cursor][0] == token_class.PAREN_LEFT:
        # print("left_paren" + str(cursor))
        cursor += 1
        return True
    else:
        return False

def right_paren():
    global code_token
    global cursor
    if code_token[cursor][0] == token_class.PAREN_RIGHT:
        # print("right_paren" + str(cursor))
        cursor += 1
        return True
    else:
        return False

def print_result():
    global symbolTable
    result_str = ''

    for key in symbolTable:
        tmp_str = key + ":" + str(symbolTable[key]) + "; "
        result_str = result_str + tmp_str

    print(f'Result ==> {result_str}')

# main program.
print("")
program()
print("")
print_result()