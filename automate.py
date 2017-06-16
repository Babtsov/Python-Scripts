from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import subprocess
import os

DEVNULL = open(os.devnull, 'w')


def execute(command):
    output = subprocess.check_output(command, shell=True, stderr=DEVNULL)
    if output:
        return output.strip().split('\n')

"""
examples:

cmd_output_lines = execute("myCmd loco list")[2:] # execute a shell script and ignore the first two lines
for line in cmd_output_lines:
    arg1, arg2 = line.split()[0:2] # extract only the columns we want :)
    result = execute('otherCmd {}:{}'.format(arg1,arg2)) # execute some other command with these arguments
    for result_line in result:
        print(result_line)
"""
