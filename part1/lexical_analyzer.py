import token_class

def whatChar(token, index):
    # https://docs.python.org/3/library/re.html
    # python internal method isalpha(), isdigit
    # check whether the given character is LETTER or DIGIT
    if (str.isalpha(token[index])):
        return token_class.LETTER
    elif (str.isdigit(token[index])):
        return token_class.DIGIT
    else:
        return token_class.UNKNOWN

def isIdentifier(token, index):
    if index == 0:
        if (whatChar(token, index) == token_class.DIGIT):
            return False
        elif(whatChar(token, index) == token_class.LETTER):
            index = index + 1
            if index == len(token):
                return True
            else:
                return isIdentifier(token, index)

    elif (whatChar(token, index) == token_class.LETTER or whatChar(token, index) == token_class.DIGIT):
        index = index + 1
        if index == len(token):
            return True
        else:
            return isIdentifier(token, index)

def isConstInt(token, index):
    if (whatChar(token, index) == token_class.DIGIT):
        index = index + 1
        if index == len(token):
            return True
        else:
            return isConstInt(token, index)
    else:
        return False

                

def lexical(token):
    """
    analyze the code and finde lexeme of the code.
    save the token's type to next_token
    save the token's string to token_string

    Args:
        code(list): tokens of the given code
    
    Return:
        (int, string): token's type, token's string
    """
    next_token = 0
    token_string = ''

    # check if token conforms to token type
    if(token == ':='):
        next_token = token_class.OP_ASSIGN
        token_string = token
        return (next_token, token_string)

    elif(token == '+'):
        next_token = token_class.OP_ADD
        token_string = token
        return (next_token, token_string)

    elif(token == '*'):
        next_token = token_class.OP_MULT
        token_string = token
        return (next_token, token_string)

    elif(token == ';'):
        next_token = token_class.SEMICOLON
        token_string = token
        return (next_token, token_string)

    elif(token == '('):
        next_token = token_class.PAREN_LEFT
        token_string = token
        return (next_token, token_string)
    
    elif(token == ')'):
        next_token = token_class.PAREN_RIGHT
        token_string = token
        return (next_token, token_string)

    elif(token == ')'):
        next_token = token_class.PAREN_RIGHT
        token_string = token
        return (next_token, token_string)

    # check if token is IDENTIFIER
    elif(isIdentifier(token, 0)):
        next_token = token_class.IDENT
        token_string = token
        return (next_token, token_string)

    # check if token is CONST_INT
    elif(isConstInt(token, 0)):
        next_token = token_class.CONST_INT
        token_string = token
        return (next_token, token_string)

    else:
        next_token = token_class.UNKNOWN
        token_string = token
        return (next_token, token_string)

# print(lexical(':='))
# print(lexical('+'))
# print(lexical('operand1'))
# print(lexical('op:'))
# print(lexical('123'))
# print(lexical('a123'))
# print(lexical('123d'))