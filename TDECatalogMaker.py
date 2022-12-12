"""TDECatalogMaker.py"""

"""
This module takes in:

1) 'TDE_List.tsv' file with columns: ['TDE Name','TDE Discovery Date','TDE Host Galaxy Name']

2) 'TDE Observations' folder with individual TDE observation folders that contain observational TDE observation '.txt' files from XMM Newton, Chandra, and Swift space observatories obtained from the NASA HEASARC database (https://heasarc.gsfc.nasa.gov)

to produce a '.csv' file that shows observational information for each TDE.

The output filename is 'TDE_Output_Data.csv'
"""

from matplotlib import pyplot as plt
import numpy as np
import datetime as dt
from scipy import stats
from glob import glob
import pandas as pd
import os
import csv

### Read-in tde list file
tde_file_name = 'TDE_List.tsv'
tde_list = pd.read_csv(tde_file_name, sep='\t')

### Convert dates to datetime objects
tde_list['Disc Date'] = tde_list['Disc Date'].apply(pd.to_datetime)

### Cull empty rows
tde_list = tde_list[tde_list['Name'].notnull()]


### Building Storage
def createFolder(primary_directory, alt_directory):
    ### Example
    ### >>>createFolder(f'./{folder_name}/')
    ### Creates a folder in the current directory called "folder_name"
    try:
        if not os.path.exists(primary_directory):
            # Check to see if alt directory exists
            if not os.path.exists(alt_directory):
                os.makedirs(primary_directory)
                print(f"{primary_directory} \t ***Created***")
            else:
                print(f"{primary_directory} exists as {alt_directory}")
                # give user option to rename alt --> primary
                user_rename_response = input(f"rename {alt_directory} --> {primary_directory}? (y or n)")
                                             
                if user_rename_response == "y" or "yes":
                    os.rename(alt_directory, primary_directory)

        elif os.path.exists(primary_directory):
            print(f"{primary_directory} \t ~~~Already exists~~~")
    except OSError:
        print('Error: Creating directory. ' + primary_directory)
                                             
### Rename Storage (Optional: Use only if needed)                   
def renameFolder(primary_directory, alt_directory):
    os.rename(directory_folder, new_revised_folder)
                                             
### Toggle folder creation on/off (Only choose one)
# folder_creation = True
folder_creation = False
                                             
###
num_tdes = len(tde_list)

for row_num in range(num_tdes):
    print(row_num)
    
    row = tde_list.iloc[row_num]
    
    row_tde = row['Name']
    row_host = row['Host Name'] if pd.isnull(row['Host Name']) == False else "host_name_na"


    if pd.isnull(row['Disc Date']) == False:
        row_date = row['Disc Date']
        ryear, rmonth, rday = str(row_date.year), str(row_date.month).zfill(2), str(row_date.day).zfill(2)

    if pd.isnull(row['Disc Date']) == True:
        new_folder_name = f'{row_tde}_Data_NoDateInfo'
        alt_folder_name = f'{row_host}_Data_NoDateInfo'
    else:
        new_folder_name = f'{row_tde}_Data_{ryear}_{rmonth}_{rday}'
        alt_folder_name = f'{row_host}_Data_{ryear}_{rmonth}_{rday}'

    print('\t new \t \t', new_folder_name, '\n','\t alt/host \t', alt_folder_name)

    # Create new directory
    if folder_creation == True:
        createFolder( cwd + f'/TDE Observations/{new_folder_name}/', cwd + f'/TDE Observations/{alt_folder_name}/')

print("Program completed")
        
### Automated Extraction for TDE info from NASA HEASARC Database

# run_automator = True
run_automator = False
                                             
def random_num_generator():
    from random import randint
    random_num = randint(1,3)
    return random_num

def rand_sleep():
    import time
    sleep_time = random_num_generator()
    print(f"sleeping for {sleep_time} sec")
    time.sleep(sleep_time)
                                             
def HEASARC_search_automator():
    
    # NOTE: this function uses the Selenium module. 
    # For documentation see here: https://pypi.org/project/selenium/

    from selenium import webdriver
    import time
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC


    url = "https://heasarc.gsfc.nasa.gov/xamin/"

    # Code to parse HTML content

    driver = webdriver.Safari() # for Safari 

    driver.set_page_load_timeout("10")  # Upper limit on for initial load time. Times out after.
    driver.get(url)  # Goes to website

    # driver.maximize_window()

    tde_object = input("Please enter TDE or Host name: ")
    tde_date = input("Please enter discovery date: (format: XXXX/XX/XX) ")

    # Defaults for testing
    # tde_object = "ASASSN-14li"
    # tde_date = "2020/1/1"

    def search_for_object(object_for_search):
        print(f"searching for object search element in browser")
        object_search = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "textfield-1184-inputEl"))
        )
        print("element found")
        rand_sleep()

        object_search.clear() # clears text box
        rand_sleep()
        object_search.send_keys(object_for_search, Keys.RETURN)  # Types string into field
        rand_sleep()
        time.sleep(5)
        print("populated object search field")

        # object_search.send_keys(Keys.RETURN)
        # print("pressing RETURN")

    def rename_file(file_mission_source, object_name, object_date):
        print("starting renaming")
        import os, datetime
        
        # NOTE: need to change to your own chosen directory
        file_directory = "___directory_here___"
        file_name = "query.txt"

        old_file_path = f"{file_directory}/{file_name}"

        add_file_date = object_date

        # add_file_date = input(f"Enter date to add to {object_name}: ")

        add_file_year, add_file_month, add_file_day = add_file_date.split('/')[0], add_file_date.split('/')[1], \
                                                      add_file_date.split('/')[2]
        add_file_date = datetime.date(int(add_file_year), int(add_file_month), int(add_file_day))

        file_year = add_file_date.year
        file_month = str(add_file_date.month).zfill(2)
        file_day = str(add_file_date.day).zfill(2)


        # os.listdir(file_directory)
        print("checking file mission source")
        if file_mission_source == "chanmaster":
            print("mission is chandra")
            new_file_name = f"{object_name}_Chandra_Data_{file_year}_{file_month}_{file_day}.txt"
            new_file_path = f"{file_directory}/{new_file_name}"
            if file_name in os.listdir(file_directory):
                os.rename(old_file_path, new_file_path)
                print(f"file renamed: {old_file_path} --> {new_file_path}")
            else:
                print("chandra file not found")

        if file_mission_source == "swiftmastr":
            print("mission is swift")
            new_file_name = f"{object_name}_Swift_Data_{file_year}_{file_month}_{file_day}.txt"
            new_file_path = f"{file_directory}/{new_file_name}"
            # for file in os.listdir(file_directory):
            #     print(file)
            if file_name in os.listdir(file_directory):
                os.rename(old_file_path, new_file_path)
                print(f"file renamed: {old_file_path} --> {new_file_path}")
            else:
                print("swift file not found")

        if file_mission_source == "xmmmaster":
            print("mission is xmm")
            new_file_name = f"{object_name}_XMM_Data_{file_year}_{file_month}_{file_day}.txt"
            new_file_path = f"{file_directory}/{new_file_name}"
            if file_name in os.listdir(file_directory):
                os.rename(old_file_path, new_file_path)
                print(f"file renamed: {old_file_path} --> {new_file_path}")
            else:
                print("xmm file not found")

    try:

        for mission in ["chanmaster", "swiftmastr","xmmmaster"]:
            # Choose Options
            print("looking for option element")
            option_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "button-1070"))
            )
            print("element found")
            rand_sleep()
            option_button.click()
            print("clicked option button")
            rand_sleep()  # Delay for humans
            option_button.send_keys(Keys.ARROW_DOWN, Keys.ARROW_DOWN, Keys.ARROW_DOWN, Keys.ARROW_DOWN, Keys.ARROW_RIGHT,
                                    Keys.ARROW_DOWN, Keys.ARROW_DOWN, Keys.ARROW_DOWN, Keys.ARROW_DOWN, Keys.ARROW_DOWN,
                                    Keys.RETURN)
            print("navigated options")
            rand_sleep()
            #
            # option_max_row = WebDriverWait(driver, 10).until(
            #     EC.presence_of_element_located((By.ID, "textfield-1136-inputEl"))
            # )
            # time.sleep(random_num_generator())
            # option_max_row.send_keys("1000")
            # time.sleep(random_num_generator())
            #
            # option_max_time = WebDriverWait(driver, 10).until(
            #     EC.presence_of_element_located((By.ID, "textfield-1137-inputEl"))
            # )
            # time.sleep(random_num_generator())
            # option_max_row.send_keys("1000000")
            # time.sleep(random_num_generator())
    
            print("options complete")
    
    
            # Select Master Tables
            print("searching for master table element")
            master_table_search = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "xm_tablesdirect-1198-inputEl"))
            )
            print("found element")
            rand_sleep()
            # master_table_directory.click()
            
            
            print(f"search for {mission} table")
            master_table_search.send_keys(mission)
            rand_sleep()  # Delay for humans
            master_table_search.send_keys(Keys.RETURN)
            print(f"added {mission} table")
            rand_sleep()  # Delay for humans

            search_for_object(tde_object)
            print("search complete, file downloaded?")

            rename_file(mission, tde_object, tde_date)
            print("rename complete")
            
            # Refresh page to search in next database
            driver.refresh()
            rand_sleep()  # Delay for humans
            
            # Reset table to search for next database # Doesn't work anymore
            
            # print("looking for reset table button element")
            
            # try:
            #     reset_tables_button = WebDriverWait(driver, 10).until(
            #     EC.presence_of_element_located((By.ID, "button-1177"))
            #     )
            #     # reset_tables_button = WebDriverWait(driver, 10).until(
            #     #     EC.presence_of_element_located((By.LINK_TEXT, "Tables"))
            #     # )
            # except:
            #     print("reset button not found")
            #     driver.quit()
            # print("element found")
            # rand_sleep()
            # try:
            #     reset_tables_button.click()
            #     print("reset button clicked")
            # except:
            #     print("reset button not clicked")
            #     driver.quit()
            # rand_sleep()

    except:
        driver.quit()
        print("Quit by exception")

    # object_search = driver.find_element_by_id("textfield-1184-inputEl")  # ?
    # object_search.click()
    # object_search.send_keys("ASASSN-14li")  # Types string into field
    # time.sleep(3)  # Delay for humans
    # object_search.send_keys(Keys.ARROW_DOWN)  # presses Down Arrow key
    # object_search.send_keys(Keys.RETURN)  # presses Return key to instigate search

    time.sleep(5)  # Delay for humans
    driver.close()
    print("program successfully completed")

if run_automator == True:
    HEASARC_search_automator()


### Table Production

def read_folders_in(os_directory):
    import os

    folders = [folder for folder in os.listdir(os_directory)]

    tde_folders = []

    for folder in folders:  # Filters out unnecessary folders
        if not folder in [".DS_Store", ".ipynb_checkpoints"]:
            tde_folders.append(folder)

    tde_folders.sort(key=str.lower)  # alphabetizes list, key ensures that lowercase names are accounted for (otherwise they get added last)

    return tde_folders

def Universal_Data_Reader(base_directory):

    tde_folders = read_folders_in(base_directory)  # needs to be ran for the following code to work

    # read each TDE folder's files

    import math  # for numerical analysis
    import datetime as dt  # for date comparisons
    import os  # for file access
    import csv  # for writing data to csv file for easier transfer to excel

    with open('TDE_Output_Data.csv', 'w') as csv_file:
        fieldnames = ['TDE',
                      'XMM Data (#obs: ObsIDs, exp date [yyyy-mm-dd], exp dur [sec])',
                      'XMM TDE Data (#obs_TDE, minoff_TDE, maxoff_TDE, comment)',
                      'XMM Good TDE Data (total #ObsIDs with TDE, unique date, >1000 [sec])',
                      'XMM Col D ObsID (exp time, date, #days after discovery)',
                      'Chandra Data (#obs: ObsIDs, exp date [yyyy-mm-dd], exp dur [sec], detector)',
                      'Chandra TDE Data (#obs_TDE, minoff_TDE, maxoff_TDE, comment)',
                      'Chandra Good TDE Data (total #ObsIDs with TDE, unique date, >1000 [sec])',
                      'Chandra Col H ObsID (exp time, date, #days after discovery)',
                      'Swift Data (#obs: ObsIDs, exp date [yyyy-mm-dd], XRT exp dur [sec])',
                      'Swift TDE Data (#obs_TDE, minoff_TDE, maxoff_TDE, comment)',
                      'Swift Good TDE Data (total #ObsIDs with TDE, unique date, >1000 [sec])',
                      'Swift Col L ObsID (exp time, date, #days after discovery)']
        csv_writer = csv.writer(csv_file, delimiter=',')

        csv_writer.writerow(fieldnames)

        ###
        # Main folder/sub folders
        for TDE_folder in tde_folders:  # TDE_folders as returned by read_folder_in() function
            print(TDE_folder)

            tde_dictionary = {'TDE_Name': TDE_folder.split('_')[0], 'TDE_Date': TDE_folder.split('_')[2:]}
            print(tde_dictionary.values())

            tde_folder_directory = f"{base_directory}/{TDE_folder}"

            raw_tde_files = [folder for folder in os.listdir(tde_folder_directory)]

            tde_files = []

            for file in raw_tde_files:  # Filters out mac default files
                if not file in [".DS_Store",".ipynb_checkpoints"]:
                    tde_files.append(file)

            # Initialize Separate Source Output Lists
            xmm_list = [None, None, None, None, None, None]  # "None" to ensure empty cells if no data available
            chandra_list = [None, None, None, None, None, None]
            swift_list = [None, None, None, None, None, None]

            # Get TDE name
            tde_name = tde_dictionary.get('TDE_Name')

            # Get TDE Date
            tde_date = tde_dictionary.get('TDE_Date')  # Is a list in form ['yyyy',''mm','dd'] or ['NoDateInfo']

            if tde_date != ['NoDateInfo']:  # If Date exists
                tde_date = [int(element) for element in tde_date]  # convert to from str --> int
                tde_date = dt.date(tde_date[0], tde_date[1], tde_date[2])  # save as datetime object

            # elif tde_date == ['NoDateInfo']:  # If not, and want user input use this, comment out if not needed
            #     # else, get date from user
            #     tde_date = []  # Initialize
            #     # Check for correct format. Prompt user if not.
            #     while tde_date == [] or len(tde_date) != 10 or len(tde_date.split('/')) != 3 or len(
            #             tde_date.split('/')[0]) != 4 or len(tde_date.split('/')[1]) != 2 or len(
            #         tde_date.split('/')[2]) != 2:
            #         tde_date = input("Date of TDE? (format: numerical YYYY/MM/DD): ")
            #     # Convert Date to datetime format
            #     tde_date = tde_date.split('/')  # separate into individual components
            #     discYear, discMonth, discDay = int(tde_date[0]), int(tde_date[1]), int(tde_date[2])
            #
            #     tde_date = dt.date(discYear, discMonth, discDay)

            # Main folder/Sub folder/tde files
            for file_name in tde_files:

                print(file_name)

                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                # Input # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

                input_file_name = f"{tde_folder_directory}/{file_name}"

                # Open and read/copy file for use
                with open(input_file_name) as f:
                    full_read_data = f.readlines()

                reduced_read_data = []

                for line_num, line in enumerate(full_read_data):
                    if line == "\n":  # stops after main body
                        break
                    if line_num > 0:  # skips header
                        reduced_read_data.append(line)

                # print(reduced_read_data)
                if reduced_read_data == []:
                    continue  # skips empty file and moves to next file in folder

                # Grab header and strip excess whitespace and characters
                stripped_header = [header.strip().strip('_') for header in full_read_data[0].split('|')]

                read_data_dictionary = csv.DictReader(reduced_read_data, fieldnames=stripped_header, delimiter='|')

                # Determine file source name for appropriate data reader
                if "xmm" in file_name.lower().split('_')[1:]:
                    file_telescope_source_name = "xmm"
                elif "chandra" in file_name.lower().split('_')[1:]:
                    file_telescope_source_name = "chandra"
                elif "swift" in file_name.lower().split('_')[1:]:
                    file_telescope_source_name = "swift"
                else:  # unknown file type, end program
                    print(f"{input_file_name} Data type unknown. Program terminated.")
                    quit()

                # initialize variables
                output_time_discrep = ""
                output_obsid_date_exp_time = ""
                output_obsid_before_event = ""
                output_obsid_same_day_event = ""
                output_obsid_after_event = ""
                output_obsid_error = ""
                output_large_offset = ""
                offset_limit = 5  # in arcsec
                offset_list = []
                id_count = 0
                before_count = 0
                same_count = 0
                after_count = 0
                no_count = 0
                unique_date_list = []  # list for unique dates after discovery date
                observations_list = []  # list for obs id, exp time, date, # days after discovery date

                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                # Processing  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

                for line_index, observation in enumerate(read_data_dictionary):  # Runs file copy line by line
                    # print(observation)
                    
                    id_count += 1  # total num epochs

                    # format
                    # xmm: ['obsid', 'status', 'name', 'ra', 'dec', 'time', 'duration', 'pi_lname', 'pi_fname', 'public_date', 'data_in_heasarc', 'offset']
                    # swift: ['name', 'obsid', 'ra', 'dec', 'start_time', 'processing_date', 'xrt_exposure', 'uvot_exposure', 'bat_exposure', 'archive_date', 'offset']
                    # chandra: ['obsid', 'status', 'name', 'ra', 'dec', 'time', 'detector', 'grating', 'exposure', 'type', 'pi', 'public_date', 'offset']

                    observation_id = observation['obsid']
                    offset = float(observation['offset'])
                    if file_telescope_source_name == "swift":
                        observation_date = observation['start_time'].split('T')[0].strip()
                        xrt_exposure_time = float(observation['xrt_exposure'])
                        uv_exposure_time = float(observation['uvot_exposure'])
                    else:
                        observation_date = observation['time'].split('T')[0].strip()
                    if file_telescope_source_name == "xmm":
                        xrt_exposure_time = float(observation['duration'])
                    if file_telescope_source_name == "chandra":
                        xrt_exposure_time = float(observation['exposure'])

                    if file_telescope_source_name == "chandra":  # for chandra data
                        detector = observation['detector']
                        output_obsid_date_exp_time += f"{observation_id} ({observation_date}, {xrt_exposure_time}, {detector}), "
                    else:
                        output_obsid_date_exp_time += f"{observation_id} ({observation_date}, {xrt_exposure_time}), "

                    # get year, month, day info
                    if observation_date.strip() == "null":  # For rare cases where date is missing in file
                        print("date == null")
                        skip_input = input("verify skip y/n? (y: skips, n: ends program) : ")
                        if skip_input == "y":
                            continue

                    observation_date_components = observation_date.split('-')

                    observation_year, observation_month, observation_day = int(observation_date_components[0]), int(observation_date_components[1]), int(observation_date_components[2])
                    observation_date = dt.date(observation_year, observation_month, observation_day)

                    delta_date = observation_date - tde_date  # difference between epoch and discovery dates
                    delta_date = delta_date.days  # output from "# days, XX:XX:XX" to "#" of days

                    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                    # Inline File Manipulation  # # # # # # # # # # # # # # # # # # # # # # # # # #
                    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

                    # # # # # # # # # # # # # # # # # # # #
                    # Compare user input date with file date
                    def filter_function():
                        # Checks for unique date and grabs only highest xray exposure time
                        if xrt_exposure_time >= 1000 and observation_date not in unique_date_list:  # meets conditions and has unique date
                            unique_date_list.append(observation_date)
                            observations_list.append(f"{observation_id} ({xrt_exposure_time}, {observation_date}, {delta_date})")
                        elif xrt_exposure_time >= 1000 and observation_date in unique_date_list:  # meets conditions but date already accounted for, compares new data with old data and takes highest time
                            for index in range(len(observations_list)):
                                if observation_date == observations_list[index].split(',')[
                                        2].strip() and xrt_exposure_time > float(
                                        observations_list[index].split(',')[1]):  # replaces old data if new data has greater exposure time
                                    observations_list[index] = f"{observation_id} ({xrt_exposure_time}, {observation_date}, {delta_date})"

                    if observation_date < tde_date:  # Before
                        output_obsid_before_event += f"{observation_id}, "
                        before_count += 1
                    elif observation_date == tde_date:  # Same
                        output_obsid_same_day_event += f"{observation_id}, "
                        same_count += 1
                        filter_function()
                    elif observation_date > tde_date:  # After
                        output_obsid_after_event += f"{observation_id}, "
                        after_count += 1
                        filter_function()
                    else:  # No Date/ Error
                        output_obsid_error += f"{observation_id}, "
                        no_count += 1

                    # # # # # # # # # # # # # # # # # # # #

                    # # # # # # # # # # # # # # # # # # # #
                    # Comparison of xrt, uvot, and bat exposure times for Swift files

                    if file_telescope_source_name == "swift":
                        exposure_time_difference = round(abs(xrt_exposure_time - uv_exposure_time))

                        if uv_exposure_time > 0:  # ensures no div by 0
                            xr_uv_ratio = xrt_exposure_time / uv_exposure_time
                            xr_uv_ratio = math.trunc(round(10.0 ** 3 * xr_uv_ratio)) / 10.0 ** 3
                            if xr_uv_ratio > 1.05:
                                output_time_discrep += f"{observation_id} XR:UV Time Ratio: {xr_uv_ratio}:1. Dt: {exposure_time_difference} sec.\n"

                        else:
                            output_time_discrep += f"{observation_id} NO UV TIME.\n"
                    # # # # # # # # # # # # # # # # # # # #

                    # # # # # # # # # # # # # # # # # # # #
                    # Offset Data

                    # Large offsets
                    if offset > offset_limit:
                        output_large_offset += f"{observation_id} {offset}, "

                    # Full offset list
                    offset_list.append(offset)  # to find min/max offsets
                    # # # # # # # # # # # # # # # # # # # #

                # # # # # # # # # # # # # # # # # # # #
                # Reorder observations list
                if len(observations_list) > 0:  # Only run if there is not an empty list (which would make this run indefintely)
                    num_no_switches = 0  # initialize
                    while not num_no_switches == len(
                            observations_list) - 1:  # stops program once it is fully sorted. No more, no less.
                        num_no_switches = 0  # reset count with new loop
                        for index_obsList in range(len(observations_list)):
                            if index_obsList > 0:
                                # epoch current/prior are the dt's
                                epoch_current = int(observations_list[index_obsList].split(',')[2].split(')')[0].strip())
                                epoch_prior = int(observations_list[index_obsList-1].split(',')[2].split(')')[0].strip())
                                if epoch_current < epoch_prior:  # switch
                                    observations_list[index_obsList], observations_list[index_obsList - 1] = observations_list[
                                                                                                         index_obsList - 1], \
                                                                                                     observations_list[
                                                                                                         index_obsList]
                                else:  # no switch, count no switch.
                                    num_no_switches += 1
                # # # # # # # # # # # # # # # # # # # #

                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                # Output  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
                # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

                # write to CSV file

                tde_row_list = []  # initialize list for row to be written to csv file

                # column 1 'TDE'
                tde_row_list.append(tde_name)

                # column 2 source
                tde_row_list.append(file_telescope_source_name)

                # column 3 'Num ObsIDs and obs data'
                observation_data = f"{id_count}: {output_obsid_date_exp_time}"
                tde_row_list.append(observation_data)

                # column 4
                tde_data = f"{same_count + after_count}, {min(offset_list)}, {max(offset_list)}"
                tde_row_list.append(tde_data)

                # column 5
                num_unique_tde_output = len(observations_list)
                tde_row_list.append(num_unique_tde_output)

                # column 6
                obs_list_output = ""
                for element in observations_list:
                    obs_list_output += f"{element}, "

                tde_row_list.append(obs_list_output)

                # append column info to TDE row list and save to appropriate source list
                # print(tde_row_list)  # Can comment out

                if file_telescope_source_name == "xmm":
                    xmm_list = tde_row_list
                if file_telescope_source_name == "chandra":
                    chandra_list = tde_row_list
                if file_telescope_source_name == "swift":
                    swift_list = tde_row_list

                # quit() # stops after first file. uncomment for testing

            ###
            # After individual files, back to TDE Folder to compile data together for exportation to csv file

            # Append sublists together to form one master list
            master_list = []

            master_list.append(tde_name)
            for element in xmm_list[2:]:  # loops only include elements past first two to reduce redundant info
                master_list.append(element)
            for element in chandra_list[2:]:
                master_list.append(element)
            for element in swift_list[2:]:
                master_list.append(element)

            print(master_list, '\n')

            # Write master list to csv file
            csv_writer.writerow(master_list)

            # quit()  # Stops after first folder. Uncomment for testing

    print("Program Complete")
    
#Read in tde data folders
Universal_Data_Reader('TDE Observations') # designate location of main folder
                                             