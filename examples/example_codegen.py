from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    
    # Navigate to example site
    page.goto("https://example.com")
    
    # Example form interactions
    page.click("text=More information...")
    
    # Close
    context.close()
    browser.close()

if __name__ == '__main__':
    with sync_playwright() as playwright:
        run(playwright)
