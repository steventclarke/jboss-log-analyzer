from analyze_log import getClassSet, getOutputList, mapClassNameToOutputLength, formatOutput 

logFile = "server.log"
classSet = getClassSet(logFile)
outputList = getOutputList(logFile)
classMap = mapClassNameToOutputLength(classSet, outputList) 
outputList = formatOutput(classMap)
output = "\n".join(outputList)

expectedFile = open("expected_output.txt", "rb")
expected = expectedFile.read()[:-1]

assert(output == expected)
print "Test successful"
