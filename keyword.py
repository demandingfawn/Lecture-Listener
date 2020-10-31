import requests
import json
import operator
    
class node: #Linked List node class
    def __init__(self,string):
        self.word = string
        nextNode = None
        prevNode = None
        return
    
    
class linkedList:   #Linked List
    def __init__(self):
        self.head = None
        self.tail = None
        return
    def getFirst(self):
        return self.head
    
    def addNode(self, string):  #insert node to the tail
        temp = node(string)
        temp.nextNode = None
        
        if self.head == None:
            self.head = temp
            temp.prevNode = None
        else:
            temp.prevNode = self.tail
            temp.prevNode.nextNode = temp
            
        self.tail = temp
        
    
    def deleteNode(string):
        return
    
    def printNode(self):    #print node's string from head to tail
        temp = self.head
        while True:
            print(temp.word)
            if temp.nextNode != None: 
                temp = temp.nextNode
                continue
            else:
                break
        return

class keyword:
    
    def __init__(self):
        self.dict1 = {}
        self.dict2 = {}
        self.trsc = ""
        self.text = linkedList()
        
    def openTranscript(self, address):
        f = open(address, 'r',encoding='utf-8')
        self.trsc = f.read()
        return
    
    def singleWord(self):
        word = ""
        for i in range(len(self.trsc)):  #for all character in the transcript
            
            if self.trsc[i] >= 'a' and self.trsc[i] <= 'z':   #when the letter is lower case
                word += self.trsc[i]
                if i == (len(self.trsc)-1): #when it's the last letter in the transcript
                    if word in self.dict1:
                        self.dict1[word] += 1
                    else:
                        self.dict1[word] = 1
                    continue
                
            elif self.trsc[i] >= 'A' and self.trsc[i] <= 'Z': #when it's upper case
                temp = self.trsc[i].lower()
                word += temp
                if i == (len(self.trsc)-1):
                    if word in self.dict1:
                        self.dict1[word] += 1
                    else:
                        self.dict1[word] = 1
                    continue
                
            elif self.trsc[i] == '’':    #when it has apostrophe 1
                if word != "":
                    self.text.addNode(word)
                    if word in self.dict1:
                        self.dict1[word] += 1
                    else:
                        self.dict1[word] = 1
                word = "'"
            elif self.trsc[i] == '\'':   #when it has apostrophe 2
                if word != "":
                    self.text.addNode(word)
                    if word in self.dict1:
                        self.dict1[word] += 1
                    else:
                        self.dict1[word] = 1
                word = "'"
                
            else:   #when it's non of them
                if word != "":
                    self.text.addNode(word)
                    if word in self.dict1:
                        self.dict1[word] += 1
                    else:
                        self.dict1[word] = 1
                word = ""
                continue

        #list of not important words (pronouns, conjunctions, etc.)
        notImportant = ["i", "you", "we", "he", "she", "they",
                        "my", "your","our" , "his", "her", "their", "s",
                        "me", "yours", "us","him", "them", "these",
                        "mine", "ours","hers",
                        "myself", "himself", "herself", "ourselves", "yourself", "themselves",
                        "a", "an", "the",
                        "am", "is", "are", "be", "m",
                        "was", "were",
                        "what", "where", "how", "which", "whom", "who", "when",
                        "this", "that", "it","things", "thing", "its", "one", "other",
                        "not", "some", "t", "don", "well",
                        "'re", "'ve", "'ll", "'t", "'m", "'s", "'d",
                        "all", "only",
                        "have", "had", "do", "did",
                        "can", "could", "should", "shall", "may", "might", "will", "would", "maybe"]
        conjunctions = ["and", "to", "of", "as", "at", "for", "from", "both",
                        "with", "in", "on", "about", "up", "or", "so",
                        "if","unless", "before", "after", "by", "each",
                        "through", "then", "now", "next", "over", "than", "too"]


        #erase the words listed above from dictionary
        for i in range(len(notImportant)):

            if notImportant[i] in self.dict1:
                del self.dict1[notImportant[i]]

        for i in range(len(conjunctions)):
            if conjunctions[i] in self.dict1:
                del self.dict1[conjunctions[i]]


        #erase all words that just spoken only few times time
        temp = []
        for key in self.dict1.keys():
            if self.dict1[key] <= 2:
                temp.append(key)

        for item in temp:
            del self.dict1[item]
        return
    
    def multipleWord(self):
        wordCount = 0
        longWord=""

        temp = self.text.getFirst()

        while True:
            if temp.word in self.dict1:
                #when the word is in the first dictionary,
                #add it to longWord and increase wordCount
                longWord += temp.word
                longWord += " "
                wordCount += 1
                
            elif wordCount > 1:
                #when the word is not in the dictionary and composed of more than 1 word,
                #add to dict2 and reset longWord and wordCount
                if longWord in self.dict2:
                    self.dict2[longWord] += 1
                else:
                    self.dict2[longWord] = 1
                longWord = ""
                wordCount = 0
            else:
                #when it meets non of the condition
                #just reset longWord and wordCount
                longWord = ""
                wordCount = 0


                 
            if temp.nextNode != None: #move to next node when it exists
                temp = temp.nextNode
                continue
            else:   #end loop if not.
                break

        #erase multi-word keywords that appeared just once
        temp = []
        for key in self.dict2.keys():
            if self.dict2[key] == 1:
                temp.append(key)

        for item in temp:
            del self.dict2[item]
            
        return
    
    def printKeywords(self):
        #sort the dictionaries in decending order with its frequecy
        self.dict1 = dict( sorted(self.dict1.items(), key=operator.itemgetter(1),reverse=True))
        self.dict2 = dict( sorted(self.dict2.items(), key=operator.itemgetter(1),reverse=True))

        #print the dictionaries
        print(self.dict1)
        print("\n")
        print(self.dict2)
        return
    
    def getTopKeywords(self): #return keywords with top 5 frequencies.
        TopList = []
        count = 0
        prevFreq = 0
        for key in list(self.dict2.keys()):
            if count >= 5:
                break
            if prevFreq == 0:
                TopList.append(key)
                prevFreq = self.dict2[key]
                count += 1
            elif prevFreq == self.dict2[key]:
                TopList.append(key)
            else:
                TopList.append(key)
                prevFreq = self.dict2[key]
                count += 1
        return TopList

aa = keyword()
aa.openTranscript("sampletext.txt")
aa.singleWord()
aa.multipleWord()
aa.printKeywords()
print("possible keywords identified are: ", aa.getTopKeywords())
