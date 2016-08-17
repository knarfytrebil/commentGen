import re
import sys, os

rFUNCTION = r"(\w+)\ = function"
rFUNCTION_INCLASS = r"(\w+)\: function"
rPROPERTY_INCLASS = r"(\w+)\: (.*)\,"
rCLASS = r"let (\w+)\ ="
rPARAM = r"\(.*?\)"
cFUNCTION = """
/**
* Insert Method Description Here
* @method %s
%s
* @return { Insert Return Param Here }
*/
"""
cCLASS = """
/**
* This is the description for my class.
*
* @class %s
* @%s
*/
"""

PARAM = """
* @param { %s } 
"""

# Get lines from File
def getFile(f): 
    file = open(f,'r')
    contents = file.readlines()
    file.close()
    return contents

# Drill down the files
def drillDown(lines):
    indexes = []
    for line in lines:

        m = re.search(rFUNCTION, line)                 # 1.look for let = function pattern
        m_class = re.search(rCLASS, line)              # 2.look for export let <classname> pattern
        f_inclass = re.search(rFUNCTION_INCLASS, line) # 3.look for export <function_name>:<classname> pattern

        # Pattern 2
        if m_class and line.endswith('.extend({\n'):
            d = {}
            constructor = line.split('=')[1].split('.extend')[0]
            classname = m_class.group(1)
            d['line'] = line
            d['comment'] = cCLASS % (classname, constructor)
            indexes.append(d)
        # Pattern 1 and 3
        if m or (f_inclass and not line.startswith('//')):
            d = {}
            paramstr = ""
            if m:
                method = m.group(1)
            else:        
                method = f_inclass.group(1)
            isParam = re.search(rPARAM, line)
            if isParam:
                params = isParam.group(0)[1:-1].split(',')
                for item in params:
                    if item is not '':
                        paramstr = paramstr + PARAM % item

            d['line'] = line
            d['comment'] = cFUNCTION % (method, paramstr)
            # print d
            indexes.append(d)
    return indexes

def insertComments(lines, indexes, filepath):
    for item in indexes:
        i = lines.index(item['line'])
        lines.insert(i, item['comment']) 

    _f = open(filepath,'w')
    _f.writelines(lines)
    _f.close()

def walk(path):
    for subdir, dirs, files in os.walk(path):
        if not subdir.endswith('utils'):
            for file in files:
                # Get Filename
                filepath = os.path.join(subdir, file)
                if len(filepath.split('.')) > 0:
                    ext = filepath.split('.')[1]
                    if ext == 'js':
                        l = getFile(filepath)
                        i = drillDown(l)
                        insertComments(l, i, filepath)
                        print filepath 
f = sys.argv[1]
# path = os.path.join(os.getcwd(), f)
path = os.path.abspath(f)
print path
walk(path)
# l = getFile(f)
# i = drillDown(l)
# insertComments(l,i)

