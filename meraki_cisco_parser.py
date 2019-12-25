from selenium import webdriver
import csv
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time


LOGIN = "neenahkeith@gmail.com"
PASSWORD = "Plussix@88"
LINK = "https://account.meraki.com/secure/login/dashboard_login"
# PLEASE, PUT YOUR PATH TO CHROMEDRIVER
PATH_TO_CHROMEDRIVER = "C:\\Users\\Катерина\\Desktop\\Cisco-Meraki-Selenium-project-master\\chromedriver.exe"
# PLEASE, WRITE HERE FILE'S NAME
FILE = 'Network.csv'
# PLEASE, WRITE HERE PATH TO CSV FILE
PATH_TO_CSV_FILE = "C:\\Users\\Катерина\\Desktop\\Cisco-Meraki-Selenium-project-master\\"
COLUMN_NAME = 'Network Name' #Name of head column, to drop it
ORGANIZATION = 'Boyd Hyperconverged Inc' 
# THIS DICT MADE TO FOLLOW WHICH NETWORKS ALREADY DONE
CHECK = {}

browser = webdriver.Chrome(executable_path=PATH_TO_CHROMEDRIVER)

with open(PATH_TO_CSV_FILE + FILE) as f: 
    #HERE PROGRAM TAKES ALL NETWORK NAMES AND TAKE THEM TO DICTIONARY
    reader = csv.reader(f)
    for row in reader:
        if row[0] != COLUMN_NAME:
            CHECK[row[0]] = ''

def take_network_from_csv(): 
    global FILE
    global PATH_TO_CSV_FILE
    global COLUMN_NAME
    global CHECK
    global PATH_TO_CHROMEDRIVER
    for i in CHECK:
        if CHECK[i] != 'Done':
            network_name = i 
            open_link(browser, network_name)  
            CHECK[network_name] = 'Done'                
        else:
            continue
    


def open_link(browser, network_name): 
    # THIS IS MAIN FUNCTION
    global LINK 
    global LOGIN
    global PASSWORD
    browser.get(LINK)

    #LOG IN
    email = browser.find_element_by_id('email')
    password = browser.find_element_by_id('password')
    email.send_keys(LOGIN) 
    password.send_keys(PASSWORD) 
    submit_button = browser.find_element_by_id('commit') 
    submit_button.click()

    # CHOOSE NEEDED ORGANISATION
    organization = browser.find_element_by_link_text('Boyd Hyperconverged Inc')
    organization.click()

    #WAITING FOR PAGE LOADING
    time.sleep(3)

    # FIND AND CHOOSE NEEDED NETWORK
    select_arrow_zone = browser.find_element_by_class_name('Select-arrow-zone') 
    select_arrow_zone.click()
    input_network = browser.find_element_by_xpath('//*[@id="react-select-2--value"]/div[2]/input')
    input_network.send_keys(network_name)
    input_network.send_keys(Keys.ENTER) 

    #GOING TO Firewall & traffic shaping
    tables = browser.find_elements_by_class_name('menu-item-container') 
    for i in tables:
        if i.text == 'Wireless':
            needed_table = i
    needed_table.click()
    time.sleep(3)
    organization = browser.find_elements_by_tag_name('a') 
    for i in organization:
        if i.text == 'Firewall & traffic shaping' or i.text == 'Firewall':
            firewall = i
    firewall.click()

    # SWITCHES SLIDERS
    client_slider = browser.find_elements_by_class_name('simple')
    if client_slider[0].text != 'unlimited':
        source_element = browser.find_element_by_xpath('//*[@id="per_client_limit"]/table/tbody/tr/td[1]/div/div[2]/a')
        dest_element = browser.find_element_by_class_name('bandwidth_widget_toggle')
        ActionChains(browser).drag_and_drop(source_element, dest_element).perform()
    if client_slider[1].text != 'unlimited':
        source_element = browser.find_element_by_xpath('//*[@id="per_ssid_limit"]/table/tbody/tr/td[1]/div/div[2]/a')
        dest_element = browser.find_element_by_class_name('bandwidth_widget_toggle')
        ActionChains(browser).drag_and_drop(source_element, dest_element).perform()
    time.sleep(5)

    # SAVING
    try:
        save_changes = browser.find_element_by_id('floating_submit')
        save_changes.click()
    except:
        print('Already Unlimited')
    browser.quit()
    



if __name__ == '__main__':
    while True:
        try:
            take_network_from_csv()
            break
        except:
            browser.quit()    
            take_network_from_csv()
    print('DONE')
    




