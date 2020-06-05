#!/usr/bin/env python
"""Create plain text resume from LaTeX file"""
import os
import re


# Get resume from user
CONFIG = 'resume_path.cfg'
if os.path.isfile(CONFIG):
    with open(CONFIG, 'r') as config_file:
        file_path = config_file.read().strip()
else:
    from tkinter.filedialog import askopenfilename
    file_path = askopenfilename()


def RemoveBrackets(newline):
    """Returns line without brackets"""
    p = re.compile(r'\{([^}]*)\}')
    return p.sub(r'\1', newline)


ActiveFileR = open(file_path, 'r')  # LaTeX resume
ActiveFileW = open(file_path[:len(file_path)-4] + '.txt', 'w')  # plain text resume to save as

document_start = False  # becomes true after reaching \begin{document}
print_line_counter = 0  # indicates how many lines should be printed without consideration
line_count_down = 0  # indicates how many lines to wait before printing a line without consideration

for i, line in enumerate(ActiveFileR):

    if not document_start and line.find('%% PERSONAL INFO') == -1:
        pass
    else:  # document has started, begin writing
        document_start = True  # makes above 'if' statement always false
        print_line = False
        newline = line

        if print_line_counter > 0:
            # Print line without consideration; take 1 off of print_line_counter
            newline = RemoveBrackets(newline)
            if print_line_counter == 2:
                location = newline
            print_line = True
            print_line_counter -= 1

        if line_count_down > 0:
            # Take 1 off of line_count_down; print line if line_count_down is 0
            line_count_down -= 1
            if line_count_down == 0:  # when countdown reaches 0, print
                p = re.compile(r'[^\S]*(.*)')  # remove leading spaces
                newline = p.sub(r'\1\n', newline)
                print_line = True

        # Remove comments
        p = re.compile(r'[^\\]%.*|^%.*')
        if p.search(newline):
            newline = p.sub(r'', newline)

        # Address and contact information
        p = re.compile(r'\\newcommand{\\(.+?)}{(.+?)}')
        if p.search(newline):
            newline = p.sub(r'\2', newline)
            print_line = True

        # Objective
        p = re.compile(r'\\section{OBJECTIVE}')
        if p.search(newline):
            newline = '\n\nOBJECTIVE\n\n'
            print_line = True
            line_count_down = 5

        # sect
        p = re.compile(r'[^\\]*\\' + 'sect' +'\{([^}]*)\}') # finds initial spaces, backslash, header, open bracket, text, close braket
        if p.search(newline):
            newline = p.sub(r'\n\n\1', newline)  # print only text from above
            print_line = True

        # sectlist
        p = re.compile(r'[^\\]*\\' + 'sectlist' +'\{([^}]*)\}')  # finds initial spaces, backslash, header, open bracket, text, close braket
        if p.search(newline):
            newline = p.sub(r'\n\n\1\n', newline)  # print only text from above
            print_line = True

        # Entries
        entries = ['entry', 'school']
        for entry in entries:
            p = re.compile(r'[^\\]*\\' + entry +'\{([^}]*)\}')  # finds initial spaces, backslash, header, open bracket, text, close braket
            if p.search(newline):
                newline = p.sub(r'\n\1\n', newline)  # print only text from above
                company = newline
                print_line = True
                print_line_counter = 3

        # Roles
        p = re.compile(r'[^\\]*\\' + 'role' +'\{([^}]*)\}')  # finds initial spaces, backslash, header, open bracket, text, close braket
        if p.search(newline):
            ActiveFileW.write(company[:-1])
            newline = p.sub(r'\n\1\n', newline)  # print only text from above
            ActiveFileW.write(newline[:-1])
            ActiveFileW.write(location)
            print_line = True
            print_line_counter = 1
            continue

        # Items
        p = re.compile(r'\\item (.*)')
        if p.search(newline):
            newline = p.sub(r'\1', newline)
            print_line = True

        # Backslashes
        newline = newline.replace('\\', '')

        if print_line:
            ActiveFileW.write(newline)
