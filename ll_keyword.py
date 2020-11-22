import operator
import wikipediaapi
#befoer using it, download wikipedia api using "pip install wikipedia-api" in your terminal
#here is also the link to the api instruction page: "https://pypi.org/project/Wikipedia-API/"

#you also need to check location and name of the transcript file before using it. (for this code, it's using "sampleText.txt")
#the method of accessing the transcript might be changed when we work on the storing system in the database.

#when you use this code, you only need to use "getTopKeywords()"  to get a list of keywords,
#   and searchWiki(word) for getting a definition of a word from Wikipedia.

#if you want to check if it works:
#   place sampleText.txt into the same folder where this code is in,
#   and paste the code in the multiline comment below,
"""
aa = keyword()
keywords = aa.getTopKeywords()
print(keywords)
for i in range(0, len(keywords)):
    print(keywords[i])
    print(aa.searchWiki(keywords[i]))
    print("\n")
"""
#   and try to run this module


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
        self.dict1 = {} #save all words appearing in the transcript
        self.dict2 = {} #save all keywords that composed of mutiple words
        self.dict3 = {} #save all single-word keyword
        self.trsc = ""  #transcript string
        self.text = linkedList()    #transcript saved in linked list format (for internal processing)

        
    def isEndingWith(self, string1, part):
        #check if 'string1' is ending with 'part'
        #it's for finding suffixes
        if len(string1) <= len(part):
            return False
        check = True
        for i in range(0, len(part)):
            if string1[-1-i] == part[-1-i]:
                continue
            else:
                check = False
                break
        return check
        
    def openTranscript(self, address):
        #open txt file in read mode
        f = open(address, 'r',encoding='utf-8')
        self.trsc = f.read()
        return
    
    def singleWord(self):
        #find all words in the transcript
        #store them into 'dict1' with their frequency (key = word, values = frequencies)
        #and create 'text' linkedList
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
        notImportant = ["'", "i", "you", "we", "he", "she", "they",
                        "my", "your","our" , "his", "her", "their", "s",
                        "me", "yours", "us","him", "them", 
                        "mine", "ours","hers",
                        "myself", "himself", "herself", "ourselves", "yourself", "themselves",
                        "a", "an", "the",
                        "am", "is", "are", "be", "been", "being", "m",
                        "was", "were",
                        "what", "where", "how", "which", "whom", "who", "when", "why",
                        "this", "that", "it","things", "thing", "its", "one", "other", "kind",
                        "not", "some", "t", "don", "well",
                        "'re", "'ve", "'ll", "'t", "'m", "'s", "'d",
                        "all", "only",
                        "have", "had", "do", "did",
                        "here", "there", "these", "those",
                        "can", "could", "should", "shall", "may", "might", "will", "would", "maybe", "must",
                        "yeah", "yep", "yeap"]
        conjunctions = ["and", "to", "of", "as", "at", "for", "from", "both",
                        "with", "in", "on", "about", "up", "or", "so",
                        "if","unless", "before", "after", "by", "each",
                        "through", "then", "now", "next", "over", "than", "too",
                        "but", "either", "neither", "nor", "like" , "because", "since", "just", "again",
                        "more", "very", "most",
                        "though", "although", "despite", "even", "also", "let", "letting"]
        commonWords = ["new", "old", "think", "thought", "see", "saw",
                       "show", "showed", "put", "try", "trying", "tried",
                        "say", "saying", "said",
                       "make", "made", "get", "got", "go", "went", "gone", "going", "do", "done", "did", "doing", "have", "had", "has", "having"
                       "one", "two", "three",
                       "same", "different", "remember",
                       "way", "reason", "time"]

        #erase the words listed above from dictionary
        for i in range(len(notImportant)):
            if notImportant[i] in self.dict1:
                del self.dict1[notImportant[i]]

        for i in range(len(conjunctions)):
            if conjunctions[i] in self.dict1:
                del self.dict1[conjunctions[i]]

        for i in range(len(commonWords)):
            if commonWords[i] in self.dict1:
                del self.dict1[commonWords[i]]


        #erase all words that just spoken only few times time
        temp = []
        for key in self.dict1.keys():
            if self.dict1[key] <= 2:
                temp.append(key)

        for item in temp:
            del self.dict1[item]
        return
    
    def multipleWord(self):
        #find all keywords that is composed of more than one word
        #store them in 'dict2' with frequencies (key = word, values = frequencies)
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
                longWord = longWord[0:len(longWord)-1]
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

    def singleWordFilter(self):
        #only noun can be a keyword
        #because of that, it filters verb, adverb, and adjectives
        #and increase count of a noun that have same radix
        #and modify frequencies in 'dict3' since most of frequencies in dict3 tend to be higher.
        
        advSuffixes = ["ly", "ily", "ically"]
        #noun -> adj
        adjSuffixes1 = ["al", "ial", "ary", "ful", "ic", "ical", "ish", "less", "like", "ly", "ous", "y"]
                        #ic -> ical,
        #verb -> adj
        adjSuffixes2 = ["able", "ible", "ant", "ent", "ive", "ing", "ed", "en"]
        verbSuffixes = ["ate", "ates",
                       "en", "ens",
                       "ify", "ifies",
                       "ise", "ises"
                       "ize", "izes"]
        Prefixes = ["a", "an", "ab", "abs",
                    "ad", "add", "ac", "acc", "af", "aff", "ag", "agg", "al", "all", "an", "ann", "ap", "app", "at", "att", "as", "ass"
                    "ante", "anti", "ant",
                    "be", "com", "co", "col", "con", "cor",
                    "contra", "counter", "de",
                    "dia", "di", "dis", "di",
                    "en", "em", "ex", "e", "ef",
                    "extra", "hemi", "hyper", "hypo",
                    "in", "il", "im", "ir",
                    "infra", "inter", "intra", "non",
                    "ob", "oc", "of", "op",
                    "out", "over", "peri", "post", "pre",
                    "pro", "re", "semi",
                    "sub", "suc", "suf", "sug", "sup", "sur", "sus",
                    "syn", "sym", "trans", "ultra", "un", "under"]
        maxList = list(self.dict2.values())
        sumMulti = maxList[0] + maxList[1] + maxList[2]
        maximum = int((sumMulti /3 ) * 2.5)
        #print("sum : ", sumMulti)
        #print("ave : ", sumMulti/3)
        #print("maximum frequency setting: ", maximum)
        for key in list(self.dict1.keys()):
            if self.dict1[key] > maximum or len(key) <= 1:
                del self.dict1[key]
        maxList = list(self.dict1.values())
        sumSingle = maxList[0] + maxList[1] + maxList[2]
        divConst = round(sumSingle/sumMulti)
        #print("divConst: ", divConst)
        
        #remove adverb suffix
        #ly, y -> ily , le -> ly, ic -> ically
        for key in self.dict1.keys():
            #print(key)
            tempRad = key
            tempSuff = ""
            for suff in advSuffixes:
                if self.isEndingWith(key, suff):
                    if tempSuff == "":
                        tempSuff = suff
                    elif len(tempSuff) < len(suff):
                        tempSuff = suff
            if tempSuff != "":
                #tempRad = key[0:(len(key)-len(tempSuff))]
                continue
                
        #remove adjective suffix
            tempSuff = ""
            isNoun = False
            for suff in adjSuffixes1:
                if self.isEndingWith(tempRad, suff):
                    if tempSuff == "":
                        tempSuff = suff
                    elif len(tempSuff) < len(suff):
                        tempSuff = suff
                
            if tempSuff != "":
                isNoun = True
                if tempSuff == "ical":
                    tempRad = tempRad[0:len(tempRad) - 2]
                else:
                    tempRad = tempRad[0:len(tempRad) -len(tempSuff)]
                    #print("filtering adj suffix: ", tempSuff)
                    #print("resulting: ", tempRad)

            if isNoun == False : #when it looks like verb + suffix
                for suff in adjSuffixes2:
                    if self.isEndingWith(tempRad, suff):
                        if tempSuff == "":
                            tempSuff = suff
                        elif len(tempSuff) < len(suff):
                            tempSuff = suff
                
                if tempSuff != "":
                    tempRad = tempRad[0:len(tempRad) -len(tempSuff)]
                    #print("filtering adj suffix: ", tempSuff)
                    #print("resulting: ", tempRad)
        #remove verb suffix
                tempSuff = ""
                for suff in verbSuffixes:
                    if self.isEndingWith(tempRad, suff):
                        if tempSuff == "":
                            tempSuff = suff
                        elif len(tempSuff) < len(suff):
                            tempSuff = suff
                    
                if tempSuff != "":
                    tempRad = tempRad[0:len(tempRad) -len(tempSuff)]
                    #print("filtering verb suffix: ", tempSuff)
                    #print("resulting: ", tempRad)
        
        #find the word that contains radix and has shortest length
            wordImportant = ""
            for word in self.dict1.keys():
                if tempRad in word:
                    if wordImportant == "":
                        wordImportant = word
                    elif len(word) < len(wordImportant):
                        wordImportant = word
                    elif len(word) == len(wordImportant) and key == word:
                        wordImportant = word
            #print("keyword found is: ", wordImportant, "\n")
            if wordImportant in self.dict3:
                self.dict3[wordImportant] += self.dict1[key]

            else:
                self.dict3[wordImportant] = self.dict1[key]
                
                for temp in list(self.dict2.keys()):
                    if tempRad in temp:
                        self.dict3[wordImportant] -= self.dict2[temp]
                        #print("decrease count: ", temp, " ", self.dict2[temp])
                
            #print("\n")

        #remove counts that also counted in mutil-word keywords
        
        for key in list(self.dict3.keys()):
            self.dict3[key] = int(self.dict3[key]/divConst)
            
        return
    def sortDictionary(self):
        #sort the dictionaries in decending order with its frequecy
        self.dict1 = dict( sorted(self.dict1.items(), key=operator.itemgetter(1),reverse=True))
        self.dict2 = dict( sorted(self.dict2.items(), key=operator.itemgetter(1),reverse=True))
        self.dict3 = dict( sorted(self.dict3.items(), key=operator.itemgetter(1),reverse=True))
        return
    
    def printKeywords(self):
        #print the dictionaries
        print(self.dict1)
        print("\n")
        print(self.dict2)
        print("\n")
        print(self.dict3)
        print("\n")
        return
    
    def getTopKeywords(self):
        #return most frequent keywords
        self.openTranscript("sampleText.txt")
        self.singleWord()
        self.multipleWord()
        self.sortDictionary()
        self.singleWordFilter()
        self.sortDictionary()
        #self.printKeywords()
        
        TopList = []
        count = 0
        prevFreq = 0

        keysSingle = list(self.dict3.keys())
        keysMultiple = list(self.dict2.keys())
        index1 = 0
        index2 = 0
        while count < 10:
            currentFreq = 0
            a = self.dict3[keysSingle[index1]]
            b = self.dict2[keysMultiple[index2]]
            if a > b :
                TopList.append(keysSingle[index1])
                currentFreq = a
                index1 += 1
            elif a < b:
                TopList.append(keysMultiple[index2])
                currentFreq = b
                index2 += 1
            else:
                TopList.append(keysSingle[index1])
                TopList.append(keysMultiple[index2])
                currentFreq = a
                index1 += 1
                index2 += 1
            if currentFreq < prevFreq:
                count += 1
                continue
            elif prevFreq == 0:
                count += 1
                continue
        return TopList
    
    def searchWiki(self, word):
        #search word in the Wikipedia and get definition of the word if exists.
        #it returns empty string when:
        #       the page not exists in the Wikipedia
        #       or the page is a reference page that starts with "~~~ may refer to:"
        
        wiki = wikipediaapi.Wikipedia('en')
        if len(word) == 0:
            return ""
        tempWord = ""
        loopCount = 0
        while loopCount < len(word): 
            if loopCount == 0:
               tempWord += word[loopCount].upper()
            elif word[loopCount] == ' ':
                tempWord += ' '
                tempWord += word[loopCount+1].upper()
                loopCount += 1
            else:
                tempWord += word[loopCount]
            loopCount += 1
        if tempWord != "":
            search = wiki.page(tempWord)
            if search.exists():         #when it exists
                #check if the page is for referencing list of page
                checkDef = False
                message = "to:"
                loopCount = 0
                messCount = 0
                while True:
                    
                    if messCount == len (message):
                        checkDef = True
                        break;
                    if loopCount > 40:
                        break
                    if search.summary[loopCount] == message[messCount]:
                        loopCount += 1
                        messCount += 1
                    else:
                        messCount = 0
                        loopCount += 1
                if checkDef:
                    return ""

                #if the page is only about the word
                else:
                    tempDef = ""
                    loopCount = 0
                    while loopCount < len(search.summary):
                        if search.summary[loopCount] == '.':
                            tempDef += '.'
                            break
                        else:
                            tempDef += search.summary[loopCount]
                        loopCount += 1
                    return tempDef
            else:
                return ""
        return ""
    
