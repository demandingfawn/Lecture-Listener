#It assume that .md file have same name as the ID number of the lecture

#like when a lecture have ID number '123456',
#   the file .md file that linked to the lecture needs to be '123456.md'

#you can get list of timestamps that are in seconds form (ex. 1h10m40s would be 4240 (seconds) in the stamp list)

#To link timestamps to the transcript,
#   you need to count number of timestamps places in the transcript
#   and link timestamp into the place with same order
#   (For example, 3rd timestamp in the .md file need to be connected to the 3rd place of timestamp in the transcript)

# the sample timestamp list is also posted with name "123456.md"

class mdReader:
    
    def __init__(self):
        self.stampList = []


    #read .md file and get all timestamps in the file
    def readMD(self, address):
        f = open(address,'r',encoding='utf-8')
        
        stampIndex = 0
        
        while True:
            string = f.readline()
            if string == "":
                break
            elif len(string) < 2:
                print("syntax error!")
                
            elif string[0] == '>':
                temp = ""
                
                for i in range(1,len(string)):
                    temp += string[i]
                
                if int(temp) != stampIndex:
                    print("Stamp Index Error!")
                    break
                else:
                    stampIndex += 1
                    continue
    
            elif string[0] == '#':
                h = 0
                m = 0
                s = 0
                temp = ""
                for i in range(1,len(string)):
                    
                    if string[i] == 'h':
                        h = int(temp)
                        temp = ""
                        continue

                    elif string[i] == 'm':
                        m = int(temp)
                        temp = ""
                        continue

                    elif string[i] == 's':
                        s = int(temp)
                        temp = ""
                        continue

                    elif string[i] >= '0' and string[i] <= '9':
                        temp += string[i]
                        
                    elif string[i] == '\n':
                        continue

                    else:
                        print("Stamp Content Error! ", string[i])
                tempTime = 0
                tempTime = h * 3600 + m * 60 + s
                self.stampList.append(tempTime)
                continue
            
            else:
                print("Syntax Error!")
                break
                
    def getStamps(self):
        return self.stampList
"""
temp = mdReader()
temp.readMD("123456.md")

print(temp.getStamps())
"""
