from time import sleep
import glob
import os
import getpass
import keyboard as kb
import threading
import pyautogui
import sys

##import pydirectinput
##import requests
##import argparse,csv
##import json
##from playsound import playsound
##import tkinter as tk
##import ctypes

sysFile = open("lista_nawigacyjna.txt","r")

def getCurrSys():
    list_of_files = glob.glob(f"C:\\Users\\{getpass.getuser()}\\Saved Games\\Frontier Developments\\Elite Dangerous\\Journal.*")
    latestJournal = open(max(list_of_files,key=os.path.getmtime),'r')
    currSys = ""
    for line in latestJournal:
        if line.count('StarSystem')>0:
            currSys = line
    currSys = currSys.split('"StarSystem":"')[1].split('"')[0]
    return currSys

def locate(image):
    #print("locate_and_click", image)
    set1 = pyautogui.locateOnScreen(image,confidence=0.75)
    if set1 == None:
        print("X", end='')
        #print("\nNie można zlokalizować przycisku", image)
        pass
    else:
        print("O", end='')
        x = set1.left+set1.width//2
        y = set1.top+set1.height//2
        pyautogui.moveTo(x,y,1)
        pyautogui.click()
    
def locate_and_click(image):
    #print("locate_and_click", image)
    set1 = pyautogui.locateOnScreen(image,confidence=0.75)
    if set1 == None:
        print("X", end='')
        #print("\nNie można zlokalizować przycisku", image)
    else:
        print("O", end='')
        x = set1.left+set1.width//2
        y = set1.top+set1.height//2
        pyautogui.moveTo(x,y,1)
        pyautogui.click()
    
def press_and_release(key, press_wait, release_wait):
    #print("press_and_release:", key)
    print("#", end='')
    kb.press(key)
    sleep(press_wait)
    kb.release(key)
    sleep(release_wait)

def oneJump(sysName):
# aktywacja i przejście do CARRIER SERVICES
    press_and_release('1', 0.2, 1)
    press_and_release('1', 0.2, 1)
    press_and_release('space', 0.2, 5)
    press_and_release('s', 0.2, 0.5)
    press_and_release('s', 0.2, 0.5)

# tankowanie (DONATE)
    press_and_release('space', 0.2, 1)
    press_and_release('space', 0.2, 1)
    press_and_release('w', 0.2, 0.5)
    press_and_release('space', 0.2, 1)
    press_and_release('s', 0.2, 0.5)
    press_and_release('s', 0.2, 0.5)
    press_and_release('space', 0.2, 1)

# tankowanie (przeładunek)
    press_and_release('4', 0.2, 1)
    press_and_release('d', 0.2, 0.5)
    press_and_release('w', 0.2, 0.5)
    press_and_release('d', 0.2, 0.5)
    press_and_release('space', 0.2, 1)
    #towary = 2 # pozycja TRITIUM w SHIP CARGO (licząc od dołu)
    #for i in range(towary):
    #    press_and_release('w', 0.2, 0.5)
    press_and_release('w', 5, 0.5) # lepsze rozwiązanie ale 5x dłużej się wykonuje
    press_and_release('a', 8, 0.5)
    press_and_release('space', 0.2, 1)
    press_and_release('space', 0.2, 1)
    press_and_release('4', 0.2, 1)
    
# FC MANAGMENT -> GALAXY MAP
    press_and_release('d', 0.2, 0.5)
    press_and_release('d', 0.2, 0.5)
    press_and_release('space', 0.2, 2)
    press_and_release('s', 0.2, 1)
    press_and_release('space', 0.2, 1)
    press_and_release('space', 0.2, 3)
    
# wprowadzenie docelowego systemu i zatwierdzenie trasy
#
# uwaga to miejsce w sekwencji jest problematyczne;
# mapa ED czasami zachowuje się nieprzewidywalnie;
#
    locate_and_click('lupka.png')
    press_and_release('space', 0.3, 2)
    kb.write(sysName)
    locate_and_click('szukaj.png')
    press_and_release('enter', 0.3, 2) 
    sleep(5)
    locate_and_click('przycisk.png')
    press_and_release('space', 0.3, 2)

# przerwa
    print(" PRZERWA 20 MINUT", end='')
    sleep(1205)
    print(" KONIEC SKOKU")
    pass

print("Colonie Express - autopilot do Elite Dangerous: Odyssey\n")
print("Lista startowa:")
print("(1) - Dla wygody ustaw ED na wyświetlanie w oknie\n      i przesuń je tak abyś widział tą konsole.")
print("(2) - Okno ED nie może wychodzić poza krawędź ekranu\n      i musi być na pierwszym planie.")
print("(3) - Prawy panel musi być ustawiony na zakładce\n      INVENTORY - SHIP CARGO.")
print("(4) - SHIP CARGO musi być napełnione do pełna\n      TRITIUM (minimum 132 tony).")
print("(5) - Lotniskowiec musi znajdować się\n      w dowolnym systemie z listy.")
print("(6) - Autopilot wykonuje skok do systemu następującego\n      po bieżącym systemie z listy.")
input("...nacisnij enter aby wystarować.")
      
currSys = getCurrSys()
print("\nAktualny system:", currSys)

nSys = 0
checkSys = 0
for line in sysFile.readlines():
    if (len(line) > 1): nSys = nSys + 1
    if (currSys == line[0:-1]): checkSys = checkSys + 1
if (checkSys == 0):
    print("Bieżący system nie znajduje się na liście nawigacyjnej!")
    print("Ustaw lotniskowiec w dowolnym systemie z listy nawigacyjnej!")
    sys.exit()
print("Lista nawigacyjna (liczba systemów):", nSys)

# ustawienie znacznika na następnym po bieżącym systemie z listy
startSys = 0
sysFile.seek(0)
for line in sysFile.readlines():
    startSys = startSys + 1
    line = line[0:-1]
    if (line == currSys): break

# główna pętla autopilota
zwloka = 10
print("\nMasz", zwloka, "sek. na wejście do okna ED!")
for i in "#" * zwloka:
    sleep(1)
    print(i, end='')
print(" START!")

print("\nAutopilot uruchomiony!")
cSys = 0
sysFile.seek(0)
for line in sysFile.readlines():
    line = line[0:-1]
    cSys = cSys + 1
    if (cSys > startSys):
        print('(', cSys, '/', nSys, ')', line)
        oneJump(line)

print("\n# KONEC #")
