import requests
import json
import operator

class word: #class for store word
    def __init__(self, temp):
        self.word = temp
        frequency = 1
        return
        
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

#read in the sample text of a lecture
f=open("sampletext.txt", 'r',encoding='utf-8')
trsc = f.read()
text = linkedList() #a linked list for storing lecture to linked list form


#count frequency of each words
dict1 = {}
word = ""

for i in range(len(trsc)):  #for all character in the transcript
    
    if trsc[i] >= 'a' and trsc[i] <= 'z':   #when the letter is lower case
        word += trsc[i]
        if i == (len(trsc)-1): #when it's the last letter in the transcript
            if word in dict1:
                dict1[word] += 1
            else:
                dict1[word] = 1
            continue
        
    elif trsc[i] >= 'A' and trsc[i] <= 'Z': #when it's upper case
        temp = trsc[i].lower()
        word += temp
        if i == (len(trsc)-1):
            if word in dict1:
                dict1[word] += 1
            else:
                dict1[word] = 1
            continue
        
    elif trsc[i] == '’':    #when it has apostrophe 1
        if word != "":
            text.addNode(word)
            if word in dict1:
                dict1[word] += 1
            else:
                dict1[word] = 1
        word = "'"
    elif trsc[i] == '\'':   #when it has apostrophe 2
        if word != "":
            text.addNode(word)
            if word in dict1:
                dict1[word] += 1
            else:
                dict1[word] = 1
        word = "'"
        
    else:   #when it's non of them
        if word != "":
            text.addNode(word)
            if word in dict1:
                dict1[word] += 1
            else:
                dict1[word] = 1
        word = ""
        continue

#list of not important words (pronouns, conjunctions, etc.)
notImportant = ["i", "you", "we", "he", "she", "they",
                "my", "your","our" , "his", "her", "their", "s",
                "me", "yours", "us","him", "them", "these",
                "mine", "ours","hers",
                "myself", "himself", "herself", "ourselves", "yourself", "themselves"
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

    if notImportant[i] in dict1:
        del dict1[notImportant[i]]

for i in range(len(conjunctions)):

    if conjunctions[i] in dict1:
        del dict1[conjunctions[i]]


#erase all words that just spoken only few times time
temp = []
for key in dict1.keys():
    if dict1[key] <= 2:
        temp.append(key)

for item in temp:
    del dict1[item]


#print first result
dict1 = dict( sorted(dict1.items(), key=operator.itemgetter(1),reverse=True))
print(dict1)
print("\n")


#find multi-word keywords
dict2 = {}
wordCount = 0
longWord=""

temp = text.getFirst()

while True:
    if temp.word in dict1:
        #when the word is in the first dictionary,
        #add it to longWord and increase wordCount
        longWord += temp.word
        longWord += " "
        wordCount += 1
        
    elif wordCount > 1:
        #when the word is not in the dictionary and composed of more than 1 word,
        #add to dict2 and reset longWord and wordCount
        if longWord in dict2:
            dict2[longWord] += 1
        else:
            dict2[longWord] = 1
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
for key in dict2.keys():
    if dict2[key] == 1:
        temp.append(key)

for item in temp:
    del dict2[item]

#print multi-word keywords.
dict2 = dict( sorted(dict2.items(), key=operator.itemgetter(1),reverse=True))
print(dict2)


