# Created by Kyle Johnston on 2014-08-01
# Last update: 2018-09-08

# Get resume from user
from tkinter.filedialog import askopenfilename
file_path = askopenfilename()


import re

def RemoveBrackets(newline):
    p = re.compile(r'\{([^}]*)\}') # remove brackets
    return p.sub(r'\1', newline)

ActiveFileR = open(file_path, 'r') # LaTeX resume
ActiveFileW = open(file_path[:len(file_path)-4] + '.txt', 'w') # plain text resume to save as

DocumentStart = False # becomes true after reaching \begin{document}
PrintLineCounter = 0 # indicates how many lines should be printed without consideration
LineCountDown = 0 # indicates how many lines to wait before printing a line without consideration

for i, line in enumerate(ActiveFileR):

    if DocumentStart == False and line.find('%% PERSONAL INFO') == -1:
        pass
    else: # document has started, begin writing
        DocumentStart = True # makes above 'if' statement always false
        PrintLine = False
        newline = line
        if PrintLineCounter != 0:
            # Print line without consideration; take 1 off of PrintLineCounter
            newline = RemoveBrackets(newline)
            PrintLine = True
            PrintLineCounter -= 1

        if LineCountDown != 0:
            # Take 1 off of LineCountDown; print line if LineCountDown is 0
            LineCountDown -= 1
            if LineCountDown == 0: # when countdown reaches 0, print
                p = re.compile(r'[^\S]*(.*)') # remove leading spaces
                newline = p.sub(r'\1\n', newline)
                PrintLine = True

        # Remove comments
        p = re.compile(r'%.*')
        if p.search(newline):
            newline = p.sub(r'', newline)

        # Address and contact information
        p = re.compile(r'\\newcommand{\\(.+?)}{(.+?)}')
        if p.search(newline):
            newline = p.sub(r'\2', newline)
            PrintLine = True

        # Objective
        p = re.compile(r'\\section{OBJECTIVE}')
        if p.search(newline):
            newline = '\n\nOBJECTIVE\n\n'
            PrintLine = True
            LineCountDown = 5

        # sect
        p = re.compile(r'[^\\]*\\' + 'sect' +'\{([^}]*)\}') # finds initial spaces, backslash, header, open bracket, text, close braket
        if p.search(newline):
            newline = p.sub(r'\n\n\1', newline) # print only text from above
            PrintLine = True

        # sectlist
        p = re.compile(r'[^\\]*\\' + 'sectlist' +'\{([^}]*)\}') # finds initial spaces, backslash, header, open bracket, text, close braket
        if p.search(newline):
            newline = p.sub(r'\n\n\1\n', newline) # print only text from above
            PrintLine = True

        # Entries
        entries = ['entry', 'school']
        for entry in entries:
            p = re.compile(r'[^\\]*\\' + entry +'\{([^}]*)\}') # finds initial spaces, backslash, header, open bracket, text, close braket
            if p.search(newline):
                newline = p.sub(r'\n\1\n', newline) # print only text from above
                PrintLine = True
                PrintLineCounter = 3

        # Items
        p = re.compile(r'\\item (.*)')
        if p.search(newline):
            newline = p.sub(r'\1', newline)
            PrintLine = True

        # Backslashes
        newline = newline.replace('\\', '')

        if PrintLine:
            ActiveFileW.write(newline)
