# author: Le Anh Tai
# email: leanhtai01@gmail.com
# GitHub: https://github.com/leanhtai01
import re
import subprocess
from datetime import datetime


def backup(file_name):
    """backup a file use current datetime"""
    current_datetime = str(datetime.now()).replace(' ', '_')
    subprocess.run([
        'cp',
        file_name,
        file_name + '_' + current_datetime + '.bak'
    ])


def multiple_replace_in_line(file_name, pattern, replace_pairs):
    """perform multiple text replace in line"""
    with open(file_name) as reader:
        lines = reader.readlines()

    # find the line number contain pattern
    linum = None
    for i in range(len(lines)):
        if re.search(pattern, lines[i]):
            linum = i
            break

    # multiple replace in line
    if linum:
        for pair in replace_pairs:
            lines[linum] = lines[linum].replace(pair[0], pair[1])

    # save modified file
    with open(file_name, 'w') as writer:
        writer.writelines(lines)
