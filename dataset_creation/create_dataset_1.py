import random
import json
import time
import pandas as pd
from playwright.sync_api import Playwright, sync_playwright, expect

dates_list = [
    "dimanche 1 décembre 2024",
    "lundi 2 décembre 2024",
    "mardi 3 décembre 2024",
    "mercredi 4 décembre 2024",
    "jeudi 5 décembre 2024",
    "vendredi 6 décembre 2024",
    "samedi 7 décembre 2024",
    "dimanche 8 décembre 2024",
    "lundi 9 décembre 2024",
    "mardi 10 décembre 2024",
    "mercredi 11 décembre 2024",
    "jeudi 12 décembre 2024",
    "vendredi 13 décembre 2024",
    "samedi 14 décembre 2024",
    "dimanche 15 décembre 2024",
    "lundi 16 décembre 2024",
    "mardi 17 décembre 2024",
    "mercredi 18 décembre 2024",
    "jeudi 19 décembre 2024",
    "vendredi 20 décembre 2024",
    "samedi 21 décembre 2024",
    "dimanche 22 décembre 2024",
    "lundi 23 décembre 2024",
    "mardi 24 décembre 2024",
    "mercredi 25 décembre 2024",
    "jeudi 26 décembre 2024",
    "vendredi 27 décembre 2024",
    "samedi 28 décembre 2024",
    "dimanche 29 décembre 2024",
    "lundi 30 décembre 2024",
    "mardi 31 décembre 2024"
]

cities = pd.read_csv("./dataset.csv")["airport_depart"].unique()

def run(playwright: Playwright) -> None:
    for i in range(59, 100):
        print(f"Run {i}")
        save_dict = {
            "images": []*4,
            "prefixes": []*4,
            "suffixes": []*4
        }
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        context.clear_cookies()
        page = context.new_page()
        page.goto("https://consent.google.com/m?continue=https://www.google.com/travel/flights&gl=FR&m=0&pc=flt&cm=2&hl=en&src=1")
        try:
            page.mouse.wheel(0, 20)
            page.get_by_role("button", name="Tout accepter", timeout=10).click()
        except:pass
        page.mouse.wheel(0, 20)
        city = random.choice(cities)
        date = random.choice(dates_list[:29])
        second_date = random.choice(dates_list[dates_list.index(date)+1:])
        task = "Je cherche un vol de Paris à {city} du {date} au {second_date}".format(city=city, date=date, second_date=second_date)
        p = random.random()
        if p < 0.5:
            page.get_by_role("combobox", name="Où allez-vous ?").click()
            page.get_by_role("combobox", name="Où allez-vous ?").fill(city)
            page.get_by_role("combobox", name="Où allez-vous ?").press("Enter")
            save_dict["images"].append(f"runs/run{i}_image1.png")
            save_dict["prefixes"].append(f"Task: {task} \n Action:")
            save_dict["suffixes"].append(f"""page.get_by_role("combobox", name="Où allez-vous ?").click()
            page.get_by_role("combobox", name="Où allez-vous ?").fill('{city}')
            page.get_by_role("combobox", name="Où allez-vous ?").press("Enter")""")
            page.screenshot(path=f"runs/run{i}_image1.png")
            page.get_by_role("textbox", name="Départ").click()
            page.get_by_role("button", name=date).click()
            save_dict["images"].append(f"runs/run{i}_image2.png")
            save_dict["prefixes"].append(f"Task: {task} \n Action:")
            save_dict["suffixes"].append(f"""page.get_by_role("textbox", name="Départ").click()
            page.get_by_role("button", name='{date}').click()""")
            page.screenshot(path=f"runs/run{i}_image2.png")
            page.get_by_role("button", name=second_date).click()
            save_dict["images"].append(f"runs/run{i}_image3.png")
            save_dict["prefixes"].append(f"Task: {task} \n Action:")
            save_dict["suffixes"].append(f"""page.get_by_role("textbox", name="Départ").click()
            page.get_by_role("button", name='{second_date}').click()""")
            page.screenshot(path=f"runs/run{i}_image3.png")
            page.keyboard.press("Enter")
        else:
            page.get_by_role("textbox", name="Départ").click()
            page.get_by_role("button", name=date).click()
            save_dict["images"].append(f"runs/run{i}_image1.png")
            save_dict["prefixes"].append(f"Task: {task} \n Action:")
            save_dict["suffixes"].append(f"""page.get_by_role("textbox", name="Départ").click()
            page.get_by_role("button", name='{date}').click()""")
            page.screenshot(path=f"runs/run{i}_image1.png")
            save_dict["images"].append(f"runs/run{i}_image2.png")
            save_dict["prefixes"].append(f"Task: {task} \n Action:")
            save_dict["suffixes"].append(f"""page.get_by_role("textbox", name="Départ").click()
            page.get_by_role("button", name='{second_date}').click()""")
            page.get_by_role("button", name=second_date).click()
            page.screenshot(path=f"runs/run{i}_image2.png")
            page.keyboard.press("Enter")
            page.get_by_role("combobox", name="Où allez-vous ?").click()
            page.get_by_role("combobox", name="Où allez-vous ?").fill(city)
            page.get_by_role("combobox", name="Où allez-vous ?").press("Enter")
            save_dict["images"].append(f"runs/run{i}_image3.png")
            save_dict["prefixes"].append(f"Task: {task} \n Action:")
            save_dict["suffixes"].append(f"""page.get_by_role("combobox", name="Où allez-vous ?").click()
            page.get_by_role("combobox", name="Où allez-vous ?").fill('{city}')
            page.get_by_role("combobox", name="Où allez-vous ?").press("Enter")""")
            page.screenshot(path=f"runs/run{i}_image3.png") 
        save_dict["images"].append(f"runs/run{i}_image4.png")
        save_dict["prefixes"].append(f"Task: {task} \n Action:")
        save_dict["suffixes"].append(f"""page.get_by_label("Rechercher", exact=True).click()""")
        page.screenshot(path=f"runs/run{i}_image4.png")
        page.get_by_label("Rechercher", exact=True).click()
        with open(f"runs/run{i}.json", "w") as json_file:
            json.dump(save_dict, json_file)
        context.close()
        browser.close()
    # ---------------------


with sync_playwright() as playwright:
    run(playwright)