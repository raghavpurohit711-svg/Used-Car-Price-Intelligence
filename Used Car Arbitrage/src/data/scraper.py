import time
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By

def setup_driver():

    options = webdriver.ChromeOptions()

    driver = webdriver.Chrome(options=options)

    return driver

def extract_car_data(car_details):
    data_car={}

    try:
        title = car_details.find('span',class_='sc-ksBlki dxpZAa')
        data_car['Title'] = title.text.strip() if title else None

        price = car_details.find('div', class_='styles_priceWrap__VwWBV')
        data_car['Price'] = price.text.strip() if price else None

        spec_list = car_details.find('ul',class_='sc-gsGlKM hCHamb')

        if spec_list:
            specs = spec_list.find_all('p')
            data_car['Kilometers'] = specs[0].text.strip() if len(specs) > 0 else None
            data_car['Fuel_Type'] = specs[1].text.strip() if len(specs) > 1 else None
            data_car['Transmission'] = specs[2].text.strip() if len(specs) > 2 else None

    except Exception as e:
        print(f"Skipping a car due to extraction error: {e}")

    return data_car

def scroll_and_scraper(driver, url, target_car_count = 500):
    driver.get(url)
    time.sleep(8)

    all_extracted_cars = []
    seen_cars = set()

    last_height = driver.execute_script("return document.body.scrollHeight")
    while len(all_extracted_cars) < target_car_count:

        driver.execute_script("window.scrollBy(0,document.body.scrollHeight);")
        time.sleep(10)

        try:
            view_more_btn = driver.find_element(By.XPATH,"//*[contains(translate(text(),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz',)'more')]")    
            driver.execute_script("arguments[0].click();",view_more_btn)
            print("Found and clicked the 'View more' button! Loading next batch...")
            time.sleep(3)

        except:
            pass
        soup = BeautifulSoup(driver.page_source, 'lxml')
        current_cards = soup.find_all('div', class_='styles_contentWrap__9oSrl')

        for card in current_cards:
            car_data = extract_car_data(card)

            if car_data['Title'] and car_data['Price']:
                unique_id = f"{car_data['Title']} - {car_data['Price']}"

                if unique_id not in seen_cars:
                    seen_cars.add(unique_id)
                    all_extracted_cars.append(car_data)

        print(f"Currently loaded {len(current_cards)}/{target_car_count} cars.....")

        if len(current_cards) >= target_car_count:
            print("Target car volume reached!")
            break

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print("Height didn't change. Waiting 3 extra seconds to double check...")
            time.sleep(3)
            new_height = driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                print("End of the page truly reached. No more cars to load")
                break

        last_height = new_height

    print("Extracting data into Dataframe...")
    final_soup = BeautifulSoup(driver.page_source,'lxml')
    car_cards = final_soup.find_all('div',class_="styles_normalCardWrapper__qDZjq")

    all_cars = []
    for card in car_cards:
        car_data = extract_car_data(card)
        if car_data:
            all_cars.append(car_data)
    return pd.DataFrame(all_cars)

if __name__=='__main__':
    url = 'https://www.cars24.com/buy-used-cars-new-delhi/'
    driver = setup_driver()
    print("Starting the scraper...")

    df = scroll_and_scraper(driver, url, target_car_count=500)

    driver.quit()

    df.to_csv(r"C:\Programming\Machine Learning\Used Car Price Intelligence\Used Car Arbitrage\data\raw\raw_car_listing.csv",index=False)
    print(f"Success! Saved {len(df)} cars to raw_car_listing.csv")