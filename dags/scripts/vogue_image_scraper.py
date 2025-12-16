#!/usr/bin/env python
# coding: utf-8

# In[4]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import os
import re
import time
from PIL import Image
from dotenv import load_dotenv
from pathlib import Path


load_dotenv()

### CONFIG ###
SLIDESHOW_URL = "https://www.vogue.com/fashion-shows/spring-2026-ready-to-wear/christophe-lemaire/slideshow/collection#1"
ROOT = Path.cwd().parents[1]
IMAGES_DIR = ROOT / "images"
IMAGES_DIR.mkdir(exist_ok=True)
WAIT_TIME = 20
USER_AGENT = "Mozilla/5.0"


# In[5]:

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

service = Service(ChromeDriverManager().install())
service.path = str(Path(service.path).with_name("chromedriver"))  # force correct binary



options = Options()
options.add_argument("--start-maximized")
options.add_argument(f"user-agent={USER_AGENT}")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(
    service=service,
    options=options
)

# driver = webdriver.Chrome( 
#     options=options
# )
wait = WebDriverWait(driver, WAIT_TIME)


# In[6]:


def is_logged_in(d):
    cookies = d.get_cookies()
    for c in cookies:
        if "vogue.com" in c["domain"] or c["name"] in ["cnid", "session", "auth_token"]:
            return True
    return False

def login_to_vogue(email: str, password: str):
    driver.get("https://id.condenast.com/")

    # The selector name may change when they update the website
    vogue_login_button = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#main-content > div > div.utility-card__grid.utility-card > div:nth-child(16) > a"))
    )
    vogue_login_button.click()

    email_input = wait.until(
            EC.presence_of_element_located((By.NAME, "email"))
    )
    email_input.send_keys(email)

    email_continue_button = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#email-continue-button"))
    )
    # Need to use execute_script as it uses javascript, simulating a real user click 
    driver.execute_script("arguments[0].click();", email_continue_button)

    password_input = wait.until(
            EC.presence_of_element_located((By.NAME, "password"))
    )
    password_input.send_keys(password)

    sign_in_button = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#log-in-sign-in-button-password"))
    )
    driver.execute_script("arguments[0].click();", sign_in_button)


    # no_passkey_button = wait.until(
    #     EC.presence_of_element_located((By.CSS_SELECTOR, "#do-not-setup-passkey-button"))
    # )
    # driver.execute_script("arguments[0].click();", no_passkey_button)

    WebDriverWait(driver, 25).until(is_logged_in)
    driver.get(SLIDESHOW_URL)


# In[7]:


def resize_image(path, size=(400, 400)):
    with Image.open(path) as img: 
        img.thumbnail(size, Image.Resampling.LANCZOS)
        img.save(path)
    


# In[8]:


def extract_image_from_slide(slide_number: int):
    """Extracts and downloads image for a given slide number."""
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    img_tag = soup.find("img", {"data-src": True})
    if not img_tag:
        print(f"[Slide {slide_number}] No image found.")
        return

    img_url = img_tag["data-src"]
    print(f"[Slide {slide_number}] Image URL: {img_url}")

    response = requests.get(img_url, headers={"User-Agent": USER_AGENT})
    response.raise_for_status()

    filename = IMAGES_DIR / f"vogue_image_{slide_number}.jpg"
    with open(filename, "wb") as f:
        f.write(response.content)

    resize_image(filename)

    print(f"[Slide {slide_number}] Image saved as {filename.name}")


# In[9]:


def scrape_slideshow():
    """Navigates the Vogue slideshow and downloads images sequentially."""
    driver.get(SLIDESHOW_URL)

    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "img[data-src]")))
    previous_slide = 0

    while True:
        # Get current slide number from URL
        current_url = driver.current_url
        match = re.search(r'#(\d+)', current_url)
        if not match:
            print("No slide number detected — exiting.")
            break

        current_slide = int(match.group(1))

        # Stop if slideshow loops back to the first image
        if current_slide < previous_slide:
            print("Slideshow loop detected — stopping.")
            break

        extract_image_from_slide(current_slide)
        previous_slide = current_slide

        # Try to click the "Next" button
        next_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div[aria-label='Next']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", next_btn)
        next_btn.click()
        time.sleep(2)  # Small delay for next image to load

# Current issue is that its downloading the same image across different slides, the images should be unique per slide


# In[10]:


if __name__ == "__main__":
    try:
        login_to_vogue(os.getenv("VOGUE_EMAIL"), os.getenv("VOGUE_PASSWORD"))
        scrape_slideshow()
    finally:
        driver.quit()

