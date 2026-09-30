from playwright.sync_api import sync_playwright, expect
import os
from dotenv import load_dotenv

# Guest Scrape
def guestScrape():
  page.goto(os.environ['LEETIFY_ACCOUNT'])
  print("Loading profile...")

  print(getRating())

  page.screenshot(path="tss.guest.png")

# User Scrape
def userScrape():
  # Logins
  print("Logging in...")
  
  page.goto("https://leetify.com/auth/login")
  page.fill("#email", os.environ["LEETIFY_EMAIL"])
  page.fill("#password", os.environ["LEETIFY_PASSWORD"])
  with page.expect_navigation():
    page.get_by_role("button", name="Log in").click()
  print("Loading home page...")

  page.goto(os.environ['LEETIFY_ACCOUNT'])
  print("Loading profile...")

  print(getRating())

  page.screenshot(path="tss.user.png")

def getRating():
  expect(page.locator("div.content")).to_be_visible()
  return page.locator("div.content").inner_text()


# Main
load_dotenv()
with sync_playwright() as p:
  browser = p.firefox.launch(headless = True)
  page = browser.new_page()

  # ! Requires string validation ! #
  guestCS = ['guest', 'g']
  userCS = ['user', 'u']
  guestUserChoice = input("Guest or User? ")
  if guestUserChoice.lower() in guestCS:
    guestScrape()
  elif guestUserChoice.lower() in userCS:
    userScrape()
  # ! End ! #

  browser.close()