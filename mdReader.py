#It assume that .md file have same name as the ID number of the lecture

#like when a lecture have ID number '123456',
#   the file .md file that linked to the lecture needs to be '123456.md'

#To link timestamps to the transcript,
#   you need to count number of timestamps places in the transcript
#   and link timestamp into the place with same order
#   (For example, 3rd timestamp in the .md file need to be connected to the 3rd place of timestamp in the transcript)

# the sample timestamp list is also posted with name "123456.md"

import os.path
from os import path

class mdReader:
    def __init__(self):
        self.stampList = []
        return
    
    def generateMD(self, string, lectureID):
        if path.exists("lectures/" + str(lectureID) + ".md"):
            print("timestamp file already exists!")
            return ""
        
        f = open(("lectures/" + str(lectureID) + ".md"), 'w')
        tempStr = ""
        tempTime = ""
        isStamp = False
        indexCount = 0
        for i in range(0, len(string)):
            if string[i] == '}':
                f.write(">" + str(indexCount) +"\n#" + tempTime + "\n")
                isStamp = False
                tempTime = ""
                tempStr += ("{" + str(indexCount) + "}")
                indexCount += 1
                
            elif isStamp:
                tempTime += string[i]
                
            elif string[i] == '{':
                isStamp = True
                
            
            else:
                tempStr += string[i]
                
        f.close()
        return tempStr

    #read .md file and get all timestamps in the file
    def readMD(self, lectureID):
        if path.exists("lectures/" + str(lectureID) + ".md") == False:
            print("timestamp file does not exists!")
            return
        
        f = open("lectures/" + str(lectureID) + ".md",'r',encoding='utf-8')
        stampIndex = 0
        
        while True:
            string = f.readline()
            print(string)
            if string == "":
                break
            elif len(string) < 2:
                print("syntax error!")
                
            elif string[0] == '>':
                if int(string[1:len(string)]) != stampIndex:
                    print("Stamp Index Error!")
                    break
                else:
                    stampIndex += 1
                    continue
    
            elif string[0] == '#':
                tempTime = int(string[1:len(string)])
                self.stampList.append(tempTime)
                print(tempTime)
                print(self.stampList)
                continue
            
            else:
                print("Syntax Error!")
                break
                
    def getStamps(self):
        return self.stampList
"""
temp = mdReader()
string = temp.generateMD("this is test message 11.{7} this is test message 22.{312}", "aaaaa1")
print(string)

temp.readMD("aaaaa1")
print(temp.getStamps())
"""

