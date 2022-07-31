import glob, os, csv
# sys, time, ctypes, math, json, winsound
import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

# from random import seed, randint

HOME_PATH = os.getenv("HOMEDRIVE") + os.getenv("HOMEPATH")
DOWNLOADS_PATH = HOME_PATH + r"\Downloads"
OPTIONS_PATH = (
    HOME_PATH + r"\AppData\Local\Frontier Developments\Elite Dangerous\Options"
)
JOURNAL_PATH = HOME_PATH + r"\Saved Games\Frontier Developments\Elite Dangerous"
STATUS_FILE = HOME_PATH + JOURNAL_PATH + r"\Status.json"
DISPLAY_SETTINGS_FILE = OPTIONS_PATH + r"\Graphics\DisplaySettings.xml"
EDO_BINDS_FILE = OPTIONS_PATH + r"\Bindings\Custom.4.0.binds"
EDH_BINDS_FILE = OPTIONS_PATH + r"\Bindings\Custom.3.0.binds"
lista_systemow = ""


def getDS(parametr):
    """
    Zwraca ustawienia wuświetlania ED.
    FullScreen = 2 - zgodny z nakładkami (borderless)
    FullScreen = 0 - window
    Dostępne parametry: ScreenWidth, ScreenHeight, VSync, FullScreen,
    PresentInterval, Adapter, Monitor, DX11_RefreshRateNumerator,
    DX11_RefreshRateDenominator, LimitFrameRate, MaxFramesPerSecond
    @params:
        parametr    - Required  : nazwa parametru (Str)
    """
    tree = ET.parse(DISPLAY_SETTINGS_FILE)
    root = tree.getroot()
    for child in root:
        if child.tag == parametr:
            return child.text


def getKEYS():
    """
    Zwraca ustawienia klawiszy do sterowania UI.
    Zwracany jest słownik.
    Wybiera zestaw Secondary dla UI a dla reszty
    wybiera niepusty ale wpierw Primary.
    """
    tree = ET.parse(EDO_BINDS_FILE)
    root = tree.getroot()
    myKeys = (
        "UI_Up",
        "UI_Down",
        "UI_Left",
        "UI_Right",
        "UI_Select",
        "CyclePreviousPanel",
        "CycleNextPanel",
        "FocusRightPanel",
    )
    myKeysS = ("UI_Up", "UI_Down", "UI_Left", "UI_Right")
    setKeys = {}
    for child in root:
        if child.tag in myKeys:
            ## print("Primary:", child.tag, child[0].attrib['Key'])
            ## print("Secondary:", child.tag, child[1].attrib['Key'])
            if child.tag in myKeysS:
                setKeys[child.tag] = child[1].attrib["Key"]
            else:
                if child[0].attrib["Key"] == "":
                    setKeys[child.tag] = child[1].attrib["Key"]
                else:
                    setKeys[child.tag] = child[0].attrib["Key"]
    return setKeys


def latest_csv():
    """
    Wyszukuje ostatni plik CSV w forlderze Downloads.
    """
    list_of_files = glob.glob(DOWNLOADS_PATH + r"\*.csv")
    try:
        latest_csv = max(list_of_files, key=os.path.getmtime)
    except:
        latest_csv = ""
    return latest_csv


def read_csv():
    """
    Wczytuje CSV zgodny z spansh.co.uk/fleet-carrier
    i zwraca listę. Uwaga - zwracana lista zawiera nagłówki
    w pozycji [0].
    """
    lista_systemow = []
    if latest_csv() != "":
        with open(latest_csv(), "r") as file:
            reader = csv.reader(file)
            for row in reader:
                lista_systemow.append(row)
        file.close()
    return lista_systemow


def get_curr_sys():
    """
    Zwraca aktualmy system.
    Główna pętla przeszukuje pliki .log od najnowszego do najstarszego
    w poszukiwaniu klucza "StarSystem".
    """
    list_of_files = glob.glob(JOURNAL_PATH + r"\Journal.*.log")
    list_of_files.sort(key=os.path.getmtime, reverse=True)
    currSys = ""
    i = 0
    test = 0
    while test == 0:
        latestJournal = open(list_of_files[i], "r")  # ostatni dla i = 0
        for line in latestJournal:
            if line.count("StarSystem") > 0:
                currSys = line
                test = test + 1
        if test > 0:
            currSys = currSys.split('"StarSystem":"')[1].split('"')[
                0
            ]  # wycina nazwę systemu z ostatniego wystąpienia klucza
        else:
            i = i + 1
    latestJournal.close()
    return currSys


def next_jump(lista_systemow):
    """
    Zwraca następny system z listy.
    Warunek - aktualny system musi być jednym z tych na liście.
    @params:
        lista_systemow - Required  : lista systemów (List)
    """
    nextSys = None
    if len(lista_systemow) > 0:
        currSys = get_curr_sys()
        i = 1
        while i < len(lista_systemow):
            if currSys == lista_systemow[i][0]:
                nextSys = lista_systemow[i + 1][0]
                break
            i = i + 1
    return nextSys


def jumps_left(lista_systemow):
    """
    Zwraca ilość pozostałych skoków.
    @params:
        lista_systemow - Required  : lista systemów (List)
    """
    jumps = None
    if len(lista_systemow) > 0:
        currSys = get_curr_sys()
        i = 1
        while i < len(lista_systemow):
            if currSys == lista_systemow[i][0]:
                break
            i = i + 1
    jumps = len(lista_systemow) - i - 1
    return jumps


def print_sys_list(lista_systemow):
    """
    Wyświetla listę wczytanych z pliku CSV
    systemów z podsumowaniem.
    @params:
        lista_systemow - Required  : lista systemów (List)
    """
    i = 1  # na i = 0 znajdują się nagłowki
    while i < len(lista_systemow):
        print(i, lista_systemow[i][0])
        i = i + 1
    print("Razem", len(lista_systemow) - 1, "systemów.")


def print_const():
    """
    Wyświetla listę stałych i kilka innych drobiazgów.
    Przeznaczone do testowania.
    """
    print("HOME_PATH:", HOME_PATH)
    print("DOWNLOADS_PATH:", DOWNLOADS_PATH)
    print("OPTIONS_PATH:", OPTIONS_PATH)
    print("JOURNAL_PATH:", JOURNAL_PATH)
    print("STATUS_FILE:", STATUS_FILE)
    print("DISPLAY_SETTINGS_FILE:", DISPLAY_SETTINGS_FILE)
    print("EDO_BINDS_FILE:", EDO_BINDS_FILE)
    print("EDH_BINDS_FILE:", EDH_BINDS_FILE)
    print("FullScreen:", getDS("FullScreen"))
    print("Lista:", latest_csv())
    print_sys_list(lista_systemow)


def print_next_sys():
    """
    Wyświetla informację o następnym skoku.
    """
    lista_systemow = read_csv()
    print("Aktualny system:", get_curr_sys())
    print("Następny skok do:", next_jump(lista_systemow))
    print("Pozostało skoków:", jumps_left(lista_systemow))


#################################
#################################


def select_file():
    filename = fd.askopenfilename(
        title="Załaduj listę pobraną ze strony spansh.co.uk",
        initialdir=glob.glob(DOWNLOADS_PATH),
        filetypes=[("CSV files", "*.csv")],
    )
    showinfo(title="Selected File", message=filename)

    f = fd.askopenfile(filetypes=[("CSV files", "*.csv")])
    text.insert("1.0", f.readlines())
    return filename


def print_tk_txt(txt):
    text.insert("1.0", txt + "\n")


def test():
    print_tk_txt("HOME_PATH: " + HOME_PATH)
    print_tk_txt("DOWNLOADS_PATH: " + DOWNLOADS_PATH)
    print_tk_txt("OPTIONS_PATH: " + OPTIONS_PATH)
    print_tk_txt("JOURNAL_PATH: " + JOURNAL_PATH)
    print_tk_txt("STATUS_FILE: " + STATUS_FILE)
    print_tk_txt("DISPLAY_SETTINGS_FILE: " + DISPLAY_SETTINGS_FILE)
    print_tk_txt("EDO_BINDS_FILE: " + EDO_BINDS_FILE)
    print_tk_txt("EDH_BINDS_FILE: " + EDH_BINDS_FILE)
    print_tk_txt("Aktualny system: " + get_curr_sys())
    print_tk_txt("Lista: " + latest_csv())
    print_tk_txt("FullScreen: " + getDS("FullScreen"))
    lista_systemow = read_csv()
    i = 1  # na i = 0 znajdują się nagłowki
    while i < len(lista_systemow):
        print_tk_txt(lista_systemow[i][0])
        i = i + 1

if __name__ == '__main__':
    # create the root window
    root = tk.Tk()
    root.title("Next Jump")
    root.resizable(True, True)
    # root.eval("tk::PlaceWindow . center")
    x = root.winfo_screenwidth() // 2 - 425
    y = int(root.winfo_screenheight() * 0.1)
    print(x, y)
    root.geometry("850x650+" + str(x) + "+" + str(y))

    ##frame1 = Frame(root)
    ##frame1.pack(expand=True, fill='both', ipadx=10, ipady=10)
    ##
    ##frame2 = Frame(root)
    ##frame2.pack(expand=False, ipadx=10, ipady=10, side='bottom')

    # Text editor
    text = tk.Text(root, height=12)
    text.pack(expand=True, fill="both", ipadx=10, ipady=10)

    # Buttons
    open_button = ttk.Button(root, text="Załaduj listę", command=select_file)
    open_button.pack(expand=False, ipadx=10, ipady=10, side="bottom", pady=10)

    open_button2 = ttk.Button(root, text="Test", command=test)
    open_button2.pack(expand=False, ipadx=10, ipady=10, side="bottom", pady=10)

    # odpal GUI
    root.mainloop()

    print_next_sys()
    exit()
