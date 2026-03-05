from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import csv

options = Options()
options.add_argument("--start-maximized")

service = Service("chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)

# ---- STEP 1: GET ALL PRODUCT LINKS ----

driver.get("https://www.shl.com/solutions/products/product-catalog/")
time.sleep(5)

all_product_links = set()
page_number = 1

while True:
    print(f"\nScraping Page {page_number}...")
    time.sleep(3)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    links = driver.find_elements(By.TAG_NAME, "a")

    for link in links:
        href = link.get_attribute("href")
        if href and "/products/product-catalog/view/" in href:
            all_product_links.add(href)

    try:
        next_page = driver.find_element(By.LINK_TEXT, str(page_number + 1))
        driver.execute_script("arguments[0].click();", next_page)
        page_number += 1
    except:
        print("No more pages.")
        break

print("\nTotal Products:", len(all_product_links))

# ---- STEP 2: VISIT EACH PRODUCT ----

data = []

for url in all_product_links:
    print("Opening:", url)
    driver.get(url)
    time.sleep(4)

    try:
        name = driver.find_element(By.TAG_NAME, "h1").text
    except:
        name = ""

    try:
        description = driver.find_element(By.CLASS_NAME, "product-catalogue-description").text
    except:
        description = ""

    try:
        job_levels = driver.find_element(By.XPATH, "//*[contains(text(),'Job levels')]/following-sibling::*").text
    except:
        job_levels = ""

    try:
        languages = driver.find_element(By.XPATH, "//*[contains(text(),'Languages')]/following-sibling::*").text
    except:
        languages = ""

    try:
        length = driver.find_element(By.XPATH, "//*[contains(text(),'Assessment length')]/following-sibling::*").text
    except:
        length = ""

    data.append([name, description, job_levels, languages, length, url])

# ---- STEP 3: SAVE TO CSV ----

with open("shl_products.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Description", "Job Levels", "Languages", "Assessment Length", "URL"])
    writer.writerows(data)

driver.quit()

print("\nData saved to shl_products.csv")