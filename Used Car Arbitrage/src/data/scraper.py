import os
import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def setup_driver():
    options = webdriver.ChromeOptions()
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def extract_car_data(card_soup):
    data_car = {}
    all_text = list(card_soup.stripped_strings)

    data_car['Title'] = "Missing Title"
    data_car['Price'] = "Missing Price"
    data_car['Kilometers'] = "Missing KM"
    data_car['Fuel_Type'] = "Missing Fuel"
    data_car['Transmission'] = "Missing Transmission"

    prices = [t for t in all_text if '₹' in t and '/m' not in t.lower() and 'emi' not in t.lower()]
    if prices:
        data_car['Price'] = prices[-1]

   
    for text in all_text:
        text_lower = text.lower()
        if 'km' in text_lower and any(char.isdigit() for char in text_lower):
            data_car['Kilometers'] = text
        elif text_lower in ['petrol', 'diesel', 'cng', 'electric', 'hybrid']:
            data_car['Fuel_Type'] = text
        elif text_lower in ['manual', 'automatic']:
            data_car['Transmission'] = text

    for text in all_text:
        if re.match(r'^(19|20)\d{2}', text): 
            data_car['Title'] = text
            break
            
    if data_car['Title'] == "Missing Title" and len(all_text) > 0:
        data_car['Title'] = max(all_text[:5], key=len)

    return data_car

def scroll_and_scrape(driver, url):
    driver.get(url)
    print("Loading page... Waiting 8 seconds for initial load...")
    time.sleep(8)
    
    all_extracted_cars = []
    seen_cars = set()
    
    stuck_counter = 0
    previous_car_count = 0
    
    while True:
        
        driver.execute_script("""
            var elements = document.querySelectorAll('div, header, footer');
            for (var i = 0; i < elements.length; i++) {
                var pos = window.getComputedStyle(elements[i]).position;
                if (pos === 'fixed' || pos === 'sticky') {
                    elements[i].style.display = 'none';
                }
            }
        """)
        
        try:
            view_btn = driver.find_element(By.XPATH, "//button[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'view') or contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'more')]")
            
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", view_btn)
            time.sleep(1)
            driver.execute_script("arguments[0].click();", view_btn)
            print(" PHYSICAL 'VIEW MORE' BUTTON CLICKED! Loading next batch...")
            time.sleep(4)
        except:
            pass
        
        driver.execute_script("window.scrollBy(0, 700);")
        time.sleep(4.5) 
        
        soup = BeautifulSoup(driver.page_source, 'lxml')
        current_cards = []
        for div in soup.find_all('div'):
            strings = list(div.stripped_strings)
            if 5 <= len(strings) <= 35:
                text_blob = " ".join(strings).lower()
                if '₹' in text_blob and 'km' in text_blob:
                    if text_blob.count('₹') <= 6:
                        current_cards.append(div)

        for card in current_cards:
            car_data = extract_car_data(card)
            
            unique_id = f"{car_data['Title']}_{car_data['Price']}_{car_data['Kilometers']}"
            if unique_id not in seen_cars:
                seen_cars.add(unique_id)
                all_extracted_cars.append(car_data)

        print(f"Currently secured {len(all_extracted_cars)} raw cars...")

        if len(all_extracted_cars) == previous_car_count:
            stuck_counter += 1
            if stuck_counter >= 3:
                print("Count hasn't changed. Nudging the network...")
                driver.execute_script("window.scrollBy(0, -400);")
                time.sleep(1.5)
                driver.execute_script("window.scrollBy(0, 1200);")
                time.sleep(3.5)
            if stuck_counter >= 6:
                print("End of the page truly reached. No more cars to load.")
                break
        else:
            stuck_counter = 0 
            previous_car_count = len(all_extracted_cars)

    return pd.DataFrame(all_extracted_cars)

if __name__ == '__main__':
    url = 'https://www.cars24.com/buy-used-cars-new-delhi/'
    driver = setup_driver()
    
    print("Starting the ultimate scraper...")
    df = scroll_and_scrape(driver, url)
    
    driver.quit()
    
    save_path = r"C:\Programming\Machine Learning\Used Car Price Intelligence\Used Car Arbitrage\data\raw"
    os.makedirs(save_path, exist_ok=True)
    file_path = os.path.join(save_path, "raw_car_listings.csv")
    df.to_csv(file_path, index=False)
    
    print(f"Success! Saved {len(df)} cars to {file_path}")