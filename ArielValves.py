import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from auth_data import ariel_password
from auth_data import ariel_login
import pandas as pd
import glob


start_time = time.time()

# Get a frame serial number base
file_name = input('Enter the name of file with a serial numbers: ')
result = pd.read_excel(f'{file_name}.xlsx')
serial_numbers = result['sn'].tolist()
total_sn = len(serial_numbers)


# Using Selenium
url = 'https://www.arielcorp.com/members/login/'

# set webdriver options
chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory" : "C:\\Users\\hp\\PycharmProjects\\ArielValvesDatabase\\Downloads"}
chromeOptions.add_experimental_option("prefs",prefs)
chromeOptions.add_argument("--disable-blink-features=AutomationControlled")
# headless mode
# chromeOptions.headless = True
driver = webdriver.Chrome(options=chromeOptions)



try:
    print('Login Ariel Website...')
    # Open and login  Ariel website
    driver.get(url=url)

    # entering a email
    email_input = driver.find_element(By.NAME,'ctl00$siteMainBodyPlaceHolder$Top$columnDisplay$ctl00$controlcolumn$ctl00$WidgetHost$WidgetHost_widget$ctl00$UsernameTB')
    email_input.clear()
    email_input.send_keys(ariel_login)

    # entering a password
    password_input = driver.find_element(By.NAME,'ctl00$siteMainBodyPlaceHolder$Top$columnDisplay$ctl00$controlcolumn$ctl00$WidgetHost$WidgetHost_widget$ctl00$PasswordTB')
    password_input.clear()
    password_input.send_keys(ariel_password)

    # press login button
    login_button_click = driver.find_element(By.NAME, 'ctl00$siteMainBodyPlaceHolder$Top$columnDisplay$ctl00$controlcolumn$ctl00$WidgetHost$WidgetHost_widget$ctl00$LoginButton').click()
    time.sleep(5)


    # Open ariel parts page
    driver.get(url='https://www.arielcorp.com/parts/portal/')

    # press equipment button
    equipment_button = driver.find_element(By.ID, 'tab-1448-btnEl')
    equipment_button.click()
    driver.implicitly_wait(10)

    print('Start downloading the valve files...')
    counter = 0
    for elem in serial_numbers:
        # fill in the field with the serial number
        text_field = driver.find_element(By.ID, 'textfield-1180-inputEl')
        text_field.clear()
        text_field.send_keys(elem)

        # press search button
        search_button = driver.find_element(By.ID, 'button-1185')
        search_button.click()
        driver.implicitly_wait(10)

        try:
            # press valves button
            valves_button = driver.find_element(By.ID, 'button-1202-btnEl')
            valves_button.click()
            driver.implicitly_wait(10)

            # downloading valves file
            download_button = driver.find_element(By.ID, 'button-1277-btnInnerEl')
            download_button.click()
            driver.implicitly_wait(10)

            # back to the equipment page
            back = driver.find_element(By.ID, 'button-1287-btnInnerEl')
            back.click()
            driver.implicitly_wait(30)

            counter += 1
            current_time = time.time()

            print(f'{counter}/ {total_sn} was downloaded. {round(current_time - start_time, 1)} seconds have passed.')

        finally:
            continue
    time.sleep(10)

except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()


# Create excel file
# getting excel files to be merged from the Downloads
path = "C:\\Users\\hp\\PycharmProjects\\ArielValveDatabaseForGithub\\Downloads"

# read all the files with extension .xlsx i.e. excel
filenames = glob.glob(path + "\*.xlsx")

# empty data frame for the new output excel file with the merged excel files
outputxlsx = pd.DataFrame()

# for loop to iterate all excel files
for file in filenames:
   # using concat for excel files
   # after reading them with read_excel()
   df = pd.concat(pd.read_excel( file, sheet_name=None), ignore_index=True, sort=False)

   # appending data of excel files
   outputxlsx = outputxlsx.append( df, ignore_index=True)

print(f'Final Excel sheet now generated at the same location: C:\\Users\\hp\\PycharmProjects\\ArielValvesDatabase\\Result_{file_name}.xlsx')
outputxlsx.to_excel(f"C:\\Users\\hp\\PycharmProjects\\ArielValvesDatabase\\Result_{file_name}.xlsx", index=False)


# Program runtime output
end_time = time.time()
elapsed_time = end_time - start_time
print(f'Program running time  = {round(elapsed_time)} seconds')