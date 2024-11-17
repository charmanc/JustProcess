# Import necessary libraries
from selenium import webdriver # For browser automation (web scraping)
from selenium.webdriver.common.by import By # For locating elements on the page
from selenium.webdriver.support.ui import WebDriverWait # For waiting for elements to load
from selenium.webdriver.support import expected_conditions as EC # For checking conditions
from selenium.webdriver.common.keys import Keys # For keyboard actions (like sending keys)

import os # For interacting with the operating system (file paths, directories)
import glob # For file searching (glob pattern matching)

import pytesseract # For OCR (Optical Character Recognition) functionality
from PIL import Image # For opening and processing images
import re # For regular expressions (pattern matching in text)

import time # For time-related functions (delays, waiting)

# import shutil
# import sys
# import threading

# Set the waiting time according to the internet speed!
waiting_time = 1 # in sec

# Login credentials
username = input("Username: ")
password = input("Password")

# Initialize Chrome WebDriver for automating browser tasks
driver = webdriver.Chrome()

# Open the Justsnap dashboard login page
driver.get("https://cb-123-dashboard.justsnap.eu/login")

# Locate the necessary input fields by inspecting the webpage, the ids are written there
username_field = driver.find_element(by='id', value = "input-13")
password_field = driver.find_element(by='id', value = "input-14")
market_dropdown_trigger = WebDriverWait(driver = driver, timeout = 10).until(EC.element_to_be_clickable((By.ID, "input-16")))
login = driver.find_element(By.CLASS_NAME, "v-btn__content")

# Input the username and password
username_field.send_keys(username)
password_field.send_keys(password)

# Wait for the dropdown of markets to be clickable and loop through to select "DACH"
market_dropdown_trigger.click()
markets = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='v-list-item__content']//div")))
for market in markets:
    if market.text == "DACH":
        market.click()
        break

# Click the login button to submit the login form
login.click()

# Wait until the next page has fully loaded and the reference number input field is available
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "input-102")))
print('Logged in successfully')

def find_refnum(upload_path):
    cwd = os.getcwd()
    # Open the image file and explicitly close it after reading
    with Image.open(upload_path) as image:
        # Set path to Tesseract executable
        pytesseract.pytesseract.tesseract_cmd = cwd + "/Tesseract-OCR/tesseract.exe"
        text = pytesseract.image_to_string(image) # Extract text from the image

        # Use regex to find the reference number in the OCR output
        match = re.search(r"Referenznummer:[ \t]*(\S{10})", text) # Returns None if not found
    return match



def enter_refnum():
    cwd = os.getcwd() # Get the current working directory
    processed_files = set()  # Initialize a set to keep track of processed files (avoiding reprocessing)

    while True: # Keep checking for new files in an infinite loop
        # Wait for user input before starting the next round of checking
        # input("Press Enter to check for new files...")
        uploads = glob.glob(cwd+"/uploads/*") # Search for files in the 'uploads' folder
        if uploads: # If there are any new files
            for upload_path in uploads: # Iterate through each file found
                if upload_path in processed_files: # Skip already processed files
                    print(f"Skipping processed file: {upload_path}")
                    continue # Move to the next file

                try:
                    match = find_refnum(upload_path)
                    if match:
                        referenznummer = None # Initialize to clear previous reference numbers
                        referenznummer = match.group(1) # Get the captured reference number
                        print("Referenznummer:", referenznummer)
                    else:
                        processed_files.add(upload_path) # Mark the file as processed
                        input("Cannot be read, try uploading the image again and press Enter!") # ?????????????????
                        continue
                    
                    max_retries = 2
                    attempt = 0
                    while attempt < max_retries:
                        # Find the reference number input field on the page and clear if there is anything written
                        reference_field = driver.find_element(By.ID, "input-102")
                        reference_field.send_keys(Keys.CONTROL + 'a') # Select all text in the input field
                        reference_field.send_keys(Keys.DELETE) # Delete the selected text
                        
                        # Enter the new reference number
                        reference_field.send_keys(referenznummer) # Enter the OCR-detected reference number

                        # Find and click the "SEARCH" button to search with the reference number
                        buttons = driver.find_elements(By.CLASS_NAME, "v-btn__content")
                        for button in buttons:
                            if button.text == "SEARCH":
                                button.click() 
                                break # Exit the loop after clicking the button
                        try:
                            # Wait for any error message regarding the reference number
                            if WebDriverWait(driver, waiting_time).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "v-snack__content"))): # Returns error if the error message is not shown
                                if attempt==0: # Try replacing 'O' with '0' on the first try
                                    referenznummer = referenznummer.replace('O', '0')
                                elif attempt==1: # Try replacing '0' with 'O' on the second try
                                    referenznummer = referenznummer.replace('0', 'O')
                                print(f'Trying new reference number:{referenznummer}')
                                attempt+=1
                                if attempt > max_retries:
                                    input('There could be a misinterpretation, please correct the referenznummer and click Enter!')
                        except:
                            # If no error message appears (timeout), assume the reference number is fine
                            print("No error detected with the reference number.")
                            break # Break if referenznummer is correct
                    
                    # Find and click the "AGENT UPLOAD FILE" button to upload a file
                    WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "clipboard")))
                    
                    buttons = driver.find_elements(By.CLASS_NAME, "v-btn__content")
                    for button in buttons:
                        # print(button.text)
                        if button.text.strip() == "AGENT UPLOAD FILE": # # Look for the "AGENT UPLOAD FILE" button (strip any leading/trailing spaces)
                            button.click()
                            break # Exit loop after finding and clicking the button

                    # Upload the image directly using the <input type="file"> element on the webpagee
                    file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']") # the CSS_SELECTOR was likely more efficient and straightforward than the XPath
                    try:
                        file_input.send_keys(upload_path) # Upload the file by sending its path to the file input element
                        print("File uploaded successfully")
                        processed_files.add(upload_path) # Mark the file as processed
                        # # delete the file from the uploads folder DOES NOT WORK (BEING USED BY ANOTHER PROCESS)
                        # os.remove(upload_path)
                        # print(f"The image {upload_path} has been deleted.")
                    except Exception as e:
                        print(f'File cannot be uploaded: {e}!')
                
                    # Prevent browser from closing immediately
                    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, "input-102"))) # Wait for the reference number input field to ensure the page is still active
            
                except PermissionError as e:
                    print(f"PermissionError: {e} - The file might be in use by another process. Retrying...")

            # Wait for 2 seconds before checking for new files again
            time.sleep(2)



enter_refnum() # it runs on the main thread

# Prevent the browser from closing immediately by keeping the main thread alive
# input("Press Enter to exit the program and close the browser...")

# Close the browser once the user chooses to exit
# driver.quit()
