# created by Kyle Johnston
# last update: 2014-08-07

import Tkinter, tkFileDialog

root = Tkinter.Tk()
root.withdraw()

file_path = tkFileDialog.askopenfilename()

import sys, fileinput, re

def RemoveBrackets(newline):
    p = re.compile(r'\{([^}]*)\}') # remove brackets
    return p.sub(r'\1', newline)

ActiveFileR = open(file_path, 'r')
ActiveFileW = open(file_path[:len(file_path)-4] + ' Plain Text' + file_path[len(file_path)-4:], 'w')

DocumentStart = False # becomes true after reaching \begin{document}
PrintLineCounter = 0 # indicates how many lines should be printed without consideration
LineCountDown = 0 # indicates how many lines to wait before printing a line without consideration

# name
ActiveFileW.write('Your Name\n\n')

for i, line in enumerate(ActiveFileR):
    if DocumentStart == False and line.find('\\begin{document}') == -1:
        pass
    else: # document has started, begin writing
        DocumentStart = True
        PrintLine = False
        newline = line
        if PrintLineCounter != 0:
            newline = RemoveBrackets(newline)
            PrintLine = True
            PrintLineCounter -= 1
        if LineCountDown != 0:
            LineCountDown -= 1
            if LineCountDown == 0: # when countdown reaches 0, print
                p = re.compile(r'[^\S]*(.*)') # remove leading spaces
                newline = p.sub(r'\1\n', newline)
                PrintLine = True

        # remove comments
        p = re.compile(r'%.*')
        if p.search(newline):
            newline = p.sub(r'', newline)

        # address and contact information
        p = re.compile(r'\\normalsize (.+)')
        if p.search(newline):
            newline = p.sub(r'\1\n', newline)
            newline = newline.replace(' \\bt\\ ', '\n')
            newline = RemoveBrackets(newline)
            PrintLine = True

        # sections and entries
        headings = ['section', 'sect', 'sectlist']
        for header in headings:
            p = re.compile(r'[^\\]*\\' + header +'\{([^}]*)\}') # finds initial spaces, backslash, header, open bracket, text, close braket
            if p.search(newline):
                newline = p.sub(r'\n\n\1', newline) # print only text from above
                PrintLine = True
                if newline.find('OBJECTIVE') != -1:
                    LineCountDown = 5

        # entries
        entries = ['entry', 'school']
        for entry in entries:
            p = re.compile(r'[^\\]*\\' + entry +'\{([^}]*)\}') # finds initial spaces, backslash, header, open bracket, text, close braket
            if p.search(newline):
                newline = p.sub(r'\n\1\n', newline) # print only text from above
                PrintLine = True
                PrintLineCounter = 3

        # items
        p = re.compile(r'\\item (.*)')
        if p.search(newline):
            newline = p.sub(r'\1', newline)
            PrintLine = True

        # backslashes
        newline = newline.replace('\\', '')

        if PrintLine:
            ActiveFileW.write(newline)