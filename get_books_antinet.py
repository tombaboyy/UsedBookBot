# -*- coding: utf-8 -*-
"""
@author: Tomi Räsänen


################################
#                              #
# THIS FILE ISN'T READY YET!!' #
#                              #
################################

"""

from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def got_book_antinet(driver, last_artic_all, tekija, name):
    driver.get("https://www.antikvariaatti.net/")
    books = {}
    try:
        hakusana = "{} {}".format(tekija, name)
        book_haku = driver.find_element_by_xpath("//*[@id='qsearch']")
        book_haku.send_keys(hakusana)
        button_hae = driver.find_element_by_xpath("//*[@id='searchbutton']")
        button_hae.click()
        
        try:
            tuoreimmatMain = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID,"1")))
            how_many_in_page = tuoreimmatMain.find_element_by_xpath("//*[@id='resultcount']").text

            sivujen_maara = how_many_in_page
            
            books_in_page = tuoreimmatMain.find_elements_by_xpath("//*[@id='datacontainer']")[0].text
            print(books_in_page)
            
            
        except Exception as e: 
            print(e)
            driver.quit()
        
        """
        try:                
        
            tuoreimmatMain = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//*[@id='__next']/div/div[2]/div[3]/div[3]/ul")))
            how_many_pages = tuoreimmatMain.find_element_by_xpath("//*[@id='__next']/div/div[2]/div[3]/div[3]/p").text      
            sivujen_maara = how_many_pages.split("/")[1].strip()[:-1]
            
            for i in range(int(sivujen_maara)):

                books_in_page = tuoreimmatMain.find_elements_by_xpath("//*[@id='__next']/div/div[2]/div[3]/div[3]/ul")[0].text

                book_list = books_in_page.split("\n");
                spl_hinta = [s for s in book_list if "Hinta" in s]
                spl_myyja = [s for s in book_list if "Myyjä" in s]
                
                spl_kunto_ja_vuosi_kansi = [s for s in book_list if "Kunto" in s]
                
                lista_kirjoille = []
                
                # Tässä eri ominaisuuksia
                for maara in range(len(spl_hinta)):

                    lista_kirjoille.append(spl_hinta[maara].split(":")[1].strip())
                    
                    sivumaara = [s for s in spl_kunto_ja_vuosi_kansi[maara].split(",") if "Sivumäärä" in s]
                    if sivumaara != []:                        
                        lista_kirjoille.append(sivumaara[0].split(":")[1].strip())
                        
                    painovuosi = [s for s in spl_kunto_ja_vuosi_kansi[maara].split(",") if "Painovuosi" in s]
                    if painovuosi != []:
                        lista_kirjoille.append(painovuosi[0].split(":")[1].strip())
                    
                    kunto = [s for s in spl_kunto_ja_vuosi_kansi[maara].split(",") if "Kunto" in s]
                    if kunto != []:
                        lista_kirjoille.append(kunto[0].split(":")[1].strip())
                    
                    sidottu = [s for s in spl_kunto_ja_vuosi_kansi[maara].split(",") if "Sidottu" in s]
                    if sidottu != []:
                        lista_kirjoille.append(sidottu[0])
                    
                    if spl_myyja[maara] in books:
                        books[spl_myyja[maara]].append(lista_kirjoille)
                    else:
                        books[spl_myyja[maara]] = [lista_kirjoille]
                        
                    lista_kirjoille = []
                    
                
                
                if i == int(sivujen_maara)-1:
                    continue
                
                else:
                    if int(sivujen_maara) >= 9:                       
                        clicking = tuoreimmatMain.find_element_by_xpath("//*[@id='__next']/div/div[2]/div[3]/div[3]/div/nav/ul/li[11]/button")
                        clicking.click()
                    else:
                        clicking = tuoreimmatMain.find_element_by_xpath("//*[@id='__next']/div/div[2]/div[3]/div[3]/div/nav/ul/li[{}]/button".format(int(sivujen_maara)+2))
                        clicking.click()
                    tuoreimmatMain = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//*[@id='__next']/div/div[2]/div[3]/div[3]/ul")))
            
        except Exception as e: 
            print(e)
            driver.quit()
        return books
        """
    except Exception as e: 
        print(e)
        driver.quit()
        
