import sys
import time

from termcolor import colored

def delete_last_lines(n):
    "Use this function to delete the last line in the STDOUT"

    for i in range(n):
    	#cursor up one line	
	    sys.stdout.write('\x1b[1A')

	    #delete last line
	    sys.stdout.write('\x1b[2K')
def check_input_string(lst):
	for i in lst:
		if not len(i)>0:
			return False
	return True