from playwright.sync_api import sync_playwright, expect
import os
from dotenv import load_dotenv
import numpy as np
import matplotlib.pyplot as plt

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

# Maybe could make this a dict with data types as key?
def convertDictValues(type):
  convertedValues = []
  for value in type:
    if value.endswith("%"):
      value = float(value[:-1])/100
    elif value.endswith("°") or value.endswith("$"):
      value = float(value[:-1])
    elif value.endswith("ms"):
      value = int(value[:-2])
    elif value.endswith("sec"):
      value = float(value[:-3])
    convertedValues.append(value)
  print(convertedValues)
  return convertedValues

### ! Main ! ###
load_dotenv()
with sync_playwright() as p:
  browser = p.firefox.launch(headless = True)
  page = browser.new_page()
  page.set_default_timeout(5000)

  guestCS = ['guest', 'g']
  userCS = ['user', 'u']
  # ! Requires string validation ! #
  #guestUserChoice = input("Guest or User? ")
  guestUserChoice = "u"
  # ! End ! #
  if guestUserChoice.lower() in guestCS:
    ### ! Login ! ###
    page.goto(os.environ['GUEST_LEETIFY_ACCOUNT'])
    print("Loading profile...")

    ### ! Data Retrieval ! ###
    print(getRating('leetify'))

    # ! Debug ! #
    page.screenshot(path="tss.guest.png")
    # ! End ! #
  elif guestUserChoice.lower() in userCS:
    ### ! Login ! ###
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

    # Utility Rating
    utilityReturn = getRating('utility')
    utilityDict = utilityReturn[0]
    utilityAvgDict = utilityReturn[1]

    # Leetify Rating
    leetifyDict = getRating('leetify')

    ### ! Data Display ! ###
    # Convert values from String to Float/ Integer
    aimDictKeys = list(aimDict.keys())
    aimDictValues = convertDictValues(list(aimDict.values()))
    aimAvgDictKeys = list(aimAvgDict.keys())
    aimAvgDictValues = convertDictValues(list(aimAvgDict.values()))
    utilityDictKeys = list(utilityDict.keys())
    utilityDictValues = convertDictValues(list(utilityDict.values()))
    utilityAvgDictKeys = list(utilityAvgDict.keys())
    utilityAvgDictValues = convertDictValues(list(utilityAvgDict.values()))
    leetifyDictKeys = list(leetifyDict.keys())
    leetifyDictValues = convertDictValues(list(leetifyDict.values()))

    # Split into data types
    percentageKeys = aimDictKeys[:4] + aimDictKeys[-2:]
    print(percentageKeys)
    percentageValues = aimDictValues[:4] + aimDictValues[-2:]
    percentageAvgKeys = aimAvgDictKeys[:4] + aimAvgDictKeys[-2:]
    percentageAvgValues = aimAvgDictValues[:4] + aimAvgDictValues[-2:]

    w, x = 0.4, np.arange(len(percentageKeys))
    fig, ax = plt.subplots()

    ax.bar(x - w/2, percentageValues, width=w, label="Player")
    ax.bar(x + w/2, percentageAvgValues, width=w, label="Average")

    ax.set_xticks(x)
    ax.set_xticklabels(percentageKeys)
    ax.set_ylabel("Rating")
    ax.set_title("Aim Ratings (%)")

    plt.show(block=True)
    # ! ALL OF THE DATA IS A STRING TT ! #

    # Data needs to be compared to something: itself or others.
    
    # To compare to itself, you will need values from previous weeks or such.
    # # Graphs are shown as canvases, no good
    # # General shows previous period data, changes with 'Current Period' and 'Previous Period' filter (default will be {7 days current, 30 previous, Faceit} but should add config?)
    # # Consider storing previous 12 months worth of ratings for comparison? (Much harder to parse)
    # # Best comparison comes from match-to-match comparison (How would i save all the data for all the previous matches? Request from 'Matches' page?)

    # To compare to others, you will need values across average ranges.
    # # Data library can be used to compare ranks, players and maps

    # ! Debug ! #
    page.screenshot(path="tss.user.png")
    # ! End ! #

  browser.close()