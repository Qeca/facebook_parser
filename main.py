from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from parser_facebook import parse_posts
chrome_options = webdriver.ChromeOptions()

chrome_options.add_argument(r"--user-data-dir=C:/path/to/your/selenium/profile")
chrome_options.add_argument("--profile-directory=Default")

chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

n = 200
driver.get('https://www.facebook.com/romangold')

parse_posts(n, driver)