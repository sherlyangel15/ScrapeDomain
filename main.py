from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import time
import imaplib
import email
import re

# Set up Selenium (Chrome in this example)
driver = webdriver.Chrome()  # Make sure ChromeDriver is installed

# 1. Open login page
driver.get("https://www.expireddomains.net/login/")  # Replace with your login page

# 2. Fill in login form
wait = WebDriverWait(driver, 10)
username_input = wait.until(EC.presence_of_element_located((By.NAME, "login")))
password_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))
username_input.send_keys("Bananapixelflarez845")
password_input.send_keys("EeRj;:+.7qbf,]s")
password_input.send_keys(Keys.RETURN)  # Press Enter

# 3. Wait for OTP input or CAPTCHA
input("🛑 Enter OTP or solve CAPTCHA, then press Enter here to continue...")
def get_latest_otp(email_user, email_pass, imap_server='imap.gmail.com'):
    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(email_user, email_pass)
    mail.select('inbox')
    result, data = mail.search(None, 'ALL')
    ids = data[0].split()
    latest_id = ids[-1]
    result, data = mail.fetch(latest_id, '(RFC822)')
    raw_email = data[0][1]
    msg = email.message_from_bytes(raw_email)
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True).decode()
    else:
        body = msg.get_payload(decode=True).decode()
    otp_match = re.search(r'\b\d{6}\b', body)  # Adjust regex for your OTP format
    if otp_match:
        return otp_match.group(0)
    return None

# filepath: c:\GitHub\ScrapeDomain\main.py
# 3. Wait for OTP input or CAPTCHA
print("⏳ Waiting for OTP email...")
otp_code = None
for _ in range(10):  # Try for up to 50 seconds
    otp_code = get_latest_otp("pixelflarez845@gmail.com", "W]pN!64~-e'-Xr~")
    if otp_code:
        print("✅ OTP found:", otp_code)
        break
    time.sleep(5)
if otp_code:
    otp_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "otp")))  # Adjust selector if needed
    otp_input.send_keys(otp_code)
    otp_input.send_keys(Keys.RETURN)
else:
    input("❌ OTP not found. Enter it manually, then press Enter to continue...")

# 4. Now you're logged in; scrape starting page
text_data = []
max_pages = 5
current_page = 1

while current_page <= max_pages:
    print(f"📄 Scraping page {current_page}...")
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    # Extract visible text
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    text = soup.get_text(separator="\n", strip=True)
    text_data.append(text)

    # Try to click "Next" button or link
    try:
        next_button = driver.find_element(By.LINK_TEXT, "Next")  # or use class, XPath, etc.
        next_button.click()
        time.sleep(2)  # Wait for page to load
        current_page += 1
    except:
        print("⚠️ No more pages or can't find 'Next'")
        break

# 5. Save to file
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("\n\n".join(text_data))

print("✅ Scraping finished. Text saved to output.txt")

# Close browser
driver.quit()
