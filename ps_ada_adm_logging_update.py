# Annual update: Update end year
# Maintenance Checks: powerschool, report, and queue urls

"""IMPORT LIBRARIES"""
import os
import re
import time
import json
# import boto3
import logging
import pandas as pd
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

# URL variables
powerschool = "https://sis-sboe.tnk12.gov/admin/pw.html"
report = "https://sis-sboe.tnk12.gov/admin/reports_engine/report_w_param.html?ac=reports_get_using_ID;repo_ID=PSPRE_ADAADM_ByStudent"
queue = "https://sis-sboe.tnk12.gov/admin/reportqueue/home.html"

# Date variables
end_year = 2025
start_year = end_year - 1
current_datetime = datetime.now()
previous_day = current_datetime - timedelta(days=1)
yesterday = previous_day.strftime("%m/%d/%Y")
start_day = previous_day.strftime(f"08/01/{start_year}")
end_day = yesterday
print(f"SY {start_year}-{end_year}")
print("Start Day:", start_day)
print("End Day:", end_day)


# # File Name
# output_file = "ada_adm.txt"
# print(output_file)

"""CONFIGURE logging & CREATE Functions"""
# Configure logging
logging.basicConfig(
    filename='/home/KIPPNashvilleData/powerschool/powerschool_ada_adm.log',
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


# # Log to Google Sheets
# def log_to_google_sheets(sheet, message):
#     sheet.append_row([time.strftime("%Y-%m-%d %H:%M:%S"), message])

# Log to Google Sheets and log file
def log_message(sheet, message):
    # Log to Google Sheets
    sheet.append_row([time.strftime("%Y-%m-%d %H:%M:%S"), message])

    # Log to the local log file
    logging.info(message)

# Setup Google Sheets
spreadsheet_name = 'PythonAnywhereLogs'  # Name of your Google Sheets workbook
sheet_name = 'ps_ada_adm'  # Name of the sheet within the workbook
sheet = setup_google_sheets(spreadsheet_name, sheet_name)
message = "INFO: Google Sheets setup complete. Starting the script."
print(message)
log_message(sheet, message)

"""Set up Credentials"""
#create credentials to extract to credentials file later
# Open JSON file with credentials & save credentials as variables
message = "INFO: Retrieving credentials and variables"
print(message)
log_message(sheet, message)

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
message = "INFO: Credentials retrieved"
print(message)
log_message(sheet, message)

download_dir = "/home/KIPPNashvilleData/ps_downloads/"
message = "INFO: Starting ChromeDriver set up"
print(message)
log_message(sheet, message)

# Log variables to Google Sheets & Log file
log_message(sheet, f"INFO: Start of data extraction for SY {start_year}-{end_year}")
log_message(sheet, f"INFO: Start Day:{start_day}")
log_message(sheet, f"INFO: End Day: {end_day}")

"""Set up Chrome Driver"""
chrome_options = get_chrome_options(download_dir)
driver = webdriver.Chrome(options=chrome_options)
# enable_download_headless(driver, download_dir)
# Print Chrome options for debugging
message = "INFO: Chrome Options for Troubleshooting:"
print(message)
log_message(sheet, message)
for option in chrome_options.arguments:
    print(option)
    log_message(sheet, option)

#Initialize the Chrome WebDriver with the specified options
driver = webdriver.Chrome(options=chrome_options)
message = "INFO: Chromedrive set up and intialized"
print(message)
log_message(sheet, message)
# function to handle setting up headless download
enable_download_headless2(driver, download_dir)


"""Beging Accessing PowerSchool"""
# Navigate to the PowerSchool Login Page
driver.get(site)
message = "INFO: Site Name is {driver.title}"
print(message)
log_message(sheet, message)

WebDriverWait(driver, 60).until(EC.title_is("PowerSchool"))
# Once the title is "PowerSchool", send the username
driver.find_element(By.ID, "fieldUsername").send_keys(username)

#Enter the remaining Credentials and Login
driver.find_element(By.ID, "fieldPassword").send_keys(password)
time.sleep(10)
driver.find_element(By.ID, "btnEnter").click()
time.sleep(25)
message = f"INFO Site Name is {driver.title}"
print(message)
log_message(sheet, message)
WebDriverWait(driver, 60).until(EC.title_is("Start Page"))

"""1ST RUN OF THE REPORT FOR KACPE"""
# Go to the Report Page
driver.get(report)
message = f"INFO: Site Name is {driver.title}"
print(message)
log_message(sheet, message)

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
message = f"INFO: Site Name is {driver.title}"
print(message)
log_message(sheet, message)

"""2ND RUN OF THE REPORT FOR KACPM"""
#Switch to KACPM
school_picker = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, school_menu)))
school_picker.click()

# Locate the desired option and click it
kacpm_school = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, kacpm)))
kacpm_school.click()
# Wait for Start Page to load to confirm school switch is successful
WebDriverWait(driver, 60).until(EC.title_is("Start Page"))

#Run the Report again
WebDriverWait(driver, 60).until(EC.title_is("Start Page"))
message = f"INFO: Site Name is {driver.title}"
print(message)
log_message(sheet, message)
driver.get(report)

# Wait for the Correct page title to be "ADA/ADM by Student Report"
message = f"INFO: Site Name is {driver.title}"
print(message)
log_message(sheet, message)
WebDriverWait(driver, 60).until(EC.title_is("ADA/ADM by Student Report"))

message = f"INFO: Site Name is {driver.title}"
print(message)
log_message(sheet, message)

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
message = f"INFO: Site Name is {driver.title}"
print(message)
log_message(sheet, message)
driver.get(report)

# Wait for the Correct page title to be "ADA/ADM by Student Report"
message = f"INFO: Site Name is {driver.title}"
print(message)
log_message(sheet, message)
WebDriverWait(driver, 60).until(EC.title_is("ADA/ADM by Student Report"))

message = f"INFO: Site Name is {driver.title}"
print(message)
log_message(sheet, message)

# Wait for the Correct page title to be "ADA/ADM by Student Report"
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
message = f"INFO: Site Name is {driver.title}"
print(message)
log_message(sheet, message)
driver.get(report)

# Wait for the Correct page title to be "ADA/ADM by Student Report"
message = f"INFO: Site Name is {driver.title}"
print(message)
log_message(sheet, message)
WebDriverWait(driver, 60).until(EC.title_is("ADA/ADM by Student Report"))

message = f"INFO: Site Name is {driver.title}"
print(message)
log_message(sheet, message)

# Wait for the Correct page title to be "ADA/ADM by Student Report"
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

all_complete = False
max_retries = 10  # Set a max number of retries
retry_count = 0

while not all_complete and retry_count < max_retries:
    all_complete = True
    retry_count += 1

    for cell_xpath in cell_xpaths:
        cell_text = check_cell(cell_xpath)

        if cell_text.lower() == "running":
            message = f"INFO: Process in cell {cell_xpath} is running. Clicking the reload button."
            print(message)
            log_message(sheet, message)
            reload_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, reload_button_id)))
            reload_button.click()
            all_complete = False
            break
        elif cell_text.lower() != "completed  view":
            message = f"WARNING: Unexpected cell text in {cell_xpath}: {cell_text}"
            print(message)
            log_message(sheet, message)
            all_complete = False
            break

    if not all_complete:
        message = "INFO: Waiting for 30 seconds before checking again."
        print(message)
        log_message(sheet, message)
        time.sleep(30)

if all_complete:
    message = "INFO: All processes are complete."
    print(message)
    log_message(sheet, message)
else:
    message = "ERROR: Max retries reached, but not all processes completed."
    print(message)
    log_message(sheet, message)



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
rows, columns = kaghs_df.shape
# Print the DataFramer
message =  f"INFO: KAGHS DataFrame has {columns} Columns and {rows} Rows"
print(kaghs_df.head(5))
# print(kaghs_df.shape)
print(message)
log_message(sheet, message)

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

rows, columns = kagms_df.shape
# Print the DataFramer
message =  f"INFO: KAGMS DataFrame has {columns} Columns and {rows} Rows"
print(kagms_df.head(5))
# print(kagms_df.shape)
print(message)
log_message(sheet, message)


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

rows, columns = kacpm_df.shape
# Print the DataFramer
message =  f"INFO: KACPM DataFrame has {columns} Columns and {rows} Rows"
print(kacpm_df.head(5))
# print(kacpm_df.shape)
print(message)
log_message(sheet, message)

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

rows, columns = kacpe_df.shape
# Print the DataFramer
message =  f"INFO: KACPE DataFrame has {columns} Columns and {rows} Rows"
print(kacpe_df.head(5))
# print(kacpe_df.shape)
print(message)
log_message(sheet, message)

#Close the driver
driver.close()

"""Remove summary bottom rows from reports"""
dfs = [kaghs_df, kagms_df, kacpm_df, kacpe_df]
# Loop through the list and apply the operation to each DataFrame
for i in range(len(dfs)):
    dfs[i] = dfs[i].iloc[:-3]

# Print the modified DataFrames to verify changes
for i, df in enumerate(dfs):
    message = f"INFO: Shape of DataFrame {i+1}:{df.shape}"
    print(message)
    log_message(sheet, message)
    print(f"Tail of DataFrame {i+1}:")
    print(df.tail(3))
    print()  # For better readability

"""Concatenate the reports into one Dataframe"""

concatenated_df = pd.concat(dfs, ignore_index=True)

print(f"Shape of DataFrame: {concatenated_df.shape}")
print("Head of DataFrame:")
print(concatenated_df.head(5))
print()  # For better readability

rows, columns = concatenated_df.shape
message = f"INFO: Concatenated DataFrame has {columns} Columns and {rows} Rows"
print(message)
log_message(sheet, message)

# Drop the first two columns

concatenated_df = concatenated_df.drop(concatenated_df.columns[:2], axis=1)
concatenated_df['end_year'] = end_year
rows, columns = concatenated_df.shape
message = f"INFO: DataFrame after dropping first two columns has {columns} Columns and {rows}."
print(message)
log_message(sheet, message)
print(f"Head of DataFrame:")
print(concatenated_df.head(5))
print()  # For better readability



# Define a function to remove the pattern '(A)' from the grade column
def clean_numeric_data(value):
    return re.sub(r'\s*\([A-Za-z]\)', '', value)


# Apply the function to the grade column
concatenated_df['Grade(Track)'] = concatenated_df['Grade(Track)'].astype(str).apply(clean_numeric_data)
concatenated_df.rename(columns={'Grade(Track)': 'Grade'}, inplace=True)

rows, columns = concatenated_df.shape
message = f"INFO: DataFrame after cleaning has {columns} Columns and {rows} Rows"
print(message)
log_message(sheet, message)

# Save DataFrame to a a csv or tab-delimited text file
concatenated_df.to_csv(download_dir + output_file, index=False, quotechar='"')
message = f"INFO: {output_file} saved to {download_dir}"
print(message)
log_message(sheet, message)

message = "INFO: All tasks completed successfully. Script has ended."
print(message)
log_message(sheet, message)