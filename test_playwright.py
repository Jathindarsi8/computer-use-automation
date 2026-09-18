from playwright.sync_api import sync_playwright
import os

def test_browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        print("Opening demo.opencart.com...")
        page.goto("https://demo.opencart.com")
        page.wait_for_load_state("networkidle")
        
        os.makedirs("evidence", exist_ok=True)
        page.screenshot(path="evidence/step_001_homepage.png")
        
        print(f"✅ Browser works!")
        print(f"Page title: {page.title()}")
        print(f"Screenshot saved to evidence/step_001_homepage.png")
        
        browser.close()

if __name__ == "__main__":
    test_browser()