from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from bs4 import BeautifulSoup
import time

SBR_WEBDRIVER = 'https://brd-customer-hl_692d2ac7-zone-scraping_browser2:w6cwseofin87@brd.superproxy.io:9515'

def scrape_website(website):
    try:
        print("[🌐] Connecting to Scraping Browser...")
        sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, "goog", "chrome")
        
        with Remote(sbr_connection, options=ChromeOptions()) as driver:
            driver.get(website)
            print("[🧠] Waiting for captcha solving...")

            solve_res = driver.execute(
                "executeCdpCommand",
                {
                    "cmd": "Captcha.waitForSolve",
                    "params": {"detectTimeout": 10000}
                }
            )

            status = solve_res["value"]["status"]
            print(f"[✅] Captcha solve status: {status}")

            time.sleep(2)  # Small delay for stability
            html = driver.page_source
            print("[📄] Page content scraped successfully!")
            return html

    except Exception as e:
        print(f"[❌] Error during scraping: {e}")
        return ""

def extract_body_content(html_content):
    try:
        soup = BeautifulSoup(html_content, "html.parser")
        body_content = soup.body
        return str(body_content) if body_content else ""
    except Exception as e:
        print(f"[❌] Error extracting body content: {e}")
        return ""

def clean_body_content(body_content):
    try:
        soup = BeautifulSoup(body_content, "html.parser")
        for script_or_style in soup(["script", "style"]):
            script_or_style.extract()
        
        cleaned = soup.get_text(separator="\n")
        cleaned_lines = [line.strip() for line in cleaned.splitlines() if line.strip()]
        return "\n".join(cleaned_lines)

    except Exception as e:
        print(f"[❌] Error cleaning content: {e}")
        return ""

def split_dom_content(dom_content, max_length=6000):
    try:
        return [
            dom_content[i:i + max_length]
            for i in range(0, len(dom_content), max_length)
        ]
    except Exception as e:
        print(f"[❌] Error splitting DOM content: {e}")
        return []
