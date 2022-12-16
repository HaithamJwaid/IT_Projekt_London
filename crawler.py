# Import necessary modules

#Grund Problem bei allem, wie viel darf vorgegeben werden?
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from colorama import init, Fore, Style

#für die Farben
init()
INJECTION_STRING = "INJECTIONPOSIBLE"

"""FÜhrt injections versuche auf einem input feld aus
BRUTFORCE für die anzahl der spalten"""
def runInjection():
    checkString = "1 UNION SELECT ".INJECTION_STRING

"""Scheckt anhand des resultats ob eine INjection erfolgreich war"""
def checkIfInjectionIsSuccessful(pageContent):
    if(pageContent.find(INJECTION_STRING) != -1):
        print(Fore.RED + "Injection möglich !" + Style.RESET_ALL)
    else:
        print(Fore.GREEN + "KEINE Injection möglich!" + Style.RESET_ALL)

""" Wenn injections möglich sind können weitere Daten herausgefunden werden, Version, schema etc"""
def informationGathering():
    pass


url = "http://localhost:8000/Views/indexView.php"
driver = webdriver.Chrome()
driver.get(url)
time.sleep(5)

input_field = driver.find_element(By.ID,"id")
input_field.send_keys("1 UNION SELECT " + '"' + INJECTION_STRING + '"')

input_field.send_keys(Keys.RETURN)
checkIfInjectionIsSuccessful(driver.page_source)

time.sleep(5)
