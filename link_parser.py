import argparse
import asyncio
import json
import os
import random
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium import webdriver
from selenium.webdriver import ActionChains
from utils.constants import ACCEPT_BUTTON
from faker import Faker
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService

fake = Faker()


def generate_random_user_agent():
    agent = fake.chrome()
    print(agent)
    return agent


def generate_random_ip():
    ip = fake.ipv4()
    print(ip)
    return ip


# options = webdriver.FirefoxOptions()
# options.add_argument("-headless")
# options.binary_location = "/Applications/Firefox.app/Contents/MacOS/firefox"
# profile = webdriver.FirefoxProfile()
# profile.set_preference("general.useragent.override", f"{generate_random_user_agent()}")
# driver = webdriver.Chrome(
#     executable_path="",
#     options=options,
# )

# options = webdriver.ChromeOptions()
# # options.add_argument("-headless")
# options.add_argument(f"--user-agent='{generate_random_user_agent()}'")
# driver = webdriver.Chrome(
#     executable_path="",
#     options=options,
# )

# options = webdriver.ChromeOptions()
# # options.add_argument("-headless")
# options.add_argument(f"--user-agent='{generate_random_user_agent()}'")
# driver = webdriver.Chrome(
#     executable_path="",
#     options=options,
# )


chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chromedriver_path = "/usr/local/bin/chromedriver"
chrome_binary_path = "/usr/bin/google"
chrome_options.binary_location = chrome_binary_path
driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)


class LinksCollector:
    def __init__(
        self,
        driver,
        link="https://yandex.ru/maps",
        max_errors=5,
        accept_button=ACCEPT_BUTTON,
        accept=False,
    ):
        self.driver = driver
        self.slider = None
        self.max_errors = max_errors
        self.link = link
        self.accept_button = accept_button
        self.accept = accept

    def _init_driver(self):
        self.driver.maximize_window()

    def _open_page(self, request):
        self.driver.get(self.link)
        sleep(random.uniform(2, 3))
        self.driver.find_element_by_class_name(name="input__control").send_keys(request)
        sleep(random.uniform(1, 2))
        self.driver.find_element_by_class_name(
            name="small-search-form-view__button"
        ).click()
        sleep(random.uniform(5, 6))
        self.slider = self.driver.find_element_by_class_name(
            name="scroll__scrollbar-thumb"
        )

        if self.accept:
            flag = True
            count = 0
            while flag:
                try:
                    count += 1
                    sleep(3)
                    self.driver.find_element_by_xpath(self.accept_button).click()
                    flag = False
                except:
                    if count > 5:
                        self.driver.quit()
                        self._init_driver()
                        self._open_page(request)
                    flag = True

    def run(self, city, district, type_org_ru, type_org):
        self._init_driver()
        request = city + " " + district + " " + type_org_ru
        self._open_page(request)
        organizations_hrefs = []

        count = 0
        link_number = [0]
        errors = 0
        while self.max_errors > errors:
            try:
                ActionChains(self.driver).click_and_hold(self.slider).move_by_offset(
                    0, int(100 / errors)
                ).release().perform()
                slider_organizations_hrefs = self.driver.find_elements_by_class_name(
                    name="search-snippet-view__link-overlay"
                )
                slider_organizations_hrefs = [
                    href.get_attribute("href") for href in slider_organizations_hrefs
                ]
                organizations_hrefs = list(
                    set(organizations_hrefs + slider_organizations_hrefs)
                )
                count += 1
                if count % 3 == 0:
                    if len(organizations_hrefs) == link_number[-1]:
                        errors = errors + 1
                    print(len(organizations_hrefs))
                    link_number.append(len(organizations_hrefs))

                sleep(random.uniform(0.05, 0.1))
            except Exception:
                errors = errors + 1
                print("errors", errors)
                sleep(random.uniform(0.3, 0.4))

        directory = f"links/{type_org}"
        if not os.path.exists(directory):
            os.makedirs(directory)
        self.driver.quit()
        with open(f"{directory}/{request}.json", "w") as file:
            json.dump({"1": organizations_hrefs}, file)


async def get_links(city, query):
    parser = argparse.ArgumentParser()
    parser.add_argument("type_org", help="organization type")

    for district in ["Россия"]:
        sleep(1)
        # driver = webdriver.Safari()
        grabber = LinksCollector(driver)
        grabber.run(
            city=city,
            district=district,
            type_org_ru=query,
            type_org=query,
        )


# asyncio.run(get_links("Самара", "Салон мебели"))
