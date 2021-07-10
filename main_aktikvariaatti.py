# -*- coding: utf-8 -*-
"""
@author: Tomi Räsänen
"""

""" 
    Get bookprices from web and do price table.
        Pages to grab:
            - https://www.antikvaari.fi/
            - https://www.antikvariaatti.net/
            
        
"""


from selenium import webdriver
from get_books_antifi import got_book_antifi
import PySimpleGUI as sg
from webdriver_manager.chrome import ChromeDriverManager


# Path for chrome drivers
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(ChromeDriverManager().install())

# All data
last_artic_all = {"antikvariaatti.fi": {},
                  "antikvariaatti.net": {}}

# Eri laatuluokat
# luokat = ["K1", "K2-" ,"K2" ,"K2+", "K3-", "K3", "K3+", "K4-", "K4", "K5-", "K5"]

seller_store = {"Antikvaari Helsingius/Paikalliset palvelut ry/Nurm":"Nurmijärvi",
               "Antikvaarinen kirjakauppa Aleksis K.":"Lahti",
               "Antikvariaatti Punaparta":"Luumäki",
               "Arkadia International Bookshop":"Helsinki",
               "Finlandia Kirja":"Netti",
               "Ilkan kirja ay":"Netti",
               "Kiannan Aitta":"Suomussalmi",
               "Kirjamari Oy":"Netti",
               "Kirjavaari":"Järvenpää",
               "Kirstin Kirjahuone":"Netti?",
               "Laatu Torikirjat":"Netti",
               "OllinOnni":"Kotka",
               "Pispalan kirjastoyhdistys ry":"Tampere",
               "Saimaan Antikvariaatti":"Savonlinna",
               "Salpakirja Oy":"Hamina",
               "Sataman Tarmo":"Kuopio",
               "Wanhat Unelmat Gamla Drömmar Old Dreams":"Vääksy",
               "Antikvaarinen kirjakauppa T. Joutsen":"Tuusula",
               "Divari & Antikvariaatti Kummisetä":"Helsinki",
               "Antikvaarinen Kirjakauppa Johannes":"Helsinki",
               "Vilikka Oy":"Keuruu",
               "Cityn Kirja":"Rovaniemi",
               "Tomin antikvariaatti": "Pori",
               "Päijänne Antikvariaatti Oy":"Jyväskylä",
               "Kirjavehka":"Netti",
               "Biokustannus Oy":"Helsinki",
               "Antikvariaatti Pufendorf":"Helsinki",
               "Kustannus Apis":"Helsinki",
               "Antikvaarinen Kirjakauppa Kvariaatti":"Turku",
               "Kirja-Tiina":"Keuruu",
               "Antikvariaatti Taide ja kirja":"Netti",
               "Antikvariaatti Bookkolo":"Netti",
               "Antikvaari Kirja- ja Lehtilinna / Raimo Kreivi":"Kuopio",
               "Antikvariaatti Lukuhetki":"Jyväskylä",
               "Vesan Kirja":"Netti?",
               "Vantaan Antikvariaatti Oy":"Netti",
               "Vaisaaren kirja":"Raisio",
               "AntiWaari Ay":"Netti",
               "Helsingin Antikvariaatti":"Netti",
               "Brahen Antikvariaatti":"Turku",
               "Finn-Scholar - Tietokirjoja":"Netti",
               "Antikvaarinen Kirjakauppa Tessi":"Espoo",
               "Kirja-Kissa Oy":"Raisio",
               "Booksbymuni":"Rovaniemi",
               "Kuvaklassikko Oy": "Espoo"}

met_area = ["Helsinki", "Vantaa", "Tuusula", "Järvenpää", "Vihti", "Kirkkonummi", "Nurmijärvi",
            "Sipoo", "Kerava", "Espoo", "Kauniainen", "Mäntsälä", "Hyvinkää"]

# One column program
columnn = [
    [
        sg.Text("Author:"),
        sg.In(size=(25, 1), enable_events=True, key="-TEKIJA-"),
    ],
    [
        sg.Text("Book's name:"),
        sg.In(size=(25, 1), enable_events=True, key="-NAME-"),

    ],
    [
        sg.Checkbox('Only the metropolitan area', default=False, key="-CHECK-"),
        sg.Button("OK"),
    ],
    [
         sg.Button("QUIT")
    ]
]

# layout
window = sg.Window("Prices", columnn)


def calculate_and_datamani(webpage):
    text = ""
    text += "Prices by quality in the antique store {}: \n \n".format(webpage)
    
    # New dict using a city name as a key.
    city_and_book_dict = {}
    
    city = ""
    amount = 0;
    
    
    
    for store in last_artic_all[webpage]:
        
        if store in seller_store:
            city = seller_store[store]
        else:
            city = "Unknown"
        
        
        # Every book from the store. Name of the store is also appended to that list.
        for book in last_artic_all[webpage][store]:
            
            book.append(store)
            
            if city in city_and_book_dict:               
                city_and_book_dict[city].append(book)
            else:
                city_and_book_dict[city] = [book]
    
    for current_city in city_and_book_dict:
        
        # If only metropolitan area checked
        if values["-CHECK-"]:
            if current_city in met_area:
                text += "--------------------------------- {} ---------------------------------".format(current_city)
                text += "\n"
                for book in city_and_book_dict[current_city]:
                    for qualities in book:
                        text += qualities
                        text += "   |  "
                    text += "\n"
                    amount += 1
                text += "\n"

            else:
                continue
        
        # Kaikki
        else:
            text += "--------------------------------- {} ---------------------------------".format(current_city)
            text += "\n"
            for book in city_and_book_dict[current_city]:
                for qualities in book:
                    text += qualities
                    text += "   |  "
                text += "\n"
                amount += 1
            text += "\n"
    text += "Total number found = {}".format(amount)

    return text
            
            
# Event loop
while True:
    
    event, values = window.read()
    
    if event == "QUIT" or event == sg.WIN_CLOSED:
        break
    
    if event == "OK":
        tekija = values["-TEKIJA-"]
        name = values["-NAME-"]
        if name == "":
            continue
        else:
            
            antika_books = got_book_antifi(driver, last_artic_all["antikvariaatti.fi"], tekija, name)
            
            
            last_artic_all["antikvariaatti.fi"] = antika_books
            
            # Make the outlook of tha page using data from goot_book_antifi.
            tekstii = calculate_and_datamani("antikvariaatti.fi")
            sg.Popup(tekstii, title="Kirjat", line_width=200, grab_anywhere=True, location=(50,50))
            

            #antinet_books = got_book_antinet(driver, last_artic_all["antikvariaatti.net"], tekija, name)
            #last_artic_all["antikvariaatti.net"] = antinet_books
            #calculate_and_datamani("antikvariaatti.net")

            
window.close()


