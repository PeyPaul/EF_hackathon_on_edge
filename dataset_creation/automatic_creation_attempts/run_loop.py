"""Failed methods but kept for consignation purposes."""

from smart_crawler import SmartCrawler
import selenium
import time
smart_crawler = SmartCrawler()

driver = selenium.webdriver.Chrome()

# navigate to google flights
driver.get("https://www.google.com/flights")

# wait for the page to load
time.sleep(5)

while True:
    # take a screenshot of the page
    timestamp = time.time()
    driver.save_screenshot(f"{timestamp}.jpg")

    # get the next step
    next_step = smart_crawler.get_next_step(f"{timestamp}.jpg")

    # execute the next step
    exec(next_step)

    # wait for the page to load
    time.sleep(5)
