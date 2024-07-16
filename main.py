import time

from selenium import webdriver
from selenium.common import exceptions, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Keep  Chrome browser open after program finishes
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://orteil.dashnet.org/experiments/cookie/")

cookie = driver.find_element(By.ID, value="cookie")

items = driver.find_elements(By.CSS_SELECTOR, value="#store div")
item_ids = [item.get_attribute("id") for item in items]

print(item_ids)

timeout = time.time() + 5
five_min = time.time() + 5*60


while True:
    cookie.click()

    if time.time() > timeout:
        # Get all <b> tags
        all_prices = driver.find_elements(By.CSS_SELECTOR, value="#store b")
        items_prices = []

        # get all the items t
        for price in all_prices:
            element_text = price.text
            if element_text != "":
                price_int = int(element_text.split("- ")[1].replace(",", ""))
                items_prices.append(price_int)

        # create dictionary of items prices
        cookie_upgrades = {}
        for i in range(len(items_prices)):
            cookie_upgrades[items_prices[i]] = item_ids[i]

        print(cookie_upgrades)

        # get cookie count
        money_element = driver.find_element(By.ID, value="money").text
        if "," in money_element:
            money_element = money_element.replace(",", "")
        cookie_count = int(money_element)
        print(cookie_count)

        # Find upgrades that we can currently afford
        affordable_upgrades = {}
        for item_cost, item_id in cookie_upgrades.items():
            if cookie_count > item_cost:
                affordable_upgrades[item_cost] = item_id

        # Purchase the most expensive afforable upgrade
        highest_price_affordable_upgrade = max(affordable_upgrades)
        print(f"highest affordable is: {highest_price_affordable_upgrade}")
        to_purchase_id = affordable_upgrades[highest_price_affordable_upgrade]

        driver.find_element(By.ID, to_purchase_id).click()

        # Ad another 5 seconds until the next check
        timeout = time.time() + 5

    # after 5 min stop the bot and check the cookies per seccond count

    if time.time() > five_min:
        cookie_per_5 = driver.find_element(By.ID, value="cps").text
        print(cookie_per_5)
        break




