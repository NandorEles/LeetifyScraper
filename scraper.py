from playwright.sync_api import sync_playwright, expect
import os
from dotenv import load_dotenv

def getRating(type):
  expect(page.locator("div.content")).to_be_visible()
  if type =="leetify":
    page.locator("button", has_text="Leetify Rating").click()
    leetifyDict = {}
    # Leetify Rating
    tab = page.locator("app-profile-overview-recent-games-ratings")
    leetifyDict.update({"Leetify Rating": tab.locator(".leetify-rating .content").inner_text()})
    # Win Rate
    for x in tab.locator(".win-rate").locator("> div").all():
      leetifyDict.update({x.locator("dt").inner_text(): x.locator("dd").inner_text()})
    for x in tab.locator(".stats").locator("> div").all():
      leetifyDict.update({x.locator("dt").inner_text(): x.locator("dd").inner_text()})
    # Side Ratings
    leetifyStats = page.locator("div.sides").locator(".value").all()
    # Side Labels
    leetifyLabels = page.locator("div.sides").locator(".label").all()
    for x in range(len(leetifyStats)):
      # Side Label: Side Rating
      leetifyDict.update({leetifyLabels[x].inner_text().replace(u'\xa0', u' '): leetifyStats[x].inner_text()})
    page.locator("button", has_text="Top Stats").click()
    return leetifyDict
  if type=="aim":
    page.locator("button", has_text="Aim Stats").click()
    aimDict = {}
    aimAvgDict = {}
    # For all 'li' elements in '.aim-rating'
    for li in page.locator("div.aim-rating").locator("ul > li").all():
      # Aim Rating Stat: Value
      aimDict.update({li.locator(".player .label").inner_text(): li.locator(".player .value").inner_text()})
      # Aim Rating Avg Stat: Value
      aimAvgDict.update({li.locator(".player .label").inner_text()+" Avg": li.locator(".rank-avg .value").inner_text()})
    page.locator("button", has_text="Top Stats").click()
    return [aimDict, aimAvgDict]
  if type=="utility":
    page.locator("button", has_text="Utility Stats").click()
    utilityDict = {}
    utilityAvgDict = {}
    # For all 'li' elements in '.utility-rating'
    for li in page.locator("div.utility-rating").locator("ul > li").all():
      # Utility Rating Stat: Value
      utilityDict.update({li.locator(".player .label").inner_text(): li.locator(".player .value").inner_text()})
      # Utility Rating Avg Stat: Value
      utilityAvgDict.update({li.locator(".player .label").inner_text()+" Avg": li.locator(".rank-avg .value").inner_text()})
    page.locator("button", has_text="Top Stats").click()
    return [utilityDict, utilityAvgDict]
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
  guestUserChoice = input("Guest or User? ")
  if guestUserChoice.lower() in guestCS:
    # Login
    page.goto(os.environ['GUEST_LEETIFY_ACCOUNT'])
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

    ### Data Retrieval ###
    # Aiming Rating
    aimReturn = getRating('aim')
    aimDict = aimReturn[0]
    aimAvgDict = aimReturn[1]
    print(">"+str(aimDict))
    print(">"+str(aimAvgDict))

    # Utility Rating
    utilityReturn = getRating('utility')
    utilityDict = utilityReturn[0]
    utilityAvgDict = utilityReturn[1]
    print(">"+str(utilityDict))
    print(">"+str(utilityAvgDict))

    # Leetify Rating
    leetifyDict = getRating('leetify')
    print(leetifyDict)

    # ! Debug ! #
    page.screenshot(path="tss.user.png")
    # ! End ! #

  browser.close()