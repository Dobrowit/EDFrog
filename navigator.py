import os
import sys
import glob
import getpass
import pyautogui
import pywinauto
import colorama as cr
import keyboard as kb
import edtools as ed
from time import sleep

os.system('cls')
cr.init()

ED_VER = "4.0.0.1302"

# Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Style: DIM, NORMAL, BRIGHT, RESET_ALL

def mkquit(str):
    print("\n" + cr.Fore.RED + str + cr.Style.RESET_ALL)
    input("...nacisnij enter aby zakończyć.")
    quit()

def getCurrSys():
    list_of_files = glob.glob(f"C:\\Users\\{getpass.getuser()}\\Saved Games\\Frontier Developments\\Elite Dangerous\\Journal.*")
    latestJournal = open(max(list_of_files,key=os.path.getmtime),'r')
    currSys = ""
    for line in latestJournal:
        if line.count('StarSystem')>0:
            currSys = line
    currSys = currSys.split('"StarSystem":"')[1].split('"')[0]
    latestJournal.close()
    return currSys

def get_ed_ver():
    list_of_files = glob.glob(f"C:\\Users\\{getpass.getuser()}\\Saved Games\\Frontier Developments\\Elite Dangerous\\Journal.*")
    latestJournal = open(max(list_of_files,key=os.path.getmtime),'r')
    ed_ver = ""
    for line in latestJournal:
        if line.count('gameversion')>0:
            ed_ver = line
    ed_ver = ed_ver.split('"gameversion":"')[1].split('"')[0]
    latestJournal.close()
    return ed_ver

def locate(image):
    sleep(1)
    set1 = pyautogui.locateOnScreen(image, confidence=0.8)
    if set1 == None:
        pass
        return False
    else:
        pass
        return True
    
def locate_and_click(image):
    sleep(1)
    set1 = pyautogui.locateOnScreen(image, confidence=0.8)
    if set1 == None:
        pass
    else:
        x = set1.left+set1.width//2
        y = set1.top+set1.height//2
        pyautogui.moveTo(x,y,1)
        pyautogui.click()
    
def press_and_release(key, release_wait=0.3, press_wait=0.2, rep=1):
    for i in range(rep):
        kb.press(key)
        sleep(press_wait)
        kb.release(key)
        sleep(release_wait)

def oneJump(sysName):
# aktywacja i przejście z kokpitu do CARRIER SERVICES
    press_and_release('space', 5)
    press_and_release('s')
    press_and_release('s')

# tankowanie (DONATE)
    press_and_release('space', 1)
    press_and_release('space', 1)
    press_and_release('w')
    press_and_release('space', 1)
    press_and_release('s')    
    press_and_release('s')
    press_and_release('space', 1)

# tankowanie (przeładunek; prawy panel)
    press_and_release('s')
    press_and_release('space', 1)
    press_and_release('4', 1)
    press_and_release('d')
    press_and_release('w')
    press_and_release('d')
    press_and_release('space', 1)
##    press_and_release('w', rep=1) # rep to pozycja TRITIUM w SHIP CARGO (licząc od dołu)
    press_and_release('w', 0.5, 5) # uniwersalne rozwiązanie ale dłużej się wykonuje
    press_and_release('a', 0.3, 8)
    press_and_release('space', 1)
    press_and_release('space', 1)
    press_and_release('4', 1)
    
# FC MANAGMENT -> GALAXY MAP
    press_and_release('space', 2)
    press_and_release('s')
    press_and_release('s')
    press_and_release('d')
    press_and_release('d')
    press_and_release('space', 4)
    press_and_release('s', 1)
    press_and_release('space', 1)
    press_and_release('space', 3)
    
# wprowadzenie docelowego systemu i zatwierdzenie trasy
    press_and_release('w', 2)
    press_and_release('space', 2)
    kb.write(sysName, delay=0.1)
    press_and_release('enter', 2)
    press_and_release('d', 2)
    press_and_release('space', 2)
    sleep(5)
    press_and_release('d', 2)
    press_and_release('space', 2)
    sleep(3)
    
    if locate("img/no_route_set.png"):
        mkquit("Nie udało się wyznaczyć celu: brak miejsca lub system zapełniony!")
    
# przerwa 15 minut plus margines
    sleep(900)
    while sysName != ed.get_curr_sys():
        sleep(15)
# cooldown
    sleep(200)



################################################################################################################################
################################################################################################################################
################################################################################################################################
################################################################################################################################

# sprawdza czy pobrano plik csv (z listą z https://www.spansh.co.uk)
if ed.latest_csv() != '':
    lista_systemow = ed.read_csv()
    f = open("lista_nawigacyjna.txt", "w")
    i = 1  # na i = 0 znajdują się nagłowki
    while i < len(lista_systemow):
        f.write(lista_systemow[i][0]+'\n')
        i = i + 1
    f.close()
else:
    if os.path.exists("lista_nawigacyjna.txt"):
        pass
    else:
        mkquit("Brak pliku lista_nawigacyjna.txt!")

sysFile = open("lista_nawigacyjna.txt","r")

print(cr.Back.BLUE, "ED FROG - autopilot do Elite Dangerous Odyssey", ED_VER, cr.Style.RESET_ALL)
if get_ed_ver() != ED_VER:
    print("")
    print(cr.Back.RED, "Aktualna wersja ED jest inna od obsługiwanej! ")
    print(" Autopilot może działać nieprawidłowo!", cr.Style.RESET_ALL)
print("\nTrasa jest czytana z pliku lista_nawigacyjna.txt, w którym należy kolejno w każdej linii zapisać nazwę systemu.")
print("Opcjonalnie można wygenerować trasę za pomocą " + cr.Fore.BLUE, end='')
print("https://www.spansh.co.uk/fleet-carrier/" + cr.Style.RESET_ALL + ".")
print("Trasę zapisać należy przy pomocy przycisku " + cr.Fore.BLUE + "Download as CSV" + cr.Style.RESET_ALL, end='')
print(" do domyślnego katalogu " + cr.Fore.BLUE + "Pobrane" + cr.Style.RESET_ALL + ".")
print("Przy uruchomieniu ED Frog przepisuje ostatni plik CSV do lista_nawigacyjna.txt.")
print("\nLista startowa:")
print("(1) Ustaw ED na wyświetlanie w oknie.")
print("(2) Okno ED nie może wychodzić poza krawędź ekranu i musi być na pierwszym planie.")
print("(3) Prawy panel musi być ustawiony na zakładce INVENTORY - SHIP CARGO.")
print("(4) SHIP CARGO musi być napełnione do pełna tylko TRITIUM (minimum 132 tony).")
print("(5) Lotniskowiec musi znajdować się w dowolnym systemie z listy.")
input("...nacisnij enter aby wystarować.")

if ed.getDS("FullScreen") != '0':
    mkquit("Ustaw ED na wyświetlanie w oknie!")

currSys = getCurrSys()
print("\nAktualny system:" + cr.Fore.YELLOW, currSys, cr.Style.RESET_ALL)

# zlicza systemy na liście i sprawdza prawidłową pozycję FC
nSys = 0 # liczba systemów na liście
checkSys = 0
for line in sysFile.readlines():
    if (len(line) > 1): nSys = nSys + 1
    if (currSys == line[0:-1]): checkSys = checkSys + 1
if (checkSys == 0):
    print("Bieżący system nie znajduje się na liście nawigacyjnej!")
    mkquit("Ustaw lotniskowiec w dowolnym systemie z listy nawigacyjnej!")

# szuka system końcowy
i = 0
sysFile.seek(0)
for line in sysFile.readlines():
    i = i +1
    if (i == nSys): lastSys = line
lastSys = lastSys[:-1]
if lastSys == currSys:
    mkquit(cr.Fore.CYAN + "Dotarłeś do celu!" + cr.Style.RESET_ALL)
print("System docelowy:"+ cr.Fore.YELLOW, lastSys, cr.Style.RESET_ALL)

# ustawienie znacznika na następnym po bieżącym systemie z listy
startSys = 0
sysFile.seek(0)
for line in sysFile.readlines():
    startSys = startSys + 1
    line = line[0:-1]
    if (line == currSys): break

app = pywinauto.Application(backend="uia")
try:
    app = app.connect(title_re=".*Elite - Dangerous (CLIENT)*.", visible_only=False)
except:
    mkquit("Elite Dangerous nie jest uruchomione!")

print("Autopilot uruchomiony!")
app.top_window().restore()

# sprawdzenie prawego panelu
press_and_release('1', 1)
press_and_release('4', 1)
if locate('img/cargo.png') == False:
    if locate('img/holo-me.png') == True:
        press_and_release('e', rep=4)
    else:
        mkquit("Ustaw prawy panel na zakładkę INVENTORY i ponownie uruchom autopilota!")
press_and_release('4', 0.2, 1)

cSys = 0
sysFile.seek(0)
for line in sysFile.readlines():
    line = line[0:-1]
    cSys = cSys + 1
    if (cSys > startSys):
        print('(', cSys, '/', nSys, ')', cr.Fore.YELLOW, line, cr.Style.RESET_ALL)
        app.top_window().restore()
        sleep(2)
        oneJump(line)

mkquit("# KONEC #")
