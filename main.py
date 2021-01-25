from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time

form_link = "https://forms.gle/c1tkNaGbB4s7Tr3DA"
chrome_driver_path = 'C:/Users/paulw/Documents/Developement/chromedriver.exe'

zillow_search_link = "https://www.zillow.com/atlantic-city-nj/rentals/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22Atlantic%20City%2C%20NJ%22%2C%22mapBounds%22%3A%7B%22west%22%3A-74.55574840551758%2C%22east%22%3A-74.35490459448242%2C%22south%22%3A39.34658795079454%2C%22north%22%3A39.40086161722161%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A10201%2C%22regionType%22%3A6%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22price%22%3A%7B%22min%22%3A0%2C%22max%22%3A872627%7D%2C%22mp%22%3A%7B%22min%22%3A0%2C%22max%22%3A3000%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22ah%22%3A%7B%22value%22%3Atrue%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A13%7D"
req_headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.8',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}

response = requests.get(url=zillow_search_link, headers=req_headers).text
soup = BeautifulSoup(response, 'html.parser')

listing_addresses = soup.findAll(name="address", class_="list-card-addr")
listing_prices = soup.findAll(name="div", class_="list-card-price")
listing_links = soup.findAll(name="a", href=True, class_='list-card-link')

listing_info = []

for i in range(len(listing_addresses)):
    new_listing = [listing_addresses[i].getText(), listing_prices[i].getText(), listing_links[i]['href']]
    listing_info.append(new_listing)


driver = webdriver.Chrome(executable_path=chrome_driver_path)

driver.get(form_link)
driver.maximize_window()
time.sleep(2)

for listing in listing_info:
    address_question_xpath = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input'
    price_question_xpath = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input'
    link_question_xpath = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input'
    submit_button_xpath = '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div'

    address_question = driver.find_element_by_xpath(address_question_xpath)
    price_question = driver.find_element_by_xpath(price_question_xpath)
    link_question = driver.find_element_by_xpath(link_question_xpath)
    submit_button = driver.find_element_by_xpath(submit_button_xpath)

    address_question.send_keys(listing[0])
    price_question.send_keys(listing[1])
    link_question.send_keys(listing[2])

    submit_button.click()

    time.sleep(3)

    start_over_xpath = '/html/body/div[1]/div[2]/div[1]/div/div[4]/a'
    start_over = driver.find_element_by_xpath(start_over_xpath)
    start_over.click()

    time.sleep(3)

driver.quit()
