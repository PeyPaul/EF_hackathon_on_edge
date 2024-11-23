# Functions
import playwright

def run(playwright):
    browser = playwright.chromium.launch()
    context = browser.new_context()
    page = context.new_page()
    return page

with playwright.sync_playwright() as p:
    page = run(p)


def click_and_type(x, y, text):
    global page
    page.mouse.click(x,y)
    page.keyboard.type(text)

def click(x,y):
    global page
    page.mouse.click(x,y)

def type(text):
    global page
    page.keyboard.type(text)

def end():
    pass

def scroll(i):
    page.mouse.scroll(i)