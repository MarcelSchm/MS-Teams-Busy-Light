"""Main File that opens a serial connection and sends commands to an arduino, depending on the Teams log file."""

import sys
import time
import os
import re
from datetime import datetime
import configparser
import logging
from logging.handlers import RotatingFileHandler
import serial
import serial.tools.list_ports
from file_read_backwards import FileReadBackwards
from easygui import msgbox, choicebox


# Global variables to store the last known status of the user, as well as some serial data stuff
last_known_availability = "unknown"
last_known_notification_count = "unknown"
last_known_call_status = "unknown"
COM_BAUD = 9600
ser = serial.Serial()


def load_settings(config_file):
    """
    Loads configuration settings from the specified configuration file.

    Args:
        config_file (str): Path to the configuration file.

    Returns:
        dict: A dictionary of configuration settings.
    """
    config = configparser.ConfigParser()
    try:
        config.read(config_file)
        settings = {
            "newTeams": config["Version"]["newTeams"],
            "logfolder_new": config["Version"]["logfolder_new"],
            "logfolder_old": config["Version"]["logfolder_old"],
            "SearchString": config["TeamsSettings"]["SearchValue"],
            "StatusStates": {k: v for k, v in config["StateSettings"].items()},
            "debug": {k: v for k, v in config["DebugSettings"].items()},
        }
        return settings
    except KeyError as e:
        logging.error(f"Missing key in configuration file: {e}")
    except configparser.Error as e:
        logging.error(f"Error reading configuration file: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
    return None

def configure_logging(config_settings):
    """
    Configures the logging system based on settings from the configuration file.

    Args:
        settings (dict): A dictionary of configuration settings.
    """
    try:
        debug_settings = config_settings.get("debug", {})
        log_level = debug_settings.get("logginglevel").upper()
        if log_level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            log_file_path = debug_settings.get("log_file_path")
            max_size_mb = int(debug_settings.get("max_size_mb"))
            backup_count = int(debug_settings.get("backup_count"))

            # Ensure the log folder exists
            log_folder = os.path.dirname(log_file_path)
            if not os.path.exists(log_folder):
                os.makedirs(log_folder)


            logging.getLogger('').setLevel(log_level)
            # Use RotatingFileHandler for size-based rotation
            size_handler = RotatingFileHandler(
                log_file_path, maxBytes=max_size_mb * 1024 * 1024, backupCount=backup_count
            )
            size_handler.setFormatter(logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
            ))
            logging.getLogger('').addHandler(size_handler)
        else:
            logging.disable(logging.CRITICAL)
    except (OSError, ValueError) as e:
        logging.error("Failed to configure logging: %s", e)


def read_com_ports():
    """
    Function to call a library, that returns all open COM-Ports. Returns 0, if no ports exist.

    """
    logging.info("Reading COM ports...")
    ports = serial.tools.list_ports.comports()
    if len(ports) == 0:
        return 0
    else:
        for port, desc, hwid in sorted(ports):
            print("{}: {} [{}]".format(port, desc, hwid))
        return sorted(ports)


def process_log_file(file_path, settings):
    """
    Processes the specified log file to extract the user's availability, call status, and notification count.
    If the expected patterns are not found in the log file, the status values are set to "unknown".

    Args:
        file_path (str): The path to the log file to be processed.
        settings (dict): A dictionary containing configuration settings, including Home Assistant connection details.
    """
    # Compile regex patterns to search for availability, notification count, and call status
    search_pattern = re.compile(
        r"availability: (\w+), unread notification count: (\d+)"
    )
    search_pattern_start = re.compile(
        r"WebViewWindowWin:.*tags=Call.*Window previously was visible = false"
    )
    search_pattern_end = re.compile(
        r"BluetoothRadioManager: Device watcher is Started."
    )

    # Initialize default statuses
    call_status = "Not in a call"  # Default call status
    found_text = False  # Flag to indicate if any expected pattern is found in the log

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                # Check for availability and notification count
                match = search_pattern.search(line)
                if match:
                    # Update last known statuses if a match is found
                    last_availability, last_notification_count = match.groups()
                    found_text = True  # Indicate that expected text has been found

                # Infer call status from the current line using the start and end patterns
                if search_pattern_start.search(line):
                    call_status = "In a call"
                    found_text = True
                elif search_pattern_end.search(line):
                    call_status = "Not in a call"
                    found_text = True

        # If no expected text is found in the entire file, set status values to "unknown"
        if not found_text:
            last_availability = "unknown"
            last_notification_count = "unknown"
            call_status = "unknown"
            logging.info(
                "No specific patterns were found in the log file. Setting status to 'unknown'."
            )

        # Update Home Assistant with the detected statuses
        logging.info(
            f"Detected status: {last_availability}, Call Status: {call_status}, Notification Count: {last_notification_count}"
        )
    except Exception as e:
        logging.error(f"Error reading file {file_path}: {e}")


def process_last_lines_of_log(file_path, settings):
    """
    Processes the last few lines of the selected most recent log file to fetch latest status

    Args:
        file_path (str): The path to the log file to be processed.
        settings (dict): A dictionary of configuration settings.
    """
    global last_known_availability, last_known_notification_count, last_known_call_status

    search_pattern = re.compile(
        r"availability: (\w+), unread notification count: (\d+)"
    )
    search_pattern_start = re.compile(
        r"WebViewWindowWin:.*tags=Call.*Window previously was visible = false"
    )
    search_pattern_end = re.compile(
        r"BluetoothRadioManager: Device watcher is Started."
    )

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()[-10:]  # Read only the last 10 lines

        # Check each line for status updates
        for line in reversed(lines):
            if match := search_pattern.search(line):
                new_availability, new_notification_count = match.groups()
                if (
                    new_availability != last_known_availability
                    or new_notification_count != last_known_notification_count
                ):
                    last_known_availability = new_availability
                    last_known_notification_count = new_notification_count
                    logging.info("Status update found in the log.")
                    break  # Update found, no need to check further

            if search_pattern_start.search(line):
                last_known_call_status = "In a call"
                break
            elif search_pattern_end.search(line):
                last_known_call_status = "Not in a call"
                break

    except Exception as e:
        logging.error(f"Error reading file {file_path}: {e}")


def startup_log_read(settings):
    """
    Reads the most recent log file at startup to determine the user's current status.
    This function is intended to be called when the script starts to initialize the status.

    Args:
        settings (dict): A dictionary containing configuration settings, including the log folder path.
    
    Return:
        str: Returns the status value as a string.
    """
    if (settings("newTeams") == True):
    
        log_dir = os.path.expandvars(settings["logfolder"])
        if not os.path.exists(log_dir):
            print("Log directory does not exist, check configuration.")
            exit()  # Exit the script if the log directory does not exist

        file_pattern = re.compile(
            r"MSTeams_(\d{4}-\d{2}-\d{2})_(\d{2}-\d{2}-\d{2}\.\d+)\.log"
        )
        latest_file = None
        latest_time = None

        # Iterate through all files in the log directory to find the most recent log file
        for file_name in os.listdir(log_dir):
            match = file_pattern.match(file_name)
            if match:
                # Parse the datetime from the filename to determine if it's the most recent
                file_datetime = datetime.strptime(
                    f"{match.group(1)} {match.group(2)}", "%Y-%m-%d %H-%M-%S.%f"
                )
                if latest_time is None or file_datetime > latest_time:
                    # Update the latest time and file if this file is more recent
                    latest_time = file_datetime
                    latest_file = file_name

        # If a latest file is found, process it to initialize the user's status
        if latest_file:
            process_log_file(os.path.join(log_dir, latest_file), settings)


    
    #if (settings["newTeams"] == True):


def select_com_ports():
    """Function to select COM Port. Stops programm if none is available, auto selects COM Port if only one is available or shows a choicebox to select if there are more than one COMPorts."""
    ports = read_com_ports()
    msg = (
        "Which COM-Port is your device connected to? Please Select from the List Below"
    )
    title = "MS-Teams-Busy-Light"
    choices = []
    if ports == 0:
        msg = "Unfortunately you have no COM-Port available in your System. Please check connections and start again."
        msgbox(msg, title, ok_button="Stop Program")
        sys.exit(0)
    for port, desc, hwid in ports:
        choices.append(port + ":  " + desc)
    if len(choices) == 1:
        msg = "There is only 1 COM-Port available. Auto - Selected: \n\n" + choices[0]
        result = msgbox(msg, title, ok_button="OK")
        if result is None:
            sys.exit(0)
        else:
            return port
    choice = choicebox(msg, title, choices)
    if choice is None:
        sys.exit(0)
    else:
        return str.split(choice, ":")[0]


def write_initial_COM_Port():
    """
    Function to initialize COM Port.Send String "White" as first status for initialize/unknown.
    """
    logging.info("Writing initial COM port configuration...")
    COM_PORT = select_com_ports()
    ser.port = COM_PORT
    ser.baudrate = COM_BAUD
    ser.open()
    time.sleep(3)
    ser.write(b"White")


def write_status_to_busy_light(status):
    """
    simply writes the some predefined status value via Serial to Arduino in Busy Light.

    Args:
        status (string): String that matches to one of the status values in config file.

    """
    # Implementation of writing status to busy light
    logging.info("Writing status %s to busy light...",status)
    match status:
        case "available":
            ser.write(b"Green")
            time.sleep(2)
        case "busy":
            ser.write(b"Red")
            time.sleep(2)
        case "inameeting":
            ser.write(b"Red")
            time.sleep(2)
        case "onthephone":
            ser.write(b"Red")
            time.sleep(2)
        case "donotdisturb":
            ser.write(b"Red")
            time.sleep(2)
        case "berightback":
            ser.write(b"Yellow")
            time.sleep(2)
        case "presenting":
            ser.write(b"Red")
            time.sleep(2)
        case "away":
            ser.write(b"Yellow")
            time.sleep(2)
        case "offline":
            ser.write(b"Yellow")
            time.sleep(2)
        case "unknown":
            ser.write(b"Red")
            time.sleep(2)
        case "newactivity":
            # ser.write(b'Red')
            time.sleep(2)
        case "connectionerror":
            ser.write(b"Red")
            time.sleep(2)
        case "nonetwork":
            ser.write(b"Red")
            time.sleep(2)
        case "initialize":
            ser.write(b"White")
            time.sleep(2)
        case "outdated":
            ser.write(b"Green")
            time.sleep(2)
        case "incomingcall":
            ser.write(b"BlinkRed")
            time.sleep(2)
        case _:
            msgbox(
                msg="MS Teams Presence Status Script: The following Status is not yet known and needs to be added to the python Script: \n"
                + status,
                title="MS-Teams-Busy-Light Script",
            )
            time.sleep(2)
            logging.error("The following Status is not yet known and needs to be added to the python Script: %s", status)


def check_new_or_modified_log(settings, last_checked_time):
    """
    Checks if a new log file has been created in a folder or if the latest log file has been modified since the last read.

    Args:
        settings (dict): A dictionary containing configuration settings, including the path to the log folder.
        last_checked_time (datetime): The time when the log files were last checked.

    Returns:
        bool: True if a new log file has been created or the latest log file has been modified since the last read, otherwise False.
        str: The path to the latest log file.
        datetime: Timestamp of the latest changed log file.
    """
    # Determine the log folder path based on the newTeams flag
    if bool(settings["newTeams"]) == True:
        log_dir = os.path.expandvars(settings["logfolder_new"])
    else:
        log_dir = os.path.expandvars(settings["logfolder_old"])
     
    # Check if the log directory exists
    if not os.path.exists(log_dir):
        logging.error("Log directory does not exist, check configuration.")
        return False, None,None  # Exit the function if the log directory does not exist

    # Regular expression pattern to match log file names
    file_pattern = re.compile(
        r"MSTeams_(\d{4}-\d{2}-\d{2})_(\d{2}-\d{2}-\d{2}\.\d+)\.log"
    )
    latest_file = None
    latest_time = None

    # Iterate through all files in the log directory to find the most recent log file
    for file_name in os.listdir(log_dir):
        match = file_pattern.match(file_name)
        if match:
            # Parse the datetime from the filename to determine if it's the most recent
            file_datetime = datetime.strptime(
                f"{match.group(1)} {match.group(2)}", "%Y-%m-%d %H-%M-%S.%f"
            )
            if latest_time is None or file_datetime > latest_time:
                # Update the latest time and file if this file is more recent
                latest_time = file_datetime
                latest_file = file_name

    # If no log files are found, return False
    if latest_file is None:
        logging.error("check_new_or_modified_log - No Log Files found")
        return False, None, None

    # Get the full path to the latest log file
    latest_file_path = os.path.join(log_dir, latest_file)
    
    # Get the modification time of the latest log file
    latest_file_mtime = datetime.fromtimestamp(os.path.getmtime(latest_file_path))

    # Check if the latest file is new or has been modified since the last check
    if latest_file_mtime >= last_checked_time:
        return True, latest_file_path,latest_file_mtime
    logging.info("check_new_or_modified_log - No new file or modification to it, since last check.")
    return False, latest_file_path,latest_file_mtime

def search_availability_in_log(log_file_path, availability_string, status_states):
    """
    Search for the last occurrence of the "availability" string in the log file given as argument and return the value of the last occurence.

    Args:
        log_file_path (str): Path to the log file.
        availability_string (str): The string to search for in the log file.
        status_states (str): The list of possible status states.

    Returns:
        str: The value of the last occurrence of the availability string.
    """
    if not os.path.exists(log_file_path):
        raise FileNotFoundError(f"Log file not found: {log_file_path}")

    last_value = None
    search_string = f"{availability_string}:"

    with FileReadBackwards(log_file_path, encoding="utf-8") as frb:
        for line in frb:        
            if search_string in line:
                # Extract the value after the availability string
                # examplestring from log:
                # 2024-09-07T21:18:25.244338+02:00 0x00003de8 <INFO> native_modules::UserDataCrossCloudModule: BroadcastGlobalState: New Global State Event: UserDataGlobalState total number of users: 1 { user id :31e6a1801808ed67, availability: PresenceUnknown, unread notification count: 0 }
                last_value = line.split(search_string)[-1].strip().split(',',1)[0].lower()
                logging.info("Logfile: %s. Following Status found: %s",log_file_path,last_value)
                if last_value not in status_states:
                    logging.error("search_availability_in_log -  Status %s read in log is not yet part of settings.ini",last_value)
                break
    if last_value is None:
        logging.error("search_availability_in_log - No occurrence of %s found in file %s",search_string,log_file_path)
    return last_value

if __name__ == "__main__":
    timestamp = datetime.now()
    settings = load_settings("MS_Teams_Settings.ini")
    configure_logging(settings) # activates debug logs according to .ini file
    if not settings["debug"]["enabled"].lower() in ['true', 'yes', 'y']:
        read_com_ports()
        write_initial_COM_Port()
        status = "initialize"
    else:
        logging.info("Bypassing Setup of read_com_ports and write_initial_COM_Port() due to debug mode.")
    while True:
        newLog,path,latest_file_mtime = check_new_or_modified_log(settings,timestamp)
        timestamp = latest_file_mtime
        if newLog:
            status = search_availability_in_log(path,settings["SearchString"],settings["StatusStates"])
        #status = startup_log_read(settings)
        if not settings["debug"]["enabled"].lower() in ['true', 'yes', 'y']:
            write_status_to_busy_light(status.lower())
        else:
            logging.info("Bypassing write_status_to_busy_light due to debug mode.")
