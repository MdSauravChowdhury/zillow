from time import sleep
import csv
from selenium.webdriver import Chrome
from parsel import Selector
from selenium.common.exceptions import NoSuchElementException


# past your driver path
driver = Chrome('/home/your_dir_name/chromedriver')
# driver = Chrome('')

# past your url

# example
# driver.get("") 
driver.get("https://www.zillow.com/homes/New-York,-NY_rb/")
sleep(10)
# sleep menualy 10 secound

# get home link "a"
single_home_item = driver.find_elements_by_xpath('.//*[@class="list-card-link list-card-info"]')

# get all singel home page "href"
all_link = [single_home_item.get_attribute('href') for single_home_item in single_home_item]
sleep(2)

# csv name path
path = 'home.csv'

with open(path, 'a') as file:

	for all_link in all_link:
		driver.get(all_link)
		sleep(4)
		# add extract selector in parsel 
		sel = Selector(text=driver.page_source)

		try:
			price = sel.xpath(".//*[@class='ds-value']/text()").extract_first() 
		except:
			price = None
		try:
			address_one = sel.xpath(".//*[@class='ds-address-container']/span/text()").extract_first() 
		except:
			address_one = None
		
		try:
			address_two = sel.xpath(".//*[@class='ds-address-container']/span/text()").extract()[1] 
		except:
			address_one = None

		if address_one or address_two:
			address = address_one + address_two
		elif address_one:
			address = address_one
		elif address_two:
			address = address_two

			
		try:
			phone = driver.find_element_by_xpath(".//*[@class='RCFAgentPhoneDesktopText__phoneNumber']").text
		except:
			phone = None
		try:	
			phone2 = driver.find_elements_by_xpath(".//*[@class='listing-field']")
		except:
			phone2 = None
		try:	
			contact_two = [pn.text for pn in phone2] 
		except:
			contact_two = None  

		try:
			option_num = contact_two[0] 
		except:
			option_num = None
		try:
			option_num_two = contact_two[2] 
		except:
			option_num_two = None     

		print("\n")
		print(price)
		print(address)  
		print(phone)
		print(option_num)
		print(option_num_two)
		print("\n")

		# define row name
		fieldnames = ['Price', 'Address', 'Contact One', 'Contact Two', 'Contact Three']
		write = csv.DictWriter(file, fieldnames=fieldnames)

		# get data and store the row
		write.writerow({"Price": price, 'Address': address, 'Contact One': phone, 'Contact Two': option_num, 'Contact Three': option_num_two})

	# driver.quit()




