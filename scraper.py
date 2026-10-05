from playwright.sync_api import sync_playwright, expect
import os
from dotenv import load_dotenv

def getRating(type):
  expect(page.locator("div.content")).to_be_visible()
  if type =="leetify":
    leetifyDict = {}
    # Leetify Rating
    leetifyDict.update({"Leetify Rating": page.locator("div.content").inner_text()})
    # Leetify T Side Rating
    leetifyDict.update({"T Side": "0"})
    # Leetify CT Side Rating
    leetifyDict.update({"CT Side": "0"})
    return leetifyDict
  if type=="aim":
    page.locator("button", has_text="Aim Stats").click()
    aimDict = {}
    # Leetify Aim Rating
    aimDict.update({"Aim Rating": page.locator("div.player-avg").nth(0).inner_text()})
    # Headshot accuracy
    aimDict.update({"Headshot Accuracy": "100%"}) # ! Temp Placeholder !
    # Accuracy (Enemy Spotted)
    aimDict.update({"Accuracy (Enemy Spotted)": "100%"}) # ! Temp Placeholder !
    # Spray Accuracy
    aimDict.update({"Spray Accuracy": "100%"}) # ! Temp Placeholder !
    # Proper Counter-Strafing
    aimDict.update({"Proper Counter-Strafing": "100%"}) # ! Temp Placeholder !
    # Crosshair Placement
    aimDict.update({"Crosshair Placement": "0°"}) # ! Temp Placeholder !
    # Time to Damage
    aimDict.update({"Time to Damage": "0ms"}) # ! Temp Placeholder !
    # Accuracy (All Shots)
    aimDict.update({"Accuracy (All Shots)": "100%"}) # ! Temp Placeholder !
    # Headshot Kill Percentage
    aimDict.update({"Headshot Kill Percentage": "100%"}) # ! Temp Placeholder !
    return aimDict
  if type=="utility":
    utilityDict = {}
    # Leetify Utility Rating
    utilityDict.update({"Utility Rating": page.locator("div.player-avg").nth(1).inner_text()})
    # Quality Rating
    utilityDict.update({"Quality Rating": "100"})
    # Flashbangs Leading to Kills
    utilityDict.update({"Flashbangs Leading to Kills": "100%"})
    # Enemies Flashed per Flashbang
    utilityDict.update({"Enemies Flashed per Flashbang": "5"})
    # Friends Flashed per Flashbang
    utilityDict.update({"Friends Flashed per Flashbang": "0"})
    # Flash Blind Duration per Flashed Enemy
    utilityDict.update({"Flash Blind Duration per Flashed Enemy": "5"})
    # Damage to Enemies per HE
    utilityDict.update({"Damage to Enemies per HE": "100"})
    # Damage to Teammates per HE
    utilityDict.update({"Damage to Teammates per HE": "0"})
    # Unused Utility on Death
    utilityDict.update({"Unused Utility on Death": "0$"})
    # Quantity Rating
    utilityDict.update({"Quantity Rating": "100"})
    return utilityDict
  else:
    return "! RUNTIME ERROR !"

# Main
load_dotenv()
with sync_playwright() as p:
  browser = p.firefox.launch(headless = True)
  page = browser.new_page()
  page.set_default_timeout(5000)

  # ! Requires string validation ! #
  guestCS = ['guest', 'g']
  userCS = ['user', 'u']
  #guestUserChoice = input("Guest or User? ")
  guestUserChoice = "u"
  if guestUserChoice.lower() in guestCS:
    # Login
    page.goto(os.environ['LEETIFY_ACCOUNT'])
    print("Loading profile...")

    # Data Retrieval
    print(getRating('leetify'))

    # Debug
    page.screenshot(path="tss.guest.png")
  elif guestUserChoice.lower() in userCS:
    # Login
    print("Logging in...")
    
    page.goto("https://leetify.com/auth/login")
    page.fill("#email", os.environ["LEETIFY_EMAIL"])
    page.fill("#password", os.environ["LEETIFY_PASSWORD"])
    with page.expect_navigation():
      page.get_by_role("button", name="Log in").click()
    print("Loading home page...")

    page.goto(os.environ['LEETIFY_ACCOUNT'])
    print("Loading profile...")

    # Data Retrieval
    # Aiming Rating
    print(getRating('aim'))

    # Utility Rating
    print(getRating('utility'))

    # Leetify Rating
    print(getRating('leetify'))

    # Debug
    page.screenshot(path="tss.user.png")
    # ! End ! #

  browser.close()