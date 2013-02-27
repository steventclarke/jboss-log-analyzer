#!/usr/bin/python

import re
import sys

"""
Script takes a path to a log file and analyzes the file
to determine all classes which produce log output.

It then performs additional analysis to determine the
amount of output in bytes that each class is responsible for.

Output takes the format of [fully.qualified.classname] : outputLength
sorted by outputLength in ascending order

Output prints to stdout.

To Run : >> python analyze_log.py path/to/server.log
"""

def getClassSet(fileName) :
    """
    Given a filename, reads file line by line and extracts
    fully qualified class names of classes responsible for
    log output into a returned list
    """
    reader = open(fileName, 'rb')
    classList = []
    pattern = re.compile(r'\[[\w|\.]+\]')
    for line in reader :
        classMatch = re.search(pattern, line)
        if classMatch is not None :
            classList.append(classMatch.group(0))
    classSet = set(classList)
    reader.close()
    return classSet

def getOutputList(fileName) :
    """
    Given a filename, reads file into memory and splits by 
    combined timestamp and LOG level indicator to return a
    list of log output statements.
    TODO : develop buffered approach to reduce memory footprint
    """
    reader = open(fileName, 'rb')
    contents = reader.read()
    delimPattern = re.compile(r'\n.{24}[INFO|DEBUG|TRACE|ERROR|WARN]')
    outputList = re.split(delimPattern, contents)
    reader.close()
    return outputList

def mapClassNameToOutputLength(classSet, outputList) :
    """
    Given a set of bracketed, fully qualified class names
    and a list of log ouptut chunks, iterate through log
    output chunks and associate chunks with the class
    that produced the output.  Return map of class name to
    length of log output produced by that class.
    """
    classMap = {}
    for classString in classSet :
        classOutputTotal = 0
        for outputString in outputList :
            if classString in outputString :
                classOutputTotal += len(outputString)
        classMap[classString] = classOutputTotal
    return classMap

def formatOutput(classMap) :
    """
    Given a map of fully qualified class name to length
    of associated log output, format output string and
    sort by length of associated log output.
    Prints output to stdout
    """
    classStringLength = max([len(x) for x in classMap])
    strings = []
    for key in classMap :
        strings.append("%s : %s" % (key + (" " * (classStringLength - len(key))), classMap[key]))
    strings.sort(cmp)
    return strings

def printOutput(outputList) :
    for string in outputList :
        print string

def outputLength(string) :
    """
    Given a script output string which consists of 
    "[fully.qualified.classname] : outputLength"
    extracts outputLength as int for use by 
    comparator
    TODO : change impl to split by colon and 
    strip whitespace from second item (more robust)
    """
    return int(string[string.find(':') + 2:])

def cmp(x, y) :
    """
    Comparator which compares strings based on the
    result of outputLength(string)
    """
    bx = outputLength(x)
    by = outputLength(y)
    if bx < by :
        return -1
    elif bx == by :
        return 0
    return 1
    
### MAIN ###

def main() :
    if len(sys.argv) == 2 :
        logFile = sys.argv[1]
    else :
        print "Invalid arguments.\nUsage : >> python analyze_log.py path/to/server.log"
        exit()
    classSet = getClassSet(logFile)
    outputList = getOutputList(logFile)
    classMap = mapClassNameToOutputLength(classSet, outputList) 
    printOutput(formatOutput(classMap))

if __name__ == "__main__":
    main()
