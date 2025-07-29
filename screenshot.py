from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait # Changed this line
from selenium.webdriver.support.wait import WebDriverWait # Changed this line
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

# Config
screenshotDir = "Screenshots"
screenWidth = 400
screenHeight = 800

def getPostScreenshots(filePrefix, script):
    print("Taking screenshots...")
    driver, wait = __setupDriver(script.url)
    script.titleSCFile = __takeScreenshot(filePrefix, driver, wait)
    for commentFrame in script.frames:
        commentFrame.screenShotFile = __takeScreenshot(filePrefix, driver, wait, f"t1_{commentFrame.commentId}")
    driver.quit()

def __takeScreenshot(filePrefix, driver, wait, handle="Post"):
    # method = By.CLASS_NAME if (handle == "Post") else By.ID
    handler = "[post-title]" if (handle == "Post") else f"[thingid={handle}]"
    search = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, handler)))
    driver.execute_script("window.focus();")

    fileName = f"{screenshotDir}/{filePrefix}-{handle}.png"
    fp = open(fileName, "wb")
    fp.write(search.screenshot_as_png)
    fp.close()
    return fileName

def __setupDriver(url: str):
    options = webdriver.ChromeOptions()
    options.headless = False
    options.enable_mobile = False
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)

    driver.set_window_size(width=screenWidth, height=screenHeight)
    driver.get(url)

    return driver, wait 