# -*- coding: utf-8 -*-
"""
@author: Tomi Räsänen
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def got_book_antifi(driver, last_artic_all, author, name):
    driver.get("https://haku.antikvaari.fi/hakukone")
    books = {}
    try:
        
        """ Input the name of the author of the book and the name of the book 
        to search section"""
        name_book = driver.find_element_by_id("name")
        writer_book = driver.find_element_by_id("writer")
        name_book.send_keys(name)
        writer_book.send_keys(author)
        button_search = driver.find_element_by_xpath("//*[@id='__next']/div/div[2]/div/div[2]/button[1]/span[1]")
        
        # Click the search button
        button_search.click()
        
        
        try:                
        
            # Wait search results to load
            refreshed_page = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//*\
                    [@id='__next']/div/div[2]/div/div[3]/div[2]/ul")))
            
            # Number of pages
            how_many_pages = refreshed_page.find_element_by_xpath("//*\
                            [@id='__next']/div/div[2]/div/div[3]/div[2]/div[2]/nav/ul/li[3]/button").text

            
            for i in range(int(how_many_pages)):
                
                books_in_page = refreshed_page.find_elements_by_xpath("//*\
                            [@id='__next']/div/div[2]/div/div[3]/div[2]/ul")[0].text
                            

                book_list = books_in_page.split("Signeerattu")
                
                # Go through every book of the current page. Each book is 
                # one element of the "book_list" list.
                for book in book_list:
                    
                    no_enter_book = book.split("\n")
                    number_of_elements = len(no_enter_book)

                    store = ""
                    price = ""
                    quality = ""
                    number_of_pages = ""
                    year_of_printing = ""                    

                    for index in range(number_of_elements):
                        
                        # Price
                        if "Hinta:" in no_enter_book[index]:
                            price = no_enter_book[index].split(":")[1].strip()
                            
                        # Store
                        if "Kauppias:" in no_enter_book[index]:
                            store = no_enter_book[index].split(":")[1].strip()
                            
                        # Quality 
                        if "Kunto:" in no_enter_book[index]:
                            quality = no_enter_book[index].split(":")[1].strip()
                        
                        # Number of pages
                        if "Sivumäärä" in no_enter_book[index]:
                            number_of_pages = no_enter_book[index+1].strip()
                        
                        # Year of printing
                        if "Painovuosi" in no_enter_book[index]:
                            year_of_printing = no_enter_book[index+1].strip()
                            
                    # Just check that the book element wasn't empty
                    if store == "":
                        continue                       
                    
                    else:
                        one_book_list = [price, quality, number_of_pages, year_of_printing]
                        if store in books:
                            books[store].append(one_book_list)
                            
                        else:
                            books[store] = [one_book_list]
                        
                
                # This takes care of changing page if not in the last page
                if i == int(how_many_pages)-1:
                    continue
                
                else:
                    if int(how_many_pages) >= 9:       
                        
                        clicking = refreshed_page.find_element_by_xpath("//*\
                                    [@id='__next']/div/div[2]/div/div[3]/div[2]/div[2]/nav\
                                    /ul/li[11]/button")
                                    
                        clicking.click()
                        
                    else:
                        
                        clicking = refreshed_page.find_element_by_xpath("//*\
                                    [@id='__next']/div/div[2]/div/div[3]/div[2]/div[2]/nav\
                                    /ul/li[{}]/button".format(int(how_many_pages)+2))
                                    
                        clicking.click()
                        
                    refreshed_page = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//*\
                                   [@id='__next']/div/div[2]/div/div[3]/div[2]/ul")))
          
        except Exception as e: 
            
            print(e)
            driver.quit()
            
        return books
        
    except Exception as e: 
        
        print(e)
        driver.quit()
        
