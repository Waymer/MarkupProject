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

    #This function calculates the score for a given html file
    def calculateScore(self, filename):
        path = "../data/"
        fo = open(path + filename)
        st = fo.read().lower()

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

    #This function returns key name (unique id) and date from a given filename
    def getFileId(self, filename):
        nameID = re.search("[^_]*", filename).group(0)
        originalDate = None
        if (re.search("\d+[^.]*", filename) != None):
            originalDateString = re.search("\d+[^.]*", filename).group(0)
            if (re.search("\d{4}_\d{2}_\d{2}", originalDateString) != None):
                originalDate = datetime.datetime.strptime(originalDateString, "%Y_%m_%d").date()
        return([nameID, originalDate])

    #This function calculates and adds score information to the db for a given html file
    def addScore(self, filename):
        db = sqlite3.connect("../schema/markup_db.sqlite")
        cursor = db.cursor()
        score = self.calculateScore(filename)
        IDs = self.getFileId(filename)
        nameID = IDs[0]
        originalDate = IDs[1]
        runDate = datetime.datetime.now()
        cursor.execute('''
            INSERT INTO master(key_name, score, original_date, run_date)
            VALUES(?,?,?,?)
        ''', (nameID, score, originalDate, runDate))
        cursor.execute('''
            INSERT OR REPLACE INTO recent (key_name, score)
            VALUES(?,?)
        ''', (nameID, score))
        db.commit()

    #This function gives a list of scores associated with a key name (unique id)
    def getScoresById(self, nameID):
        db = sqlite3.connect("../schema/markup_db.sqlite")
        db.text_factory = str
        cursor = db.cursor()
        cursor.execute("SELECT score FROM master WHERE key_name = \'" + nameID + "'")
        raw = cursor.fetchall()
        scores = []
        for record in raw:
            scores.append(record[0])
        return(scores)

    #This function returns the latest highest score and its associated key name (unique id)
    def getHighestScore(self):
        db = sqlite3.connect("../schema/markup_db.sqlite")
        db.text_factory = str
        cursor = db.cursor()
        cursor.execute('''
            SELECT key_name, score FROM recent ORDER BY score DESC LIMIT 1
            ''')
        info = cursor.fetchone()
        return(info)

    #This function returns the latest lowest score and its associated key name (unique id)
    def getLowestScore(self):
        db = sqlite3.connect("../schema/markup_db.sqlite")
        db.text_factory = str
        cursor = db.cursor()
        cursor.execute('''
            SELECT key_name, score FROM recent ORDER BY score ASC LIMIT 1
            ''')
        info = cursor.fetchone()
        return(info)

    #This function returns a list of scores and associated id for additions that were run between the given dates
    def getScoresForDates(self, start, end):
        db = sqlite3.connect("../schema/markup_db.sqlite")
        db.text_factory = str
        cursor = db.cursor()
        cursor.execute("SELECT key_name, score FROM master WHERE date(run_date) BETWEEN \'" + start + "\' AND \'" + end + "'")
        raw = cursor.fetchall()
        scores = []
        for record in raw:
            scores.append([record[0], record[1]])
        return(scores)

    #This function returns a list of average scores and associated key names (unique id)
    def getAvgScores(self):
        db = sqlite3.connect("../schema/markup_db.sqlite")
        db.text_factory = str
        cursor = db.cursor()
        cursor.execute('''
            SELECT key_name, AVG(score) FROM master GROUP BY key_name
            ''')
        raw = cursor.fetchall()
        scores = []
        for record in raw:
            scores.append([record[0], record[1]])
        return(scores)

#This function creates the initial database and tables
def createDatabaseTables():
    db = sqlite3.connect("../schema/markup_db.sqlite")
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS master(id INTEGER PRIMARY KEY AUTOINCREMENT, 
            key_name TEXT, score INTEGER, original_date TEXT, run_date TEXT)
        ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recent(key_name TEXT PRIMARY KEY, score INTEGER)
        ''')
    db.commit()

createDatabaseTables()

sc = Scorer();

sc.addScore("bob_2013_02_10.html")
sc.addScore("bob_2013_02_15.html")
sc.addScore("bob_2013_03_01.html")
sc.addScore("cari_2013_02_15.html")
sc.addScore("cari_2013_02_16.html")
sc.addScore("cari_2013_03_05.html")
sc.addScore("john_2013_01_05.html")
sc.addScore("john_2013_02_13.html")
sc.addScore("john_2013_03_13.html")

print(sc.getScoresById('bob'))
print(sc.getScoresById('cari'))
print(sc.getScoresById('john'))
print(sc.getLowestScore())
print(sc.getHighestScore())
print(sc.getScoresForDates('2017-10-27','2017-10-30'))
print(sc.getAvgScores())
