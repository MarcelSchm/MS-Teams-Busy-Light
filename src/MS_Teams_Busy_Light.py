"""Main File that opens a serial connection and sends commands to an arduino, depending on the Teams log file."""
import sys
import time
from os import path
from datetime import datetime, timezone
import serial
import serial.tools.list_ports
import regex
from file_read_backwards import FileReadBackwards
from easygui import msgbox, choicebox


COM_BAUD = 9600


def read_com_ports():
    """Function to call a library, that returns all open COM-Ports"""
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
        test = msgbox(msg, title, ok_button="Stop Program")
        sys.exit(0)
    for port, desc, hwid in ports:
        choices.append(port + ":  " + desc)
    if len(choices) == 1:
        msg = "There is only 1 COM-Port available. Auto - Selected: \n\n" + choices[0]
        result = msgbox(msg, title, ok_button="OK")
        if result == None:
            sys.exit(0)
        else:
            return port
    choice = choicebox(msg, title, choices)
    if choice == None:
        sys.exit(0)
    else:
        return str.split(choice, ":")[0]


def main():
    COM_PORT = select_com_ports()
    ser = serial.Serial()
    ser.port = COM_PORT
    ser.baudrate = COM_BAUD
    log_file_path = path.expandvars(r"%APPDATA%\Microsoft\Teams\logs.txt")
    # Define the regex pattern
    regex_pattern_status = "(?=StatusIndicatorStateService: Added )(?!.*StatusIndicatorStateService:Added )[^\\(]+"
    regex_pattern_calls = "DeviceCallControlManager Desktop: reportIncomingCall"
    status = "initialize"
    now_script = datetime.now(
        timezone.utc
    )  # timestamp from start to compare with last status in log file

    ser.open()
    time.sleep(3)
    ser.write(b"White")

    while 1:
        try:
            with FileReadBackwards(log_file_path, encoding="utf-8") as frb:
                for l in frb:
                    if not None is regex.search(regex_pattern_status, l):
                        now_statuslog = datetime.strptime(
                            "".join(l.split()[:6]), "%a%b%d%Y%H:%M:%SGMT%z"
                        )  # Grab whole log string and extract timestamp
                        if now_script < now_statuslog:
                            status = l.split("Added ")[1].split(" ")[0]
                        else:
                            status = "Outdated"
                        # msgbox(status)
                        break
                    if not None is regex.search(regex_pattern_calls, l):
                        now_statuslog = datetime.strptime(
                            "".join(l.split()[:6]), "%a%b%d%Y%H:%M:%SGMT%z"
                        )  # Grab whole log string and extract timestamp
                        if now_script < now_statuslog:
                            status = "IncomingCall"
                        else:
                            status = "Outdated"

        except FileNotFoundError:
            msgbox(
                msg="can't open file: \n"
                + log_file_path
                + "\n No such file or directory",
                title="FileNotFoundError in MS-Teams-Busy-Light Script",
            )

        match status:
            case "Available":
                ser.write(b"Green")
                time.sleep(2)
            case "Busy":
                ser.write(b"Red")
                time.sleep(2)
            case "InAMeeting":
                ser.write(b"Red")
                time.sleep(2)
            case "OnThePhone":
                ser.write(b"Red")
                time.sleep(2)
            case "DoNotDisturb":
                ser.write(b"Red")
                time.sleep(2)
            case "BeRightBack":
                ser.write(b"Yellow")
                time.sleep(2)
            case "Presenting":
                ser.write(b"Red")
                time.sleep(2)
            case "Away":
                ser.write(b"Yellow")
                time.sleep(2)
            case "Offline":
                ser.write(b"Yellow")
                time.sleep(2)
            case "Unknown":
                ser.write(b"Red")
                time.sleep(2)
            case "NewActivity":
                # ser.write(b'Red')
                time.sleep(2)
            case "ConnectionError":
                ser.write(b"Red")
                time.sleep(2)
            case "NoNetwork":
                ser.write(b"Red")
                time.sleep(2)
            case "Initialize":
                ser.write(b"White")
                time.sleep(2)
            case "Outdated":
                ser.write(b"Green")
                time.sleep(2)
            case "IncomingCall":
                ser.write(b"BlinkRed")
                time.sleep(2)
            case _:
                msgbox(
                    msg="MS Teams Presence Status Script: The following Status is not yet known and needs to be added to the python Script: \n"
                    + status,
                    title="MS-Teams-Busy-Light Script",
                )
        time.sleep(2)

    ser.close()


if __name__ == "__main__":
    sys.exit(main())
