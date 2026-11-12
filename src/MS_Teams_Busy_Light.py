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
COM_BAUD = 9600
ARDUINO_RESET_DELAY_SECONDS = 3  # Arduino resets when DTR toggles on port open
POLL_INTERVAL_SECONDS = 2
ser = serial.Serial()
ser.write_timeout = 2  # never block forever if the device stops draining the buffer
serial_connected = False
reported_unknown_statuses = set()

# status value from the Teams log (lower case) -> command for the Arduino. None = send nothing.
STATUS_TO_COMMAND = {
    "available": b"Green\r\n",
    "busy": b"Red\r\n",
    "inameeting": b"Red\r\n",
    "onthephone": b"Red\r\n",
    "donotdisturb": b"Red\r\n",
    "focusing": b"Red\r\n",
    "inacall": b"Red\r\n",
    "berightback": b"Yellow\r\n",
    "presenting": b"Red\r\n",
    "away": b"Yellow\r\n",
    "offline": b"Yellow\r\n",
    "unknown": b"Red\r\n",
    "presenceunknown": b"Red\r\n",
    "newactivity": None,
    "notinacall": None,
    "connectionerror": b"Red\r\n",
    "nonetwork": b"Red\r\n",
    "initialize": b"White\r\n",
    "outdated": b"Green\r\n",
    "incomingcall": b"BlinkRed\r\n",
}


def is_truthy(value):
    """Interprets a string value from the .ini file as a boolean."""
    return str(value).strip().lower() in ("true", "yes", "y", "1", "on")


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
        if not config.getboolean("Version", "newTeams"):
            raise ValueError(
                "The legacy Teams log format is not supported; set newTeams = True."
            )
        settings = {
            "logfolder_new": config["Version"]["logfolder_new"],
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


def open_serial_port(com_port):
    """
    (Re-)opens the COM port and waits for the Arduino to finish its reset.

    Args:
        com_port (str): Name of the COM port, e.g. "COM3".

    Returns:
        bool: True if the port is open afterwards.
    """
    global serial_connected
    try:
        if ser.is_open:
            ser.close()
        ser.port = com_port
        ser.baudrate = COM_BAUD
        ser.open()
        time.sleep(ARDUINO_RESET_DELAY_SECONDS)
        serial_connected = True
        logging.info("Serial port %s opened.", com_port)
        return True
    except (serial.SerialException, OSError) as e:
        # log only on the transition to disconnected so a missing device does not flood the log
        if serial_connected:
            logging.error("Failed to open COM port %s: %s", com_port, e)
        else:
            logging.debug("Still unable to open COM port %s: %s", com_port, e)
        serial_connected = False
        return False


def close_serial_port():
    """Closes the COM port, ignoring errors from an already invalid handle."""
    global serial_connected
    serial_connected = False
    try:
        ser.close()
    except (serial.SerialException, OSError) as e:
        logging.debug("Error while closing serial port: %s", e)


def send_to_busy_light(command):
    """
    Writes a command to the Arduino. On any serial error (device unplugged, port grabbed by another
    process, sleep/resume, ...) the port is closed and re-opened on the next call instead of crashing.

    Args:
        command (bytes): Command including line ending, e.g. b"Red\\r\\n".

    Returns:
        bool: True if the command was written successfully.
    """
    if not ser.is_open and not open_serial_port(ser.port):
        return False
    try:
        ser.write(command)
        ser.flush()
        return True
    except (serial.SerialException, OSError) as e:
        if serial_connected:
            logging.error("Serial communication on %s failed, will try to reconnect: %s", ser.port, e)
        close_serial_port()
        return False


def write_initial_COM_Port(com_port):
    """
    Function to initialize COM Port.Send String "White" as first status for initialize/unknown.

    Args:
        com_port (str): Name of the COM port selected by the user.
    """
    logging.info("Writing initial COM port configuration...")
    # treat the very first attempt as "connected" so a failure is logged at error level
    global serial_connected
    serial_connected = True
    if open_serial_port(com_port) and send_to_busy_light(b"White\r\n"):
        logging.info("Initial COM port configuration written successfully.")
    else:
        logging.error("Could not initialize COM port %s, will keep retrying in the main loop.", com_port)


def write_status_to_busy_light(status):
    """
    simply writes the some predefined status value via Serial to Arduino in Busy Light.

    Args:
        status (string): String that matches to one of the status values in config file.

    """
    logging.info("write_status_to_busy_light - Writing status %s to busy light...", status)
    if status not in STATUS_TO_COMMAND:
        logging.error("The following Status is not yet known and needs to be added to the python Script: %s", status)
        if status not in reported_unknown_statuses:
            reported_unknown_statuses.add(status)
            msgbox(
                msg="MS Teams Presence Status Script: The following Status is not yet known and needs to be added to the python Script: \n"
                + status,
                title="MS-Teams-Busy-Light Script",
            )
        return
    command = STATUS_TO_COMMAND[status]
    if command is not None:
        send_to_busy_light(command)


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
    log_dir = os.path.expandvars(settings["logfolder_new"])
     
    # Check if the log directory exists
    if not os.path.isdir(log_dir):
        logging.error("Log directory %s does not exist, check configuration.", log_dir)
        return False, None, None  # Exit the function if the log directory does not exist

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
    if latest_file_mtime > last_checked_time:
        return True, latest_file_path, latest_file_mtime
    logging.info("check_new_or_modified_log - No new file or modification to it, since last check.")
    return False, latest_file_path, latest_file_mtime

def read_from_serial():
    """
    Check for Log Messages of Arduino. Reads everything in serial buffer and logs it.
    Args:

    Returns:

    """
    if not ser.is_open:
        return
    try:
        while ser.in_waiting > 0:
            line = ser.readline()
            logging.info("read_from_serial - Received from serial: %s", line)
    except (serial.SerialException, OSError) as e:
        if serial_connected:
            logging.error("read_from_serial - Serial read on %s failed, will try to reconnect: %s", ser.port, e)
        close_serial_port()

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

    # Regular expression to match the word after "availability:"
    pattern = re.compile(rf"{re.escape(search_string)}\s*([A-Za-z]+)")

    with FileReadBackwards(log_file_path, encoding="utf-8") as frb:
        for line in frb:    
            match = pattern.search(line)
            if match:
                last_value = match.group(1)    
                # Extract the value after the availability string
                # examplestring from log:
                # 2024-09-07T21:18:25.244338+02:00 0x00003de8 <INFO> native_modules::UserDataCrossCloudModule: BroadcastGlobalState: New Global State Event: UserDataGlobalState total number of users: 1 { user id :31e6a1801808ed67, availability: PresenceUnknown, unread notification count: 0 }
                logging.info("Logfile: %s. Following Status found: %s",log_file_path,last_value)
                if last_value not in status_states:
                    logging.error("search_availability_in_log -  Status %s read in log is not yet part of settings.ini",last_value)
                break
    if last_value is None:
        logging.error("search_availability_in_log - No occurrence of %s found in file %s",search_string,log_file_path)
        return "unknown"  # or return a default value like "unknown"
    return last_value.lower()

def main():
    """Sets up logging and the COM port, then polls the Teams log and drives the busy light forever."""
    settings = load_settings("MS_Teams_Settings.ini")
    if settings is None:
        msgbox(
            msg="MS_Teams_Settings.ini could not be read or uses unsupported settings. Only newTeams = True is supported.",
            title="MS-Teams-Busy-Light Script",
        )
        sys.exit(1)
    configure_logging(settings)  # activates debug logs according to .ini file
    debug_mode = is_truthy(settings["debug"]["enabled"])

    status = "initialize"
    timestamp = datetime.min  # forces the first loop iteration to read the current log file
    if not debug_mode:
        write_initial_COM_Port(select_com_ports())
    else:
        logging.info("Main initialize - Bypassing Setup of read_com_ports and write_initial_COM_Port() due to debug mode.")

    while True:
        try:
            newLog, path, latest_file_mtime = check_new_or_modified_log(settings, timestamp)
            if latest_file_mtime is not None:
                timestamp = latest_file_mtime
            if newLog:
                tempStatus = status
                status = search_availability_in_log(path, settings["SearchString"], settings["StatusStates"])
                if status not in settings["StatusStates"]:
                    logging.error("Main loop - Status Value %s read in log is not yet part of settings.ini", status)
                    status = tempStatus
                logging.info("Main loop - Status Value set to: %s", status)
            if not debug_mode:
                write_status_to_busy_light(status)
                read_from_serial()
            else:
                logging.info("While True loop - Bypassing write_status_to_busy_light due to debug mode.")
        except Exception:
            # e.g. the log file got rotated/deleted between listing and reading; keep running
            logging.exception("Main loop - unexpected error, retrying on next cycle")
        time.sleep(POLL_INTERVAL_SECONDS)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logging.exception("Fatal error, exiting")
        msgbox(
            msg="MS-Teams-Busy-Light stopped due to an unexpected error:\n\n" + repr(e)
            + "\n\nSee the log file for details.",
            title="MS-Teams-Busy-Light Script",
        )
        sys.exit(1)
    finally:
        close_serial_port()
