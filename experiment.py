# from constants import *
# print(SEPARATOR)
# print("hello:",end="")
# input()

import re
string = "Yo what the hell #bro_what hey #hello"
regex = '#\w+'
match = re.findall(regex,string)
print(match)