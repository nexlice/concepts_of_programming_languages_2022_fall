import constant
import re
from sys import argv

isV = False
if argv[1] == '-v':
    isV = True
    txt = open(argv[2], 'r')
    code = txt.read().rstrip()   # this is code file
    print(code)
else:
    txt = open(argv[1], 'r')
    code = txt.read().rstrip()  # this is code file
    output = ""
    print(code)
    print("======================")

# lexical analyzer part
nextToken = 0
nextChar = ''
lexeme = ""
charClass = 0
index = -1  # 어디까지 읽었는지

sentence = ""
countId = 0
countConst = 0
countOp = 0
hasError = False
errorMsg = ""
symbolTable = {}
toCalc = ""

def is_integer(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()

def is_symbol(c):
    if c == '+' or c == '-' or c == '*' or c == '/' or c == '(' or c == ')':
        return True
    else:
        return False


# functions
def addChar():
    global nextToken, nextChar, lexeme, charClass, index, sentence, countId, countConst, countOp, hasError, errorMsg, symbolTable, toCalc
    lexeme += nextChar


def getChar():
    global nextToken, nextChar, lexeme, charClass, index, sentence, countId, countConst, countOp

    index += 1
    if len(code) <= index:
        charClass = constant.EOF

    else:
        nextChar = code[index]
        if nextChar.isalpha():
            charClass = constant.LETTER
        elif nextChar.isdigit():
            charClass = constant.DIGIT
        else:
            charClass = constant.UNKNOWN
        sentence += code[index]


def lookup():
    global nextToken, nextChar, lexeme, charClass, index, sentence
    if nextChar == '(':
        addChar()
        nextToken = constant.LEFT_PAREN
    elif nextChar == ')':
        addChar()
        nextToken = constant.RIGHT_PAREN
    elif nextChar == '+':
        addChar()
        nextToken = constant.ADD_OP
    elif nextChar == '-':
        addChar()
        nextToken = constant.SUB_OP
    elif nextChar == '*':
        addChar()
        nextToken = constant.MULT_OP
    elif nextChar == '/':
        addChar()
        nextToken = constant.DIV_OP
    elif nextChar == ':':
        addChar()
        nextToken = constant.ASSIGN_OP
        addChar()
        getChar()
        if nextChar == '=':
            addChar()
            nextToken = constant.ASSIGN_OP
    elif nextChar == '':
        addChar()
        nextToken = constant.EOF
    elif nextChar == ';':
        addChar()
        nextToken = constant.SEMICOLON


def getNoneBlank():
    global nextToken, nextChar, lexeme, charClass, index, sentence
    while nextChar.isspace():
        getChar()


def lex():
    global nextToken, nextChar, lexeme, charClass, index, sentence, countId, countConst, countOp, hasError, errorMsg, symbolTable, toCalc
    lexeme = ""
    getNoneBlank()
    if charClass == constant.LETTER:
        addChar()
        getChar()
        while charClass == constant.LETTER or charClass == constant.DIGIT:
            addChar()
            getChar()
        nextToken = constant.IDENT

    elif charClass == constant.DIGIT:
        addChar()
        getChar()
        while charClass == constant.DIGIT:
            addChar()
            getChar()
        nextToken = constant.INT_LIT
    elif charClass == constant.UNKNOWN:
        lookup()
        getChar()
    elif charClass == constant.EOF:
        nextToken = constant.EOF
        lexeme = "EOF"
    if isV:
        print(f"Next token is {nextToken}, Next lexeme is {lexeme}")
        #print(nextToken)
    return lexeme, nextToken


def program():
    #print("Enter <program>")
    statements()
    #print("Exit <program>")


def statements():
    # 각 문장!
    #print("Enter <statements>")
    statement()
    new()
    #print("Exit <statements>")


def statement():
    global nextToken, nextChar, lexeme, charClass, index, sentence, countId, countConst, countOp, hasError, errorMsg, symbolTable, toCalc
    #print("Enter <statement>")
    lex()  # ident():  any names conforming to C identifier rulesr
    countId += 1

    lex()  # assignment_op(): :=
    expression()
    if not isV:
        print(sentence, end='')

    a = sentence.split(":=").copy()
    m_key = a[0].strip()
    #print(m_key)
    r = [] + a
    #b = r[1].replace(';', ' ').split(" ")
    #b = re.split(r' |;]', r[1])

    b = re.split('([^a-zA-Z0-9])',r[1])

    while '' in b:
        b.remove('')
    while ' ' in b:
        b.remove(' ')
    while ';' in b:
        b.remove(';')
    while ';\n' in b:
        b.remove(';\n')
    while '\n' in b:
        b.remove('\n')

    t_idx = 0
    unknownIncluded = False
    while t_idx <= len(b) - 1:
        value = b[t_idx]

        # 키 값만 검사하기 위해서
        if not is_integer(value) and not is_symbol(value):
            # hashTable에서 찾기
            if value in symbolTable and symbolTable[value] != "Unknown":
                # print(f"Key exists! value is {symbolTable[value]}")
                b[t_idx] = symbolTable[value]
                # print(b)
            elif value in symbolTable and symbolTable[value] == "Unknown":
                symbolTable[m_key] = "Unknown"
                unknownIncluded = True
                break
            else:
                hasError = True
                errorMsg = f"정의되지 않은 변수({value})가 참조됨"

                # Unknown으로 추가해준다.
                symbolTable[value] = "Unknown"
                symbolTable[m_key] = "Unknown"
                break
        t_idx += 1

    #print(b)
    if not hasError and not unknownIncluded:
        if "Unknown" not in b:
            c = ''.join(str(e) for e in b)
            #print(eval(c))
            symbolTable[m_key] = eval(c)
    if not isV:
        print(f"ID: {countId}; CONST: {countConst}; OP: {countOp};")
    #print(symbolTable)
    if hasError:
        print(f"(ERROR): {errorMsg}")
    # elif hasWarning:
    #     print(f"(WARNING): {warningMsg}")
    else:
        if not isV:
            print("(OK)")
    sentence = ""
    countId = 0
    countConst = 0
    countOp = 0
    hasError = False
    errorMsg = ""
    #print("Exit <statement>")

def new():
    global nextToken, nextChar, lexeme, charClass, index, sentence, countId, countConst, countOp, hasError, errorMsg, symbolTable, toCalc
    #print("Enter <new>")
    if nextToken == constant.SEMICOLON:
        lex()
        statements()
    elif nextToken == constant.EOF:
        return
    #print("Exit <new>")


def expression():
    term()
    term_tail()


def term():
    factor()
    factor_tail()


def term_tail():
    global nextToken, nextChar, lexeme, charClass, index, sentence, countId, countConst, countOp, hasError, errorMsg, symbolTable, toCalc
    if nextToken == constant.ADD_OP:
        t_lexeme, t_token = lex()  # add_op
        toCalc += t_lexeme
        countOp += 1

        term()
        term_tail()
    # 없을 때 판단 모르겠음...


def factor():
    global nextToken, nextChar, lexeme, charClass, index, sentence, countId, countConst, countOp, hasError, errorMsg, symbolTable
    if nextToken == constant.LEFT_PAREN:
        lex()
        expression()
        if nextToken == constant.RIGHT_PAREN:
            lex()
        else:
            error()
    elif nextToken == constant.IDENT:
        lex()
        countId += 1
    elif nextToken == constant.INT_LIT:
        lex()
        countConst += 1
    else:
        error()


def factor_tail():
    global nextToken, nextChar, lexeme, charClass, index, sentence, countId, countConst, countOp
    if nextToken == constant.MULT_OP:
        lex()  # 곱셈
        countOp += 1
        factor()
        factor_tail()
    # elif nextToken == constant.EOF:
    # good?
    # else:
    # error()


def error():
    # parsing error happened
    return


# main
lex()
program()
if not isV:
    print(f"Result => {symbolTable}")