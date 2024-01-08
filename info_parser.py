import argparse
import json
import os
import random
from time import sleep

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from soup_parser import SoupContentParser
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
options.add_argument("-headless")
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)


class Parser:
    def __init__(self, driver):
        self.driver = driver
        self.soup_parser = SoupContentParser()

    def parse_data(self, hrefs, type_org):
        self.driver.maximize_window()
        self.driver.get("https://yandex.ru/maps")
        parent_handle = self.driver.window_handles[0]
        org_id = 0

        for organization_url in hrefs:
            try:
                # if True:
                self.driver.execute_script(
                    f'window.open("{organization_url}","org_tab");'
                )
                child_handle = [
                    x for x in self.driver.window_handles if x != parent_handle
                ][0]
                self.driver.switch_to.window(child_handle)
                sleep(0.7)
                soup = BeautifulSoup(self.driver.page_source, "lxml")
                org_id += 1
                name = self.soup_parser.get_name(soup)
                address = self.soup_parser.get_address(soup)
                website = self.soup_parser.get_website(soup)
                opening_hours = self.soup_parser.get_opening_hours(soup)
                ypage = self.driver.current_url
                rating = self.soup_parser.get_rating(soup)
                social = self.soup_parser.get_social(soup)
                phone = self.soup_parser.get_phone(soup)
                goods, reviews = None, None
                df = pd.DataFrame(
                    columns=[
                        "org_id",
                        "name",
                        "address",
                        "website",
                        "opening_hours",
                        "ypage",
                        "goods",
                        "rating",
                        "reviews",
                        "phone",
                        "social",
                    ]
                )

                # Создаем строку с данными
                row_data = [
                    org_id,
                    name,
                    address,
                    website,
                    opening_hours,
                    ypage,
                    goods,
                    rating,
                    reviews,
                    phone,
                    social,
                ]

                # Добавляем строку в DataFrame
                df.loc[len(df)] = row_data

                # Записываем DataFrame в CSV-файл
                df.to_csv(
                    f"result_output/{type_org}_outputs.csv",
                    mode="a",
                    header=not os.path.isfile(f"result_output/{type_org}_outputs.csv"),
                    index=False,
                )

                print(f"Данные добавлены, id - {org_id}")

                self.driver.switch_to.window(parent_handle)
                sleep(random.uniform(0.2, 0.4))
            except Exception as e:
                print(f"Ошибка при обработке {organization_url}: {e}")
        print("Данные сохранены")
        self.driver.quit()


async def get_info(query):
    parser = argparse.ArgumentParser()
    parser.add_argument("query", help="organization type")
    type_org = query
    # driver = webdriver.Safari()
    all_hrefs = []
    files = os.listdir(f"links/{type_org}")
    for file in files:
        with open(f"links/{type_org}/{file}", "r", encoding="utf-8") as f:
            hrefs = json.load(f)["1"]
            all_hrefs += hrefs
    all_hrefs = list(set(all_hrefs))
    print("all_hrefs", len(all_hrefs))
    parser = Parser(driver)
    parser.parse_data(all_hrefs, type_org)
