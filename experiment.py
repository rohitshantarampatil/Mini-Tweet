# from constants import *
# print(SEPARATOR)
# print("hello:",end="")
# input()

import re
string = "#testing testing #_testing"
regex = '#\w+'
match = re.findall(regex,string)
print(match)