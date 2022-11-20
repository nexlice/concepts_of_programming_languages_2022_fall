from sys import argv
import token_class
import lexical_analyzer as la

# argv[0] is always main.py

# python internal functions
# open()
# https://docs.python.org/ko/3/library/functions.html?highlight=open#open
# 'r' open in read mode.

txt = ""
txt_tmp = ""

# print(txt)
# prints the instance of text not the content.

# read()
# read file's contents line by line

# Define the symbol table.
symbolTable = {}

# Define result message.
message_OK = '<OK>'
message_ERROR = '<ERROR>'
message_WARNING = '<WARNING>'

# define code_token
code_token = []

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
errList = []
errorMessage = ''

# Define LHS identifier
ident_LHS = ''

# Define RHS eval string
eval_RHS = ''
# all of the derivations uses cursor and code_token as global value.

def start():
    functions()

def functions():
    _function()
    functions_new()

def _function():
    identifier()
    left_paren()
    function_body()
    right_paren()

def functions_new():

    #check if the next token is identifier.
    if code_token[cursor][0] == token_class.IDENT:
       functions()
    else:
        # epsilon
        pass

def function_body():
    if var_definitions():
        statements()
    else:
        statements()

def var_definitions():
    var_definition()
    var_definitions_new()

def var_definitions_new():

    #check if the next token is variable.
    if code_token[cursor][0] == token_class.VARIABLE:
        var_definitions()
    else:
        #epsilon
        pass

def var_definition():
    variable()
    var_list()
    semi_colon()

def var_list():
    identifier()
    var_list_new()

def var_list_new():
    if comma():
        var_list()
    else:
        #epsilon
        pass

def statements():
    statement()
    statements_new()   

def statements_new():
    if semi_colon():
        statements()
    else:
        #epsilon
        pass

def statement():
    if call():
        identifier()
        semi_colon()
    elif print_ari():
        semi_colon()
    elif identifier():
        semi_colon
    else:
        #error
        pass

def semi_colon():
    global code_token
    global cursor
    if code_token[cursor][0] == token_class.SEMICOLON:
        # print("semi_colon" + str(cursor))
        cursor += 1
        return True
    else:
        return False

def identifier():
    global code_token
    global cursor
    if code_token[cursor][0] == token_class.IDENT:
        # print("ident" + str(cursor))
        cursor += 1
        return True
    else:
        return False

def print_ari():
    global code_token
    global cursor
    if code_token[cursor][0] == token_class.PRINT_ARI:
        # print("print_ari" + str(cursor))
        cursor += 1
        return True
    else:
        return False

def call():
    global code_token
    global cursor
    if code_token[cursor][0] == token_class.CALL:
        # print("call" + str(cursor))
        cursor += 1
        return True
    else:
        return False


def variable():
    global code_token
    global cursor
    if code_token[cursor][0] == token_class.VARIABLE:
        # print("variable" + str(cursor))
        cursor += 1
        return True
    else:
        return False

def comma():
    global code_token
    global cursor
    if code_token[cursor][0] == token_class.COMMA:
        # print("comma" + str(cursor))
        cursor += 1
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

def sa(arg_input):
    global txt
    global txt_tmp
    global code_token
    global cursor

    txt = open(arg_input, 'r')
    txt_tmp = open(arg_input, 'r')

    # split()
    # https://docs.python.org/3/library/stdtypes.html?highlight=rstrip#str.rstrip
    # return a list of words in the string, using sep as the delimeter string.
    tokens = txt.read().split()
    # adjust the error of the comma.
    for i in range(len(tokens)):
        if tokens[i][-1] == ',':
            if len(tokens[i]) == 1:
                continue
            to_insert = tokens[i]
            tokens.insert(i, to_insert[:-1])
            tokens.insert(i + 1, ',')
            tokens.remove(to_insert)

    # bug: len do not update > do it twice..
    # adjust the error of semi_colon.
    for i in range(len(tokens)):
        if tokens[i][-1] == ';':
            if len(tokens[i]) == 1:
                continue
            to_insert = tokens[i]
            tokens.insert(i, to_insert[:-1])
            tokens.insert(i + 1, ';')
            tokens.remove(to_insert)

    for i in range(len(tokens)):
        if tokens[i][-1] == ';':
            if len(tokens[i]) == 1:
                continue
            to_insert = tokens[i]
            tokens.insert(i, to_insert[:-1])
            tokens.insert(i + 1, ';')
            tokens.remove(to_insert)

    for token in tokens:
        code_token.append(la.lexical(token))

    # append EOF
    code_token.append((token_class.EOF, "EOF"))

    total_len = len(code_token)

    # do analyzing
    start()

    if total_len == cursor + 1:
        print("Syntax O.K.")
        print("")
    else:
        print("Syntax Error.")
        exit()

    return code_token
    