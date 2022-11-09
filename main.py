from sys import argv

# python internal functions
# https://docs.python.org/ko/3/library/functions.html?highlight=open#open
isV = False
txt = open(argv[0], 'r')
code = txt.read().rstrip()  # this is code file
output = ""
print(code)
print("======================")