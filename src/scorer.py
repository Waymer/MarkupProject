import re
import datetime
import sqlite3

class Scorer:
    def __init__(self):
        #Score Modifiers
        self.divScore = 3
        self.pScore = 1
        self.h1Score = 3
        self.h2Score = 2
        self.htmlScore = 5
        self.bodyScore = 5
        self.headerScore = 10
        self.footerScore = 10
        self.fontScore = -1
        self.centerScore = -2
        self.bigScore = -2
        self.strikeScore = -1
        self.ttScore = -2
        self.framesetScore = -5
        self.frameScore = -5
    def calculateScore(self, filename):
        path = "../data/"
        fo = open(path + filename)
        st = fo.read().lower()

        #Score Modifiers
        #divScore = 3
        #pScore = 1
        #h1Score = 3
        #h2Score = 2
        #htmlScore = 5
        #bodyScore = 5
        #headerScore = 10
        #footerScore = 10
        #fontScore = -1
        #centerScore = -2
        #bigScore = -2
        #strikeScore = -1
        #ttScore = -2
        #framesetScore = -5
        #frameScore = -5

        #Tag Matching
        divList = re.findall("<div", st)
        pList = re.findall("<p", st)
        h1List = re.findall("<h1", st)
        h2List = re.findall("<h2", st)
        htmlList = re.findall("<html", st)
        bodyList = re.findall("<body", st)
        headerList = re.findall("<header", st)
        footerList = re.findall("<footer", st)
        fontList = re.findall("<font", st)
        centerList = re.findall("<center", st)
        bigList = re.findall("<big", st)
        strikeList = re.findall("<strike", st)
        ttList = re.findall("<tt", st)
        framesetList = re.findall("<frameset", st)
        frameList = re.findall("<frame", st)

        #Tag Counts
        divCount = len(divList)
        pCount = len(pList)
        h1Count = len(h1List)
        h2Count = len(h2List)
        htmlCount = len(htmlList)
        bodyCount = len(bodyList)
        headerCount = len(headerList)
        footerCount = len(footerList)
        fontCount = len(fontList)
        centerCount = len(centerList)
        bigCount = len(bigList)
        strikeCount = len(strikeList)
        ttCount = len(ttList)
        framesetCount = len(framesetList)
        frameCount = len(frameList)

        #Scoring
        score = divCount * self.divScore + \
                pCount * self.pScore + \
                h1Count * self.h1Score + \
                h2Count * self.h2Score + \
                htmlCount * self.htmlScore + \
                bodyCount * self.bodyScore + \
                headerCount * self.headerScore + \
                footerCount * self.footerScore + \
                fontCount * self.fontScore + \
                centerCount * self.centerScore + \
                bigCount * self.bigScore + \
                strikeCount * self.strikeScore + \
                ttCount * self.ttScore + \
                framesetCount * self.framesetScore + \
                frameCount * self.frameScore

        return(score)
    def getFileId(self, filename):
        nameID = re.search("[^_]*", filename).group(0)
        if (re.search("\d+[^.]*", filename) != None):
            originalDateString = re.search("\d+[^.]*", filename).group(0)
            if (re.search("\d{4}_\d{2}_\d{2}", originalDateString) != None):
                originalDate = datetime.datetime.strptime(originalDateString, "%Y_%m_%d").date()
                print(originalDate)
        #print(originalDate)
        return(nameID)

    def addScore(self, filename):
        db = sqlite3.connect("../schema/markup_db.sqlite")
        score = calculateScore(self, filename)
        nameID = getFileId(self, filename)
        

def createDatabaseTables():
    db = sqlite3.connect("../schema/markup_db.sqlite")
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS master(id INTEGER PRIMARY KEY, key_name TEXT, 
            score INTEGER, original_date TEXT, run_date TEXT)
        ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recent(key_name TEXT PRIMARY KEY, score INTEGER)
        ''')
    db.commit()




sc = Scorer();
sc.getFileId("bob_2013_02_10.html")
#sc.getFileId("example.html")


#| TagName | Score Modifier | TagName | Score Modifier |
#| ------- | :------------: | ------- | -------------- |
#| div     | 3              | font    | -1             |
#| p       | 1              | center  | -2             |
#| h1      | 3              | big     | -2             |
#| h2      | 2              | strike  | -1             |
#| html    | 5              | tt      | -2             |
#| body    | 5              | frameset| -5             |
#| header  | 10             | frame   | -5             |
#| footer  | 10             |