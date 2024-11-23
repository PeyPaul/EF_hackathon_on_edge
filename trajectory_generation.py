import time
import re
from playwright.sync_api import Playwright, sync_playwright, expect
import json

metadata = []

def run(playwright: Playwright, from_city: str, to_city: str, from_date: str, to_date: str) -> None:
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={"width": 500, "height": 500}
    )
    metadata.append({
        "from_city": from_city,
        "to_city": to_city,
        "from_date": from_date,
        "to_date": to_date,
        "timestamps": [],
        "positive": True
    })

    print(f"from_city: {from_city}, to_city: {to_city}, from_date: {from_date}, to_date: {to_date}")

    delay_step = 2
    page = context.new_page()
    # agree to cookies
    page.goto("https://google.com/travel/flights")
    page.mouse.wheel(0, 10000)
    time.sleep(delay_step)
    page.screenshot(path="screenshot.png")
    page.mouse.click(350, 350)
    time.sleep(delay_step)


    page.mouse.click(150, 250)
    time.sleep(delay_step)
    page.keyboard.press("Backspace")
    page.keyboard.press("Backspace")
    page.keyboard.press("Backspace")
    page.keyboard.press("Backspace")
    page.keyboard.press("Backspace")
    page.keyboard.press("Backspace")
    page.keyboard.press("Backspace")
    page.keyboard.press("Backspace")
    page.keyboard.press("Backspace")
    page.keyboard.press("Backspace")
    page.keyboard.press("Backspace")
    page.keyboard.press("Backspace")
    page.keyboard.press("Backspace")
    time.sleep(delay_step)
    page.keyboard.type(from_city)
    page.keyboard.press("Enter")
    time.sleep(delay_step)
    timestamp = time.time()
    page.screenshot(path=f"{timestamp}.png")
    metadata[-1]["timestamps"] += [timestamp]

    # Click on to destination
    page.mouse.click(350, 250)
    time.sleep(0.1)
    page.keyboard.type(to_city)
    page.keyboard.press("Enter")
    timestamp = time.time()
    page.screenshot(path=f"{timestamp}.png")
    metadata[-1]["timestamps"] += [timestamp]
    time.sleep(delay_step)

    # Click on from date
    page.mouse.click(150, 350)
    time.sleep(delay_step)
    page.keyboard.type(from_date)
    page.keyboard.press("Enter")
    timestamp = time.time()
    page.screenshot(path=f"{timestamp}.png")
    metadata[-1]["timestamps"] += [timestamp]
    time.sleep(delay_step)

    # Click on to date
    page.keyboard.press("Tab")
    time.sleep(delay_step)
    page.keyboard.type(to_date)
    page.keyboard.press("Enter")
    time.sleep(delay_step)
    timestamp = time.time()
    page.screenshot(path=f"{timestamp}.png")
    metadata[-1]["timestamps"] += [timestamp]

    # Click on done
    page.mouse.click(480, 480)
    time.sleep(delay_step)
    timestamp = time.time()
    page.screenshot(path=f"{timestamp}.png")
    metadata[-1]["timestamps"] += [timestamp]

    # Click on search
    page.mouse.click(250, 400)
    time.sleep(delay_step)
    timestamp = time.time()
    page.screenshot(path=f"{timestamp}.png")
    metadata[-1]["timestamps"] += [timestamp]

    # Click on cheapest
    page.mouse.click(300, 300)
    time.sleep(delay_step)
    timestamp = time.time()
    page.screenshot(path=f"{timestamp}.png")
    metadata[-1]["timestamps"] += [timestamp]

    # wait for results to load
    time.sleep(delay_step * 4)

    # Scroll down to see all results
    page.mouse.wheel(0, 250)
    time.sleep(delay_step)
    timestamp = time.time()
    page.screenshot(path=f"{timestamp}.png")
    metadata[-1]["timestamps"] += [timestamp]
    time.sleep(3)


    # ---------------------

    # Check if we're on the correct results page
    current_url = page.url
    if not current_url.startswith("https://www.google.com/travel/flights/search"):
        print(f"Error: Unexpected URL: {current_url}")
        metadata[-1]["positive"] = False
    else:
        metadata[-1]["positive"] = True
    
    context.close()
    browser.close()

try:
    with sync_playwright() as playwright:
        import pandas as pd
        df = pd.read_csv("dataset/dataset.csv")
        rows = [row for _, row in df.iterrows()]
        for i, row in enumerate(rows[58:]):
            run(playwright, row["airport_depart"], row["airport_retour"], row["date_depart"], row["date_retour"])
            with open("metadata.json", "w") as f:
                json.dump(metadata, f)
            print(f"Saved metadata for {row['airport_depart']} to {row['airport_retour']} ({i+58}/{len(rows)})")
except Exception as e:
    print(e)

