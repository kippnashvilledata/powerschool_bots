# #IMPORT LIBRARIES
# import os
# import re
# # import sys
# # import glob
# import time
# import json
# # import boto3
# import logging
# # import html5lib
# import pandas as pd
# # from time import sleep
# from datetime import datetime, timedelta
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# # from selenium.webdriver.support.select import Select
# # from selenium.webdriver.chrome.options import Options
# # from selenium.common.exceptions import StaleElementReferenceException
# from navigator2 import get_chrome_options, enable_download_headless2
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials

# # Set up Google Sheets credentials and client
# def setup_google_sheets(spreadsheet_name, sheet_name):
#     scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
#     creds = ServiceAccountCredentials.from_json_keyfile_name('/home/KIPPNashvilleData/creds.json', scope)
#     client = gspread.authorize(creds)
#     sheet = client.open(spreadsheet_name).worksheet(sheet_name)
#     return sheet

# # Log to Google Sheets
# def log_to_google_sheets(sheet, message):
#     sheet.append_row([time.strftime("%Y-%m-%d %H:%M:%S"), message])

# # Setup Google Sheets
# spreadsheet_name = 'PythonAnywhereLogs'  # Name of your Google Sheets workbook
# sheet_name = 'ps_ada_adm'  # Name of the sheet within the workbook
# sheet = setup_google_sheets(spreadsheet_name, sheet_name)

# """CREATE VARIABLES"""

# end_year = 2025
# start_year = end_year - 1
# log_to_google_sheets(sheet, f"SY {start_year}-{end_year}")

# #URL variables
# powerschool = "https://sis-sboe.tnk12.gov/admin/pw.html"
# report = "https://sis-sboe.tnk12.gov/admin/reports_engine/report_w_param.html?ac=reports_get_using_ID;repo_ID=PSPRE_ADAADM_ByStudent"
# queue = "https://sis-sboe.tnk12.gov/admin/reportqueue/home.html"


# """Calculate YESTERDAY variable for use in report settings"""
# # Get the current date and time
# current_datetime = datetime.now()

# # Subtract one day to get the previous day
# previous_day = current_datetime - timedelta(days=1)
# """Calculate YESTERDAY variable for use in report settings"""
# # Get the current date and time
# current_datetime = datetime.now()
# # Subtract one day to get the previous day
# previous_day = current_datetime - timedelta(days=1)
# # Format the previous day as MM/DD/YYYY
# yesterday = previous_day.strftime("%m/%d/%Y")

# # Format the previous day as MM/DD/YYYY
# # yesterday = previous_day.strftime("%m/%d/%Y")
# # Adjusting the start_day and end_day to use start_year and end_year
# start_day = previous_day.strftime(f"08/01/{start_year}")
# end_day = yesterday
# # end_day = previous_day.strftime(f"05/31/{end_year}")

# log_to_google_sheets(sheet, f"Start Day: {start_day}")
# log_to_google_sheets(sheet, f"End Day: {end_day}")

# output_file = "ada_adm.txt"
# log_to_google_sheets(sheet, output_file)

# # Configure logging
# logging.basicConfig(
#     filename='/home/KIPPNashvilleData/powerschool_ada_adm.log',
#     level=logging.INFO,
#     format='%(asctime)s:%(levelname)s:%(message)s'
# )



# """Set up Credentials"""
# #create credentials to extract to credentials file later
# # Open JSON file with credentials & save credentials as variables
# log_to_google_sheets(sheet, "Retrieving credentials and variables")
# config_file_path = os.path.join("/home/KIPPNashvilleData/", "credentials_all.json")
# with open(config_file_path) as config_file:
#     data = json.load(config_file)
# config = json.load(open(config_file_path))["powerschool"]
# username = config["username"]
# password = config["password"]
# site = config["site"]
# report = config["report"]
# queue = config["queue"]

# school_menu = config["school_menu"]
# kacpm = config["kacpm"]
# kaghs = config["kaghs"]
# kagms = config["kagms"]

# cue_table = config["cue_table"]
# rpt_1 = config["kaghs_rpt"]
# rpt_2 = config["kagms_rpt"]
# rpt_3 = config["kacpm_rpt"]
# rpt_4 = config["kacpe_rpt"]

# output_file = config["output_file"]
# # download_dir = ["ps_directory"]

# log_to_google_sheets(sheet, "Credentials retrieved")
# # # username = "cdiehl"
# # # password = "r0mp_f45t_h3ckleR!"
# download_dir = "/home/KIPPNashvilleData/ps_downloads/"

# log_to_google_sheets(sheet, "Starting Chromedriver set up")

# chrome_options = get_chrome_options(download_dir)
# driver = webdriver.Chrome(options=chrome_options)
# # enable_download_headless(driver, download_dir)
# # Print Chrome options for debugging
# log_to_google_sheets(sheet, "Chrome Options:")
# for option in chrome_options.arguments:
#     log_to_google_sheets(sheet, option)

# #Initialize the Chrome WebDriver with the specified options
# driver = webdriver.Chrome(options=chrome_options)
# log_to_google_sheets(sheet, "Chromedriver set up and intialized")
# # function to handle setting up headless download
# enable_download_headless2(driver, download_dir)

# # Navigate to the PowerSchool Login Page
# driver.get(site)
# # log_to_google_sheets(sheet, f"Site Name: {driver.title}")
# WebDriverWait(driver, 60).until(EC.title_is("PowerSchool"))
# # Once the title is "PowerSchool", send the username
# driver.find_element(By.ID, "fieldUsername").send_keys(username)
# #Enter the remaining Credentials and Login
# driver.find_element(By.ID, "fieldPassword").send_keys(password)
# time.sleep(10)
# driver.find_element(By.ID, "btnEnter").click()
# time.sleep(25)
# log_to_google_sheets(sheet, f"Site Name: {driver.title}")
# WebDriverWait(driver, 60).until(EC.title_is("Start Page"))

# """1ST RUN OF THE REPORT FOR KACPE"""
# # Go to the Report Page
# driver.get(report)
# log_to_google_sheets(sheet, f"Site Name: {driver.title}")

# """ENTER REPORT DATES"""
# # Wait for the Report Page to load
# WebDriverWait(driver, 60).until(EC.title_is("ADA/ADM by Student Report"))

# # Enter the report dates
# start_date = driver.find_element(By.NAME, "param_startdate")
# start_date.send_keys(Keys.CONTROL + "a")
# start_date.send_keys(Keys.DELETE)
# start_date.send_keys(start_day)

# end_date = driver.find_element(By.NAME, "param_enddate")
# end_date.send_keys(Keys.CONTROL + "a")
# end_date.send_keys(Keys.DELETE)
# end_date.send_keys(end_day)

# """SUBMIT REPORT"""
# # Click the report submit button to run the report
# driver.find_element(By.ID, "btnSubmit").click()

# # log to check that Report Queue has loaded
# log_to_google_sheets(sheet, f"Site Name: {driver.title}")

# """2ND RUN OF THE REPORT FOR KACPM"""
# #Switch to KACPM
# school_picker = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, school_menu)))
# school_picker.click()

# # Locate the desired option and click it
# kacpm_school = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, kacpm)))
# kacpm_school.click()
# # Wait for Start Page to load to confirm school switch is successful
# WebDriverWait(driver, 60).until(EC.title_is("Start Page"))

# #Run the Report again by returning to the ADA/ADM report page
# driver.get(report)
# log_to_google_sheets(sheet, f"Site Name: {driver.title}")

# # Wait for the Correct page title to be "ADA/ADM by Student Report"
# WebDriverWait(driver, 60).until(EC.title_is("ADA/ADM by Student Report"))

# # Enter the report dates
# start_date = driver.find_element(By.NAME, "param_startdate")
# start_date.send_keys(Keys.CONTROL + "a")
# start_date.send_keys(Keys.DELETE)
# start_date.send_keys(start_day)

# end_date = driver.find_element(By.NAME, "param_enddate")
# end_date.send_keys(Keys.CONTROL + "a")
# end_date.send_keys(Keys.DELETE)
# end_date.send_keys(end_day)

# #Click the submit button to run the report again
# driver.find_element(By.ID, "btnSubmit").click()

# WebDriverWait(driver, 60).until(EC.title_is("Report Queue - My Jobs"))

# """3RD RUN OF THE REPORT FOR KAGMS"""
# #Switch to KAGMS
# school_picker = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, school_menu)))
# school_picker.click()

# # Locate the desired option and click it
# kagms_school = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, kagms)))
# kagms_school.click()
# # Wait for Start Page to load to confirm school switch is successful
# WebDriverWait(driver, 60).until(EC.title_is("Start Page"))

# #Run the Report again by returning to the ADA/ADM report page
# driver.get(report)
# log_to_google_sheets(sheet, f"Site Name: {driver.title}")

# # Wait for the Correct page title to be "ADA/ADM by Student Report"
# WebDriverWait(driver, 60).until(EC.title_is("ADA/ADM by Student Report"))

# # Enter the report dates
# start_date = driver.find_element(By.NAME, "param_startdate")
# start_date.send_keys(Keys.CONTROL + "a")
# start_date.send_keys(Keys.DELETE)
# start_date.send_keys(start_day)

# end_date = driver.find_element(By.NAME, "param_enddate")
# end_date.send_keys(Keys.CONTROL + "a")
# end_date.send_keys(Keys.DELETE)
# end_date.send_keys(end_day)

# #Click the submit button to run the report again
# driver.find_element(By.ID, "btnSubmit").click()

# WebDriverWait(driver, 60).until(EC.title_is("Report Queue - My Jobs"))

# """4TH RUN OF THE REPORT FOR KAGHS"""
# #Switch to KAGHS
# school_picker = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, school_menu)))
# school_picker.click()

# # Locate the desired option and click it
# kaghs_school = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, kaghs)))
# kaghs_school.click()
# # Wait for Start Page to load to confirm school switch is successful
# WebDriverWait(driver, 60).until(EC.title_is("Start Page"))

# #Run the Report again by returning to the ADA/ADM report page
# driver.get(report)
# log_to_google_sheets(sheet, f"Site Name: {driver.title}")

# # Wait for the Correct page title to be "ADA/ADM by Student Report"
# WebDriverWait(driver, 60).until(EC.title_is("ADA/ADM by Student Report"))

# # Enter the report dates
# start_date = driver.find_element(By.NAME, "param_startdate")
# start_date.send_keys(Keys.CONTROL + "a")
# start_date.send_keys(Keys.DELETE)
# start_date.send_keys(start_day)

# end_date = driver.find_element(By.NAME, "param_enddate")
# end_date.send_keys(Keys.CONTROL + "a")
# end_date.send_keys(Keys.DELETE)
# end_date.send_keys(end_day)

# #Click the submit button to run the report again
# driver.find_element(By.ID, "btnSubmit").click()

# WebDriverWait(driver, 60).until(EC.title_is("Report Queue - My Jobs"))

# log_to_google_sheets(sheet, "Report queue - My Jobs")

# # Time delay to ensure report generation and download
# log_to_google_sheets(sheet, "Waiting for Reports to Generate")
# time.sleep(10)

# log_to_google_sheets(sheet, "Checking for Downloaded Reports")
# # Check if the files have been downloaded
# # For each file, check for its presence in the download directory
# downloaded_files = [f for f in os.listdir(download_dir) if f.endswith(".txt")]

# for file in downloaded_files:
#     log_to_google_sheets(sheet, f"Downloaded file: {file}")

# log_to_google_sheets(sheet, "Script completed.")
# # End of script
# driver.quit()



#IMPORT LIBRARIES
import os
import re
# import sys
# import glob
import time
import json
# import boto3
import logging
# import html5lib
import pandas as pd
# from time import sleep
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.select import Select
# from selenium.webdriver.chrome.options import Options
# from selenium.common.exceptions import StaleElementReferenceException
from navigator2 import get_chrome_options, enable_download_headless2
import gspread
from oauth2client.service_account import ServiceAccountCredentials

"""CREATE VARIABLES"""

end_year = 2025
start_year = end_year - 1
print(f"SY {start_year}-{end_year}")

#URL variables
powerschool = "https://sis-sboe.tnk12.gov/admin/pw.html"
report = "https://sis-sboe.tnk12.gov/admin/reports_engine/report_w_param.html?ac=reports_get_using_ID;repo_ID=PSPRE_ADAADM_ByStudent"
queue = "https://sis-sboe.tnk12.gov/admin/reportqueue/home.html"


"""Calculate YESTERDAY variable for use in report settings"""
# Get the current date and time
current_datetime = datetime.now()

# Subtract one day to get the previous day
previous_day = current_datetime - timedelta(days=1)
"""Calculate YESTERDAY variable for use in report settings"""
# Get the current date and time
current_datetime = datetime.now()
# Subtract one day to get the previous day
previous_day = current_datetime - timedelta(days=1)
# Format the previous day as MM/DD/YYYY
yesterday = previous_day.strftime("%m/%d/%Y")


# Format the previous day as MM/DD/YYYY
# yesterday = previous_day.strftime("%m/%d/%Y")
# Adjusting the start_day and end_day to use start_year and end_year
start_day = previous_day.strftime(f"08/01/{start_year}")
end_day = yesterday
# end_day = previous_day.strftime(f"05/31/{end_year}")

print("Start Day:", start_day)
print("End Day:", end_day)

output_file = "ada_adm.txt"
print(output_file)

# Configure logging
logging.basicConfig(
    filename='/home/KIPPNashvilleData/powerschool_ada_adm.log',
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(message)s'
)

# Set up Google Sheets credentials and client
def setup_google_sheets(spreadsheet_name, sheet_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('/home/KIPPNashvilleData/creds.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open(spreadsheet_name).worksheet(sheet_name)
    return sheet

# Log to Google Sheets
def log_to_google_sheets(sheet, message):
    sheet.append_row([time.strftime("%Y-%m-%d %H:%M:%S"), message])

# Setup Google Sheets
spreadsheet_name = 'PythonAnywhereLogs'  # Name of your Google Sheets workbook
sheet_name = 'ps_ada_adm'  # Name of the sheet within the workbook
sheet = setup_google_sheets(spreadsheet_name, sheet_name)

"""Set up Credentials"""
#create credentials to extract to credentials file later
# Open JSON file with credentials & save credentials as variables
print("Retrieving credentials and variables")
config_file_path = os.path.join("/home/KIPPNashvilleData/", "credentials_all.json")
with open(config_file_path) as config_file:
    data = json.load(config_file)
config = json.load(open(config_file_path))["powerschool"]
username = config["username"]
password = config["password"]
site = config["site"]
report = config["report"]
queue = config["queue"]

school_menu = config["school_menu"]
kacpm = config["kacpm"]
kaghs = config["kaghs"]
kagms = config["kagms"]

cue_table = config["cue_table"]
rpt_1 = config["kaghs_rpt"]
rpt_2 = config["kagms_rpt"]
rpt_3 = config["kacpm_rpt"]
rpt_4 = config["kacpe_rpt"]


output_file = config["output_file"]
# download_dir = ["ps_directory"]

print("Credentials retrieved")
# # username = "cdiehl"
# # password = "r0mp_f45t_h3ckleR!"
download_dir = "/home/KIPPNashvilleData/ps_downloads/"

print("Starting Chromedriver set up")

chrome_options = get_chrome_options(download_dir)
driver = webdriver.Chrome(options=chrome_options)
# enable_download_headless(driver, download_dir)
# Print Chrome options for debugging
print("Chrome Options:")
for option in chrome_options.arguments:
    print(option)

#Initialize the Chrome WebDriver with the specified options
driver = webdriver.Chrome(options=chrome_options)
print("Chromedriver set up and intialized")
# function to handle setting up headless download
enable_download_headless2(driver, download_dir)

# Navigate to the PowerSchool Login Page
driver.get(site)
# print(f"Site Name: {driver.title}")
WebDriverWait(driver, 60).until(EC.title_is("PowerSchool"))
# Once the title is "PowerSchool", send the username
driver.find_element(By.ID, "fieldUsername").send_keys(username)
#Enter the remaining Credentials and Login
driver.find_element(By.ID, "fieldPassword").send_keys(password)
time.sleep(10)
driver.find_element(By.ID, "btnEnter").click()
time.sleep(25)
print(f"Site Name: {driver.title}")
WebDriverWait(driver, 60).until(EC.title_is("Start Page"))

"""1ST RUN OF THE REPORT FOR KACPE"""
# Go to the Report Page
driver.get(report)
print(f"Site Name: {driver.title}")

"""ENTER REPORT DATES"""
# Wait for the Report Page to load
WebDriverWait(driver, 60).until(EC.title_is("ADA/ADM by Student Report"))

# Enter the report dates
start_date = driver.find_element(By.NAME, "param_startdate")
start_date.send_keys(Keys.CONTROL + "a")
start_date.send_keys(Keys.DELETE)
start_date.send_keys(start_day)

end_date = driver.find_element(By.NAME, "param_enddate")
end_date.send_keys(Keys.CONTROL + "a")
end_date.send_keys(Keys.DELETE)
end_date.send_keys(end_day)

"""SUBMIT REPORT"""
# Click the report submit button to run the report
driver.find_element(By.ID, "btnSubmit").click()

# Print Site to check that Report Queue has loaded
print(f"Site Name: {driver.title}")

"""2ND RUN OF THE REPORT FOR KACPM"""
#Switch to KACPM
school_picker = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, school_menu)))
school_picker.click()

# Locate the desired option and click it
kacpm_school = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, kacpm)))
kacpm_school.click()
# Wait for Start Page to load to confirm school switch is successful
WebDriverWait(driver, 60).until(EC.title_is("Start Page"))

#Run the Report again by returning to the ADA/ADM report page
driver.get(report)
print(f"Site Name: {driver.title}")

# Wait for the Correct page title to be "ADA/ADM by Student Report"
WebDriverWait(driver, 60).until(EC.title_is("ADA/ADM by Student Report"))

# Enter the report dates
start_date = driver.find_element(By.NAME, "param_startdate")
start_date.send_keys(Keys.CONTROL + "a")
start_date.send_keys(Keys.DELETE)
start_date.send_keys(start_day)

end_date = driver.find_element(By.NAME, "param_enddate")
end_date.send_keys(Keys.CONTROL + "a")
end_date.send_keys(Keys.DELETE)
end_date.send_keys(end_day)

#Click the submit button to run the report again
driver.find_element(By.ID, "btnSubmit").click()

WebDriverWait(driver, 60).until(EC.title_is("Report Queue - My Jobs"))

"""3RD RUN OF THE REPORT FOR KAGMS"""
#Switch to KAGMS
school_picker = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, school_menu)))
school_picker.click()

# Locate the desired option and click it
kagms_school = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, kagms)))
kagms_school.click()

#Run the Report again
WebDriverWait(driver, 60).until(EC.title_is("Start Page"))
driver.get(report)
print(f"Site Name: {driver.title}")
WebDriverWait(driver, 60).until(EC.title_is("ADA/ADM by Student Report"))

start_date = driver.find_element(By.NAME, "param_startdate")
start_date.send_keys(Keys.CONTROL + "a")
start_date.send_keys(Keys.DELETE)
start_date.send_keys(start_day)

end_date = driver.find_element(By.NAME, "param_enddate")
end_date.send_keys(Keys.CONTROL + "a")
end_date.send_keys(Keys.DELETE)
end_date.send_keys(end_day)
driver.find_element(By.ID, "btnSubmit").click()
WebDriverWait(driver, 60).until(EC.title_is("Report Queue - My Jobs"))


"""4TH RUN OF THE REPORT FOR KAGHS"""
#Switch to KAGHS
school_picker = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, school_menu)))
school_picker.click()

# Locate the desired option and click it
kagms_school = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, kaghs)))
kagms_school.click()

#Run the Report again
WebDriverWait(driver, 60).until(EC.title_is("Start Page"))
driver.get(report)
print(f"Site Name: {driver.title}")
WebDriverWait(driver, 60).until(EC.title_is("ADA/ADM by Student Report"))

start_date = driver.find_element(By.NAME, "param_startdate")
start_date.send_keys(Keys.CONTROL + "a")
start_date.send_keys(Keys.DELETE)
start_date.send_keys(start_day)

end_date = driver.find_element(By.NAME, "param_enddate")
end_date.send_keys(Keys.CONTROL + "a")
end_date.send_keys(Keys.DELETE)
end_date.send_keys(end_day)
driver.find_element(By.ID, "btnSubmit").click()
WebDriverWait(driver, 60).until(EC.title_is("Report Queue - My Jobs"))


"""Function and Loop to Load all 4 reports in queue"""
# Define the XPaths for the cells in each row and the reload button
cell_xpaths = [
    '//*[@id="content-main"]/div[3]/table/tbody/tr[1]/td[6]',
    '//*[@id="content-main"]/div[3]/table/tbody/tr[2]/td[6]',
    '//*[@id="content-main"]/div[3]/table/tbody/tr[3]/td[6]',
    '//*[@id="content-main"]/div[3]/table/tbody/tr[4]/td[6]'
]
reload_button_id = "prReloadButton"

# Function to check the text of a cell
def check_cell(cell_xpath):
    cell = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, cell_xpath)))
    return cell.text

# Main loop to check each cell's text and click the button if needed
all_complete = False
while not all_complete:
    all_complete = True  # Assume all are complete unless we find one that isn't
    for cell_xpath in cell_xpaths:
        cell_text = check_cell(cell_xpath)

        if cell_text.lower() == "running":
            print(f"Process in cell {cell_xpath} is running. Clicking the reload button.")
            reload_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, reload_button_id)))
            reload_button.click()
            all_complete = False  # Found a running process, so we need to keep checking
            break
        elif cell_text.lower() != "completed  view":
            print(f"Unexpected cell text in {cell_xpath}: {cell_text}")
            all_complete = False
            break

    if not all_complete:
        print("Waiting for 30 seconds before checking again.")
        time.sleep(30)

if all_complete:
    print("All processes are complete.")

"""Get KAGHS rpt_1 to Dataframe"""
rpt_1 = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, rpt_1)))
rpt_1.click()

#Downloads the Global Repoart
table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, cue_table)))
# Get the HTML of the table
table_html = table.get_attribute('outerHTML')

# Use pandas to read the table HTML into a DataFrame
dfs = pd.read_html(table_html, header=0)
kaghs_df = dfs[0]

# Print the DataFrame
print(kaghs_df.head(5))
print(kaghs_df.shape)

#Go back to report queue
driver.get(queue)

"""Get KAGMS rpt_2 to Dataframe"""
#Get KACPM Report Page
rpt_2 = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, rpt_2)))
rpt_2.click()

#Downloads the KACPM Repoart
table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, cue_table)))
# Get the HTML of the table
table_html = table.get_attribute('outerHTML')

# Use pandas to read the table HTML into a DataFrame
dfs = pd.read_html(table_html, header=0)
kagms_df = dfs[0]  # If there's only one table, it will be the first element in the list

# Print the DataFrame
print(kagms_df.head(5))
print(kagms_df.shape)

# Go back to report queue
driver.get(queue)

# Get KACPM report
rpt_3 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, rpt_3)))
rpt_3.click()

#Downloads the KACPE Repoart
table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, cue_table)))
# Get the HTML of the table
table_html = table.get_attribute('outerHTML')

# Use pandas to read the table HTML into a DataFrame
dfs = pd.read_html(table_html, header=0)
kacpm_df = dfs[0]  # If there's only one table, it will be the first element in the list

# Print the DataFrame
print(kacpm_df.head(5))
print(kacpm_df.shape)

# Go back to report queue
driver.get(queue)

# Get KACPM report
rpt_4 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, rpt_4)))
rpt_4.click()

#Downloads the KACPE Repoart
table = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, cue_table)))
# Get the HTML of the table
table_html = table.get_attribute('outerHTML')

# Use pandas to read the table HTML into a DataFrame
dfs = pd.read_html(table_html, header=0)
kacpe_df = dfs[0]  # If there's only one table, it will be the first element in the list

# Print the DataFrame
print(kacpe_df.head(5))
print(kacpe_df.shape)


#Close the driver
driver.close()

"""Remove summary bottom rows from reports"""
dfs = [kaghs_df, kagms_df, kacpm_df, kacpe_df]
# Loop through the list and apply the operation to each DataFrame
for i in range(len(dfs)):
    dfs[i] = dfs[i].iloc[:-3]

# Print the modified DataFrames to verify changes
for i, df in enumerate(dfs):
    print(f"Shape of DataFrame {i+1}:{df.shape}")
    print(f"Tail of DataFrame {i+1}:")
    print(df.tail(3))
    print()  # For better readability


"""Concatenate the reports into one Dataframe"""

concatenated_df = pd.concat(dfs, ignore_index=True)

print(f"Shape of DataFrame: {concatenated_df.shape}")
print("Head of DataFrame:")
print(concatenated_df.head(5))
print()  # For better readability


# Drop the first two columns

concatenated_df = concatenated_df.drop(concatenated_df.columns[:2], axis=1)
concatenated_df['end_year'] = end_year
print(f"Shape of DataFrame: {concatenated_df.shape}")
print(f"Head of DataFrame:")
print(concatenated_df.head(5))
print()  # For better readability


# Define a function to remove the pattern ' (A)' from the grade column
def clean_numeric_data(value):
    return re.sub(r'\s*\([A-Za-z]\)', '', value)


# Apply the function to the grade column
concatenated_df['Grade(Track)'] = concatenated_df['Grade(Track)'].astype(str).apply(clean_numeric_data)
concatenated_df.rename(columns={'Grade(Track)': 'Grade'}, inplace=True)

# Save DataFrame to a a csv or tab-delimited text file
concatenated_df.to_csv(download_dir + output_file, index=False, quotechar='"')
print(f"{output_file} saved to {download_dir}")



